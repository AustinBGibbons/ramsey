# An Order-94 Rowley Template and the Bound R₅(5) ≥ 42,078

[![Verify certificates](https://github.com/AustinBGibbons/ramsey/actions/workflows/verify-certificates.yml/badge.svg)](https://github.com/AustinBGibbons/ramsey/actions/workflows/verify-certificates.yml)

**Austin Lin Gibbons**

> **Theorem.** There exists a five-colouring of the edges of
> $K_{42{,}077}$ with no monochromatic $K_5$. Consequently,
> $$
> \boxed{R_5(5)\ge 42{,}078}.
> $$

**Explicit construction:** [complete five-colouring of
K₄₂,₀₇₇](results/r5_5_order42077.linear-coloring)
([raw file / direct download](https://raw.githubusercontent.com/AustinBGibbons/ramsey/main/results/r5_5_order42077.linear-coloring)).

The linked file is the complete finite object establishing the lower bound.
Its SHA-256 digest is
`a97d5dce8a927db2889ba220119f9d4f3d1b88ee24d441f82a803a195ae8028d`.

## Reading the explicit colouring

The construction is recorded as a linear distance colouring:

```text
order 42077
clique_sizes 5,5,5,5,5
colors c(1)c(2)...c(42076)
```

Label the vertices of $K_{42{,}077}$ by
$0,1,\ldots,42{,}076$. For $0\le i<j\le42{,}076$, colour the edge
$\{i,j\}$ with the symbol

$$
c(j-i)\in\{1,2,3,4,5\}.
$$

Thus the 42,076-symbol word specifies every one of the
$\binom{42{,}077}{2}$ edges. None of its five colour classes contains a
copy of $K_5$.

## Construction

The colouring is obtained from two explicit inputs to Rowley's generalized
linear Ramsey construction:

- an [effective $(5,5,3)$ template of order
  94](results/order94_t12.template), with period $93$ and extension
  parameter $\phi=40$; and
- a [linear $(5,5,5;453)$
  prototype](sources/rowley_exoo_order453.prototype).

The compound order is

$$
(94-1)(453-1)+1+40
=93\cdot452+41
=42{,}077.
$$

The template's third distance class is sum-free and therefore triangle-free.
Its first two distance classes remain $K_5$-free under period-93 repetition
through Rowley's exact compression cutoff

$$
4(94-2)=368.
$$

The three colour classes of the order-453 prototype are $K_5$-free.
Rowley's composition replaces the template colour by the prototype's three
colours and preserves the two inherited $K_5$-free colours, yielding the
displayed five-colouring.

## Verify the result

The release certificate suite requires Python 3, a C++17 compiler, and a
POSIX shell. It has no third-party Python dependencies.

```sh
git clone https://github.com/AustinBGibbons/ramsey.git
cd ramsey
sh tests/run_certificate_checks.sh
```

The suite:

1. validates positive and deliberately corrupted verifier fixtures;
2. checks the order-94 template with independent Python and C++ exact clique
   searches;
3. checks the order-453 prototype with separate Python and C++ exact clique
   searches;
4. reconstructs all 42,076 symbols of the compound colouring from the two
   compact inputs; and
5. checks the reconstructed colouring against the frozen SHA-256 digest.

GitHub Actions runs this suite on both Ubuntu and macOS for every push and
pull request. To additionally verify that the compact inputs agree with the
archived primary-source material, run:

```sh
sh tests/run_end_to_end_checks.sh
```

## Artifacts

| Artifact | Purpose | SHA-256 |
|---|---|---|
| [Complete K₄₂,₀₇₇ five-colouring](results/r5_5_order42077.linear-coloring) | The explicit Ramsey construction | `a97d5dce8a927db2889ba220119f9d4f3d1b88ee24d441f82a803a195ae8028d` |
| [Order-94 template](results/order94_t12.template) | Effective $(5,5,3)$ input with $\phi=40$ | `a3dd3415956277d68fc0197f6f5e35c38f2ed7936c66f11f658b0c57688abec1` |
| [Order-453 prototype](sources/rowley_exoo_order453.prototype) | Linear $(5,5,5;453)$ input | `19c97e6279c184f6f462786cadda4b7c9773d870a5b680a04eb1503ef384a2d0` |
| [Paper](output/pdf/order94-rowley-template.pdf) | Definitions, composition theorem, proof, and verification algorithms | — |
| [Paper source](paper/order94-rowley-template.tex) | LaTeX source | — |

## Mathematical references

- Fred Rowley, “A generalised linear Ramsey graph construction,”
  [arXiv:1912.01164](https://arxiv.org/abs/1912.01164), 2021.
- Fred Rowley, “Improved Lower Bounds for Multicolour Ramsey Numbers using
  SAT-Solvers,” [arXiv:2203.13476](https://arxiv.org/abs/2203.13476), 2022.
- Stanisław P. Radziszowski, “Small Ramsey Numbers,” *Electronic Journal of
  Combinatorics*, Dynamic Survey DS1,
  [doi:10.37236/21](https://doi.org/10.37236/21).
