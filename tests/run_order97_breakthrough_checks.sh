#!/bin/sh
set -eu

# Verify the reflected order-95 through order-97 templates.  In particular,
# order 97 is the lower positive witness surrounding the order-98 hole.

project_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
tmp_root=${TMPDIR:-/tmp}
template_bin=$(mktemp "${tmp_root%/}/ramsey-order97-template.XXXXXX")
trap 'rm -f -- "$template_bin"' EXIT HUP INT TERM

"${CXX:-c++}" -std=c++17 -O2 -Wall -Wextra -Wpedantic -Werror \
  "$project_dir/verifiers/verify_template_cpp.cpp" \
  -o "$template_bin"

for witness in \
  "$project_dir/results/order95_reflected.template" \
  "$project_dir/results/order96_reflected.template" \
  "$project_dir/results/order97_reflected.template"
do
  printf '%s\n' "PYTHON $witness"
  python3 "$project_dir/verifiers/verify_template_py.py" "$witness"
  printf '%s\n' "C++ $witness"
  "$template_bin" "$witness"
done

printf '%s\n' "PASS reflected order-95 through order-97 template suite"
