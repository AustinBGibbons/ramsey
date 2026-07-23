# Problem

## Exact statements now resolved

The project establishes two finite statements about effective Rowley
\((5,5,3)\) templates at the fixed threshold \(\phi=40\).

### Positive statement

Find and certify a word

\[
c:\{1,\ldots,98\}\longrightarrow\{1,2,3\}
\]

such that:

1. \(c(98)=3\);
2. \(c(d)\ne3\) for \(1\le d\le40\);
3. \(T=c^{-1}(3)\) contains no positive \(a,b,a+b\);
4. for each \(s\in\{1,2\}\), the graph on
   \(\{0,\ldots,388\}\) with
   \[
   ij\in E_s
   \Longleftrightarrow
   c\!\left(((j-i-1)\bmod98)+1\right)=s
   \quad(i<j)
   \]
   contains no \(K_5\).

This is resolved by `results/order99_linear_prefix8.template`.

### Negative statement

Prove that no analogous word

\[
c:\{1,\ldots,97\}\longrightarrow\{1,2,3\}
\]

exists with terminal distance \(97\), forbidden template colour through
distance 40, interval-sum-free template colour, and both inherited colours
\(K_5\)-free under period-97 repetition through span
\(4(98-2)=384\).

This is resolved by the exhaustive CNF/DRAT packet in
`certificates/order98_phi40_exhaustion/`.

Because `results/order97_reflected.template` and the order-99 template are
valid while order 98 is impossible, fixed-\(\phi\) template feasibility is
nonmonotone in the order.

## Ramsey payoff

Rowley's Theorem 3.2, applied to the verified order-99 template and the
independently checked linear \((5,5,5;453)\) prototype, gives order

\[
(99-1)(453-1)+1+40=98\cdot452+41=44,337.
\]

Therefore the explicit compound word proves

\[
\boxed{R_5(5)\ge44,338}.
\]

## Scope boundary

The positive result is an explicit linear distance colouring, not an
exhaustive statement about all five-colourings of \(K_{44,337}\).

The negative result is exhaustive over **all** effective order-98
\((5,5,3)\) templates with \(\phi\ge40\); it is not restricted to cyclic,
reflected, or fixed-prefix tails. It does not rule out order 98 with smaller
\(\phi\), or any order \(m\ge99\).

A base \((5,5,3;m)\) colouring is insufficient: the first two colours must
remain \(K_5\)-free under periodic repetition through the exact Rowley cutoff
\(4(m-2)\). A heuristic score, solver assignment, undersized span, or
single-verifier pass is not a result.

## Success criteria

- **Positive theorem:** a frozen word passes independent Python and C++ exact
  verifiers and its Rowley compound is independently reconstructed.
- **Negative theorem:** exhaustive case coverage is explicit, every CNF
  clause has independently checked semantics, and every UNSAT claim has a
  verified proof certificate.
- **Priority claim:** kept separate from correctness and deferred to current
  literature review and external author confirmation.
