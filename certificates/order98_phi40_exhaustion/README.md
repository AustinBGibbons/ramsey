# Certified order-98 obstruction for effective Rowley (5,5,3) templates

## Exact statement certified

There is no word

\[
c:\{1,\ldots,97\}\to\{1,2,3\}
\]

such that:

1. \(c(97)=3\);
2. \(c(d)\ne3\) for \(1\le d\le40\);
3. \(T=c^{-1}(3)\) is interval-sum-free;
4. for each \(s\in\{1,2\}\), the periodically repeated color-\(s\)
   graph contains no \(K_5\).

The repetition certificate uses period \(97\) and span
\[
4(98-2)=384.
\]

This is a nonexistence result at order exactly 98. It does not rule out
templates of order 99 or larger.

## Stage 1: exhaustive 41-vertex prefixes

Because color 3 is forbidden at distances 1 through 40, every candidate
induces a two-color linear distance coloring of \(K_{41}\). For Boolean
variables \(x_d\), \(1\le d\le40\), true means color 1 and false means
color 2.

For each five-set \(V\subseteq\{0,\ldots,40\}\), put

\[
\Delta(V)=\{|u-v|:u,v\in V,\ u\ne v\}.
\]

The two clauses

\[
\bigvee_{d\in\Delta(V)}x_d,\qquad
\bigvee_{d\in\Delta(V)}\neg x_d
\]

forbid a color-2 or color-1 \(K_5\), respectively. Deduplication gives
45,374 distinct distance sets and 90,748 base clauses.

There are 11 listed solutions up to global exchange of colors 1 and 2.
The prefix CNF adds one blocking clause for each listed solution and its
color complement. Its verified UNSAT proof establishes exhaustion of
the prefix list. Each listed solution is also checked directly against
all 45,374 distance sets.

Artifacts:

- `prefix41_representatives.txt`
- `prefix41_exhaust.cnf`
- `prefix41_exhaust.drat`
- `prefix41_manifest.json`

## Stage 2: complete tail elimination for each prefix

For each of the 11 prefix representatives, the tail search leaves every
distance 41 through 96 completely free in colors 1, 2, and 3, and forces
distance 97 to color 3. A global color-1/color-2 exchange handles the
complementary prefix.

For distance \(d\) and color \(s\in\{0,1,2\}\), the CNF variable is

\[
X_{d,s}=3(d-1)+s+1.
\]

The encoding contains:

1. exactly-one-color clauses for all 97 distances;
2. unit clauses fixing the selected 40-symbol prefix and terminal color;
3. for every \(a,b>0\) with \(a+b\le97\), a clause forbidding
   \(c(a)=c(b)=c(a+b)=3\);
4. valid monochromatic-\(K_5\) clauses obtained by exact separation.

For a recorded ordered witness
\[
0=v_0<v_1<\cdots<v_4\le384,
\]
the associated period-97 distance set is

\[
D(V)=\{((v_j-v_i-1)\bmod97)+1:0\le i<j\le4\}.
\]

For color \(s\in\{1,2\}\), the clause

\[
\bigvee_{d\in D(V)}\neg X_{d,s}
\]

is valid because a violation colors every edge of this explicit
five-vertex set with color \(s\).

Each `order98_prefix_NN.clauses.jsonl` sidecar records every sum or
\(K_5\) witness used in its CNF. The independent checker reconstructs
the CNF byte-for-byte from this sidecar, validates every witness
mathematically, and then checks the corresponding DRAT proof.

## Verification

From the repository root, compile the pinned vendored checker and run:

```sh
cc -O2 tools/drat-trim/drat-trim.c -o /tmp/drat-trim
DRAT_TRIM=/tmp/drat-trim \
  python3 certificates/order98_phi40_exhaustion/verify_certificates.py
```

Alternatively, point `DRAT_TRIM` to an independently obtained checker binary.
The complete repository release gate performs the vendored-source build
automatically:

```sh
sh tests/run_certificate_checks.sh
```

Expected final line:

```text
ALL CERTIFICATES VERIFIED
```

All 12 DRAT proofs were independently verified on 23 July 2026. The vendored
source is upstream `drat-trim` commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, preserved under its MIT license.

## Manifests

- `prefix41_manifest.json` contains hashes and dimensions for Stage 1.
- `order98_tail_manifest.json` contains hashes, dimensions, and
  `drat-trim` results for all 11 Stage-2 cases.

The checker also reconstructs every CNF byte-for-byte from its semantic
sidecar before invoking `drat-trim`.
