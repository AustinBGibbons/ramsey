# External review packet

## An order-94 effective \((5,5,3)\) Rowley template and the bound
\(\boldsymbol{R_5(5)\ge42078}\)

Date: 22 July 2026

Status: complete exact certificate and complete source-theorem reduction;
priority and publication readiness intentionally await external review.

## 1. Lead claim

There is a linear three-coloring

\[
c:\{1,\ldots,93\}\to\{1,2,3\}
\]

whose color-3 distances form a Rowley triangle-free template with
\(\phi=40\), and whose colors 1 and 2 remain \(K_5\)-free under period-93
repetition through maximum distance \(368=4(94-2)\).

Fred Rowley's Generalised Construction Theorem then combines this template
with a linear \((5,5,5;453)\) prototype to produce a linear five-coloring of
\(K_{42077}\) with no monochromatic \(K_5\). Therefore

\[
\boxed{R_5(5)\ge42078}.
\]

The canonical order-94 word, the recovered order-453 word, and the expanded
42076-symbol five-color word are all explicit and frozen below or in the
referenced artifacts.

## 2. Exact definitions

For a word \(c:\{1,\ldots,m-1\}\to\{1,2,3\}\), color edge
\(\{i,j\}\), \(i<j\), of \(K_m\) by \(c(j-i)\). Write

\[
L_1=c^{-1}(1),\qquad L_2=c^{-1}(2),\qquad T=c^{-1}(3).
\]

The color-3 class is a Rowley tf-template when \(m-1\in T\) and it is
triangle-free. In a linear distance coloring, the latter is equivalent to

\[
\nexists\,a,b>0\quad a,b,a+b\in T,
\]

with \(a=b\) allowed. Its extension parameter is

\[
\phi=\min(T)-1.
\]

For an inherited color \(s\in\{1,2\}\), period-\((m-1)\) repetition gives
positive distance \(d\) color \(s\) exactly when

\[
c\!\left(((d-1)\bmod(m-1))+1\right)=s.
\]

The representative of residue zero is \(m-1\), not 0. This convention is
load-bearing.

## 3. Source theorem and hypothesis map

Primary source:

Fred Rowley, *A generalised linear Ramsey graph construction*,
arXiv:1912.01164v3, Definition 3.1 and Theorem 3.2 with proof, printed
pp. 4–6.

The theorem takes:

- a linear \(U(k_1,\ldots,k_{q-1},3;m)\) whose final color is a
  tf-template \(T\), and
- a linear \(V(k_{q+1},\ldots,k_{q+r};n)\),

and constructs a linear Ramsey graph of order

\[
(m-1)(n-1)+1+\phi,\qquad \phi=\min(T)-1.
\]

The template color is eliminated. Clique numbers in the colors inherited
from \(V\) equal those of \(V\). For an inherited color of \(U\) that forbids
\(K_k\), Rowley's proof compresses every offending clique to maximum edge
length at most

\[
(k-1)(m-2).
\]

Here \(m=94\) and \(k=5\), so it is sufficient and exact for our use to check
maximum distance

\[
4(94-2)=368,
\]

meaning the 369 vertices \(0,\ldots,368\). This is not a 368-vertex test.

Source caveat: the displayed theorem statement describes its cutoff parameter
\(Q\) differently from the proof. We use the proof's explicit per-color
\((k_s-1)(m-2)\) argument. The full proof text was audited, and our finite
test uses that larger explicit cutoff.

## 4. Canonical order-94 certificate

Artifact:

```text
results/order94_t12.template
SHA-256 a3dd3415956277d68fc0197f6f5e35c38f2ed7936c66f11f658b0c57688abec1
```

Distance word \(c(1)c(2)\cdots c(93)\):

```text
111212212222121112122121112122221221211131312321323233333333333333333333333333333232312321313
```

The three distance classes are:

```text
color 1:
1 2 3 5 8 13 15 16 17 19 22 24 25 26 28 33 36 38 39 40
42 44 48 86 90 92

color 2:
4 6 7 9 10 11 12 14 18 20 21 23 27 29 30 31 32 34 35 37
45 47 50 52 82 84 87 89

template color 3:
41 43 46 49 51 53 54 55 56 57 58 59 60 61 62 63 64 65 66
67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 83 85 88 91 93
```

Immediate checks:

- \(93\in T\);
- \(T\cap[1,40]=\varnothing\);
- \(\min T=41\), hence \(\phi=40\);
- exact enumeration finds no \(a,b,a+b\in T\);
- two independent exact algorithms find no \(K_5\) in either repeated
  inherited color on vertices \(0,\ldots,368\).

The word also obeys

