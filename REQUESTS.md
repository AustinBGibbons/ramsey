# Cross-Role Requests

## 2026-07-23 — Independent adversarial review

Role: computational Ramsey theorist / skeptical referee.

Normalized statements:

> The word in `results/order99_linear_prefix8.template` is a full effective
> Rowley \((5,5,3)\) template of order 99 with \(\phi=40\). Together with
> `sources/rowley_exoo_order453.prototype`, Rowley's Theorem 3.2 produces the
> explicit five-colouring
> `results/r5_5_order44337.linear-coloring` of \(K_{44,337}\) with no
> monochromatic \(K_5\). Hence \(R_5(5)\ge44,338\).

> No effective Rowley \((5,5,3)\) template of order 98 has \(\phi\ge40\).
> The complete finite certificate is
> `certificates/order98_phi40_exhaustion/`.

Requested output: a read-only report with separate verdicts for:

1. source-theorem and hypothesis fidelity;
2. order-99 finite-certificate correctness;
3. composition and explicit-word correctness;
4. coverage and semantics of the order-98 exhaustion;
5. independent DRAT verification;
6. current-record collision and priority;
7. novelty; and
8. publication readiness.

Required attacks:

1. clean-room verification of the order-99 periodic condition through the
   exact span 388;
2. clean-room \(K_5\) verification of the order-453 prototype;
3. line-by-line audit of Rowley's cutoff and composition formula;
4. independent reconstruction of all 44,336 compound distances;
5. independent regeneration of the 45,374 prefix distance sets;
6. validation that the 11 representatives plus colour swaps exhaust the
   admissible prefixes;
7. validation that every tail coordinate is unrestricted except for the
   stated theorem conditions;
8. proof checking with an independently obtained DRAT checker; and
9. current literature and private-result inquiry.

Limitations:

- do not edit the project;
- do not infer nonexistence at any order other than 98;
- do not promote reconnaissance at orders 100–105;
- do not merge correctness with priority or novelty; and
- report counterexamples or coverage failures first.

Primary handoff: `REVIEW_PACKET.md`.
