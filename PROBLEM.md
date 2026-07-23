# Problem

## Exact target — resolved

Find an order-\(94\) effective Rowley \((5,5,3)\) template with
\(\phi\ge 40\).

Concretely, find a word

\[
c:\{1,\ldots,93\}\longrightarrow\{1,2,3\}
\]

such that:

1. \(c(93)=3\);
2. \(c(d)\ne3\) for \(1\le d\le40\);
3. the set \(T=c^{-1}(3)\) is interval-sum-free: there are no positive
   \(a,b\) with \(a,b,a+b\in T\);
4. for each \(s\in\{1,2\}\), form the graph on
   \(\{0,\ldots,368\}\) in which \(i<j\) is an edge exactly when
   \[
   c\!\left(((j-i-1)\bmod93)+1\right)=s.
   \]
   Neither graph may contain \(K_5\).

By Rowley's compression theorem, span \(4(94-2)=368\) is sufficient for
the inherited \(K_5\)-free colors. An explicit word satisfying these
conditions would be a finite certificate for `CON-001`.

The canonical certificate is now
`results/order94_t12.template`. Two additional distinct certificates are
retained in `results/order94_direct.template` and
`results/order94_lazy.template`.

## Payoff

Rowley's composition theorem, with the extracted and independently checked
order-\(453\) \((5,5,5)\) prototype, gives a five-color \(K_5\)-free complete graph
of order at least

\[
(94-1)(453-1)+1+40=93\cdot452+41=42077.
\]

Therefore the resolved target gives

\[
R_5(5)\ge42078,
\]

improving the revision-18 survey bound \(R_5(5)\ge41626\) by \(452\).

## Scope boundary

This project searches a highly structured class of linear distance
colorings. It is not an exhaustive search over all five-colorings of a
complete graph, and failure to find an order-\(94\) template does not prove
that no such template exists unless a precisely specified restricted class
is exhaustively certified.

A base \((5,5,3;94)\) coloring is not enough. The periodically repeated
colors 1 and 2 must remain \(K_5\)-free through span 368. A heuristic score,
solver assignment, or single-verifier pass is not a result.

## Success and failure conditions

- **Certified success:** an explicit 93-symbol word passes both independent
  exact verifiers on all four conditions above. The source-to-certificate map
  and composition arithmetic are retained with the witness.
- **Restricted negative:** every member of an exactly defined finite search
  class is eliminated, with complete coverage and preferably a checkable
  unsatisfiability certificate.
- **Censored search:** a timed or iteration-limited run ends without a
  witness. This is steering evidence only.
- **Failure:** a purported order-\(94\) word passes only the base condition,
  only one inherited color, an undersized span, or a search-engine-local
  checker.
