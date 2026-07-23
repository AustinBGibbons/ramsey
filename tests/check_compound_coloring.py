#!/usr/bin/env python3
"""Independently check the expanded five-colour word by Rowley's set formulas."""

from __future__ import annotations

import hashlib
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
TEMPLATE = PROJECT / "results" / "order94_t12.template"
PROTOTYPE = PROJECT / "sources" / "rowley_exoo_order453.prototype"
COMPOUND = PROJECT / "results" / "r5_5_order42077.linear-coloring"
EXPECTED_SHA256 = (
    "a97d5dce8a927db2889ba220119f9d4f3d1b88ee24d441f82a803a195ae8028d"
)


def records(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for raw in path.read_text(encoding="ascii").splitlines():
        line = raw.partition("#")[0].strip()
        if not line:
            continue
        key, value = line.split()
        assert key not in result
        result[key] = value
    return result


def main() -> int:
    template = records(TEMPLATE)
    prototype = records(PROTOTYPE)
    compound = records(COMPOUND)
    m = int(template["order"])
    n = int(prototype["order"])
    u = template["colors"]
    v = prototype["colors"]
    phi = min(distance for distance, color in enumerate(u, 1) if color == "3") - 1
    expected_order = (m - 1) * (n - 1) + 1 + phi
    assert expected_order == 42077
    assert int(compound["order"]) == expected_order
    assert compound["clique_sizes"] == "5,5,5,5,5"

    # Construct L''_s literally as the unions displayed in Rowley's proof,
    # rather than using the block/residue loop in the generation program.
    assignments: dict[int, str] = {}
    period = m - 1
    for inherited_color in ("1", "2"):
        base_lengths = [
            distance
            for distance, color in enumerate(u, 1)
            if color == inherited_color
        ]
        for mu in range(1, n):
            for length in base_lengths:
                distance = length + (mu - 1) * period
                assert distance not in assignments
                assignments[distance] = inherited_color
        for length in base_lengths:
            if length <= phi:
                distance = length + (n - 1) * period
                assert distance not in assignments
                assignments[distance] = inherited_color

    template_lengths = [
        distance for distance, color in enumerate(u, 1) if color == "3"
    ]
    for prototype_color in ("1", "2", "3"):
        output_color = str(int(prototype_color) + 2)
        prototype_lengths = [
            distance
            for distance, color in enumerate(v, 1)
            if color == prototype_color
        ]
        for mu in prototype_lengths:
            for length in template_lengths:
                distance = length + (mu - 1) * period
                assert distance not in assignments
                assignments[distance] = output_color

    assert set(assignments) == set(range(1, expected_order))
    independently_built = "".join(
        assignments[distance] for distance in range(1, expected_order)
    )
    assert independently_built == compound["colors"]
    assert hashlib.sha256(COMPOUND.read_bytes()).hexdigest() == EXPECTED_SHA256
    assert all(
        independently_built[distance - 1]
        == independently_built[expected_order - distance - 1]
        for distance in range(1, expected_order)
    )
    print("OK compound order 42077")
    print("OK all 42076 distances assigned exactly once")
    print("OK independent set-union construction matches frozen word")
    print("OK cyclic reflection")
    print(f"OK SHA-256 {EXPECTED_SHA256}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
