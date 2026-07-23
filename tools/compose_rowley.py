#!/usr/bin/env python3
"""Expand a Rowley template and prototype into a compound linear colouring.

This implements the distance-set construction in Rowley's Theorem 3.2.  The
template colours are 1,2,3 with 3 eliminated.  Prototype colours 1,2,3 are
relabelled 3,4,5 in the output.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


def records(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for line_number, raw in enumerate(path.read_text(encoding="ascii").splitlines(), 1):
        line = raw.partition("#")[0].strip()
        if not line:
            continue
        fields = line.split()
        if len(fields) != 2 or fields[0] in result:
            raise ValueError(f"{path}:{line_number}: malformed or duplicate record")
        result[fields[0]] = fields[1]
    return result


def compose(template_path: Path, prototype_path: Path) -> tuple[int, str]:
    template = records(template_path)
    prototype = records(prototype_path)
    m = int(template["order"])
    n = int(prototype["order"])
    template_word = template["colors"]
    prototype_word = prototype["colors"]
    if len(template_word) != m - 1 or set(template_word) - set("123"):
        raise ValueError("template word is not a three-colour word of length m-1")
    if len(prototype_word) != n - 1 or set(prototype_word) - set("123"):
        raise ValueError("prototype word is not a three-colour word of length n-1")
    template_distances = [
        distance
        for distance, color in enumerate(template_word, 1)
        if color == "3"
    ]
    if not template_distances or template_distances[-1] != m - 1:
        raise ValueError("template colour must be nonempty and contain m-1")
    phi = template_distances[0] - 1

    period = m - 1
    output_order = period * (n - 1) + 1 + phi
    output: list[str] = []
    for distance in range(1, output_order):
        block = (distance - 1) // period + 1
        residue = (distance - 1) % period + 1
        template_color = template_word[residue - 1]
        if template_color in "12":
            output.append(template_color)
        else:
            if block > n - 1:
                raise AssertionError("template colour entered final partial block")
            # Rowley's labels would be 4,5,6 because colour 3 is eliminated.
            # Relabel them monotonically to contiguous output colours 3,4,5.
            output.append(str(int(prototype_word[block - 1]) + 2))
    return output_order, "".join(output)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("template", type=Path)
    parser.add_argument("prototype", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    order, word = compose(args.template, args.prototype)
    cyclic = all(
        word[distance - 1] == word[order - distance - 1]
        for distance in range(1, order)
    )
    payload = (
        "# Explicit Rowley compound linear five-colouring.\n"
        f"# Generated from {args.template.as_posix()} and\n"
        f"# {args.prototype.as_posix()}.\n"
        f"order {order}\n"
        "clique_sizes 5,5,5,5,5\n"
        f"colors {word}\n"
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(payload, encoding="ascii")
    digest = hashlib.sha256(payload.encode("ascii")).hexdigest()
    print(f"order {order}")
    print(f"distance_word_length {len(word)}")
    print(f"cyclic_reflection {str(cyclic).lower()}")
    for color in "12345":
        print(f"color_{color}_distance_count {word.count(color)}")
    print(f"sha256 {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
