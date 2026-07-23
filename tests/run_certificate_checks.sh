#!/bin/sh
set -eu

# Verify every finite object used by the claimed Ramsey lower bound without
# depending on downloaded primary-source archives or on the heuristic search.

project_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
tmp_root=${TMPDIR:-/tmp}
prototype_bin=$(mktemp "${tmp_root%/}/ramsey-prototype-cpp.XXXXXX")
trap 'rm -f -- "$prototype_bin"' EXIT HUP INT TERM

sh "$project_dir/tests/run_python_verifier_tests.sh"
sh "$project_dir/tests/run_cpp_verifier_tests.sh"

printf '%s\n' "PYTHON order-453 prototype"
python3 "$project_dir/verifiers/verify_linear_prototype_py.py" \
  "$project_dir/sources/rowley_exoo_order453.prototype"

"${CXX:-c++}" -std=c++17 -O2 -Wall -Wextra -Wpedantic -Werror \
  "$project_dir/verifiers/verify_linear_prototype_cpp.cpp" \
  -o "$prototype_bin"
printf '%s\n' "C++ order-453 prototype"
"$prototype_bin" "$project_dir/sources/rowley_exoo_order453.prototype"

sh "$project_dir/tests/run_order94_witness_tests.sh"
python3 "$project_dir/tests/check_compound_coloring.py"

printf '%s\n' "PASS Ramsey certificate suite"
