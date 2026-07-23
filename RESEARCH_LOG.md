# Research Log

## 2026-07-22 — Hour 0 target audit

- Checked Radziszowski's revision-18 survey: Table XIa still records
  \(R_5(5)\ge41626\).
- Checked Campos--Pohoata, arXiv:2601.15183v1. It is an asymptotic
  multicolor result and does not contain a competing specific order-94
  template or 42078 bound.
- Bounded web and arXiv searches found no order-94 collision. This is recorded
  only as a target-liveness check.
- Recomputed the amplification:
  order 93 gives \(92\cdot452+41=41625\);
  order 94 would give \(93\cdot452+41=42077\).

## 2026-07-22 — Source semantics and off-by-one audit

- Read arXiv:1912.01164v3, Definition 3.1 and Theorem 3.2 with proof.
  The inherited-color cutoff for \(K_5\) is span \(4(m-2)\).
- Therefore order 94 requires maximum distance 368 and vertices
  \(0,\ldots,368\), a graph of order 369.
- The ancillary order-93 fixture tests to the same maximum distance 368,
  overtesting its theorem-required span 364 by four.
- Confirmed the periodic residue convention maps a multiple of \(m-1\) to
  base distance \(m-1\), which is template-colored.

## 2026-07-22 — Verifier-first baseline

- Extracted the published 92-symbol order-93 word from the source ODS/XML.
- Built two independent exact verifiers:
  a Python forward-bit-mask clique search and a C++ explicit candidate-list
  intersection search.
- Both accept the order-93 source seed through span 368.
- Both reject fixtures for malformed length, missing terminal template
  distance, forbidden-prefix template use, additive template triple,
  insufficient span, and explicit color-1/color-2 repeated \(K_5\)'s.
- This establishes `FIN-001`, not `CON-001`.

## 2026-07-22 — Search portfolio and three positive witnesses

- Implemented lazy exact \(K_5\)-constraint separation, Kissat repair,
  exact-profile local descent, seed lifts, unrestricted/reflected partitions,
  and a natural twelve-variable Rowley extension class in
  `search/template_search.py`.
- The structured `rowley-t12` run with random seed 12 found
  `results/order94_t12.template`. The search fixes distances \(1,\ldots,40\)
  to the published seed, fixes 41, 54 through 80, and 93 to the template
  color, and varies the twelve reflection pairs
  \(\{d,134-d\}\), \(42\le d\le53\).
- A direct exact-profile run with seed 1101 independently found
  `results/order94_direct.template`.
- An asymmetric lazy-separation/SAT run with seed 2202 independently found
  `results/order94_lazy.template`.
- The three words are pairwise distinct. Their template-class sizes are
  respectively 39, 35, and 37.
- Both independent full-condition verifiers accept all three words. The
  canonical word was additionally tested through span 372, four full periods,
  and again accepted by both verifiers.

The canonical word is

```text
111212212222121112122121112122221221211131312321323233333333333333333333333333333232312321313
```

Its template distances are

```text
41 43 46 49 51 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68
69 70 71 72 73 74 75 76 77 78 79 80 81 83 85 88 91 93
```

It also satisfies the two reflection identities sufficient for a cyclic
compound:

\[
c(d)=c(41-d)\quad(1\le d\le40),\qquad
c(d)=c(134-d)\quad(41\le d\le93).
\]

## 2026-07-22 — Restricted negative and censored branch

- A 14-variable local repair branch around the one-sum-defect lift was
  reported UNSAT by Kissat and emitted `results/local14.cnf` and
  `results/local14.drat`.
- No independent DRAT checker was available, so this is **not** promoted to a
  certificate-checked nonexistence statement.
- A broader 55-variable local branch was manually interrupted and is
  explicitly censored. Neither negative is needed for the positive result.

## 2026-07-22 — Recovering the order-453 prototype

- Rowley's 2022 construction description says that an order-\(2n+t\)
  template copies a cyclic order-\(n\) prototype verbatim at distances
  \(1,\ldots,n-1\), then puts the new template color at distance \(n\).
- The paper says its order-\(977\) template extends the Exoo-derived
  order-\(453\) \((5,5,5)\) graph.
- In ancillary column `AB`, rows 19 through 470 therefore give all 452
  prototype distances, and row 471 (distance 453) is the new color 4.
- The recovered word is frozen in
  `sources/rowley_exoo_order453.prototype`.
- Independent Python bit-mask and C++ candidate-list searches both find no
  monochromatic \(K_5\) in any of the three colors. They also independently
  confirm cyclic reflection. This closes the previously unpublished-prototype
  dependency.

## 2026-07-22 — Explicit compound coloring

- `tools/compose_rowley.py` expands the canonical template and recovered
  prototype by Rowley's block formula into a 42076-symbol five-color distance
  word on \(K_{42077}\).
- `tests/check_compound_coloring.py` independently reconstructs Rowley's five
  distance sets as literal unions, verifies that every distance
  \(1,\ldots,42076\) is assigned exactly once, and matches the frozen word
  symbol for symbol.
- The compound is cyclic. Its SHA-256 is
  `a97d5dce8a927db2889ba220119f9d4f3d1b88ee24d441f82a803a195ae8028d`.
- By the source-checked composition theorem and the independently verified
  input certificates, it is \(K_5\)-free in all five colors. Hence it proves
  \(R_5(5)\ge42078\).
