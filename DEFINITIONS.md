# Definitions

## Ramsey notation

\(R_r(k)\) is the least integer \(N\) such that every \(r\)-edge-coloring
of \(K_N\) contains a monochromatic \(K_k\). Thus an explicit
\(r\)-coloring of \(K_M\) without a monochromatic \(K_k\) proves
\(R_r(k)\ge M+1\).

## Linear distance coloring (`DEF-001`)

For \(m\ge2\), label the vertices of \(K_m\) by
\(\{0,\ldots,m-1\}\). A linear three-coloring is specified by a word

\[
c:\{1,\ldots,m-1\}\to\{1,2,3\},
\]

where edge \(\{i,j\}\), \(i<j\), receives color \(c(j-i)\). Put
\(p=m-1\), the period used in Rowley's compound construction.

## Template color and \(\phi\)

Let

\[
L_1=c^{-1}(1),\qquad L_2=c^{-1}(2),\qquad T=c^{-1}(3).
\]

The distinguished color 3 is the template color. It is a Rowley
tf-template when \(p\in T\) and the color-3 graph is triangle-free.
For a linear coloring, triangle-freeness is exactly

\[
\nexists\,a,b>0\quad a,b,a+b\in T.
\]

The extension parameter is

\[
\phi=\min(T)-1.
\]

The target \(\phi\ge40\) is therefore equivalent to
\(T\cap\{1,\ldots,40\}=\varnothing\).

The equation \(a=b\) is allowed in the sum-free test. All distances are
ordinary positive integers, not residues modulo \(p\).

## Periodically repeated inherited colors

For \(s\in\{1,2\}\), define its repeated positive-distance set

\[
L_s^\infty=\{\,\ell+rp:\ell\in L_s,\ r\in\mathbb Z_{\ge0}\,\}.
\]

Equivalently, a positive distance \(d\) has repeated inherited color \(s\)
when

\[
c\!\left(((d-1)\bmod p)+1\right)=s.
\]

This residue convention is load-bearing: a multiple of \(p\) maps to
base distance \(p\), which is template-colored, rather than to a nonexistent
distance zero.

## Operational full certificate (`DEF-002`)

An operational \((5,5,3)\) template certificate records:

- `order` \(m\);
- `phi_min` \(q\);
- `repeat_span` \(s\);
- the length-\(m-1\) word `colors`.

It is valid when \(p\in T\), \(T\cap[1,q]=\varnothing\), \(T\) is
interval-sum-free, and neither repeated inherited color graph on
\(\{0,\ldots,s\}\) contains \(K_5\). It is **full** when additionally
\(s\ge4(m-2)\), the Rowley cutoff for inherited \(K_5\)'s.

For the target \(m=94\), a repeat span of 368 means 369 vertices,
\(\{0,\ldots,368\}\). Allocating only 368 vertices is an off-by-one error.

## Candidate-file format

Both independent verifiers accept the same data format but parse and check it
independently:

```text
order 94
phi_min 40
repeat_span 368
colors <93 symbols from 1,2,3>
```

Blank lines and text after `#` are ignored. Unknown fields, duplicate fields,
and malformed values are rejected.
