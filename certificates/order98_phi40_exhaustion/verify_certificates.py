#!/usr/bin/env python3
"""Independent semantic and DRAT checker for the order-98 nonexistence packet."""

import itertools
import json
import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DRAT_TRIM_VALUE = os.environ.get("DRAT_TRIM") or shutil.which("drat-trim")
if DRAT_TRIM_VALUE is None:
    raise SystemExit(
        "drat-trim was not found; install it or set DRAT_TRIM=/path/to/drat-trim"
    )
DRAT_TRIM = Path(DRAT_TRIM_VALUE)


def check_drat(stem):
    cnf = ROOT / f"{stem}.cnf"
    drat = ROOT / f"{stem}.drat"
    result = subprocess.run(
        [str(DRAT_TRIM), str(cnf), str(drat)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0 and "s VERIFIED" in result.stdout, result.stdout


def parse_representatives():
    words = []
    for line in (ROOT / "prefix41_representatives.txt").read_text(
        encoding="ascii"
    ).splitlines():
        index, word = line.split()
        assert int(index) == len(words) + 1
        assert len(word) == 40 and set(word) <= {"1", "2"}
        words.append(word)
    assert len(words) == 11
    return words


def check_prefix_certificate(words):
    distance_sets = set()
    for vertices in itertools.combinations(range(41), 5):
        distance_sets.add(
            tuple(
                sorted(
                    {
                        b - a
                        for a, b in itertools.combinations(vertices, 2)
                    }
                )
            )
        )
    assert len(distance_sets) == 45374
    expected = []
    for distances in sorted(distance_sets):
        expected.append(tuple(distances))
        expected.append(tuple(-d for d in distances))
    for word in words:
        assignment = tuple(ch == "1" for ch in word)
        for distances in distance_sets:
            colors = {assignment[d - 1] for d in distances}
            assert len(colors) == 2
        expected.append(
            tuple(-d if assignment[d - 1] else d for d in range(1, 41))
        )
        expected.append(
            tuple(d if assignment[d - 1] else -d for d in range(1, 41))
        )
    lines = (ROOT / "prefix41_exhaust.cnf").read_text(
        encoding="ascii"
    ).splitlines()
    assert lines[0] == f"p cnf 40 {len(expected)}"
    actual = [
        tuple(map(int, line.split()[:-1]))
        for line in lines[1:]
    ]
    assert actual == expected
    check_drat("prefix41_exhaust")


def variable(unit, color):
    return 3 * unit + color + 1


def check_tail(index, prefix):
    stem = f"order98_prefix_{index:02d}"
    sidecar = ROOT / f"{stem}.clauses.jsonl"
    records = [
        json.loads(line)
        for line in sidecar.read_text(encoding="utf-8").splitlines()
    ]
    header = records[0]
    assert header["kind"] == "header"
    assert header["period"] == 97
    assert header["units"] == [[unit] for unit in range(97)]
    allowed = header["allowed"]
    assert len(allowed) == 97
    for distance, symbol in enumerate(prefix, 1):
        assert allowed[distance - 1] == [int(symbol) - 1]
    for distance in range(41, 97):
        assert allowed[distance - 1] == [0, 1, 2]
    assert allowed[96] == [2]

    rendered = []
    for unit, unit_allowed in enumerate(allowed):
        rendered.append(
            [variable(unit, color) for color in (0, 1, 2)]
        )
        rendered.extend(
            [
                [-variable(unit, 0), -variable(unit, 1)],
                [-variable(unit, 0), -variable(unit, 2)],
                [-variable(unit, 1), -variable(unit, 2)],
            ]
        )
        for color in (0, 1, 2):
            if color not in unit_allowed:
                rendered.append([-variable(unit, color)])

    seen = set()
    for expected_index, record in enumerate(records[1:]):
        assert record["kind"] == "database_clause"
        assert record["index"] == expected_index
        forbidden = record["forbidden_color"]
        units = tuple(record["units"])
        key = (forbidden, units)
        assert key not in seen
        seen.add(key)
        witness = record["witness"]
        origin = record["origin"]
        if origin == "sum":
            assert forbidden == 2
            a, b, total = witness
            assert 1 <= a <= b and total == a + b <= 97
            expected_units = tuple(sorted({a - 1, b - 1, total - 1}))
        else:
            assert origin in {"k5-1", "k5-2"}
            assert forbidden == (0 if origin == "k5-1" else 1)
            assert len(witness) == 5
            assert witness[0] == 0
            assert witness == sorted(witness)
            assert len(set(witness)) == 5 and witness[-1] <= 384
            expected_units = tuple(
                sorted(
                    {
                        (witness[right] - witness[left] - 1) % 97
                        for left in range(5)
                        for right in range(left + 1, 5)
                    }
                )
            )
        assert units == expected_units
        rendered.append(
            [-variable(unit, forbidden) for unit in units]
        )

    expected_lines = [f"p cnf 291 {len(rendered)}"]
    expected_lines.extend(
        " ".join(map(str, clause)) + " 0" for clause in rendered
    )
    actual_text = (ROOT / f"{stem}.cnf").read_text(encoding="ascii")
    assert actual_text == "\n".join(expected_lines) + "\n"
    check_drat(stem)


def main():
    words = parse_representatives()
    check_prefix_certificate(words)
    for index, prefix in enumerate(words, 1):
        check_tail(index, prefix)
        print(f"VERIFIED {index:02d}", flush=True)
    print("ALL CERTIFICATES VERIFIED")


if __name__ == "__main__":
    main()
