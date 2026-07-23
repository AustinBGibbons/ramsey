#!/bin/sh
set -eu

project_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)

python3 "$project_dir/tests/check_source_extractions.py"
sh "$project_dir/tests/run_certificate_checks.sh"
