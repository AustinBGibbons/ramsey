#!/usr/bin/env python3
"""Prepare a macOS Quick Look DOCX preview for headless PDF visual QA."""

from __future__ import annotations

import re
import sys
from pathlib import Path


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: prepare_quicklook_print.py INPUT_HTML OUTPUT_HTML")

    source = Path(sys.argv[1])
    target = Path(sys.argv[2])
    html = source.read_text(encoding="utf-8")

    # Quick Look represents explicit Word page breaks as a form-feed in a
    # one-run paragraph. Turn those into print page breaks for Chromium.
    html, count = re.subn(
        r'<p[^>]*><span[^>]*>\x0c</span></p>',
        '<div class="manual-page-break"></div>',
        html,
    )
    if count != 8:
        raise SystemExit(f"expected 8 manual page breaks, found {count}")

    print_css = """
<style id="codex-print-qa">
@page { size: Letter portrait; margin: 0.72in 0.78in 0.72in 0.78in; }
html, body { margin: 0 !important; padding: 0 !important; }
.s1 {
  width: auto !important;
  min-height: 0 !important;
  padding: 0 !important;
  overflow: visible !important;
}
.manual-page-break { break-before: page; page-break-before: always; height: 0; }
table { break-inside: avoid; page-break-inside: avoid; }
p, div { orphans: 2; widows: 2; }
</style>
"""
    html = html.replace("</head>", print_css + "</head>", 1)
    target.write_text(html, encoding="utf-8")
    print(target)


if __name__ == "__main__":
    main()
