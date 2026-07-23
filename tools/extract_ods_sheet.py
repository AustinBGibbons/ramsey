#!/usr/bin/env python3
"""Print nonempty cells from an ODS sheet stored inside Rowley's source tarball.

The arXiv source bundle stores the unzipped ODS members below ``anc/`` rather
than a standalone ``.ods`` file.  This reader intentionally uses only the
Python standard library.  It expands repeated ODF cells only up to a caller
supplied column limit, preserving row/column coordinates and cell styles.
"""

from __future__ import annotations

import argparse
import tarfile
import xml.etree.ElementTree as ET
from pathlib import Path


NS = {
    "office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0",
    "table": "urn:oasis:names:tc:opendocument:xmlns:table:1.0",
    "text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0",
}
TABLE_NAME = f"{{{NS['table']}}}name"
CELL_REPEAT = f"{{{NS['table']}}}number-columns-repeated"
ROW_REPEAT = f"{{{NS['table']}}}number-rows-repeated"
CELL_STYLE = f"{{{NS['table']}}}style-name"
OFFICE_VALUE = f"{{{NS['office']}}}value"
OFFICE_STRING = f"{{{NS['office']}}}string-value"


def column_name(index: int) -> str:
    """Return the one-based spreadsheet column name for zero-based *index*."""
    result = ""
    value = index + 1
    while value:
        value, remainder = divmod(value - 1, 26)
        result = chr(ord("A") + remainder) + result
    return result


def cell_text(cell: ET.Element) -> str:
    text = "".join(cell.itertext()).strip()
    if text:
        return " ".join(text.split())
    return cell.get(OFFICE_STRING, cell.get(OFFICE_VALUE, ""))


def print_sheet(
    archive: Path,
    sheet_name: str,
    max_rows: int,
    max_columns: int,
) -> None:
    with tarfile.open(archive, "r:*") as bundle:
        xml_bytes = bundle.extractfile("anc/content.xml")
        if xml_bytes is None:
            raise ValueError("archive has no anc/content.xml")
        root = ET.parse(xml_bytes).getroot()

    sheets = root.findall(".//table:table", NS)
    selected = next(
        (sheet for sheet in sheets if sheet.get(TABLE_NAME) == sheet_name),
        None,
    )
    if selected is None:
        names = [sheet.get(TABLE_NAME, "") for sheet in sheets]
        raise ValueError(f"unknown sheet {sheet_name!r}; available: {names}")

    logical_row = 0
    for row in selected.findall("table:table-row", NS):
        row_repeat = int(row.get(ROW_REPEAT, "1"))
        if logical_row >= max_rows:
            break

        expanded: list[tuple[int, str, str]] = []
        logical_column = 0
        for cell in row:
            if cell.tag not in {
                f"{{{NS['table']}}}table-cell",
                f"{{{NS['table']}}}covered-table-cell",
            }:
                continue
            repeat = int(cell.get(CELL_REPEAT, "1"))
            value = cell_text(cell)
            style = cell.get(CELL_STYLE, "")
            for offset in range(min(repeat, max(0, max_columns - logical_column))):
                if value:
                    expanded.append((logical_column + offset, value, style))
            logical_column += repeat
            if logical_column >= max_columns:
                break

        for repetition in range(min(row_repeat, max_rows - logical_row)):
            row_number = logical_row + repetition + 1
            for column, value, style in expanded:
                print(
                    f"{column_name(column)}{row_number}\t"
                    f"style={style or '-'}\t{value}"
                )
        logical_row += row_repeat


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    parser.add_argument("--sheet", default="Paper_Sep_2022")
    parser.add_argument("--max-rows", type=int, default=1200)
    parser.add_argument("--max-columns", type=int, default=40)
    args = parser.parse_args()
    print_sheet(args.archive, args.sheet, args.max_rows, args.max_columns)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