\[
c(d)=c(41-d)\quad(1\le d\le40),
\]

and

\[
c(d)=c(134-d)\quad(41\le d\le93).
\]

These are Rowley's sufficient reflection conditions for the compound to be
cyclic when the second prototype is cyclic.

Two additional, distinct accepted words are frozen as
`results/order94_direct.template` and
`results/order94_lazy.template`. Their template-class sizes are 35 and 37,
versus 39 for the canonical word. They are robustness evidence, not needed
for the proof.

## 5. Exact verification algorithms

### 5.1 Template checks

Both verifiers first perform the non-graph checks literally:

1. parse exactly four records: order, phi lower bound, repeat span, and word;
2. check word length \(m-1\) and alphabet \(\{1,2,3\}\);
3. check \(c(m-1)=3\);
4. list \(T\) and check \(\min T-1\ge40\);
5. for every \(a,b\in T\), including \(a=b\), reject if \(a+b\in T\);
6. reject unless the requested span is at least \(4(m-2)\).

For each \(s=1,2\), they then construct the exact graph on
\(\{0,\ldots,\text{span}\}\) by the periodic residue rule and exhaustively
search for \(K_5\).

### 5.2 DFS pseudocode

```text
Algorithm 1  Exact monochromatic clique search
Input: ordered vertices V, adjacency predicate Adj, target size k
Output: a k-clique, or NONE

Search(prefix, candidates, need):
    If need = 0:
        Return prefix
    If |candidates| < need:
        Return NONE
    While |candidates| >= need:
        v <- least vertex in candidates
        Delete v from candidates
        next <- {u in candidates : Adj(v,u)}
        result <- Search(prefix followed by v, next, need-1)
        If result is not NONE:
            Return result
    Return NONE

Return Search(empty sequence, V, k)
```

Every recursive candidate list is strictly increasing. Thus each possible
clique is represented once. Intersecting with the new vertex's forward
neighbors maintains exactly the vertices adjacent to every prefix vertex.
The cardinality prune removes only branches that cannot reach size \(k\).
Consequently returning `NONE` is an exhaustive proof of nonexistence.

The implementations are deliberately different:

- `verifiers/verify_template_py.py` uses Python arbitrary-precision integers
  as forward-neighbor bit masks.
- `verifiers/verify_template_cpp.cpp` uses explicit ordered integer vectors
  and pairwise filtering; it shares neither parser nor clique-search code.

For the canonical span-368 witness, the Python verifier visits 550,261 search
nodes in color 1 and 718,490 in color 2. Both implementations return `VALID`.
Both also return `VALID` when the same word is overtested through span 372.

Seven negative fixtures cover malformed length, missing terminal template
distance, forbidden-prefix use, an additive template triple, insufficient
span, and explicit repeated \(K_5\)'s in each inherited color.

## 6. Recovering and checking the order-453 prototype

The second prototype was previously described as unpublished, but it is
recoverable from Rowley's archived 2022 data.

Primary source:

Fred Rowley, *Improved Lower Bounds for Multicolour Ramsey Numbers using
SAT-Solvers*, arXiv:2203.13476v3, Section 5 and Table 1, printed pp. 5–6,
plus ancillary sheet `Paper_Sep_2022`.

The construction on printed p. 5 begins from a cyclic order-\(n\) prototype
and copies its colors verbatim at distances \(1,\ldots,n-1\), before assigning
the new template color at distance \(n\). Printed p. 6 says that the
order-\(977\) \((5,5,5,3)\) template was obtained by extending an
Exoo-derived \((5,5,5;453)\) graph. In ancillary column `AB`, therefore,
rows 19–470 are precisely its 452 prototype distances; row 471, representing
distance 453, is color 4.

The source archive is:

```text
sources/arxiv-2203.13476-source.tar.gz
SHA-256 5041096a33d6898c116a35a102e521fb14fe872fb18c20ff7d30822ed4c396b2
```

Recovered prototype word:

```text
12223333221211121312122313122213232232332221323223233221111122121112213132231212232313223121323231222132332111122233231221212233323221121321211122312112223323233233232332223323321111122111112313122221312231312212132223121122233222112132223121221313221312222131321111122111112332332223323233233232332221121322111212312112232333221212213233222111123323122213232312132231323221213223131221112122111112233232232312223323223231222131322121312111212233332221
```

Artifact:

```text
sources/rowley_exoo_order453.prototype
SHA-256 19c97e6279c184f6f462786cadda4b7c9773d870a5b680a04eb1503ef384a2d0
```

`tests/check_source_extractions.py` compares every symbol with the hash-fixed
ancillary XML and checks the metadata and first new-template position.

Two further independent exact verifiers check the finite linear graph
directly:

