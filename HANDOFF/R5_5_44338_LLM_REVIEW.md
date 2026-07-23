# An order-99 Rowley template, a certified hole at order 98, and \(R_5(5)\ge44,338\)

**Austin Lin Gibbons**
**Self-contained LLM review packet — 23 July 2026**

## Executive result

We have exact finite evidence for the following two statements.

### Theorem A: record-improving construction

There is an effective Rowley \((5,5,3)\) template of order \(99\) with
\(\phi=40\). Combined with a verified linear \((5,5,5;453)\) prototype by
Rowley's published composition theorem, it gives a five-coloring of
\(K_{44,337}\) with no monochromatic \(K_5\). Consequently,

\[
\boxed{R_5(5)\ge44,338}.
\]

The latest standard survey checked, revision 18 of Radziszowski's
*Small Ramsey Numbers* dated 24 April 2026, records
\(R_5(5)\ge41,626\). The proposed improvement is therefore \(2,712\).

### Theorem B: certified nonmonotonicity

There is no effective Rowley \((5,5,3)\) template of order \(98\) with
\(\phi\ge40\), although such templates exist at orders \(97\) and \(99\).

Thus feasibility at a fixed extension threshold is not monotone in template
order. In particular, the order-99 construction is not a one-position lift of
the order-97 construction: it crosses a provably empty order.

Theorem A has been checked by independent Python and C++ verifiers. Theorem B
is backed by 12 independently checked DRAT certificates plus a semantic
checker that reconstructs every CNF from explicit \(K_5\) and sum witnesses.

Correctness and priority remain separate. The local finite checks are
complete; external reproduction, source-theorem review, and author contact
remain required before making an absolute novelty or publication claim.

## 1. Exact order-99 object

The frozen template is:

```text
order 99
phi_min 40
repeat_span 388
colors 21112112111222112222222211222111211211123211321111332323233313333313333113333133323332333111231123
```

It is stored at:

```text
results/order99_linear_prefix8.template
```

SHA-256:

```text
2643001cc425898d584bd374e20928d1dbc6a72fd4011711151343d0ad072966
```

The template has period \(p=98\), actual \(\phi=40\), 33 template-color
distances, and the exact required repeated-color span

\[
4(99-2)=388.
\]

Independent verifier results:

```text
Python: VALID
  color 1 search nodes: 1,645,997
  color 2 search nodes:   917,897

C++: VALID
  order: 99
  period: 98
  actual_phi: 40
  required_repeat_span: 388
  repeat_span: 388
```

The first 40 symbols form a non-cyclic linear \((5,5;41)\) prefix. That
symmetry break is load-bearing: it escapes the cyclic/reflected family that
terminates before order 98.

## 2. Ramsey composition

The second input is the frozen linear \((5,5,5;453)\) prototype:

```text
sources/rowley_exoo_order453.prototype
```

SHA-256:

```text
19c97e6279c184f6f462786cadda4b7c9773d870a5b680a04eb1503ef384a2d0
```

Both independent prototype verifiers confirm that all three colors are
\(K_5\)-free.

Rowley's Theorem 3.2 gives compound order

\[
(99-1)(453-1)+1+40
=98\cdot452+41
=44,337.
\]

The complete 44,336-symbol five-color distance word is:

```text
results/r5_5_order44337.linear-coloring
```

SHA-256:

```text
274acbf17bf7732b16ef7d20c97486eb469486907fd1357c16990ed4332f7158
```

The compound is linear and non-cyclic. Cyclicity is not a hypothesis of the
linear composition theorem.

The generator and an independently written literal set-union reconstruction
agree on every distance:

```text
OK compound order 44337
OK all 44336 distances assigned exactly once
OK independent set-union reconstruction
cyclic_reflection false
sha256 274acbf17bf7732b16ef7d20c97486eb469486907fd1357c16990ed4332f7158
```

Run the complete positive certificate suite with:

