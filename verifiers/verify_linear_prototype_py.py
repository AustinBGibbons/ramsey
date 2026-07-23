#!/usr/bin/env python3
"""Exact verifier for a finite linear multicolour Ramsey prototype.

Input format:

    order 453
    clique_sizes 5,5,5
    colors 122...1

The symbol at position d gives the colour of every edge {i,j} with
|i-j|=d.  The verifier constructs the finite graph on vertices 0,...,n-1
and performs an exact bit-parallel clique search independently in each colour.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse(path: Path) -> tuple[int, tuple[int, ...], str]:
    fields: dict[str, str] = {}
    for line_number, raw in enumerate(path.read_text(encoding="ascii").splitlines(), 1):
        line = raw.partition("#")[0].strip()
        if not line:
            continue
        pieces = line.split()
        if len(pieces) != 2 or pieces[0] not in {
            "order",
            "clique_sizes",
            "colors",
        }:
            raise ValueError(f"line {line_number}: malformed record")
        key, value = pieces
        if key in fields:
            raise ValueError(f"line {line_number}: duplicate key {key}")
        fields[key] = value
    if set(fields) != {"order", "clique_sizes", "colors"}:
        raise ValueError("expected exactly order, clique_sizes, and colors")
    order = int(fields["order"])
    clique_sizes = tuple(int(token) for token in fields["clique_sizes"].split(","))
    colors = fields["colors"]
    return order, clique_sizes, colors


def forward_masks(order: int, colors: str, target: int) -> list[int]:
    masks = [0] * order
    symbol = str(target)
    for left in range(order):
        mask = 0
        for right in range(left + 1, order):
            if colors[right - left - 1] == symbol:
                mask |= 1 << right
        masks[left] = mask
    return masks


def find_clique(masks: list[int], size: int) -> tuple[tuple[int, ...] | None, int]:
    nodes = 0

    def visit(prefix: tuple[int, ...], candidates: int, need: int):
        nonlocal nodes
        nodes += 1
        if need == 0:
            return prefix
        if candidates.bit_count() < need:
            return None
        remaining = candidates
        while remaining.bit_count() >= need:
            bit = remaining & -remaining
            vertex = bit.bit_length() - 1
            remaining ^= bit
            result = visit(prefix + (vertex,), remaining & masks[vertex], need - 1)
            if result is not None:
                return result
        return None

    return visit((), (1 << len(masks)) - 1, size), nodes


def verify(order: int, clique_sizes: tuple[int, ...], colors: str) -> dict:
    if order < 2:
        return {"status": "INVALID", "reason": "order_below_2"}
    if not clique_sizes or any(size < 2 for size in clique_sizes):
        return {"status": "INVALID", "reason": "invalid_clique_sizes"}
    if len(colors) != order - 1:
        return {
            "status": "INVALID",
            "reason": "wrong_word_length",
            "expected": order - 1,
            "actual": len(colors),
        }
    alphabet = {str(color) for color in range(1, len(clique_sizes) + 1)}
    if any(symbol not in alphabet for symbol in colors):
        return {"status": "INVALID", "reason": "invalid_color_symbol"}

    search_nodes: dict[str, int] = {}
    for target, forbidden_size in enumerate(clique_sizes, 1):
        clique, nodes = find_clique(
            forward_masks(order, colors, target),
            forbidden_size,
        )
        search_nodes[str(target)] = nodes
        if clique is not None:
            return {
                "status": "INVALID",
                "reason": "forbidden_monochromatic_clique",
                "color": target,
                "vertices": clique,
                "search_nodes": nodes,
            }

    cyclic_reflection = all(
        colors[distance - 1] == colors[order - distance - 1]
        for distance in range(1, order)
    )
    return {
        "status": "VALID",
        "order": order,
        "clique_sizes": clique_sizes,
        "color_counts": {
            str(color): colors.count(str(color))
            for color in range(1, len(clique_sizes) + 1)
        },
        "cyclic_reflection": cyclic_reflection,
        "clique_search_nodes": search_nodes,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prototype", type=Path)
    args = parser.parse_args()
    try:
        report = verify(*parse(args.prototype))
    except (OSError, UnicodeError, ValueError) as error:
        report = {
            "status": "INVALID",
            "reason": "malformed_prototype",
            "message": str(error),
        }
        print(json.dumps(report, indent=2, sort_keys=True))
        return 2
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "VALID" else 1


if __name__ == "__main__":
    raise SystemExit(main())
