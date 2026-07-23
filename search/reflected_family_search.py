#!/usr/bin/env python3
"""Exact lazy-SAT search in the two-reflection Rowley template family.

Let ``p = order - 1``, ``q = phi_min``, and ``r = p - 2q``.  The family uses
the following distance orbits:

* ``1,...,q`` are binary and satisfy ``c(d) = c(q + 1 - d)``;
* ``q+a`` and ``p+1-a`` share a colour for ``1 <= a <= r``;
* the ``a=1`` pair and the central interval ``q+r+1,...,2q`` are template
  coloured;
* the remaining tail pairs may use any of the three colours.

The first reflection makes the prefix a cyclic two-colour prototype.  The
second makes a compound colouring cyclic when Rowley's optional reflection
hypotheses are used.  For the template-coloured tail-pair indices ``U``, the
interval sum-free condition reduces to ``a+b+c != r+1`` for all ``a,b,c`` in
``U``.  We nevertheless add the generic interval-sum clauses from the main
search engine, keeping this program independent of that reduction.

Every learned clique clause comes from an exact repeated-distance K_5 witness.
Thus SAT means only "not yet separated"; a candidate is emitted only after an
exact oracle finds no witness.  An UNSAT result applies to the entire stated
reflection class.  Use ``--unsat-prefix`` to retain CNF and DRAT artifacts.
"""

from __future__ import annotations

import argparse
import json
import random
import shutil
import time
from pathlib import Path

from template_search import (
    BLUE,
    COLOR_CHARS,
    RED,
    TEMPLATE,
    Candidate,
    ClauseDatabase,
    Partition,
    RepeatedCliqueOracle,
    internal_check,
    random_assignment,
    run_kissat,
    write_candidate,
)


def reflected_partition(period: int, phi_min: int) -> Partition:
    q = phi_min
    r = period - 2 * q
    if q < 1:
        raise ValueError("the reflected family requires phi_min >= 1")
    if r < 1:
        raise ValueError("the reflected family requires period >= 2*phi_min+1")
    if r > q - 1:
        raise ValueError(
            "the central-interval normal form requires period <= 3*phi_min-1"
        )

    specs: list[tuple[tuple[int, ...], tuple[int, ...]]] = []
    covered: set[int] = set()

    def add(distances: tuple[int, ...], allowed: tuple[int, ...]) -> None:
        indices = tuple(sorted(distance - 1 for distance in set(distances)))
        if not indices or any(index in covered for index in indices):
            raise AssertionError("overlapping or empty reflection orbit")
        covered.update(indices)
        specs.append((indices, allowed))

    prefix_seen: set[int] = set()
    for distance in range(1, q + 1):
        if distance in prefix_seen:
            continue
        mate = q + 1 - distance
        prefix_seen.update((distance, mate))
        add((distance, mate), (RED, BLUE))

    for a in range(1, r + 1):
        allowed = (TEMPLATE,) if a == 1 else (RED, BLUE, TEMPLATE)
        add((q + a, period + 1 - a), allowed)

    for distance in range(q + r + 1, 2 * q + 1):
        add((distance,), (TEMPLATE,))

    if covered != set(range(period)):
        missing = sorted(index + 1 for index in set(range(period)) - covered)
        extra = sorted(index + 1 for index in covered - set(range(period)))
        raise AssertionError(
            f"reflection partition mismatch: missing={missing}, extra={extra}"
        )

    variable_to_unit = [-1] * period
    for unit_id, (unit, _allowed) in enumerate(specs):
        for index in unit:
            variable_to_unit[index] = unit_id
    return Partition(
        period=period,
        units=tuple(unit for unit, _allowed in specs),
        variable_to_unit=tuple(variable_to_unit),
        allowed=tuple(allowed for _unit, allowed in specs),
    )


