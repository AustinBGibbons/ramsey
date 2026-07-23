# Claim Ledger

The JSON block is authoritative. Correctness, finite verification, target
existence, and current-record status are separate claims.

```json
{
  "schema_version": 1,
  "claims": [
    {
      "id": "DEF-001",
      "statement": "For an integer m >= 2, a linear three-coloring of K_m is a map c:{1,...,m-1}->{1,2,3} that assigns edge {i,j}, 0 <= i < j <= m-1, the color c(j-i).",
      "statement_sha256": "2c1ec0b4f31531dccd21c68b04d14d06b79e772df84d167f2f500c9bbde338ac",
      "domain": "Complete graphs K_m with integer-labelled vertices and m >= 2.",
      "quantifiers": "Definition for every integer m >= 2.",
      "assumptions": ["Vertices are labelled 0 through m-1.", "Edges are undirected."],
      "status": "definition",
      "origin": "source",
      "evidence": ["arXiv:2203.13476v3, printed p. 2"],
      "obligations": [],
      "status_history": [
        {"from": null, "to": "definition", "reason": "The source definition was normalized with its vertex and distance conventions."}
      ]
    },
    {
      "id": "DEF-002",
      "statement": "An operational (5,5,3) template certificate of order m with required phi lower bound q and span s is a word c:{1,...,m-1}->{1,2,3} such that c(m-1)=3, no distance at most q has color 3, the color-3 distances contain no a,b,a+b, and, after colors 1 and 2 are repeated with period m-1 on vertices 0,...,s, neither repeated color contains K_5; a full certificate additionally has s >= 4(m-2).",
      "statement_sha256": "3ead1723e03ac01fe63604b8a9d0e66a463cd26a77aefb906a8eff52ab3a3dc0",
      "domain": "Finite words over colors 1,2,3 with integer order, phi lower bound, and checked span.",
      "quantifiers": "Definition for every m >= 2, q >= 0, and s >= 0.",
      "assumptions": ["Periodic residue 0 is represented by base distance m-1.", "The sum-free test allows a=b."],
      "status": "definition",
      "origin": "new",
      "evidence": ["DEFINITIONS.md", "SRC-001"],
      "obligations": [],
      "status_history": [
        {"from": null, "to": "definition", "reason": "Operational certificate semantics were fixed before search and include the full Rowley cutoff."}
      ]
    },
    {
      "id": "SRC-001",
      "statement": "Rowley's generalized construction compounds a linear U(k_1,...,k_{q-1},3;m) having a triangle-free template with a linear V(...;n) to obtain a linear Ramsey graph of order (m-1)(n-1)+1+phi, where phi=min(T)-1; for an inherited color forbidding K_k, any offending K_k compresses to maximum edge length at most (k-1)(m-2).",
      "statement_sha256": "95429d9ad46786ab4f33d84ec2439eee712431376476f92877b52aa1706a5bdd",
      "domain": "Rowley's finite linear Ramsey graph construction.",
      "quantifiers": "For every pair of linear prototypes satisfying Theorem 3.2 and every inherited color.",
      "assumptions": ["The first prototype has a tf-template containing m-1.", "The second prototype has the source's linear Ramsey properties."],
      "status": "sourced-known-result",
      "origin": "source",
      "evidence": ["ART-001", "KNOWN_RESULTS.md"],
      "obligations": [],
      "citations": [
        {
          "primary_id": "arXiv:1912.01164v3",
          "location": "Definition 3.1 and Theorem 3.2 with proof, printed pp. 4-6",
          "statement": "The generalized construction has order (m-1)(n-1)+1+phi and inherited-color obstructions compress to span (k_s-1)(m-2).",
          "hypotheses": ["linear first prototype", "triangle-free template containing m-1", "linear second prototype"],
          "hypotheses_verified": true,
          "verifier": "primary PDF text and formula audit on 2026-07-22",
          "verified_on": "2026-07-22"
        }
      ],
      "status_history": [
        {"from": null, "to": "sourced-known-result", "reason": "The theorem, construction sets, cutoff proof, and target hypothesis map were checked in the primary PDF."}
      ]
    },
    {
      "id": "SRC-002",
      "statement": "Rowley gives an effective (5,5,3) template of order 93 with phi=40 and, using an order-453 (5,5,5) prototype, obtains a five-color K_5-free graph of order 41625 and hence R_5(5)>=41626.",
      "statement_sha256": "453a7c5fb9dfa020001a1da90536c6f8ac35767815e18e86b7480354166677d6",
      "domain": "Specific linear Ramsey templates and their Rowley compound graphs.",
      "quantifiers": "Existence of the one published template and its stated compound construction.",
      "assumptions": ["The ancillary TFT(S) column is the Table 1 order-93 template."],
      "status": "sourced-known-result",
      "origin": "source",
      "evidence": ["ART-002", "ART-003", "ART-004", "seeds/ROWLEY_ORDER93_EXTRACTION.md"],
      "obligations": [],
      "citations": [
        {
          "primary_id": "arXiv:2203.13476v3",
          "location": "Equation (3.5), printed p. 4; Table 1, printed p. 6; ancillary spreadsheet sheet Paper_Sep_2022",
          "statement": "An effective (5,5,3) template has order 93 and phi 40, yielding compound order 41625 and the bound 41626.",
          "hypotheses": ["multiple-repetition template condition", "order-453 (5,5,5) prototype"],
          "hypotheses_verified": true,
          "verifier": "primary PDF and ancillary XML audit on 2026-07-22",
          "verified_on": "2026-07-22"
        }
      ],
      "status_history": [
        {"from": null, "to": "sourced-known-result", "reason": "The table, formula, and explicit ancillary word were checked against the primary arXiv package."}
      ]
    },
    {
      "id": "SUR-001",
      "statement": "Radziszowski's Small Ramsey Numbers, revision 18 dated 24 April 2026, records the lower bound R_5(5)>=41626 in Table XIa.",
      "statement_sha256": "e44d970e78553804e443352a4a47bb776a552912a676c4fe49e3dbbb3f101e9c",
      "domain": "Published specific multicolor Ramsey lower bounds as surveyed in revision 18.",
      "quantifiers": "One recorded lower bound current at the survey revision date.",
      "assumptions": ["Revision 18 is the checked survey version."],
      "status": "sourced-known-result",
      "origin": "source",
      "evidence": ["ART-005", "KNOWN_RESULTS.md"],
      "obligations": [],
      "citations": [
        {
          "primary_id": "DOI:10.37236/21, revision 18",
          "location": "Title page and Table XIa, printed p. 55",
          "statement": "The table entry for r=5 and m=5 is 41626.",
          "hypotheses": ["classical diagonal five-color Ramsey number R_5(5)"],
          "hypotheses_verified": true,
          "verifier": "primary survey PDF text and table audit on 2026-07-22",
          "verified_on": "2026-07-22"
        }
      ],
      "status_history": [
        {"from": null, "to": "sourced-known-result", "reason": "The exact table cell and revision date were checked in the primary survey PDF."}
      ]
    },
    {
      "id": "DER-001",
      "statement": "If an operational full (5,5,3) template certificate of order 94 with phi at least 40 exists, then Rowley's construction with an order-453 (5,5,5) prototype produces a five-color K_5-free graph on at least 93*452+41=42077 vertices, and therefore R_5(5)>=42078.",
      "statement_sha256": "2656cc49a0c89cd2e58aef5d13a162d28a9d7ccc4522080be1126ff0eae74b1d",
      "domain": "Operational full order-94 certificates and Rowley compound graphs.",
      "quantifiers": "For every order-94 certificate meeting the stated hypotheses.",
      "assumptions": ["SRC-001", "the order-453 prototype used in SRC-002", "phi >= 40"],
      "status": "sourced-known-result",
      "origin": "source",
      "evidence": ["SRC-001", "SRC-002", "KNOWN_RESULTS.md"],
      "obligations": [],
      "citations": [
        {
          "primary_id": "arXiv:1912.01164v3; arXiv:2203.13476v3",
          "location": "Theorem 3.2, printed pp. 4-6; equation (3.5), printed p. 4",
          "statement": "The compound order is (m-1)(n-1)+1+phi; substituting m=94, n=453, phi>=40 gives at least 42077.",
          "hypotheses": ["full effective (5,5,3) template of order 94", "linear (5,5,5) prototype of order 453"],
          "hypotheses_verified": true,
          "verifier": "source specialization and independent integer arithmetic on 2026-07-22",
          "verified_on": "2026-07-22"
        }
      ],
      "status_history": [
        {"from": null, "to": "sourced-known-result", "reason": "This is the direct target specialization of the checked source theorem and prototype."}
      ]
    },
    {
      "id": "FIN-001",
      "statement": "The published order-93 word in seeds/rowley_order93.template is accepted as a full effective-template certificate through span 368 by both independent exact verifiers, which use distinct clique-search algorithms.",
      "statement_sha256": "a36719a3bec8b908666b72b146862fed432607c5cdc64feadb0c831cb14e6e61",
      "domain": "The fixed 92-symbol order-93 candidate file and vertices 0 through 368.",
      "quantifiers": "Exact verification of one fixed source-derived word in both inherited colors.",
      "assumptions": ["Candidate-file semantics in DEF-002", "period 92", "span 368"],
      "status": "verified-exact-computation",
      "origin": "new",
      "evidence": ["ART-006", "ART-007", "ART-008", "tests/run_python_verifier_tests.sh", "tests/run_cpp_verifier_tests.sh"],
      "obligations": [],
      "status_history": [
        {"from": null, "to": "verified-exact-computation", "reason": "A Python bit-mask checker and an independent C++ candidate-list checker both accept the source seed and reject semantic regression fixtures."}
      ]
    },
    {
      "id": "FIN-002",
      "statement": "The 452-symbol word in sources/rowley_exoo_order453.prototype is copied exactly from distances 1 through 452 of Rowley's archived order-977 template and defines a cyclic three-coloring of K_453 with no monochromatic K_5.",
      "statement_sha256": "020eef717ef05dd525a4c3584a3548983b17c65255e828d39f49d0b13d4e61b3",
      "domain": "The fixed source-derived 452-symbol linear three-coloring on vertices 0 through 452.",
      "quantifiers": "Exact verification of one fixed prototype in all three colors.",
      "assumptions": ["Rowley's order-977 construction copies prototype distances 1 through 452 verbatim.", "The ancillary spreadsheet column AB is the published order-977 template."],
      "status": "verified-exact-computation",
      "origin": "new",
      "evidence": ["ART-003", "ART-013", "ART-014", "ART-015", "ART-023"],
      "obligations": [],
      "status_history": [
        {"from": null, "to": "verified-exact-computation", "reason": "The source extraction is hash-anchored, and independent Python bit-mask and C++ candidate-list searches find no monochromatic K_5 in any of the three colors."}
      ]
    },
    {
      "id": "FIN-003",
      "statement": "The file results/r5_5_order42077.linear-coloring is the exact Rowley composition of results/order94_t12.template with sources/rowley_exoo_order453.prototype, has order 42077, assigns every positive distance through 42076 exactly once, and is cyclic.",
      "statement_sha256": "61b22da8a4c218a2836200931e5939ee3ddf6bcf6c48c40f51ee5c41e80dff35",
      "domain": "The frozen 42076-symbol five-color distance word and Rowley's displayed set-union construction.",
      "quantifiers": "Exact verification of one fixed compound coloring.",
      "assumptions": ["SRC-001", "FIN-002", "the canonical order-94 witness recorded by CON-001"],
      "status": "verified-exact-computation",
      "origin": "new",
      "evidence": ["ART-016", "ART-013", "ART-021", "ART-022", "ART-024"],
      "obligations": [],
      "status_history": [
        {"from": null, "to": "verified-exact-computation", "reason": "A generator implements Rowley's block formula, while a separate set-union checker assigns all 42076 distances independently and matches the frozen word and hash."}
      ]
    },
    {
      "id": "CON-001",
      "statement": "There exists an operational full (5,5,3) template certificate of order 94 with phi at least 40 and repeat span 368.",
      "statement_sha256": "5f630bcce91545ada4e4052aed177e2d5f54dee783e90424adc916db198cb19e",
      "domain": "Words c:{1,...,93}->{1,2,3} under DEF-002.",
      "quantifiers": "There exists one such word.",
      "assumptions": ["order=94", "phi_min=40", "repeat_span=368"],
      "status": "verified-exact-computation",
      "origin": "new",
      "evidence": ["ART-016", "ART-017", "ART-018", "ART-007", "ART-008", "ART-020"],
      "obligations": ["OBL-001", "OBL-002"],
      "status_history": [
        {"from": null, "to": "conjecture", "reason": "The order-93 predecessor and exact verifier baseline were established; no order-94 witness had yet been certified."},
        {"from": "conjecture", "to": "verified-exact-computation", "reason": "Three distinct frozen order-94 words, found by structured, direct, and lazy-SAT searches, all pass both independent full-condition verifiers; the canonical word is also overtested through four complete periods."}
      ]
    }
  ]
}
```
