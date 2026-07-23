# Claim Ledger

The JSON block is authoritative. Correctness, certificate coverage, source
imports, and priority are separate claims.

```json
{
  "schema_version": 1,
  "claims": [
    {
      "id": "DEF-001",
      "statement": "For an integer m >= 2, a linear three-coloring of K_m is a map c:{1,...,m-1}->{1,2,3} assigning edge {i,j}, 0 <= i < j <= m-1, the color c(j-i).",
      "statement_sha256": "d78c784be8c67c1c3b27ff4ccb5f0ee3c2523f5c885823a91b96baa4cad261c2",
      "domain": "Complete graphs with vertices labelled by consecutive integers.",
      "quantifiers": "Definition for every integer m >= 2.",
      "assumptions": ["Edges are undirected.", "Distances are ordinary positive integers."],
      "status": "definition",
      "origin": "source",
      "evidence": ["DEFINITIONS.md"],
      "obligations": [],
      "status_history": [
        {"from": null, "to": "definition", "reason": "The source convention was normalized before search."}
      ]
    },
    {
      "id": "DEF-002",
      "statement": "An operational full (5,5,3) template certificate of order m and phi threshold q is a word c:{1,...,m-1}->{1,2,3} whose terminal distance has color 3, whose color-3 set avoids distances 1 through q and all triples a,b,a+b, and whose periodically repeated colors 1 and 2 contain no K_5 through span 4(m-2).",
      "statement_sha256": "f57f5640d4012ab16b28753db576d86e0ef4725f27db2a880542c26acf7aba03",
      "domain": "Finite three-symbol distance words with a distinguished template color.",
      "quantifiers": "Definition for every m >= 2 and q >= 0.",
      "assumptions": ["The terminal distance represents residue zero.", "The sum test permits a=b.", "Span is a maximum vertex label, not a vertex count."],
      "status": "definition",
      "origin": "new",
      "evidence": ["DEFINITIONS.md", "SRC-001"],
      "obligations": [],
      "status_history": [
        {"from": null, "to": "definition", "reason": "Operational semantics include every hypothesis used by the finite verifier."}
      ]
    },
    {
      "id": "SRC-001",
      "statement": "Rowley’s generalized construction combines an effective linear U(k_1,...,k_{q-1},3;m) template with a linear prototype of order n to produce a linear Ramsey coloring of order (m-1)(n-1)+1+phi, where phi=min(T)-1; inherited K_k obstructions compress to span (k-1)(m-2).",
      "statement_sha256": "bdeab25e4e47ace9930e724ab6e284af126c66f452d44b55cb0387f31e51c0f9",
      "domain": "Rowley's generalized linear Ramsey construction.",
      "quantifiers": "For every pair of linear inputs satisfying Theorem 3.2 and each inherited color.",
      "assumptions": ["The first input has a triangle-free template containing its terminal distance.", "The second input has the required linear Ramsey properties."],
      "status": "sourced-known-result",
      "origin": "source",
      "evidence": ["ART-001", "KNOWN_RESULTS.md"],
      "obligations": [],
      "citations": [
        {
          "primary_id": "Australasian Journal of Combinatorics 81(2) (2021), 245-256; arXiv:1912.01164v3",
          "location": "Definition 3.1 and Theorem 3.2 with proof, pp. 248-251",
          "statement": "The generalized construction has the stated order and finite inherited-color compression.",
          "hypotheses": ["linear first prototype", "triangle-free terminal template", "linear second prototype"],
          "hypotheses_verified": true,
          "verifier": "Primary-source formula and hypothesis audit",
          "verified_on": "2026-07-23"
        }
      ],
      "status_history": [
        {"from": null, "to": "sourced-known-result", "reason": "The published theorem and proof were mapped to the operational certificate conditions."}
      ]
    },
    {
      "id": "SRC-002",
      "statement": "Rowley gives an effective (5,5,3) template of order 93 with phi=40 and, using an order-453 (5,5,5) prototype, obtains a five-color K_5-free graph of order 41625 and hence R_5(5)>=41626.",
      "statement_sha256": "453a7c5fb9dfa020001a1da90536c6f8ac35767815e18e86b7480354166677d6",
      "domain": "Published effective Rowley templates and their compound colorings.",
      "quantifiers": "Existence of the published order-93 template and stated compound.",
      "assumptions": ["The ancillary TFT(S) column is the Table 1 order-93 template."],
      "status": "sourced-known-result",
      "origin": "source",
      "evidence": ["ART-002", "seeds/ROWLEY_ORDER93_EXTRACTION.md"],
      "obligations": [],
      "citations": [
        {
          "primary_id": "arXiv:2203.13476v3",
          "location": "Equation (3.5), Table 1, and ancillary sheet Paper_Sep_2022",
          "statement": "The order-93 effective template with phi 40 yields the bound 41626.",
          "hypotheses": ["multiple-repetition template condition", "order-453 linear prototype"],
          "hypotheses_verified": true,
          "verifier": "Primary PDF and ancillary-data audit",
          "verified_on": "2026-07-23"
        }
      ],
      "status_history": [
        {"from": null, "to": "sourced-known-result", "reason": "The table, formula, and explicit ancillary word were checked."}
      ]
    },
    {
      "id": "SUR-001",
      "statement": "Radziszowski’s Small Ramsey Numbers, revision 18 dated 24 April 2026, records R_5(5)>=41626 in Table XIa.",
      "statement_sha256": "f70ea7db60cba33566f10d704dafdbf67f34901c1c967e45108ffce70745f11e",
      "domain": "Published specific multicolor Ramsey lower bounds in survey revision 18.",
      "quantifiers": "One table entry at the stated revision date.",
      "assumptions": ["Revision 18 is the checked survey revision."],
      "status": "sourced-known-result",
      "origin": "source",
      "evidence": ["ART-003", "KNOWN_RESULTS.md"],
      "obligations": [],
      "citations": [
        {
          "primary_id": "DOI:10.37236/21, revision 18",
          "location": "Title page and Table XIa, printed p. 55",
          "statement": "The r=5, m=5 lower-bound entry is 41626.",
          "hypotheses": ["classical diagonal five-color Ramsey number"],
          "hypotheses_verified": true,
          "verifier": "Primary survey table audit",
          "verified_on": "2026-07-23"
        }
      ],
      "status_history": [
        {"from": null, "to": "sourced-known-result", "reason": "The exact table cell and revision date were checked."}
      ]
    },
    {
      "id": "FIN-002",
      "statement": "The word in sources/rowley_exoo_order453.prototype defines a linear three-coloring of K_453 with no monochromatic K_5.",
      "statement_sha256": "b90adc16c7b0291e8cd251470830fe7b1212c48e8548323dc7ffe0021ff0b377",
      "domain": "The frozen 452-symbol linear three-color word.",
      "quantifiers": "All three colors and all five-vertex subsets of K_453.",
      "assumptions": ["DEF-001"],
      "status": "verified-exact-computation",
      "origin": "new",
      "evidence": ["ART-004", "ART-015", "ART-016"],
      "obligations": ["OBL-001"],
      "status_history": [
        {"from": null, "to": "verified-exact-computation", "reason": "Independent Python and C++ exact clique searches reject K_5 in all three colors."}
      ]
    },
    {
      "id": "CON-002",
      "statement": "The word in results/order99_linear_prefix8.template is an effective Rowley (5,5,3) template of order 99 with phi=40.",
      "statement_sha256": "966daab2a5deabe7f70b92441293c2df557b8a9f2946c344297852b6bafb8fd3",
      "domain": "The frozen order-99 template word under DEF-002.",
      "quantifiers": "Both inherited colors, every template sum, and the complete span through 388.",
      "assumptions": ["DEF-002", "SRC-001"],
      "status": "verified-exact-computation",
      "origin": "new",
      "evidence": ["ART-007", "ART-005", "ART-006", "ART-008"],
      "obligations": ["OBL-002"],
      "status_history": [
        {"from": null, "to": "conjecture", "reason": "The order-99 search target was posed."},
        {"from": "conjecture", "to": "verified-exact-computation", "reason": "A frozen word passes two independent full-condition verifiers at exact span 388."}
      ]
    },
    {
      "id": "FIN-004",
      "statement": "The file results/r5_5_order44337.linear-coloring is the exact Rowley composition of the order-99 template and order-453 prototype and defines a five-coloring of K_44337 without a monochromatic K_5; therefore R_5(5)>=44338.",
      "statement_sha256": "4a7cc5b55168a61e05c7d07a25827bff9a5272964d9511567470617183fc20c2",
      "domain": "The frozen 44336-symbol five-color distance word and Rowley's composition theorem.",
      "quantifiers": "All five output colors and every edge of K_44337.",
      "assumptions": ["SRC-001", "FIN-002", "CON-002"],
      "status": "verified-exact-computation",
      "origin": "new",
      "evidence": ["ART-009", "ART-010", "ART-008"],
      "obligations": ["OBL-003"],
      "status_history": [
        {"from": null, "to": "verified-exact-computation", "reason": "The generator and independent set-union reconstruction match all distances and the source theorem transfers K_5-freeness."}
      ]
    },
    {
      "id": "NEG-001",
      "statement": "No effective Rowley (5,5,3) template of order 98 has phi>=40.",
      "statement_sha256": "e8e02ff9389458877867314155e06fc05459239d9f2c8752bc76ebe610116096",
      "domain": "All 97-symbol three-color words satisfying DEF-002 at order 98 and threshold 40.",
      "quantifiers": "Every two-color prefix and every unrestricted tail through terminal distance 97.",
      "assumptions": ["DEF-002", "Global exchange of inherited colors preserves every condition."],
      "status": "certificate-checked",
      "origin": "new",
      "evidence": ["ART-011", "ART-012", "ART-013"],
      "obligations": ["OBL-004", "OBL-005"],
      "status_history": [
        {"from": null, "to": "conjecture", "reason": "Repeated searches indicated an order-98 obstruction."},
        {"from": "conjecture", "to": "certificate-checked", "reason": "One prefix and eleven unrestricted-tail DRAT proofs verify after independent semantic CNF reconstruction."}
      ]
    },
    {
      "id": "STR-001",
      "statement": "At fixed phi=40, existence of effective Rowley (5,5,3) templates is not monotone in the template order: templates exist at orders 97 and 99, but none exists at order 98.",
      "statement_sha256": "e27d083951b417b3411e0068872cf5293becd2eea1a3d263e528c053f7004fd3",
      "domain": "Effective Rowley (5,5,3) templates at phi 40 and orders 97 through 99.",
      "quantifiers": "The three consecutive orders 97, 98, and 99.",
      "assumptions": ["CON-002", "NEG-001"],
      "status": "verified-exact-computation",
      "origin": "new",
      "evidence": ["ART-014", "ART-007", "ART-011"],
      "obligations": ["OBL-006"],
      "status_history": [
        {"from": null, "to": "verified-exact-computation", "reason": "Independent positive checks at 97 and 99 combine with the certified exhaustive negative at 98."}
      ]
    },
    {
      "id": "PRI-001",
      "statement": "Bounded primary-source and web searches completed on 23 July 2026 found no published collision with an order-99 effective (5,5,3) Rowley template or the bound R_5(5)>=44338.",
      "statement_sha256": "e8d642181793b80dfa1378e0bfceda41bf59c65c7a0b14a8a3ef107e05e7009b",
      "domain": "The explicitly checked literature corpus and indexed searches as of 23 July 2026.",
      "quantifiers": "Only the checked corpus; no claim about unpublished or unindexed work.",
      "assumptions": ["Search indexing is incomplete.", "Correctness and priority are independent."],
      "status": "finite-case-evidence",
      "origin": "new",
      "evidence": ["KNOWN_RESULTS.md", "ART-003"],
      "obligations": ["OBL-007"],
      "status_history": [
        {"from": null, "to": "finite-case-evidence", "reason": "The current survey, cited papers, arXiv update, and exact-value searches were checked without a collision."}
      ]
    }
  ]
}
```