def emit(kind: str, **payload: object) -> None:
    print(
        json.dumps(
            {"time": time.time(), "kind": kind, **payload},
            sort_keys=True,
            default=list,
        ),
        flush=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--order", type=int, required=True)
    parser.add_argument("--phi-min", type=int, required=True)
    parser.add_argument("--random-seed", type=int, default=1)
    parser.add_argument("--bootstrap-assignments", type=int, default=32)
    parser.add_argument("--oracle-batch", type=int, default=10000)
    parser.add_argument("--oracle-max-examined", type=int, default=10000000)
    parser.add_argument("--max-rounds", type=int, default=100000)
    parser.add_argument("--time-limit", type=float, default=600.0)
    parser.add_argument("--sat-timeout", type=float, default=120.0)
    parser.add_argument("--kissat", default=shutil.which("kissat"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--unsat-prefix", type=Path)
    args = parser.parse_args()
    if args.kissat is None:
        parser.error("kissat executable was not found")

    period = args.order - 1
    repeat_span = 4 * (args.order - 2)
    partition = reflected_partition(period, args.phi_min)
    database = ClauseDatabase(partition)
    database.add_all_sum_free_constraints()
    oracle = RepeatedCliqueOracle(period, repeat_span)
    rng = random.Random(args.random_seed)
    deadline = time.monotonic() + args.time_limit

    mutable_binary = sum(allowed == (RED, BLUE) for allowed in partition.allowed)
    mutable_ternary = sum(
        allowed == (RED, BLUE, TEMPLATE) for allowed in partition.allowed
    )
    emit(
        "start",
        order=args.order,
        period=period,
        phi_min=args.phi_min,
        repeat_span=repeat_span,
        units=len(partition.units),
        mutable_binary=mutable_binary,
        mutable_ternary=mutable_ternary,
        initial_sum_clauses=len(database.clauses),
    )

    for bootstrap in range(args.bootstrap_assignments):
        colors = partition.expand(random_assignment(partition, rng))
        before = len(database.clauses)
        separated = oracle.separate(
            colors,
            database,
            args.oracle_batch,
            args.oracle_max_examined,
        )
        emit(
            "bootstrap",
            index=bootstrap,
            added=len(database.clauses) - before,
            clauses=len(database.clauses),
            red=separated[RED],
            blue=separated[BLUE],
        )

    for round_number in range(args.max_rounds):
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            emit(
                "censored",
                reason="time_limit",
                round=round_number,
                clauses=len(database.clauses),
            )
            return 1
        sat = run_kissat(
            database,
            args.kissat,
            min(args.sat_timeout, remaining),
        )
        emit(
            "sat",
            round=round_number,
            status=sat.status,
            clauses=len(database.clauses),
            tail=sat.stdout_tail,
        )
        if sat.status == "timeout":
            emit("censored", reason="sat_timeout", round=round_number)
            return 1
        if sat.status == "error":
            return 3
        if sat.status == "unsat":
            if args.unsat_prefix is not None:
                cnf_path = args.unsat_prefix.with_suffix(".cnf")
                drat_path = args.unsat_prefix.with_suffix(".drat")
                rerun = run_kissat(
                    database,
                    args.kissat,
                    min(args.sat_timeout, max(1.0, deadline - time.monotonic())),
                    keep_cnf=cnf_path,
                    proof_path=drat_path,
                )
                emit(
                    "unsat-artifact",
                    status=rerun.status,
                    cnf=str(cnf_path),
                    drat=str(drat_path),
                )
            emit(
                "restricted-unsat",
                order=args.order,
                phi_min=args.phi_min,
                clauses=len(database.clauses),
            )
            return 2

        assert sat.unit_colors is not None
        colors = partition.expand(sat.unit_colors)
        before = len(database.clauses)
        separated = oracle.separate(
            colors,
            database,
            args.oracle_batch,
            args.oracle_max_examined,
        )
        added = len(database.clauses) - before
        emit(
            "separate",
            round=round_number,
            added=added,
            clauses=len(database.clauses),
            red=separated[RED],
            blue=separated[BLUE],
        )
        if added:
            continue

        candidate = Candidate(
            order=args.order,
            phi_min=args.phi_min,
            repeat_span=repeat_span,
            colors=tuple(colors),
        )
        report = internal_check(candidate)
        if not report["valid"]:
            raise AssertionError(
                f"separator/internal-check disagreement: {report}"
            )
        write_candidate(
            args.output,
            candidate,
            "two-reflection exact lazy-SAT oracle passed",
        )
        emit(
            "provisional-candidate",
            output=str(args.output),
            report=report,
            word="".join(COLOR_CHARS[color] for color in colors),
        )
        return 0

    emit(
        "censored",
        reason="round_limit",
        rounds=args.max_rounds,
        clauses=len(database.clauses),
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
