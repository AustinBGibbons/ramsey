#!/bin/sh
set -eu

# Verify the order-99 template and its explicit compound five-coloring.

project_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
tmp_root=${TMPDIR:-/tmp}
template_bin=$(mktemp "${tmp_root%/}/ramsey-order99-template.XXXXXX")
prototype_bin=$(mktemp "${tmp_root%/}/ramsey-order99-prototype.XXXXXX")
compound_tmp=$(mktemp "${tmp_root%/}/ramsey-order99-compound.XXXXXX")
trap 'rm -f -- "$template_bin" "$prototype_bin" "$compound_tmp"' \
  EXIT HUP INT TERM

"${CXX:-c++}" -std=c++17 -O2 -Wall -Wextra -Wpedantic -Werror \
  "$project_dir/verifiers/verify_template_cpp.cpp" \
  -o "$template_bin"

printf '%s\n' "PYTHON order-99 template"
python3 "$project_dir/verifiers/verify_template_py.py" \
  "$project_dir/results/order99_linear_prefix8.template"
printf '%s\n' "C++ order-99 template"
"$template_bin" "$project_dir/results/order99_linear_prefix8.template"

printf '%s\n' "PYTHON order-453 prototype"
python3 "$project_dir/verifiers/verify_linear_prototype_py.py" \
  "$project_dir/sources/rowley_exoo_order453.prototype"

"${CXX:-c++}" -std=c++17 -O2 -Wall -Wextra -Wpedantic -Werror \
  "$project_dir/verifiers/verify_linear_prototype_cpp.cpp" \
  -o "$prototype_bin"
printf '%s\n' "C++ order-453 prototype"
"$prototype_bin" "$project_dir/sources/rowley_exoo_order453.prototype"

(
  cd "$project_dir"
  python3 tools/compose_rowley.py \
    results/order99_linear_prefix8.template \
    sources/rowley_exoo_order453.prototype \
    "$compound_tmp"
)

if ! cmp -s \
  "$compound_tmp" \
  "$project_dir/results/r5_5_order44337.linear-coloring"
then
  printf '%s\n' "generated compound differs from frozen artifact" >&2
  exit 1
fi

python3 "$project_dir/tests/check_compound_coloring_generic.py" \
  "$project_dir/results/order99_linear_prefix8.template" \
  "$project_dir/sources/rowley_exoo_order453.prototype" \
  "$project_dir/results/r5_5_order44337.linear-coloring" \
  --sha256 \
  274acbf17bf7732b16ef7d20c97486eb469486907fd1357c16990ed4332f7158

printf '%s\n' "PASS order-99 breakthrough suite"