- Python bit-mask search:
  1,040,265 / 5,811,421 / 782,585 nodes in colors 1 / 2 / 3;
- C++ ordered-vector search:
  237,855 / 837,235 / 201,199 nodes in colors 1 / 2 / 3.

Both find no monochromatic \(K_5\). Both independently confirm
\(v(d)=v(453-d)\), so the prototype is cyclic. Even if the historical
attribution were ignored, this explicit independently checked word itself is
all the composition theorem needs.

## 7. The explicit 42077-vertex compound

Let \(p=93\), let \(A_1,A_2,T\) be the three distance classes of the canonical
template, and let \(B_1,B_2,B_3\) be the three distance classes of the
order-453 prototype.

For \(s=1,2\), Rowley's inherited distance sets are

\[
A'_s=
\{\ell+(\mu-1)p:\ell\in A_s,\ 1\le\mu\le452\}
\cup
\{\ell+452p:\ell\in A_s,\ 1\le\ell\le40\}.
\]

For \(j=1,2,3\), relabeling the three prototype colors as output colors
\(j+2\), put

\[
B'_j=
\{\ell+(\mu-1)p:\ell\in T,\ \mu\in B_j\}.
\]

These five sets partition exactly

\[
\{1,\ldots,42076\}.
\]

Color edge \(\{x,y\}\), \(x<y\), of \(K_{42077}\) according to the unique set
containing \(y-x\). This is the complete explicit coloring.

The order calculation is

\[
(94-1)(453-1)+1+40
=93\cdot452+41
=42077.
\]

`tools/compose_rowley.py` emits the expanded word. Independently,
`tests/check_compound_coloring.py` constructs the five sets above as literal
unions, checks that all 42076 distances occur exactly once, and compares every
symbol with the frozen output.

Expanded artifact:

```text
results/r5_5_order42077.linear-coloring
SHA-256 a97d5dce8a927db2889ba220119f9d4f3d1b88ee24d441f82a803a195ae8028d
```

It has distance-class sizes:

```text
color 1: 11772
color 2: 12676
color 3:  5304
color 4:  7566
color 5:  4758
total:   42076
```

It also satisfies cyclic reflection.

## 8. Proof of the Ramsey bound

**Theorem.** There is a five-coloring of \(K_{42077}\) with no
monochromatic \(K_5\). Consequently \(R_5(5)\ge42078\).

**Proof.**
The canonical word has template color containing distance 93, its template
set is sum-free, and \(\phi=40\). Hence it is a tf-template of order 94.

We spell out the two preservation arguments in this specialization rather
than treating the source theorem as a black box.

First suppose an inherited color \(s\in\{1,2\}\) contains a \(K_5\) in the
compound. Translate its least vertex to 0 and write its other vertices as

\[
0<h_1<h_2<h_3<h_4.
\]

Every \(h_i\) and every difference \(h_j-h_i\) has a residue in \(A_s\)
modulo \(p=93\). If \(h_1>p\), subtract \(p\) from all four positive
coordinates. If a consecutive gap \(h_{i+1}-h_i\) exceeds \(p\), subtract
\(p\) from the entire upper tail \(h_{i+1},\ldots,h_4\). Each operation
preserves positivity, strict order, and every relevant color: cross-tail
differences change by exactly \(p\), while within-tail and below-tail
differences do not change. Repeating terminates with \(h_1\le p\) and every
consecutive gap at most \(p\). No inherited-color edge can have length
divisible by \(p\), because residue \(p=93\) lies in the template color.
Therefore \(h_1\le p-1\), every consecutive gap is at most \(p-1\), and

\[
h_4\le4(p-1)=368.
\]

This would be a \(K_5\) in the exact span-368 graph rejected by both
verifiers, a contradiction.

Now fix one of the three prototype-derived output colors, corresponding to
prototype distance class \(B_j\), and suppose it contains a \(K_5\). Again
translate its least vertex to 0. Every other vertex has a unique form

\[
d_i=t_i+(\mu_i-1)p,\qquad t_i\in T,\quad \mu_i\in B_j.
\]

Take two with \(d_i<d_k\). If \(t_i<t_k\), then the positive residue of
\(d_k-d_i\) is \(t_k-t_i\). This cannot lie in \(T\), since

\[
t_i+(t_k-t_i)=t_k
\]

would violate sum-freeness. Hence an edge of the same prototype-derived color
forces \(t_i\ge t_k\). If \(t_i=t_k\), the difference is
\((\mu_k-\mu_i)p\), whose prototype index is \(\mu_k-\mu_i\). If
\(t_i>t_k\), then

