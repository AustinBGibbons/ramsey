# Known Results

## `SRC-001` — Rowley's generalized construction and finite cutoff

Primary source: Fred Rowley, *A generalised linear Ramsey graph
construction*, arXiv:1912.01164v3 (24 June 2021).

- Definition 3.1, printed p. 4: a tf-template is the distinguished
  triangle-free distance class containing \(m-1\).
- Theorem 3.2 and proof, printed pp. 4–6: a template
  \(U(k_1,\ldots,k_{q-1},3;m)\) and a second linear prototype of order \(n\)
  produce a compound graph of order
  \((m-1)(n-1)+1+\phi\), with \(\phi=\min(T)-1\).
- Proof on printed p. 5 continuing to p. 6: an inherited-color
  \(K_{k_s}\) can be compressed so that its largest edge length is at most
  \((k_s-1)(m-2)\).

Hypothesis map: our colors 1 and 2 are the inherited colors with
\(k_s=5\); color 3 is the tf-template; \(m=94\). Hence the exact sufficient
span is \(4(94-2)=368\).

Source wording caveat: the theorem statement describes \(Q\) as the maximum
clique number in \(U\), whereas the proof defines the controlling quantity
as \(\sup(k_s-1)\). For the published \((5,5,3)\) seed both inherited
colors contain \(K_4\), so both readings give \(Q=4\). This project relies on
the proof's explicit per-color bound.

## `SRC-002` — published order-93 template and 41626 bound

Primary source: Fred Rowley, *Improved Lower Bounds for Multicolour Ramsey
Numbers using SAT-Solvers*, arXiv:2203.13476v3 (18 September 2022).

- Equation (3.5), printed p. 4: the template composition formula.
- Table 1, printed p. 6: an effective \((5,5,3)\) template of order 93,
  with \(\phi=40\), and the resulting order-41625 five-color construction,
  hence \(R_5(5)\ge41626\).
- Ancillary spreadsheet, sheet `Paper_Sep_2022`, column `TFT(S)`: the
  explicit template word and a multiple-repetition test through graph order
  369.

The exact extraction, including distance-class lists and the source archive
hash, is in `seeds/ROWLEY_ORDER93_EXTRACTION.md`.

## Recovering and checking the order-453 prototype

The order-\(453\) \((5,5,5)\) prototype is described in
arXiv:1912.01164v3, printed p. 7, as an unpublished graph derived by Geoffrey
Exoo; the paper uses it in a verified order-\(4072\) construction. The later
paper arXiv:2203.13476v3 makes the prototype recoverable from primary archived
data:

- Section 5, printed p. 5, defines the search construction by copying the
  edge colors of a cyclic order-\(n\) prototype at distances \(1,\ldots,n-1\),
  before placing the new template color at distance \(n\).
- Printed p. 6 states that the archived order-\(977\)
  \((5,5,5,3)\) template was obtained by extending the order-\(453\)
  Exoo-derived graph.
- In the ancillary `Paper_Sep_2022` sheet, column `AB` is that order-\(977\)
  template. Its entries at distances \(1,\ldots,452\) therefore reproduce the
  order-\(453\) prototype verbatim; distance \(453\) is color 4, the new
  template color.

The extracted 452-symbol word is frozen in
`sources/rowley_exoo_order453.prototype`. Two independent exact clique
searches verify that it is cyclic and contains no monochromatic \(K_5\) in
any of its three colors. Thus the composition corollary no longer depends on
an unavailable private prototype file.

## `SUR-001` — current recorded specific lower bound

Primary source: Stanisław P. Radziszowski, *Small Ramsey Numbers*,
Electronic Journal of Combinatorics Dynamic Survey DS1, revision 18,
24 April 2026, DOI 10.37236/21.

Table XIa, printed p. 55, records \(R_5(5)\ge41626\). The title page identifies
revision 18 as the 24 April 2026 revision. The official survey page checked on
22 July 2026 exposed revision 18 as the latest available revision.

## January 2026 collision check

Marcelo Campos and Cosmin Pohoata, *An update on multicolor Ramsey lower
bounds*, arXiv:2601.15183v1 (21 January 2026), proves asymptotic
multicolor lower-bound improvements. It does not state a new specific
\(R_5(5)\) bound or an order-94 \((5,5,3)\) template.

Bounded search outcome, 22 July 2026: searches for the target value 42078 and
an order-94 Rowley template found no collision. This is a target-liveness
check, not a novelty conclusion.

## `DER-001` — target payoff

For a target order-94 template with \(\phi\ge40\), specialize Rowley's
formula using the order-453 \((5,5,5)\) prototype:

\[
(94-1)(453-1)+1+\phi
\ge93\cdot452+41=42077.
\]

The resulting explicit five-color \(K_5\)-free graph proves
\(R_5(5)\ge42078\).

The antecedent is now met by `results/order94_t12.template`; the second
prototype is the independently checked source extraction above. The exact
expanded 42076-symbol distance word is
`results/r5_5_order42077.linear-coloring`.
