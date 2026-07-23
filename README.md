# An Order-99 Rowley Template and the Bound R₅(5) ≥ 44,338

[![Verify certificates](https://github.com/AustinBGibbons/ramsey/actions/workflows/verify-certificates.yml/badge.svg)](https://github.com/AustinBGibbons/ramsey/actions/workflows/verify-certificates.yml)

**Austin Lin Gibbons**

> **Theorem 1.** There exists a five-colouring of the edges of
> $K_{44,337}$ with no monochromatic $K_5$. Consequently,
> $$
> \boxed{R_5(5)\ge 44,338}.
> $$

The complete finite construction is the [44,336-symbol distance
colouring](results/r5_5_order44337.linear-coloring)
([raw file](https://raw.githubusercontent.com/AustinBGibbons/ramsey/main/results/r5_5_order44337.linear-coloring)).
Its SHA-256 digest is
`274acbf17bf7732b16ef7d20c97486eb469486907fd1357c16990ed4332f7158`.

> **Theorem 2.** No effective Rowley $(5,5,3)$ template of order $98$
> has $\phi\ge40$. Effective templates with $\phi=40$ exist at orders
> $97$ and $99$.

Thus feasibility at the fixed threshold $\phi=40$ is not monotone in the
template order. The positive construction and the negative result are both
finite and exactly checkable from this repository.

The latest standard survey checked here—revision 18 of Radziszowski's
*Small Ramsey Numbers*, dated 24 April 2026—records
$R_5(5)\ge41,626$. The construction above therefore improves that checked
benchmark by 2,712. Correctness of the finite construction is separate from
priority: an external current-literature check remains appropriate before
describing the bound as the standing record.

## The explicit colouring

The construction is a linear distance colouring:

```text
order 44337
clique_sizes 5,5,5,5,5
colors c(1)c(2)...c(44336)
```

Label the vertices $0,1,\ldots,44,336$. For $i<j$, colour edge
$\{i,j\}$ by $c(j-i)$. The word therefore specifies all
$\binom{44,337}{2}$ edges. It is linear but not cyclic; cyclicity is not a
hypothesis of Rowley's construction.

The colouring is built from:

- the [order-99 effective $(5,5,3)$
  template](results/order99_linear_prefix8.template), with period $98$,
  $\phi=40$, and exact verification span $388$; and
- the [linear $(5,5,5;453)$
  prototype](sources/rowley_exoo_order453.prototype).

Rowley's composition theorem gives

$$
(99-1)(453-1)+1+40
=98\cdot452+41
=44,337.
$$

The template's third colour is sum-free and hence triangle-free. Its first
two colours remain $K_5$-free under period-98 repetition through the exact
cutoff $4(99-2)=388$. The prototype's three colours are independently
verified to be $K_5$-free. Rowley's construction replaces the template
colour by those three prototype colours and retains the first two colours.

## The certified order-98 hole

At order $98$, $\phi\ge40$ forces the first 40 distances to use only
colours 1 and 2. The certificate has two exhaustive stages:

1. A two-colour $K_5$-avoidance CNF proves that there are exactly 22
   admissible length-40 prefixes, or 11 up to exchanging colours 1 and 2.
2. For each representative, a second CNF leaves every distance
   $41,\ldots,96$ free in all three colours, forces distance 97 into the
   template colour, and imposes every sum-free and periodic-$K_5$
   condition. All 11 instances are UNSAT.

The packet contains 12 DRAT proofs. Its checker independently regenerates
the prefix constraints, validates every explicit sum or five-vertex witness,
reconstructs each CNF byte-for-byte, and then invokes a pinned, source-built
`drat-trim`. No cyclic, reflection, or fixed-tail assumption is made.

See [the certificate documentation](certificates/order98_phi40_exhaustion/README.md).

## Verify everything

Requirements are Python 3, a C compiler, a C++17 compiler, and a POSIX shell.
There are no third-party Python dependencies.

```sh
git clone https://github.com/AustinBGibbons/ramsey.git
cd ramsey
sh tests/run_certificate_checks.sh
```

The release suite:

1. tests both independent template verifiers against positive and deliberately
   corrupted fixtures;
2. verifies the order-453 prototype with independent Python and C++ clique
   searches;
3. retains and verifies the earlier order-94 certificates;
4. verifies the order-97 and order-99 templates with both implementations;
5. regenerates the $K_{44,337}$ colouring and matches all 44,336 symbols
   using an independent set-union reconstruction and frozen hash; and
6. compiles the vendored `drat-trim`, semantically reconstructs all order-98
   CNFs, and verifies all 12 DRAT proofs.

GitHub Actions runs the same suite on Ubuntu and macOS for every push and
pull request. The additional source-provenance audit is:

```sh
sh tests/run_end_to_end_checks.sh
```

## Principal artifacts

| Artifact | Role | SHA-256 |
|---|---|---|
| [Complete $K_{44,337}$ five-colouring](results/r5_5_order44337.linear-coloring) | Explicit Ramsey construction | `274acbf17bf7732b16ef7d20c97486eb469486907fd1357c16990ed4332f7158` |
| [Order-99 template](results/order99_linear_prefix8.template) | Effective $(5,5,3)$ input with $\phi=40$ | `2643001cc425898d584bd374e20928d1dbc6a72fd4011711151343d0ad072966` |
| [Order-97 template](results/order97_reflected.template) | Lower positive witness around the order-98 hole | `3287e4737fed6d355d59c4c08c3140a829508039293914109c78000c7ba3a309` |
| [Order-98 certificate packet](certificates/order98_phi40_exhaustion/) | Exhaustive nonexistence proof at $\phi\ge40$ | Hash-fixed per file in its two manifests |
| [Order-453 prototype](sources/rowley_exoo_order453.prototype) | Linear $(5,5,5;453)$ input | `19c97e6279c184f6f462786cadda4b7c9773d870a5b680a04eb1503ef384a2d0` |
| [Paper](output/pdf/order99-rowley-template.pdf) | Mathematical statement, proof, and certificate architecture | — |
| [Paper source](paper/order99-rowley-template.tex) | LaTeX source | — |
| [External-review packet](REVIEW_PACKET.md) | Self-contained adversarial handoff | — |

The earlier order-94 witnesses and their exact checks remain in the repository
as reproducibility history; they are no longer the headline result.

## Mathematical references

- Fred Rowley, “A generalised linear Ramsey graph construction,”
  *Australasian Journal of Combinatorics* **81**(2) (2021), 245–256,
  [journal PDF](https://ajc.maths.uq.edu.au/pdf/81/ajc_v81_p245.pdf).
- Fred Rowley, “Improved Lower Bounds for Multicolour Ramsey Numbers using
  SAT-Solvers,” [arXiv:2203.13476v3](https://arxiv.org/abs/2203.13476).
- Stanisław P. Radziszowski, “Small Ramsey Numbers,” *Electronic Journal of
  Combinatorics*, Dynamic Survey DS1,
  [doi:10.37236/21](https://doi.org/10.37236/21).
- Marijn Heule and Nathan Wetzler,
  [`drat-trim`](https://github.com/marijnheule/drat-trim), proof checker
  source pinned in `tools/drat-trim/`.
