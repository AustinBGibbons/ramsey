# Results and Closeout

## Lead result

An explicit effective Rowley \((5,5,3)\) template of order \(94\) and
\(\phi=40\) has been found. Rowley's composition theorem, applied to the
source-recovered cyclic \((5,5,5;453)\) prototype, gives an explicit cyclic
five-coloring of \(K_{42077}\) with no monochromatic \(K_5\). Consequently,

\[
\boxed{R_5(5)\ge42078}.
\]

The canonical template certificate is
`results/order94_t12.template`. The fully expanded five-color distance word is
`results/r5_5_order42077.linear-coloring`.

## Claims changed

- `SRC-001`, `SRC-002`, and `SUR-001` are source-verified.
- `DER-001` records the source theorem and exact 42078 implication.
- `FIN-001` is a verified exact computation for the published order-93 seed.
- `FIN-002` independently verifies the recovered order-453 prototype.
- `FIN-003` independently checks the exact expanded compound word.
- `CON-001` moved from `conjecture` to `verified-exact-computation`.

## Evidence and artifacts produced

- Preserved primary source PDFs and Rowley's ancillary source archive.
- Extracted and hashed the published order-93 word.
- Found three distinct order-94 certificates by three search routes.
- Added independent Python and C++ exact verifiers for both the template and
  the recovered order-453 prototype.
- Recovered all 452 prototype distance colors from Rowley's archived
  order-977 template and checked them against the source XML.
- Generated the complete 42076-symbol compound word and independently
  reconstructed it from the displayed set-union formulas.

## Commands run and exit results

```sh
cd /Users/austingibbons/gather/maths/ramsey-template-94
sh tests/run_python_verifier_tests.sh
sh tests/run_cpp_verifier_tests.sh
python3 search/template_search.py --self-test
sh tests/run_end_to_end_checks.sh
```

All commands exited 0. The semantic suites accept the published positive
fixture and reject all seven invalid fixtures. The end-to-end suite:

- checks both source extractions against the hash-fixed ancillary XML;
- verifies the order-453 prototype in all three colors with two algorithms;
- verifies all three order-94 words with two algorithms;
- overtests the canonical word through span 372;
- checks all 42076 compound distances, uniqueness, cyclic reflection, and the
  frozen hash.

## Continuous certificate verification

The portable release-critical entry point is now:

```sh
sh tests/run_certificate_checks.sh
```

It excludes the heuristic search and third-party source archive while
checking every frozen finite object used in the theorem. The complete local
source-provenance path remains:

```sh
sh tests/run_end_to_end_checks.sh
```

`.github/workflows/verify-certificates.yml` schedules the portable suite on
both `ubuntu-latest` and `macos-latest` for pushes, pull requests, and manual
dispatches. The workflow has read-only repository permissions and a
20-minute job timeout. Local validation completed with:

```sh
sh tests/run_certificate_checks.sh
sh tests/run_end_to_end_checks.sh
ruby -e 'require "yaml"; ARGV.each { |f| YAML.load_file(f) }' \
  .github/workflows/verify-certificates.yml
```

All exited 0. Hosted-runner execution remains an external deployment check
until the repository is pushed to GitHub.

## Failed approaches and negative results

- A one-sum-defect lift failed because \(41+52=93\).
- A 14-variable repair class was reported UNSAT by Kissat, but its DRAT output
  has not been independently checked and is not claimed as a certified
  negative.
- A larger 55-variable repair branch was interrupted and is censored.
- These branches are retained for provenance but are irrelevant to the three
  positive witnesses.

## Unresolved obligations and severity

The two critical mathematical obligations `OBL-001` and `OBL-002` are
discharged. Remaining external obligations are:

- **Priority/novelty gate:** bounded searches found no collision, and the
  current revision-18 survey still records 41626, but an external literature
  check and author contact should precede a public priority claim.
- **Independent-machine gate:** rerun `tests/run_end_to_end_checks.sh` from a
  clean checkout on a second machine.
- **Human promotion gate:** the harness deliberately does not label the result
  `certificate-checked` or publication-ready until an external reviewer signs
  off.

## Recommended next actions

1. Send the self-contained review packet and repository to Fred Rowley,
   Stanisław Radziszowski, and an independent computational Ramsey referee.
2. Ask Rowley to confirm the ancillary-column recovery of the order-453
   prototype and the exact Theorem 3.2 specialization.
3. After independent reproduction, prepare a short computational note centered
   on \(L^T(5,5,3)\ge94\) and the corollary \(R_5(5)\ge42078\).
4. Preserve the two alternative witnesses as robustness evidence; use the
   reflected canonical witness in the paper because it also yields a cyclic
   compound.

## Human gate

No human has yet approved a public novelty or publication-readiness claim.
Mathematically, the finite certificate and theorem chain are complete; the
remaining gate is independent external reproduction and priority review, not
an open proof step.