```sh
git clone https://github.com/AustinBGibbons/ramsey.git
cd ramsey
sh tests/run_order99_breakthrough_checks.sh
```

## 3. Why the finite cutoff is exact

For inherited color \(s\in\{1,2\}\), define a directed Cayley relation
\(D_s\) on \(\mathbb Z_p\) by

\[
x\longrightarrow y
\quad\Longleftrightarrow\quad
c\!\left((y-x)\bmod p\right)=s,
\]

where residue \(0\) is represented by the terminal distance \(p\).

The periodically repeated integer coloring is \(K_5\)-free in color \(s\)
if and only if \(D_s\) contains no ordered transitive \(K_5\): no distinct
residues \(r_0,\ldots,r_4\) satisfy

\[
r_j-r_i\pmod p\in c^{-1}(s)
\qquad(0\le i<j\le4).
\]

One direction reduces an increasing integer witness modulo \(p\). Conversely,
given such an ordered residue witness, lift each successive residue by its
least positive modular gap. Four gaps suffice, each at most \(p-1\), so the
lift lies inside span

\[
4(p-1)=4(m-2).
\]

This proves that the verifier's finite cutoff captures the entire periodic
condition. It also identifies the native SAT object: a ternary coloring of
distance coordinates avoiding additive triples in the template color and
ordered transitive-\(K_5\) hyperedges in two directed Cayley relations.

## 4. Certified order-98 hole

The exact certified statement is:

> There is no word \(c:\{1,\ldots,97\}\to\{1,2,3\}\) such that
> \(c(97)=3\), \(c(d)\ne3\) for \(1\le d\le40\), the template color is
> interval-sum-free, and both inherited periodic colors are \(K_5\)-free.

This is precisely nonexistence at order 98 with \(\phi\ge40\).

The certificate packet is:

```text
certificates/order98_phi40_exhaustion/
```

Verification:

```sh
cc -O2 tools/drat-trim/drat-trim.c -o /tmp/drat-trim
DRAT_TRIM=/tmp/drat-trim \
python3 certificates/order98_phi40_exhaustion/verify_certificates.py
```

Expected output:

```text
VERIFIED 01
VERIFIED 02
...
VERIFIED 11
ALL CERTIFICATES VERIFIED
```

### Stage 1: exhaustive prefixes

Because \(\phi\ge40\), distances \(1,\ldots,40\) use only colors 1 and 2.
Every candidate therefore induces a two-color linear distance coloring of
\(K_{41}\).

For each five-set \(V\subseteq\{0,\ldots,40\}\), define

\[
\Delta(V)=\{|u-v|:u,v\in V,\ u\ne v\}.
\]

The prefix CNF contains both clauses forbidding all of \(\Delta(V)\) from
being color 1 or all from being color 2. Deduplication yields 45,374
distance sets and 90,748 avoidance clauses.

The solver finds 22 admissible words, or 11 up to globally exchanging colors
1 and 2. After blocking those 22 words, `drat-trim` verifies UNSAT. The
semantic checker independently regenerates all 45,374 sets, validates all
11 representatives, rebuilds the CNF byte-for-byte, and checks the proof.

### Stage 2: exhaustive tails

For each of the 11 representative prefixes:

- the first 40 distances are fixed;
- every distance \(41,\ldots,96\) is completely free in colors 1, 2, and 3;
- distance 97 is forced to template color;
- all interval-sum constraints are included;
- every learned inherited-color clause carries an explicit five-vertex
  periodic \(K_5\) witness.

Each of the 11 resulting CNFs is UNSAT, and all 11 DRAT proofs verify. Global
exchange of colors 1 and 2 handles the complementary prefixes.

This exhausts every order-98 candidate with \(\phi\ge40\); it makes no
reflection, cyclicity, or central-interval assumption.

## 5. The structural narrative

The successful cyclic/reflected family at orders 94–97 admits a clean
additive shell. If \(p=2q+r\), the template tail can be encoded by
\(U\subseteq\{1,\ldots,r\}\), and sum-freeness reduces to

