# Cross-Role Requests

Create one dated request per handoff. Name the exact statement, input artifact
IDs, requested output artifact, role, and limitations. A skeptic request must
contain the normalized statement and evidence only, not a persuasive proof
narrative. Answer by appending a dated response that points to immutable
artifacts rather than changing the original request.

## 2026-07-22 — Independent adversarial certificate review

Role: computational Ramsey theorist / skeptical referee.

Normalized statement:

> The explicit word in `results/order94_t12.template` is a full effective
> Rowley \((5,5,3)\) template of order 94 with \(\phi=40\). The explicit word
> in `sources/rowley_exoo_order453.prototype` is a linear
> \((5,5,5;453)\) prototype. Their Rowley compound is a five-coloring of
> \(K_{42077}\) without a monochromatic \(K_5\), so \(R_5(5)\ge42078\).

Inputs: `ART-001`, `ART-003`, `ART-007`, `ART-008`, `ART-013` through
`ART-024`, and `REVIEW_PACKET.md`.

Requested output: a read-only report under `REVIEW/` with separate verdicts
for source-hypothesis fidelity, finite-certificate correctness, current-record
collision, novelty, and publication readiness.

Required attacks:

1. clean-room reimplementation of the full period-93 condition;
2. clean-room \(K_5\) verification of the order-453 prototype;
3. line-by-line audit of Rowley's cutoff and set construction;
4. independent reconstruction of the order-42077 word; and
5. current literature/priority search.

Limitations: do not edit the project; do not treat the unverified local DRAT
branch as evidence; do not merge correctness with novelty.
