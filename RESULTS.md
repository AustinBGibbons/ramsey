# Results and Closeout

## Lead theorem

The frozen order-99 effective Rowley \((5,5,3)\) template with
\(\phi=40\), combined with the verified linear \((5,5,5;453)\) prototype,
produces an explicit five-colouring of \(K_{44,337}\) with no monochromatic
\(K_5\). Hence

\[
\boxed{R_5(5)\ge44,338}.
\]

The compact certificate is `results/order99_linear_prefix8.template`; the
complete distance colouring is
`results/r5_5_order44337.linear-coloring`.

## Structural theorem

There is no effective order-98 Rowley \((5,5,3)\) template with
\(\phi\ge40\), while such templates exist at orders 97 and 99. Therefore
feasibility at fixed \(\phi=40\) is nonmonotone in template order.

The negative theorem is certified by:

- an exhaustive list of the 22 admissible two-colour length-40 prefixes,
  represented by 11 words up to colour exchange;
- one DRAT proof establishing that prefix list is exhaustive;
- 11 unrestricted tail CNFs, one per representative;
- 11 verified DRAT proofs of tail nonexistence; and
- a semantic checker that validates every sum and \(K_5\) witness and
  reconstructs each CNF byte-for-byte before proof checking.

## Exact artifacts

- Order-99 template SHA-256:
  `2643001cc425898d584bd374e20928d1dbc6a72fd4011711151343d0ad072966`.
- Complete \(K_{44,337}\) colouring SHA-256:
  `274acbf17bf7732b16ef7d20c97486eb469486907fd1357c16990ed4332f7158`.
- Order-453 prototype SHA-256:
  `19c97e6279c184f6f462786cadda4b7c9773d870a5b680a04eb1503ef384a2d0`.
- Order-98 proof packet:
  `certificates/order98_phi40_exhaustion/`, with per-file hashes in its
  manifests.

## Verification

The portable release gate is:

```sh
sh tests/run_certificate_checks.sh
```

It verifies all retained positive objects with independent algorithms,
reconstructs the order-99 compound distance by distance, compiles the pinned
`drat-trim` source, semantically reconstructs every negative CNF, and checks
all 12 DRAT proofs.

The source-provenance extension is:

```sh
sh tests/run_end_to_end_checks.sh
```

The dedicated headline-result suite is:

```sh
sh tests/run_order99_breakthrough_checks.sh
```

## Interpretation

The order-99 word uses a non-cyclic \(K_{41}\) prefix. This is not a cosmetic
variation: order 98 is globally impossible at \(\phi\ge40\), so the successful
order-99 template cannot arise by a one-position continuation through every
intermediate order. The directed-Cayley formulation identifies each
periodic inherited-colour obstruction with an ordered transitive \(K_5\) on
\(\mathbb Z_p\), explaining both the exact finite cutoff and the native SAT
constraints.

## Correctness and priority

The finite correctness claims are locally complete and machine-checkable.
The latest checked standard survey, revision 18 dated 24 April 2026, records
\(R_5(5)\ge41,626\); bounded primary-literature searches found no collision
with 44,338. Absolute priority is not claimed until an external current
literature check and author confirmation are complete.

## Human gate

Recommended status: **ready for external mathematical and computational
review**. Publication or record language should follow:

1. clean-checkout reproduction on an independent machine;
2. independent `drat-trim` build and certificate run;
3. source-level review of Rowley's Theorem 3.2 specialization; and
4. priority confirmation from domain experts.
