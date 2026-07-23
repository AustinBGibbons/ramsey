#!/usr/bin/env python3
"""Check that both frozen distance words are literal arXiv-ancillary extracts."""

from __future__ import annotations

import hashlib
import tarfile
import xml.etree.ElementTree as ET
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
ARCHIVE = PROJECT / "sources" / "arxiv-2203.13476-source.tar.gz"
EXPECTED_SHA256 = (
    "5041096a33d6898c116a35a102e521fb14fe872fb18c20ff7d30822ed4c396b2"
)
NS = {
    "office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0",
    "table": "urn:oasis:names:tc:opendocument:xmlns:table:1.0",
}


def read_colors(path: Path) -> str:
    for raw in path.read_text(encoding="ascii").splitlines():
        line = raw.partition("#")[0].strip()
        if line.startswith("colors "):
            return line.split()[1]
    raise AssertionError(f"{path}: no colors record")


def cell_value(cell: ET.Element) -> str:
    text = "".join(cell.itertext()).strip()
    if text:
        return " ".join(text.split())
    return cell.get(f"{{{NS['office']}}}value", "")


def sheet_cells() -> dict[tuple[int, int], str]:
    with tarfile.open(ARCHIVE, "r:*") as bundle:
        member = bundle.extractfile("anc/content.xml")
        if member is None:
            raise AssertionError("source archive has no anc/content.xml")
        root = ET.parse(member).getroot()
    name_attribute = f"{{{NS['table']}}}name"
    sheet = next(
        table
        for table in root.findall(".//table:table", NS)
        if table.get(name_attribute) == "Paper_Sep_2022"
    )

    cells: dict[tuple[int, int], str] = {}
    logical_row = 1
    for row in sheet.findall("table:table-row", NS):
        row_repeat = int(
            row.get(f"{{{NS['table']}}}number-rows-repeated", "1")
        )
        if logical_row > 471:
            break
        logical_column = 1
        for cell in row:
            if cell.tag not in {
                f"{{{NS['table']}}}table-cell",
                f"{{{NS['table']}}}covered-table-cell",
            }:
                continue
            column_repeat = int(
                cell.get(
                    f"{{{NS['table']}}}number-columns-repeated",
                    "1",
                )
            )
            value = cell_value(cell)
            if value and logical_column <= 28:
                for offset in range(min(column_repeat, 29 - logical_column)):
                    cells[(logical_row, logical_column + offset)] = value
            logical_column += column_repeat
            if logical_column > 28:
                break
        logical_row += row_repeat
    return cells


def main() -> int:
    actual_hash = hashlib.sha256(ARCHIVE.read_bytes()).hexdigest()
    assert actual_hash == EXPECTED_SHA256
    cells = sheet_cells()

    # N is column 14: published order-93 (5,5,3) template.
    assert cells[(6, 14)] == "93"
    assert cells[(8, 14)] == "40"
    assert cells[(15, 14)] == "369"
    published = "".join(cells[(row, 14)] for row in range(19, 111))
    assert published == read_colors(PROJECT / "seeds" / "rowley_order93.template")

    # AB is column 28: order-977 template constructed by extending the
    # order-453 (5,5,5) prototype.  By Rowley's stated construction,
    # distances 1..452 are copied verbatim from that prototype; distance 453
    # is the new template colour 4.
    assert cells[(6, 28)] == "977"
    assert cells[(8, 28)] == "452"
    prototype = "".join(cells[(row, 28)] for row in range(19, 471))
    assert prototype == read_colors(
        PROJECT / "sources" / "rowley_exoo_order453.prototype"
    )
    assert cells[(471, 28)] == "4"

    print("OK source archive SHA-256")
    print("OK order-93 template equals ancillary column N distances 1..92")
    print("OK order-453 prototype equals ancillary column AB distances 1..452")
    print("OK ancillary column AB distance 453 begins template colour 4")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
