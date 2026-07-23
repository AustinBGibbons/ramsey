# Order-94 Rowley template campaign

## Result

This directory contains an explicit effective Rowley \((5,5,3)\) template of
order \(94\) with \(\phi=40\). Combined with the independently recovered and
verified cyclic \((5,5,5;453)\) prototype, Rowley's construction gives a cyclic
five-coloring of \(K_{42077}\) without a monochromatic \(K_5\), hence

\[
R_5(5)\ge42078.
\]

The canonical certificate is
`results/order94_t12.template`. The complete expanded distance coloring is
`results/r5_5_order42077.linear-coloring`.

## Continuous certificate verification

`.github/workflows/verify-certificates.yml` runs the release-critical
certificate suite on both Ubuntu and macOS for every push and pull request,
and can also be started manually from the Actions tab.

The CI entry point is portable and has no network or third-party Python
dependency:

```sh
sh tests/run_certificate_checks.sh
```

It checks positive and negative verifier fixtures, compiles and runs the
independent C++ implementations, verifies the order-453 prototype and all
frozen order-94 witnesses, and reconstructs the complete compound word. The
separate end-to-end command below additionally checks provenance against the
locally hash-fixed arXiv source archive.

## One-command verification

```sh
cd /Users/austingibbons/gather/maths/ramsey-template-94
sh tests/run_end_to_end_checks.sh
```

The test:

1. re-extracts the published order-93 seed and order-453 prototype from the
   hash-fixed arXiv ancillary XML;
2. checks the order-453 prototype with independent Python and C++ exact
   clique searches;
3. checks three distinct order-94 witnesses with independent Python and C++
   full-period verifiers;
4. overtests the canonical witness through span 372; and
5. independently reconstructs all 42076 distances of the expanded compound
   coloring and checks its hash.

## Review

The self-contained external-review document is `REVIEW_PACKET.md`. It includes
the exact theorem statement used, both input words, the proof map, verifier
pseudocode, hashes, commands, known limitations, and an adversarial review
directive.

Correctness and priority are separate. The checked survey record is
\(R_5(5)\ge41626\), and bounded searches found no collision, but this repository
does not claim priority or publication readiness before independent external
review.
