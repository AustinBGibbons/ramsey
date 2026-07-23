# Factual extraction: Rowley's published order-93 \((5,5,3)\) template

Source artifact:

`../sources/arxiv-2203.13476-source.tar.gz`

SHA-256:

`5041096a33d6898c116a35a102e521fb14fe872fb18c20ff7d30822ed4c396b2`

The archive contains an OpenDocument spreadsheet as `anc/content.xml`.  In
sheet `Paper_Sep_2022`, the one-based spreadsheet column 14 is labelled
`TFT(S)` and has parameters `5,5,3`.  Its metadata rows give:

- order \(m=93\);
- \(\phi=40\);
- limit order tested \(=369\).

Rows indexed by edge length \(d=1,\ldots,92\) give the following base
colour word, in increasing order of \(d\):

```text
11121221222212111212212111212222122121113333112212233333333333333333333333333333322122113333
```

The word has length 92.  Its colour classes are:

```text
colour 1:
1 2 3 5 8 13 15 16 17 19 22 24 25 26 28 33 36 38 39 40 45 46 49 84 87 88

colour 2:
4 6 7 9 10 11 12 14 18 20 21 23 27 29 30 31 32 34 35 37 47 48 50 51 82 83 85 86

template colour 3:
41 42 43 44 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 89 90 91 92
```

Thus the smallest template-coloured length is 41 and the last length 92
is template-coloured, agreeing with \(\phi=41-1=40\).

The extracted word also has the two reflection properties described in
Rowley's sufficient condition for a cyclic compound graph:

```text
c(d) = c(41-d)   for 1 <= d <= 40,
c(d) = c(133-d)  for 41 <= d <= 92.
```

It is not a cyclic colouring of the base \(K_{93}\) in the stronger sense
\(c(d)=c(93-d)\) for every \(d\).

The same spreadsheet column supplies colours for edge lengths
\(1,\ldots,368\), i.e. a graph of order 369.  Across its four consecutive
92-length blocks, colours 1 and 2 repeat with period 92 exactly.  The
template positions are relabelled respectively by colours 3, 4, 5, and 6.
Consequently the archived 369-vertex test instance is a four-block
multiple-repetition test, not merely the base 93-vertex colouring.

This file records extraction facts only.  It is not, by itself, an
independent verification of the Ramsey or multiple-repetition conditions.
