"""Read-only, deterministic, evidence-bounded research-query adapter.

No network, language model, file mutation, training or autonomous action.
"""
from __future__ import annotations
import json
import os
from .benchmark import evaluate_response, VALID_CASES
from .csts import ClaimJournal
from .classifier import classify, REQUIRED
from .evidence import digest

RECORDS={
    "cycle_locality":{"case_id":"cycle_locality","status":"REFUTED_AS_STATED","unproved":"GLOBAL_FROM_LOCAL","witness":{"family":"cycle_pair","radius":2,"m":6}},
    "colap_counterexample":{"case_id":"colap_counterexample","status":"REFUTED_AS_STATED","witness":{"colap_rank":0,"overlap_rank":1,"origin":"chronos_pr279_record"},"missing_lemma":"forall admissible X, overlap(X) <= colap(X)"},
    "entropy_bridge":{"case_id":"entropy_bridge","status":"OPEN","missing_lemma":"SemanticRankRateToFiberEntropySoundness","evidence_level":"NO_FORMAL_PROOF"},
    "dashboard_not_proof":{"case_id":"dashboard_not_proof","status":"NOT_THEOREM","evidence_level":"CI_STATUS_ONLY"},
    "conditional_axiom":{"case_id":"conditional_axiom","status":"CONDITIONAL","evidence_level":"PROJECT_AXIOMS_ACTIVE"},
    "bridge_reconstruction":{"case_id":"bridge_reconstruction","status":"REFUTED_AS_STATED","witness":{"x":"00","x_prime":"01","time":0},"repair":"SUPPLY_INPUT_EXTERNALLY_OR_INCLUDE_IN_INITIAL_FRAME"},
    "bridge_chain_rule":{"case_id":"bridge_chain_rule","status":"REFUTED_AS_STATED","witness":{"input_bits":4,"rounds":1},"repair":"INCLUDE_INITIAL_MUTUAL_INFORMATION"},
    "bridge_initial_tradeoff":{"case_id":"bridge_initial_tradeoff","status":"INITIAL_INFORMATION_ALREADY_EXHAUSTS_INPUT_ENTROPY","witness":{"input_bits":4},"missing_obligation":"NONTRIVIAL_INFORMATION_TARGET_NOT_INITIALIZED_AWAY"},
    "bridge_sat_boundary":{"case_id":"bridge_sat_boundary","status":"DOES_NOT_ESTABLISH_SUPERPOLYNOMIAL_SAT_HARDNESS","witness":{"input_bits":128,"per_step_capacity_bits":7},"missing_obligation":"INDEPENDENT_SUPERPOLYNOMIAL_OR_NONTRIVIAL_REDUCTION"},
    "bridge_sat_sign_query":{"case_id":"bridge_sat_sign_query","status":"RESTRICTED_QUERY_LOWER_BOUND_ONLY","witness":{"m":8,"all_positive_signs":"00000000"},"missing_obligation":"UNRESTRICTED_SAT_TIME_LOWER_BOUND"},
    "bridge_eager_read_no_go":{"case_id":"bridge_eager_read_no_go","status":"INPUT_INFORMATION_EXHAUSTED_IN_LINEAR_TIME","witness":{"input_bits":8,"read_steps":8,"postprocessing_steps":256},"missing_obligation":"TASK_SPECIFIC_COMPUTATION_LOWER_BOUND_REQUIRED"},
}
SOURCES={
    "cycle_locality":"self-contained elementary finite graph construction",
    "colap_counterexample":"https://github.com/inaciovasquez2020/chronos-urf-rr/blob/3ce354779eb9039aef4d1153317f2535ed39fecd/docs/status/URF_AI_FRONTIER_DISCIPLINE_BENCHMARK_2026_05_14.md",
    "entropy_bridge":"https://github.com/inaciovasquez2020/chronos-urf-rr/blob/3ce354779eb9039aef4d1153317f2535ed39fecd/docs/status/URF_AI_FRONTIER_DISCIPLINE_BENCHMARK_2026_05_14.md",
    "dashboard_not_proof":"https://github.com/inaciovasquez2020/frontier-status-dashboard/blob/main/README.md",
    "conditional_axiom":"https://github.com/inaciovasquez2020/urf-core/blob/3fa960c4cbb42c4af9ca84c7b2b9265288e9e7bd/README.md",
    "bridge_reconstruction":"user-uploaded Universality Bridge PDF, Theorem 7, p. 2",
    "bridge_chain_rule":"user-uploaded Universality Bridge PDF, Theorem 16, p. 6",
    "bridge_initial_tradeoff":"user-uploaded Universality Bridge PDF, Theorem 7 and entropy-depth section, pp. 2, 6",
    "bridge_sat_boundary":"user-uploaded Universality Bridge PDF, Theorems 16 and 19, pp. 6-7",
    "bridge_sat_sign_query":"derived adversarial 1CNF family, independent finite exhaustive checker",
    "bridge_eager_read_no_go":"derived read-first information exhaustion theorem and finite fixture",
}
def answer(case_id: str) -> dict:
    if case_id not in RECORDS:
        return {"case_id":case_id,"status":"UNSUPPORTED","reason":"source missing: refuse inference"}
    response=json.loads(json.dumps(RECORDS[case_id]))
    verdict=evaluate_response(response,case_id)
    # Read-only integration: register a scoped OPEN claim, audit its event chain,
    # and deliberately refuse to infer a formal proof from a semantic fixture.
    roles={"curator":"AUTHOR","local-verifier":"VERIFIER","reviewer":"REVIEWER"}
    journal=ClaimJournal(os.urandom(32),roles,{})
    record={"claim_id":"fixture."+case_id,"semantic_version":1,"kind":"THEOREM","state":"OPEN",
            "proposition":case_id,"scope":{"domain":"bounded-research-benchmark","case_id":case_id},
            "assumptions":[],"dependencies":[],"frontier":[{"status":"OPEN","blocking":True,"id":"unverified-mathematical-mapping"}],
            "boundaries":[{"active":True,"blocks_proved":True}],"source_revision":{"uri":SOURCES[case_id],"commit":"PINNED_OR_DECLARED"},"author":"curator"}
    event=journal.apply(event_id="register."+case_id,kind="REGISTER",claim_id=record["claim_id"],actor="curator",expected_version=0,payload=record,reason="read-only benchmark registration")
    guarded={**record,"objects":{x:"present" for x in REQUIRED},"missing_proof_object":True}
    classification=classify(guarded,None,b"not-a-real-attestation-key-00000000",{},roles)
    governance={"claim_state":journal.claim(record["claim_id"])["state"],
                "theorem_ledger":classification["classification"],
                "journal_audit":journal.audit_events(),"registration_hash":event.event_hash,
                "candidate_digest":digest(response),"source_retrieval":"PINNED_REFERENCE_NOT_REPLAYED"}
    return {"answer":response,"validation":verdict,"source":SOURCES[case_id],"governance":governance,"mode":"READ_ONLY_CURATED_RESEARCH_ADAPTER"}

def benchmark() -> dict:
    out=[answer(cid) for cid in sorted(VALID_CASES)]
    return {"mode":"SYNTHETIC_GROUNDING_SELF_CHECK","total":len(out),"passed":sum(item["validation"]["pass"] for item in out),"cases":out}