\[
d_k-d_i=
\bigl(p-(t_i-t_k)\bigr)+(\mu_k-\mu_i-1)p,
\]

so its prototype index is again \(\mu_k-\mu_i\). In either case, membership
of the difference in the same output color implies
\(\mu_k-\mu_i\in B_j\). The \(\mu_i\) are strictly increasing because the
\(d_i\) are increasing while the \(t_i\) are nonincreasing. Thus

\[
\{0,\mu_1,\mu_2,\mu_3,\mu_4\}
\]

is a color-\(j\) \(K_5\) in the order-453 prototype: each \(\mu_i\in B_j\)
and every pairwise difference lies in \(B_j\). This contradicts the two
independent prototype checks.

Thus none of the five colors in the compound contains \(K_5\).

The compound has order \(93\cdot452+41=42077\). By the definition of the
diagonal multicolor Ramsey number, an admissible coloring of \(K_{42077}\)
implies \(R_5(5)\ge42078\). \(\square\)

This proof is unconditional modulo the cited, published construction theorem;
all theorem hypotheses are discharged by explicit finite objects.

## 9. Reproduction

From the project directory:

```sh
cd /Users/austingibbons/gather/maths/ramsey-template-94
sh tests/run_end_to_end_checks.sh
```

Expected exit status: 0.

The canonical search output is also reproducible with Kissat 4.0.4:

```sh
python3 search/template_search.py \
  --seed seeds/rowley_order93.template \
  --symmetry rowley-t12 \
  --time-limit 120 \
  --round-steps 20000 \
  --bootstrap-assignments 16 \
  --oracle-batch 4096 \
  --oracle-max-examined 300000 \
  --sat-every 1 \
  --sat-timeout 60 \
  --random-seed 12 \
  --output /private/tmp/reproduced_t12.template \
  --log /private/tmp/reproduced_t12.jsonl
```

The provisional search file is byte-identical across the recorded rerun:

```text
SHA-256 1f5a232f5f8bd08e92f994bf64c3ff0835f0e4912a7e41d58f1cdea6d360b259
```

Search reproducibility is not needed to trust the result: the frozen word and
independent exact verifiers are the certificate.

## 10. Current-record and novelty status

Stanisław P. Radziszowski, *Small Ramsey Numbers*, Electronic Journal of
Combinatorics Dynamic Survey DS1, revision 18 (24 April 2026),
DOI 10.37236/21, Table XIa, printed p. 55, records

\[
R_5(5)\ge41626.
\]

Marcelo Campos and Cosmin Pohoata, *An update on multicolor Ramsey lower
bounds*, arXiv:2601.15183v1, concerns asymptotic bounds and does not state this
specific improvement.

Exact searches for `42078`, an order-94 \((5,5,3)\) Rowley template, and
follow-ups to Rowley's papers found no collision in the checked corpus. This
supports target liveness only. The correct novelty status is:

```text
NOT FOUND IN THE CHECKED LITERATURE — EXTERNAL PRIORITY CHECK REQUIRED
```

No priority claim should be made until Rowley, Radziszowski, and an independent
Ramsey specialist have checked the result against unpublished or newly
circulating work.

## 11. Known limitations

1. The 42077-vertex graph was not attacked by a naive all-vertex clique
   program. Its \(K_5\)-freeness is proved through Rowley's published
   composition theorem, with every input and cutoff checked exactly.
2. The two template verifier implementations share the normalized semantics,
   although their parsers and search algorithms are independent. A clean-room
   third implementation remains welcome.
3. The local 14-variable UNSAT branch has an unverified DRAT file. It is not
   used anywhere in the positive result.
4. All local checks were run on one Apple Silicon machine. An independent
   machine rerun is the final computational-trust gate.
5. Correctness does not establish priority.

## 12. Adversarial review directive

Do not trust the narrative. Try to kill the result in this order:

1. Re-read arXiv:1912.01164v3, Definition 3.1 and Theorem 3.2, especially the
   cutoff proof and all off-by-one conventions.
2. Re-extract ancillary column `AB` from the hash-fixed 2022 source archive;
   verify independently that distances 1–452 equal the frozen prototype and
   distance 453 starts color 4.
3. Reimplement the template checks without importing project code. Check
   \(a=b\) in the sum-free test, residue-zero handling, vertices
   \(0,\ldots,368\), and both inherited colors.
4. Reimplement the finite order-453 three-color \(K_5\) check.
5. Reconstruct the compound sets from the displayed formulas and audit the
   order arithmetic.
6. Search aggressively for a literature collision or a newer lower bound.

Report correctness, novelty, and publication readiness as separate verdicts.
Any concrete counterexample or hypothesis mismatch leads the report.
