# Proof Obligations

The JSON block is authoritative. A search hit remains provisional until both
obligations are discharged.

```json
{
  "schema_version": 1,
  "obligations": [
    {
      "id": "OBL-001",
      "claim_id": "CON-001",
      "statement": "Produce and freeze an explicit 93-symbol color word with order 94, phi at least 40, terminal distance 93 in the template color, interval-sum-free template set, and both inherited colors K_5-free after period-93 repetition through span 368.",
      "kind": "constructive-certificate",
      "assumptions": ["DEF-002", "repeat vertices are 0 through 368 inclusive"],
      "depends_on": [],
      "status": "discharged",
      "severity": "critical",
      "evidence": ["results/order94_t12.template", "results/order94_direct.template", "results/order94_lazy.template"],
      "owner_role": "experimentalist",
      "hostile_review": {
        "status": "no-critical-issue",
        "finding_refs": ["Three distinct words are frozen; all have length 93, phi 40, terminal template distance 93, sum-free template class, and both repeated inherited colors K_5-free through span 368."]
      }
    },
    {
      "id": "OBL-002",
      "claim_id": "CON-001",
      "statement": "Independently verify any frozen order-94 word with both exact verifier codebases, retain exact outputs and hashes, and confirm the Rowley source-to-certificate hypothesis map before promoting the existence claim.",
      "kind": "certificate-review",
      "assumptions": ["OBL-001 candidate data", "verifier cutoff guard s >= 4(m-2)"],
      "depends_on": ["OBL-001"],
      "status": "discharged",
      "severity": "critical",
      "evidence": ["verifiers/verify_template_py.py", "verifiers/verify_template_cpp.cpp", "tests/run_order94_witness_tests.sh", "tests/run_end_to_end_checks.sh", "KNOWN_RESULTS.md"],
      "owner_role": "skeptic",
      "hostile_review": {
        "status": "no-critical-issue",
        "finding_refs": ["Both independent codebases accept all three target witnesses; the canonical witness is overtested at span 372; the Rowley cutoff, residue convention, order-453 prototype, and composition arithmetic were separately audited."]
      }
    }
  ]
}
```
