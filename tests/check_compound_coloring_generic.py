#!/usr/bin/env python3
"""Independently reconstruct and check a Rowley compound distance word.

This checker deliberately implements the set-union formulas from Rowley's
proof, rather than the block/residue loop used by ``tools/compose_rowley.py``.
It does not check the template or prototype hypotheses; the independent
template and prototype verifiers perform those checks.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


def records(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for line_number, raw in enumerate(
        path.read_text(encoding="ascii").splitlines(), 1
    ):
        line = raw.partition("#")[0].strip()
        if not line:
            continue
        fields = line.split()
        if len(fields) != 2 or fields[0] in result:
            raise ValueError(
                f"{path}:{line_number}: malformed or duplicate record"
            )
        result[fields[0]] = fields[1]
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("template", type=Path)
    parser.add_argument("prototype", type=Path)
    parser.add_argument("compound", type=Path)
    parser.add_argument("--sha256")
    args = parser.parse_args()

    template = records(args.template)
    prototype = records(args.prototype)
    compound = records(args.compound)
    m = int(template["order"])
    n = int(prototype["order"])
    template_word = template["colors"]
    prototype_word = prototype["colors"]
    template_lengths = [
        distance
        for distance, color in enumerate(template_word, 1)
        if color == "3"
    ]
    if not template_lengths:
        raise ValueError("empty template colour")
    phi = min(template_lengths) - 1
    period = m - 1
    expected_order = period * (n - 1) + 1 + phi
    if int(compound["order"]) != expected_order:
        raise AssertionError("compound order disagrees with Rowley's formula")
    if compound.get("clique_sizes") != "5,5,5,5,5":
        raise AssertionError("compound clique-size header is wrong")

    assignments: dict[int, str] = {}
    for inherited_color in ("1", "2"):
        base_lengths = [
            distance
            for distance, color in enumerate(template_word, 1)
            if color == inherited_color
        ]
        for block in range(1, n):
            for length in base_lengths:
                distance = length + (block - 1) * period
                if distance in assignments:
                    raise AssertionError("duplicate inherited assignment")
                assignments[distance] = inherited_color
        for length in base_lengths:
            if length <= phi:
                distance = length + (n - 1) * period
                if distance in assignments:
                    raise AssertionError("duplicate final-block assignment")
                assignments[distance] = inherited_color

    for prototype_color in ("1", "2", "3"):
        output_color = str(int(prototype_color) + 2)
        prototype_lengths = [
            distance
            for distance, color in enumerate(prototype_word, 1)
            if color == prototype_color
        ]
        for block in prototype_lengths:
            for length in template_lengths:
                distance = length + (block - 1) * period
                if distance in assignments:
                    raise AssertionError("duplicate substituted assignment")
                assignments[distance] = output_color

    expected_distances = set(range(1, expected_order))
    if set(assignments) != expected_distances:
        missing = sorted(expected_distances - set(assignments))
        extra = sorted(set(assignments) - expected_distances)
        raise AssertionError(
            f"distance partition is incomplete: missing={missing[:10]}, "
            f"extra={extra[:10]}"
        )
    reconstructed = "".join(
        assignments[distance] for distance in range(1, expected_order)
    )
    if reconstructed != compound["colors"]:
        raise AssertionError("independent reconstruction disagrees with artifact")

    digest = hashlib.sha256(args.compound.read_bytes()).hexdigest()
    if args.sha256 is not None and digest != args.sha256:
        raise AssertionError(
            f"SHA-256 mismatch: expected {args.sha256}, received {digest}"
        )
    cyclic = all(
        reconstructed[distance - 1]
        == reconstructed[expected_order - distance - 1]
        for distance in range(1, expected_order)
    )
    print(f"OK compound order {expected_order}")
    print(f"OK all {expected_order - 1} distances assigned exactly once")
    print("OK independent set-union reconstruction")
    print(f"cyclic_reflection {str(cyclic).lower()}")
    print(f"sha256 {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
