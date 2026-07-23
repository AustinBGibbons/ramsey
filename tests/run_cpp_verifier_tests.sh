#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
project_dir=$(CDPATH= cd -- "$script_dir/.." && pwd)
binary="${TMPDIR:-/tmp}/ramsey_verify_template_cpp_test_$$"

cleanup() {
    rm -f -- "$binary"
}
trap cleanup EXIT HUP INT TERM

c++ -std=c++17 -O2 -Wall -Wextra -Wpedantic -Werror \
    "$project_dir/verifiers/verify_template_cpp.cpp" -o "$binary"

expect_valid() {
    candidate=$1
    echo "EXPECT VALID: $candidate"
    "$binary" "$candidate"
}

expect_invalid() {
    candidate=$1
    echo "EXPECT INVALID: $candidate"
    if "$binary" "$candidate"; then
        echo "failure: invalid fixture was accepted: $candidate" >&2
        exit 1
    else
        status=$?
    fi
    if [ "$status" -ne 1 ]; then
        echo "failure: expected semantic-invalid exit 1, got $status: $candidate" >&2
        exit 1
    fi
}

expect_valid "$project_dir/tests/fixtures/cpp_valid_small.template"
expect_valid "$project_dir/seeds/rowley_order93.template"

expect_invalid "$project_dir/tests/fixtures/cpp_invalid_length.template"
expect_invalid "$project_dir/tests/fixtures/cpp_invalid_terminal.template"
expect_invalid "$project_dir/tests/fixtures/cpp_invalid_prefix.template"
expect_invalid "$project_dir/tests/fixtures/cpp_invalid_sum.template"
expect_invalid "$project_dir/tests/fixtures/cpp_invalid_short_span.template"
expect_invalid "$project_dir/tests/fixtures/cpp_invalid_repeated_k5.template"
expect_invalid "$project_dir/tests/fixtures/cpp_invalid_blue_k5.template"

echo "C++ verifier tests passed"
