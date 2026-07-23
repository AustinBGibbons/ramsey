# Known Results and Source Map

## `SRC-001` — Rowley's generalized construction

Fred Rowley, “A generalised linear Ramsey graph construction,”
*Australasian Journal of Combinatorics* **81**(2) (2021), 245–256.

- Definition 3.1 defines the distinguished triangle-free template class.
- Theorem 3.2 and its proof give compound order
  \[
  (m-1)(n-1)+1+\phi,\qquad \phi=\min(T)-1.
  \]
- The proof compresses an inherited-colour \(K_k\) obstruction to maximum
  edge length at most \((k-1)(m-2)\).

For an order-99 \((5,5,3)\) template, the exact sufficient cutoff for each
inherited colour is \(4(99-2)=388\).

Primary source:
<https://ajc.maths.uq.edu.au/pdf/81/ajc_v81_p245.pdf>

Source wording caveat: the displayed theorem and its proof phrase the
controlling clique parameter differently. The project uses the explicit
per-inherited-colour compression in the proof. The same convention agrees
with Rowley's published order-93 computation.

## `SRC-002` — Rowley's published order-93 template

Fred Rowley, “Improved Lower Bounds for Multicolour Ramsey Numbers using
SAT-Solvers,” arXiv:2203.13476v3 (18 September 2022).

- Equation (3.5) gives the template composition formula.
- Table 1 gives an effective \((5,5,3)\) template of order 93 with
  \(\phi=40\).
- With an order-453 \((5,5,5)\) prototype it yields a five-colour
  \(K_5\)-free graph of order 41,625 and hence
  \(R_5(5)\ge41,626\).

The exact seed extraction is documented in
`seeds/ROWLEY_ORDER93_EXTRACTION.md`.

Primary source: <https://arxiv.org/abs/2203.13476>

## `FIN-002` — recovered order-453 prototype

The order-453 \((5,5,5)\) prototype used by Rowley is recoverable from the
archived order-977 template in the primary ancillary data: its first 452
distance colours reproduce the prototype, and distance 453 introduces the
new template colour.

The extracted word is
`sources/rowley_exoo_order453.prototype`. Independent Python and C++ exact
clique searches verify that all three colours are \(K_5\)-free. Its
SHA-256 is
`19c97e6279c184f6f462786cadda4b7c9773d870a5b680a04eb1503ef384a2d0`.

## `SUR-001` — checked survey benchmark

Stanisław P. Radziszowski, “Small Ramsey Numbers,” *Electronic Journal of
Combinatorics*, Dynamic Survey DS1, revision 18, 24 April 2026,
DOI 10.37236/21.

Table XIa, printed p. 55, records \(R_5(5)\ge41,626\).

Primary source: <https://doi.org/10.37236/21>

## 2026 literature collision check

Marcelo Campos and Cosmin Pohoata, “An update on multicolor Ramsey lower
bounds,” arXiv:2601.15183 (2026), concerns asymptotic multicolour lower
bounds. It does not state the finite bound \(R_5(5)\ge44,338\) or an
order-99 \((5,5,3)\) template.

Bounded searches on 23 July 2026 for the exact value 44,338, an order-99
Rowley template, and follow-ups to Rowley's papers found no collision. This
is a liveness check, not proof of priority.

## `DER-002` — present payoff

Substituting \(m=99\), \(n=453\), and \(\phi=40\) into Rowley's theorem gives

\[
(99-1)(453-1)+1+40
=98\cdot452+41
=44,337.
\]

The antecedents are met by
`results/order99_linear_prefix8.template` and the recovered order-453
prototype. The complete output is
`results/r5_5_order44337.linear-coloring`, so

\[
R_5(5)\ge44,338.
\]

## `NEG-001` — order-98 nonexistence

No external theorem is imported for this claim. It is a finite exhaustive
result certified by 12 DRAT proofs and the semantic reconstructor in
`certificates/order98_phi40_exhaustion/`.

The prefix stage exhausts all two-colour linear \(K_5\)-free colourings on
the first 40 distances. The tail stage leaves every remaining nonterminal
distance free in all three colours and includes all template-sum and
periodic-\(K_5\) constraints. Global exchange of inherited colours maps the
11 stored prefix representatives to all 22 prefixes.
