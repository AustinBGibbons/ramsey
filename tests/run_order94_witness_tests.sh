#!/bin/sh
set -eu

project_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
tmp_root=${TMPDIR:-/tmp}
verifier_bin=$(mktemp "${tmp_root%/}/ramsey-template-cpp.XXXXXX")
trap 'rm -f -- "$verifier_bin"' EXIT HUP INT TERM

"${CXX:-c++}" -std=c++17 -O2 -Wall -Wextra -pedantic \
  "$project_dir/verifiers/verify_template_cpp.cpp" \
  -o "$verifier_bin"

for witness in \
  "$project_dir/results/order94_t12.template" \
  "$project_dir/results/order94_direct.template" \
  "$project_dir/results/order94_lazy.template" \
  "$project_dir/tests/fixtures/order94_t12_span372.template"
do
  printf '%s\n' "PYTHON $witness"
  python3 "$project_dir/verifiers/verify_template_py.py" "$witness"
  printf '%s\n' "C++ $witness"
  "$verifier_bin" "$witness"
done
