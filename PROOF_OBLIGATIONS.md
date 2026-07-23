# Proof Obligations

The JSON block is authoritative. Discharged finite obligations remain listed
for provenance; priority remains open.

```json
{
  "schema_version": 1,
  "obligations": [
    {
      "id": "OBL-001",
      "claim_id": "FIN-002",
      "statement": "Reject a monochromatic K_5 in every color of the frozen order-453 prototype with two independent exact implementations.",
      "kind": "finite exhaustive verification",
      "assumptions": ["The file parser implements DEF-001."],
      "depends_on": [],
      "status": "discharged",
      "severity": "critical",
      "evidence": ["ART-004", "ART-015", "ART-016"],
      "owner_role": "skeptic",
      "hostile_review": {"status": "no-critical-issue", "finding_refs": ["tests/run_certificate_checks.sh"]}
    },
    {
      "id": "OBL-002",
      "claim_id": "CON-002",
      "statement": "Verify every order-99 template condition, including the full inherited-color cutoff through maximum distance 388, with independent algorithms.",
      "kind": "finite exhaustive verification",
      "assumptions": ["DEF-002", "SRC-001"],
      "depends_on": [],
      "status": "discharged",
      "severity": "critical",
      "evidence": ["ART-007", "ART-005", "ART-006", "ART-008"],
      "owner_role": "skeptic",
      "hostile_review": {"status": "no-critical-issue", "finding_refs": ["tests/run_order99_breakthrough_checks.sh"]}
    },
    {
      "id": "OBL-003",
      "claim_id": "FIN-004",
      "statement": "Map all Rowley hypotheses, reconstruct every output distance independently, and verify the frozen order and hash.",
      "kind": "theorem application and exact reconstruction",
      "assumptions": ["SRC-001"],
      "depends_on": ["OBL-001", "OBL-002"],
      "status": "discharged",
      "severity": "critical",
      "evidence": ["ART-009", "ART-010", "ART-008"],
      "owner_role": "integrator",
      "hostile_review": {"status": "no-critical-issue", "finding_refs": ["paper/order99-rowley-template.tex", "tests/check_compound_coloring_generic.py"]}
    },
    {
      "id": "OBL-004",
      "claim_id": "NEG-001",
      "statement": "Exhaust all two-color K_5-free prefixes on distances 1 through 40 and verify the 11 representatives up to color exchange.",
      "kind": "certified finite exhaustion",
      "assumptions": ["phi>=40 forbids the template color in the prefix."],
      "depends_on": [],
      "status": "discharged",
      "severity": "critical",
      "evidence": ["ART-011", "ART-012"],
      "owner_role": "formalizer",
      "hostile_review": {"status": "no-critical-issue", "finding_refs": ["certificates/order98_phi40_exhaustion/verify_certificates.py"]}
    },
    {
      "id": "OBL-005",
      "claim_id": "NEG-001",
      "statement": "For every prefix representative, leave the entire tail unrestricted except for the theorem conditions, validate every clause semantically, and verify an UNSAT proof.",
      "kind": "certified finite exhaustion",
      "assumptions": ["Global inherited-color exchange covers complementary prefixes."],
      "depends_on": ["OBL-004"],
      "status": "discharged",
      "severity": "critical",
      "evidence": ["ART-011", "ART-013"],
      "owner_role": "formalizer",
      "hostile_review": {"status": "no-critical-issue", "finding_refs": ["certificates/order98_phi40_exhaustion/README.md"]}
    },
    {
      "id": "OBL-006",
      "claim_id": "STR-001",
      "statement": "Verify positive witnesses at orders 97 and 99 and combine them only with the exact order-98 nonexistence theorem.",
      "kind": "finite corollary",
      "assumptions": ["The same effective-template definition and threshold are used at all three orders."],
      "depends_on": ["OBL-002", "OBL-005"],
      "status": "discharged",
      "severity": "major",
      "evidence": ["ART-014", "ART-007", "ART-011"],
      "owner_role": "integrator",
      "hostile_review": {"status": "no-critical-issue", "finding_refs": ["tests/run_order97_breakthrough_checks.sh", "tests/run_order99_breakthrough_checks.sh"]}
    },
    {
      "id": "OBL-007",
      "claim_id": "PRI-001",
      "statement": "Obtain an external current-record and priority check from Rowley, Radziszowski, or another computational Ramsey specialist.",
      "kind": "external literature and priority review",
      "assumptions": ["Private and unindexed results may exist."],
      "depends_on": [],
      "status": "open",
      "severity": "major",
      "evidence": ["KNOWN_RESULTS.md", "REQUESTS.md"],
      "owner_role": "librarian",
      "hostile_review": {"status": "not-run", "finding_refs": []}
    }
  ]
}
```
