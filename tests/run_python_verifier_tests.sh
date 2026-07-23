#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
project_dir=$(CDPATH= cd -- "$script_dir/.." && pwd)
verifier="$project_dir/verifiers/verify_template_py.py"

expect_valid() {
    candidate=$1
    echo "EXPECT VALID: $candidate"
    python3 "$verifier" "$candidate"
}

expect_invalid() {
    candidate=$1
    echo "EXPECT INVALID: $candidate"
    if python3 "$verifier" "$candidate"; then
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

echo "Python verifier tests passed"