\[
a+b+c\ne r+1\qquad(a,b,c\in U).
\]

That family reaches order 97 but is DRAT-certified impossible at order 98.
The exhaustive order-98 certificate then proves that the obstruction is
deeper than reflection: no one-step order-98 continuation exists at
\(\phi\ge40\), even with every tail coordinate free.

Order 99 reappears only after changing to a genuinely non-cyclic
41-vertex prefix. Thus the mechanism is:

\[
\text{cyclic additive shell}
\;\longrightarrow\;
\text{certified hole}
\;\longrightarrow\;
\text{non-cyclic symmetry-breaking escape}.
\]

This is a more informative result than a sequence of isolated lower-bound
records. It proves that effective-template feasibility is nonmonotone and
that the correct search decomposition is by finite linear-prefix type, not by
one-position lifts.

## 6. Scope and unresolved obligations

### Established locally

- Effective templates with \(\phi=40\) exist at orders 97 and 99.
- Both frozen positive words pass independent Python and C++ exact verifiers.
- No order-98 effective template with \(\phi\ge40\) exists; 12 DRAT proofs and
  a semantic CNF reconstructor verify this.
- The order-99 composition produces the explicit frozen coloring of
  \(K_{44,337}\), independently reconstructed distance by distance.
- Subject to the published composition theorem,
  \(R_5(5)\ge44,338\).

### Not claimed

- We do not claim that order 99 is globally maximal. Nonexistence at order 98
  does not descend from or propagate to later periods.
- Solver reconnaissance found no positives at orders 100–105 within the same
  exhaustive-prefix search organization, but those negative runs are not
  certificate-backed and are not theorem claims.
- We do not claim absolute priority until Rowley, Radziszowski, and an
  independent computational referee check for private or unindexed results.

### Required external checks

1. Run `sh tests/run_certificate_checks.sh` from a clean checkout on another
   machine.
2. Re-run the complete order-98 packet with a separately obtained
   `drat-trim`, in addition to the pinned source bundled here.
3. Check the exact specialization of Rowley's Theorem 3.2 against the primary
   paper.
4. Ask Fred Rowley to confirm the order-453 prototype recovery and current
   record status.
5. Ask Stanisław Radziszowski to confirm that no later bound supersedes
   \(44,338\).

## 7. Recommended disposition

Bank and externally review the order-99 result before launching a larger
frontier scan. The paperworthy nucleus is now:

1. the record \(R_5(5)\ge44,338\);
2. the exact directed-Cayley/transitive-\(K_5\) formulation;
3. the additive reflected-shell lemma;
4. the certified order-98 hole; and
5. the non-cyclic order-99 escape proving nonmonotone feasibility.

Further search should be driven by this prefix-type decomposition, not by
blind insertion or an assumption that feasible orders form an interval.

## 8. Primary references

1. Fred Rowley, “A generalised linear Ramsey graph construction,”
   *Australasian Journal of Combinatorics* **81**(2) (2021), 245–256,
   Theorem 3.2.
   <https://ajc.maths.uq.edu.au/pdf/81/ajc_v81_p245.pdf>

2. Fred Rowley, “Improved Lower Bounds for Multicolour Ramsey Numbers using
   SAT-Solvers,” arXiv:2203.13476v3 (18 September 2022).
   <https://arxiv.org/abs/2203.13476>

3. Stanisław P. Radziszowski, “Small Ramsey Numbers,” *Electronic Journal of
   Combinatorics*, Dynamic Survey DS1, revision 18 (24 April 2026),
   DOI 10.37236/21.
   <https://doi.org/10.37236/21>

4. Marcelo Campos and Cosmin Pohoata, “An update on multicolor Ramsey lower
   bounds,” arXiv:2601.15183 (2026). This asymptotic paper does not collide
   with the finite result above.
   <https://arxiv.org/abs/2601.15183>
