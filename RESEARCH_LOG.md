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

## 2026-07-23 — Reflected extension family

- The reflected \(\phi=40\) construction extends the retained positive
  sequence through orders 95, 96, and 97.
- For period \(p=2q+r\), \(q=40\), its template shell is encoded by
  \(U\subseteq\{1,\ldots,r\}\). Within this family the template colour is
  sum-free exactly when no \(a,b,c\in U\) satisfy
  \(a+b+c=r+1\).
- The order-97 word is frozen in `results/order97_reflected.template` and
  passes both independent full-condition verifiers.
- These family searches were hypothesis generation; only frozen positive
  words and certificate-backed negative statements are promoted.

## 2026-07-23 — Exhaustive order-98 nonexistence certificate

- The constraint \(\phi\ge40\) forces a two-colour linear \(K_5\)-free
  prefix on distances \(1,\ldots,40\).
- Exact enumeration yields 22 prefixes, or 11 up to global exchange of the
  two inherited colours.
- One prefix-exhaustion CNF plus one unrestricted tail CNF for each
  representative covers every order-98 candidate. Tail distances
  \(41,\ldots,96\) are fully free in all three colours; distance 97 is the
  template colour.
- All 12 instances are UNSAT. Every DRAT proof verifies with `drat-trim`.
- The independent checker regenerates the 45,374 unique prefix distance
  sets, validates all listed prefixes, validates every recorded sum or
  five-vertex obstruction, and reconstructs every CNF byte-for-byte before
  proof checking.
- This establishes global nonexistence at order 98 with \(\phi\ge40\), not
  merely failure of the reflected family.

## 2026-07-23 — Order-99 symmetry-breaking escape

- Search over the 11 prefix types found an order-99 template using the eighth
  non-cyclic \(K_{41}\) prefix.
- The word in `results/order99_linear_prefix8.template` has period 98,
  actual \(\phi=40\), 33 template-colour distances, and exact span 388.
- Independent Python and C++ verifiers accept it. Their inherited-colour
  search counts are 1,645,997 and 917,897 nodes in the Python implementation.
- The Rowley composition has order
  \(98\cdot452+41=44,337\). The complete word is frozen in
  `results/r5_5_order44337.linear-coloring`.
- The generator and a separate literal set-union reconstruction agree on all
  44,336 distances and the SHA-256
  `274acbf17bf7732b16ef7d20c97486eb469486907fd1357c16990ed4332f7158`.
- The compound is linear and non-cyclic; no cyclicity hypothesis is used.
- Orders 100–105 produced no positive in reconnaissance runs, but those
  negatives have no retained proof certificates and are not claims.

## 2026-07-23 — Release integration

- The portable release gate now verifies the order-97 and order-99 positive
  objects, the explicit \(K_{44,337}\) compound, and the complete order-98
  DRAT packet.
- `drat-trim.c` is vendored from upstream commit
  `2e3b2dc0ecf938addbd779d42877b6ed69d9a985` under its MIT license and
  compiled from source during verification.
- The order-94 result and tests remain as reproducibility history.
