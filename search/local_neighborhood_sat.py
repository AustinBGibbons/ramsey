#!/usr/bin/env python3
"""Exact lazy-SAT repair around a fixed near-template.

This is a search engine, not an independent verifier.  It fixes every distance
outside an explicitly listed mutable set, adds every interval-sum-free clause,
and separates exact repeated-color K_5 clauses from SAT assignments until it
finds a provisional candidate, proves the restricted class unsatisfiable, or
hits a time/round limit.

The default branch starts from ``order94_near_one_sum.template``, recolors
distance 52 from template to color 1, and makes mutable the support of every
K_5 thereby created.  That support has only 14 distances, so an UNSAT result
is a genuine, sharply scoped local obstruction rather than a vague failed
search.
"""

from __future__ import annotations

import argparse
import json
import shutil
import time
from pathlib import Path
from typing import Sequence

from template_search import (
    BLUE,
    COLOR_CHARS,
    RED,
    TEMPLATE,
    Candidate,
    ClauseDatabase,
    Partition,
    RepeatedCliqueOracle,
    full_violation_profile,
    internal_check,
    read_candidate,
    run_kissat,
    write_candidate,
)


def support_after_forced_change(
    center: Candidate, distance: int, color: int
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Return the changed word and exact support of its current defects."""

    colors = list(center.colors)
    colors[distance - 1] = color
    full_partition = Partition.build(center.period, center.phi_min, "none")
    oracle = RepeatedCliqueOracle(center.period, center.repeat_span)
    profile = full_violation_profile(
        colors, full_partition, oracle, raw_k5_cap=10_000_000
    )
    if profile.truncated:
        raise RuntimeError("unexpectedly truncated initial defect profile")
    support = tuple(
        sorted({unit for _forbidden, units in profile.clauses for unit in units})
    )
    return tuple(colors), support


def restricted_partition(
    center_colors: Sequence[int],
    phi_min: int,
    mutable_indices: set[int],
    forced: dict[int, int],
) -> Partition:
    base = Partition.build(len(center_colors), phi_min, "none")
    allowed: list[tuple[int, ...]] = []
    for index, base_allowed in enumerate(base.allowed):
        if index in forced:
            if forced[index] not in base_allowed:
                raise ValueError(
                    f"forced color invalid at distance {index + 1}"
                )
            allowed.append((forced[index],))
        elif index in mutable_indices:
            allowed.append(base_allowed)
        else:
            allowed.append((center_colors[index],))
    return Partition(
        period=base.period,
        units=base.units,
        variable_to_unit=base.variable_to_unit,
        allowed=tuple(allowed),
    )


def emit(kind: str, **fields: object) -> None:
    print(
        json.dumps(
            {"time": time.time(), "kind": kind, **fields},
            sort_keys=True,
            default=list,
        ),
        flush=True,
    )


def parse_color(value: str) -> int:
    if value not in COLOR_CHARS:
        raise argparse.ArgumentTypeError("color must be 1, 2, or 3")
    return COLOR_CHARS.index(value)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--center",
        type=Path,
        default=Path(__file__).resolve().parents[1]
        / "seeds"
        / "order94_near_one_sum.template",
    )
    parser.add_argument("--force-distance", type=int, default=52)
    parser.add_argument("--force-color", type=parse_color, default=RED)
    parser.add_argument(
        "--mutable",
        help="comma-separated one-based distances; default is initial defect support",
    )
    parser.add_argument("--kissat", default=shutil.which("kissat"))
    parser.add_argument("--time-limit", type=float, default=1800.0)
    parser.add_argument("--sat-timeout", type=float, default=300.0)
    parser.add_argument("--max-rounds", type=int, default=100000)
    parser.add_argument("--oracle-batch", type=int, default=1000000)
    parser.add_argument("--oracle-max-examined", type=int, default=10000000)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("results/provisional_local_sat.template"),
    )
    parser.add_argument("--unsat-prefix", type=Path)
    arguments = parser.parse_args()

    if arguments.kissat is None:
        parser.error("kissat executable was not found")

    center = read_candidate(arguments.center)
    if not 1 <= arguments.force_distance <= center.period:
        parser.error("force distance is outside the base word")
    forced_index = arguments.force_distance - 1
    forced = {forced_index: arguments.force_color}
    branch_word, initial_support = support_after_forced_change(
        center, arguments.force_distance, arguments.force_color
    )

    if arguments.mutable is None:
        mutable = set(initial_support)
    else:
        try:
            mutable = {
                int(token) - 1
                for token in arguments.mutable.split(",")
                if token.strip()
            }
        except ValueError as error:
            parser.error(f"invalid mutable list: {error}")
        if not all(0 <= index < center.period for index in mutable):
            parser.error("mutable distance is outside the base word")
    mutable.add(forced_index)

    partition = restricted_partition(
        branch_word, center.phi_min, mutable, forced
    )
    database = ClauseDatabase(partition)
    database.add_all_sum_free_constraints()
    oracle = RepeatedCliqueOracle(center.period, center.repeat_span)
    deadline = time.monotonic() + arguments.time_limit

    emit(
        "start",
        center=str(arguments.center),
        forced_distance=arguments.force_distance,
        forced_color=COLOR_CHARS[arguments.force_color],
        mutable_distances=sorted(index + 1 for index in mutable),
        mutable_count=len(mutable),
        initial_support=tuple(index + 1 for index in initial_support),
        sum_clauses=len(database.clauses),
    )

    for round_number in range(arguments.max_rounds):
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            emit(
                "censored",
                reason="time_limit",
                round=round_number,
                clauses=len(database.clauses),
            )
            return 1

        result = run_kissat(
            database,
            arguments.kissat,
            min(arguments.sat_timeout, remaining),
        )
        emit(
            "sat",
            round=round_number,
            status=result.status,
            clauses=len(database.clauses),
            tail=result.stdout_tail,
        )
        if result.status == "timeout":
            emit("censored", reason="sat_timeout", round=round_number)
            return 1
        if result.status == "error":
            return 3
        if result.status == "unsat":
            if arguments.unsat_prefix is not None:
                cnf_path = arguments.unsat_prefix.with_suffix(".cnf")
                proof_path = arguments.unsat_prefix.with_suffix(".drat")
                rerun = run_kissat(
                    database,
                    arguments.kissat,
                    min(arguments.sat_timeout, max(1.0, deadline - time.monotonic())),
                    keep_cnf=cnf_path,
                    proof_path=proof_path,
                )
                emit(
                    "unsat-artifact",
                    status=rerun.status,
                    cnf=str(cnf_path),
                    proof=str(proof_path),
                )
            emit(
                "restricted-unsat",
                mutable_distances=sorted(index + 1 for index in mutable),
                clauses=len(database.clauses),
            )
            return 2

        assert result.unit_colors is not None
        distance_colors = partition.expand(result.unit_colors)
        before = len(database.clauses)
        separated = oracle.separate(
            distance_colors,
            database,
            arguments.oracle_batch,
            arguments.oracle_max_examined,
        )
        added = len(database.clauses) - before
        emit(
            "separate",
            round=round_number,
            added=added,
            red=separated[RED],
            blue=separated[BLUE],
        )
        if added:
            continue

        candidate = Candidate(
            order=center.order,
            phi_min=center.phi_min,
            repeat_span=center.repeat_span,
            colors=tuple(distance_colors),
        )
        report = internal_check(candidate)
        if not report["valid"]:
            raise AssertionError(
                f"separator claimed success but internal check failed: {report}"
            )
        write_candidate(
            arguments.output,
            candidate,
            "restricted lazy-SAT search oracle passed",
        )
        emit(
            "provisional-candidate",
            output=str(arguments.output),
            report=report,
            mutable_distances=sorted(index + 1 for index in mutable),
        )
        return 0

    emit(
        "censored",
        reason="round_limit",
        rounds=arguments.max_rounds,
        clauses=len(database.clauses),
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
