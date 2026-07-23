#!/usr/bin/env python3
"""Exact bit-parallel verifier for Rowley effective (5,5,3) templates.

Candidate files contain four whitespace-separated key/value records:

    order 94
    phi_min 40
    repeat_span 368
    colors 112...3

Blank lines and text after ``#`` are ignored.  The color word has length
``order - 1``.  Colors 1 and 2 must remain K_5-free after periodic repetition;
color 3 is the triangle-free template color.

This implementation is intentionally independent of the C++ verifier.  It
constructs forward-neighbor bit masks and searches them by bit intersection.
It shares neither parser code nor clique-search code with the search engine.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


REQUIRED_KEYS = frozenset({"order", "phi_min", "repeat_span", "colors"})


class CandidateError(ValueError):
    """Raised when a candidate file is malformed."""


@dataclass(frozen=True)
class Candidate:
    order: int
    phi_min: int
    repeat_span: int
    colors: str

    @property
    def period(self) -> int:
        return self.order - 1


def parse_candidate(path: Path) -> Candidate:
    """Parse the deliberately small, strict candidate format."""

    fields: dict[str, str] = {}
    for line_number, raw_line in enumerate(
        path.read_text(encoding="ascii").splitlines(), start=1
    ):
        line = raw_line.partition("#")[0].strip()
        if not line:
            continue
        tokens = line.split()
        if len(tokens) != 2:
            raise CandidateError(
                f"line {line_number}: expected exactly '<key> <value>'"
            )
        key, value = tokens
        if key not in REQUIRED_KEYS:
            raise CandidateError(f"line {line_number}: unknown key {key!r}")
        if key in fields:
            raise CandidateError(f"line {line_number}: duplicate key {key!r}")
        fields[key] = value

    missing = sorted(REQUIRED_KEYS.difference(fields))
    if missing:
        raise CandidateError(f"missing required keys: {', '.join(missing)}")

    def integer(key: str) -> int:
        token = fields[key]
        try:
            value = int(token, 10)
        except ValueError as error:
            raise CandidateError(f"value for {key!r} is not an integer") from error
        if str(value) != token and token != f"+{value}":
            raise CandidateError(f"value for {key!r} is not a canonical integer")
        return value

    return Candidate(
        order=integer("order"),
        phi_min=integer("phi_min"),
        repeat_span=integer("repeat_span"),
        colors=fields["colors"],
    )


def repeated_color(candidate: Candidate, distance: int) -> int:
    """Return the base color of a positive periodically repeated distance."""

    if distance <= 0:
        raise ValueError("distance must be positive")
    residue = (distance - 1) % candidate.period
    return ord(candidate.colors[residue]) - ord("0")


def build_forward_masks(candidate: Candidate, target_color: int) -> list[int]:
    """Build masks containing only higher neighbors in one repeated color."""

    vertex_count = candidate.repeat_span + 1
    masks = [0] * vertex_count
    for left in range(vertex_count):
        mask = 0
        for right in range(left + 1, vertex_count):
            if repeated_color(candidate, right - left) == target_color:
                mask |= 1 << right
        masks[left] = mask
    return masks


def find_k_clique_bitwise(
    forward_masks: list[int], size: int
) -> tuple[tuple[int, ...] | None, int]:
    """Find one clique by exact forward-mask intersection.

    The second return value is the number of recursive search nodes.  Vertices
    are chosen in increasing order, so every candidate clique is represented
    once.
    """

    search_nodes = 0

    def descend(
        prefix: tuple[int, ...], candidates: int, need: int
    ) -> tuple[int, ...] | None:
        nonlocal search_nodes
        search_nodes += 1
        if need == 0:
            return prefix
        if candidates.bit_count() < need:
            return None

        remaining = candidates
        while remaining.bit_count() >= need:
            low_bit = remaining & -remaining
            vertex = low_bit.bit_length() - 1
            remaining ^= low_bit
            found = descend(
                prefix + (vertex,),
                remaining & forward_masks[vertex],
                need - 1,
            )
            if found is not None:
                return found
        return None

    all_vertices = (1 << len(forward_masks)) - 1
    return descend((), all_vertices, size), search_nodes


def edge_witness(
    candidate: Candidate, vertices: Iterable[int]
) -> list[dict[str, int]]:
    ordered = tuple(vertices)
    result: list[dict[str, int]] = []
    for index, left in enumerate(ordered):
        for right in ordered[index + 1 :]:
            distance = right - left
            result.append(
                {
                    "left": left,
                    "right": right,
                    "distance": distance,
                    "residue": ((distance - 1) % candidate.period) + 1,
                    "color": repeated_color(candidate, distance),
                }
            )
    return result


def invalid(reason: str, witness: object) -> dict[str, object]:
    return {"status": "INVALID", "reason": reason, "witness": witness}


def verify(candidate: Candidate) -> dict[str, object]:
    """Return a complete exact verification report."""

    if candidate.order < 2:
        return invalid("order_must_be_at_least_2", {"order": candidate.order})
    if candidate.phi_min < 0:
        return invalid(
            "phi_min_must_be_nonnegative", {"phi_min": candidate.phi_min}
        )
    if candidate.repeat_span < 0:
        return invalid(
            "repeat_span_must_be_nonnegative",
            {"repeat_span": candidate.repeat_span},
        )

    period = candidate.period
    required_span = 4 * (candidate.order - 2)
    if candidate.repeat_span < required_span:
        return invalid(
            "repeat_span_below_required_4_times_order_minus_2",
            {"required": required_span, "actual": candidate.repeat_span},
        )
    if len(candidate.colors) != period:
        return invalid(
            "wrong_color_word_length",
            {"expected": period, "actual": len(candidate.colors)},
        )
    for distance, symbol in enumerate(candidate.colors, start=1):
        if symbol not in "123":
            return invalid(
                "color_outside_1_2_3",
                {"distance": distance, "symbol": symbol},
            )
    if candidate.colors[-1] != "3":
        return invalid(
            "terminal_distance_not_in_T",
            {"distance": period, "color": candidate.colors[-1]},
        )

    template_distances = tuple(
        distance
        for distance, symbol in enumerate(candidate.colors, start=1)
        if symbol == "3"
    )
    first_template = template_distances[0]
    if first_template <= candidate.phi_min:
        return invalid(
            "T_meets_forbidden_prefix",
            {"distance": first_template, "phi_min": candidate.phi_min},
        )

    template_set = frozenset(template_distances)
    for a in template_distances:
        for b in template_distances:
            if b < a:
                continue
            if a + b in template_set:
                return invalid(
                    "T_not_sum_free", {"a": a, "b": b, "sum": a + b}
                )

    clique_search_nodes: dict[str, int] = {}
    for color in (1, 2):
        masks = build_forward_masks(candidate, color)
        clique, nodes = find_k_clique_bitwise(masks, 5)
        clique_search_nodes[str(color)] = nodes
        if clique is not None:
            return invalid(
                "repeated_color_contains_K5",
                {
                    "color": color,
                    "vertices": list(clique),
                    "edges": edge_witness(candidate, clique),
                    "search_nodes": nodes,
                },
            )

    return {
        "status": "VALID",
        "order": candidate.order,
        "period": period,
        "phi_min": candidate.phi_min,
        "actual_phi": first_template - 1,
        "template_distance_count": len(template_distances),
        "required_repeat_span": required_span,
        "repeat_span": candidate.repeat_span,
        "repeat_vertex_count": candidate.repeat_span + 1,
        "clique_search_nodes": clique_search_nodes,
        "checks": [
            "terminal_distance_in_T",
            "T_avoids_forbidden_prefix",
            "T_interval_sum_free",
            "periodic_color_1_K5_free",
            "periodic_color_2_K5_free",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", type=Path)
    arguments = parser.parse_args()
    try:
        report = verify(parse_candidate(arguments.candidate))
    except (CandidateError, OSError, UnicodeError) as error:
        report = invalid("malformed_candidate", {"message": str(error)})
        print(json.dumps(report, indent=2, sort_keys=True))
        return 2
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "VALID" else 1


if __name__ == "__main__":
    raise SystemExit(main())
