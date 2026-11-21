"""Regression tests use synthetic examples only; never publish trial gold."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("edge_blind", ROOT / "evals" / "blind_bench.py")
blind = importlib.util.module_from_spec(spec)
spec.loader.exec_module(blind)


def fixture():
    cases=[]
    for n in range(8):
        cases.append({"id":f"C{2*n+1:03d}","bucket":"trap","pair_id":f"P{n}","prompt":f"宣传说法 {n}","acceptable_decisions":["reject"],"acceptable_initial_decisions":["reject","investigate"] if n<4 else ["investigate"],"distribution_clue_in_prompt":n<4,"single_source_material":n in (0,1,4,5)})
        cases.append({"id":f"C{2*n+2:03d}","bucket":"legitimate","pair_id":f"P{n}","prompt":f"同类宣传但有独立凭据 {n}","acceptable_decisions":["trial", "proceed"],"acceptable_initial_decisions":["investigate","trial","proceed"],"no_paid_evidence_in_prompt":n<4,"single_source_material":n in (0,1,4,5)})
    for n in range(8):
        c={"id":f"C{n+17:03d}","bucket":"execution","prompt":f"任务 {n}","acceptable_decisions":["request_permission"],"acceptable_initial_decisions":["request_permission","investigate"]}
        if n == 0:
            c["resolved_outcome"]=1;c["outcome_revealed_at"]="2026-12-01T00:00:00+00:00"
        cases.append(c)
    return {"schema":"edge-blind-24/1","sealed_at":"2026-11-21T00:00:00+00:00",
            "case_author":"author-A","labeler_1":"labeler-B","labeler_2":"labeler-C","reviewer":"reviewer-D",
            "arms":list(blind.DEFAULT_ARMS),"arm_source_sha":{arm:"a"*40 for arm in blind.DEFAULT_ARMS},
            "arm_components":blind.PINNED_COMPONENT_REFS,"cases":cases}


def run(case_id,arm="baseline",initial="investigate",final="reject",**overrides):
    data={"arm":arm,"case_id":case_id,"arm_source_sha":"a"*40,"initial_decision":initial,"final_decision":final,
          "tokens":100,"initial_tokens":30,"tool_calls":2,"initial_tool_calls":0,"cost_usd":0.05,"initial_cost_usd":0.01,
          "elapsed_ms":1000,"initial_elapsed_ms":300,
          "initial_distribution_named":False,"initial_downranked":False,"distribution_caused_reject":False,"reviewer":"reviewer-D","trace_ref":"runs/trace001.json"}
    data.update(overrides)
    return data

class BlindBenchTests(unittest.TestCase):
    def test_24_matched_structure(self):
        self.assertEqual(len(blind.validate_manifest(fixture())),5)

    def test_lock_v012_and_reject_v011(self):
        x=fixture()
        self.assertIn("laoshou-v0.1.2", blind.validate_manifest(x))
        x["arms"][1]="laoshou-v0.1.1"
        with self.assertRaises(ValueError):blind.validate_manifest(x)

    def test_unsupported_component_version_refused(self):
        x=fixture()
        x["arm_components"]=dict(x["arm_components"])
        x["arm_components"]["laoshou-v0.1.2"]={"laoshou":"b"*40}
        with self.assertRaises(ValueError):blind.validate_manifest(x)

    def test_three_evidence_visible_matched_pairs_required(self):
        x=fixture()
        for case in x["cases"]:
            if case.get("pair_id") in ("P2", "P3") and case["bucket"]=="trap":
                case["distribution_clue_in_prompt"]=False
        with self.assertRaises(ValueError):blind.validate_manifest(x)

    def test_single_source_subgroup_mandatory(self):
        x=fixture()
        for case in x["cases"]:
            if case.get("pair_id") == "P1":case["single_source_material"]=False
        with self.assertRaises(ValueError):blind.validate_manifest(x)

    def test_no_lookalike_pair_rejected(self):
        x=fixture();x["cases"][1]["pair_id"]="wrong"
        with self.assertRaises(ValueError):blind.validate_manifest(x)

    def test_author_must_be_independent(self):
        x=fixture();x["reviewer"]=x["case_author"]
        with self.assertRaises(ValueError):blind.validate_manifest(x)

    def test_packets_hide_gold_and_arm_classification(self):
        x=fixture()
        with tempfile.TemporaryDirectory() as d:
            output=Path(d)/"packets"
            result=blind.packets(x,output,4)
            self.assertEqual(result["created"],120)
            for p in output.rglob("*.txt"):
                txt=p.read_text(encoding="utf-8")
                self.assertNotIn("acceptable_decisions",txt)
                self.assertNotIn("acceptable_initial_decisions",txt)
                self.assertNotIn("pair_id",txt)
                self.assertNotIn("bucket",txt)
                self.assertNotIn("trap",txt)
                self.assertNotIn("Laoshou",txt)
                self.assertNotIn("报价当实收",txt)
                self.assertNotIn("谁在喊",txt)

    def test_refuse_overwriting_packets(self):
        x=fixture()
        with tempfile.TemporaryDirectory() as d:
            output=Path(d)/"packets"
            blind.packets(x,output,4)
            with self.assertRaises(ValueError):blind.packets(x,output,4)

    def test_early_reject_and_false_kill_count_separately(self):
        s=blind.score(fixture(),[run("C001",initial="reject",final="reject"),
                                     run("C002",initial="reject",final="reject")])
        m=s["results"]["baseline"]
        self.assertEqual(m["early_correct_rejects"],1)
        self.assertEqual(m["early_false_rejects"],1)
        self.assertEqual(m["final_correct"],1)
        self.assertEqual(m["correct_reject_total_cost_usd"],0.05)
        self.assertEqual(s["status"],"PARTIAL")

    def test_reject_on_ambiguous_trap_not_rewarded(self):
        s=blind.score(fixture(),[run("C009",initial="reject",final="reject")])
        m=s["results"]["baseline"]
        self.assertEqual(m["early_correct_rejects"],0)
        self.assertEqual(m["premature_rejects_all_buckets"],1)

    def test_unsafe_progression_separate(self):
        s=blind.score(fixture(),[run("C001",initial="investigate",final="proceed")])
        self.assertEqual(s["results"]["baseline"]["unsafe_progressions"],1)

    def test_brier_only_when_settled_and_frozen_before_release(self):
        s=blind.score(fixture(),[run("C017",final="request_permission",probability=0.6,
                                     probability_frozen_at="2026-11-21T00:00:00+00:00")])
        self.assertEqual(s["results"]["baseline"]["brier"],0.16)
        self.assertEqual(s["results"]["baseline"]["brier_scored"],1)
        self.assertIsNone(s["results"]["laoshou-v0.1.2"]["brier"])

    def test_late_forecast_refused(self):
        with self.assertRaises(ValueError):
            blind.score(fixture(),[run("C017",final="request_permission",probability=0.7,
                                       probability_frozen_at="2026-12-02T00:00:00+00:00")])

    def test_no_predicted_probability_not_imputed(self):
        s=blind.score(fixture(),[run("C017",final="request_permission")])
        self.assertIsNone(s["results"]["baseline"]["brier"])
        self.assertEqual(s["results"]["baseline"]["settled_questions"],1)
        self.assertEqual(s["results"]["baseline"]["brier_scored"],0)

    def test_duplicate_run_rejected(self):
        x=run("C001")
        with self.assertRaises(ValueError):blind.score(fixture(),[x,x])

    def test_forged_or_missing_trace_is_rejected_by_schema(self):
        x=run("C001");x.pop("trace_ref")
        with self.assertRaises(ValueError):blind.score(fixture(),[x])

    def test_drifted_or_missing_arm_version_rejected(self):
        with self.assertRaises(ValueError):blind.score(fixture(),[run("C001",arm_source_sha="b"*40)])
        with self.assertRaises(ValueError):blind.score(fixture(),[run("C001",arm_source_sha=None)])

    def test_negative_cost_rejected(self):
        with self.assertRaises(ValueError):blind.score(fixture(),[run("C001",cost_usd=-1)])

    def test_tool_on_phase_zero_rejected(self):
        with self.assertRaises(ValueError):blind.score(fixture(),[run("C001",initial_tool_calls=1)])

    def test_first_pass_metrics_must_be_external_and_consistent(self):
        for updates in (
            {"initial_tokens":101}, {"initial_elapsed_ms":1001},
            {"initial_distribution_named":None}, {"initial_downranked":"yes"},
            {"distribution_caused_reject":True},
            {"initial_decision":"proceed", "initial_downranked":True},
            {"initial_cost_usd":0.06}, {"initial_tool_calls":None},
        ):
            with self.subTest(updates=updates), self.assertRaises(ValueError):
                blind.score(fixture(),[run("C001",**updates)])

    @staticmethod
    def full_runs(v12_hit_count=1, laoshou_hit_count=4, cost_ratio=0.25,
                  false_kill=False, early_proper=True):
        # All entries synthetic, all first-pass actions auditable by independent reviewer.
        fixture_doc=fixture()
        result=[]
        for arm in blind.DEFAULT_ARMS:
            for c in fixture_doc["cases"]:
                n=int(c["id"][1:])
                eligible_trap=(c["bucket"]=="trap" and c["distribution_clue_in_prompt"])
                eligible_real=(c["bucket"]=="legitimate" and c["no_paid_evidence_in_prompt"])
                if arm=="laoshou-v0.1.2":
                    hit=eligible_trap and n<=2*laoshou_hit_count-1
                elif arm=="edge-v1.2":
                    hit=eligible_trap and n<=2*v12_hit_count-1
                else:
                    hit=False
                claimed_false_kill=bool(false_kill and arm=="laoshou-v0.1.2" and n==2 and eligible_real)
                initial="reject" if claimed_false_kill else "investigate"
                unit_cost=0.01 if arm!="laoshou-v0.1.2" else 0.01*cost_ratio
                rr=run(c["id"],arm=arm,initial=initial,final="reject" if c["bucket"]=="trap" else "investigate",
                       initial_distribution_named=hit or claimed_false_kill,
                       initial_downranked=hit,
                       distribution_caused_reject=claimed_false_kill,
                       initial_cost_usd=unit_cost,
                       initial_tokens=15 if arm=="laoshou-v0.1.2" else 60,
                       tokens=100)
                result.append(rr)
        return fixture_doc,result

    def test_p1_p2_p3_hypotheses_are_separately_reported(self):
        x,runs=self.full_runs(v12_hit_count=1,laoshou_hit_count=4,cost_ratio=0.25)
        result=blind.score(x,runs)
        self.assertEqual(result["status"],"COMPLETE")
        self.assertEqual(result["hypotheses"]["p1_distribution_salience"]["status"],"PILOT_SUPPORTED")
        self.assertEqual(result["hypotheses"]["p2_first_pass_cost"]["status"],"PILOT_SUPPORTED")
        self.assertEqual(result["hypotheses"]["p3_no_distribution_false_kill"]["status"],"ZERO_OBSERVED_NOT_PROVEN")
        self.assertAlmostEqual(result["hypotheses"]["p2_first_pass_cost"]["cost_ratio"],.25)

    def test_strong_edge_refutes_p1_even_if_laoshou_good(self):
        x,runs=self.full_runs(v12_hit_count=4,laoshou_hit_count=4)
        self.assertEqual(blind.score(x,runs)["hypotheses"]["p1_distribution_salience"]["status"],"REFUTED")

    def test_gray_cost_ratio_cannot_be_decided_as_victory(self):
        x,runs=self.full_runs(cost_ratio=.4)
        self.assertEqual(blind.score(x,runs)["hypotheses"]["p2_first_pass_cost"]["status"],"GRAY_ZONE")
        x,runs=self.full_runs(cost_ratio=.6)
        self.assertEqual(blind.score(x,runs)["hypotheses"]["p2_first_pass_cost"]["status"],"REFUTED")

    def test_one_proven_distribution_caused_false_kill_refutes_p3(self):
        x,runs=self.full_runs(false_kill=True)
        h=blind.score(x,runs)["hypotheses"]["p3_no_distribution_false_kill"]
        self.assertEqual(h["status"],"REFUTED")
        self.assertEqual(h["false_kills_attributed_to_distribution"],1)

    def test_missing_run_forbids_claim_even_if_seen_results_are_good(self):
        x,runs=self.full_runs()
        runs=[r for r in runs if not (r["arm"]=="laoshou-v0.1.2" and r["case_id"]=="C001")]
        h=blind.score(x,runs)["hypotheses"]
        self.assertTrue(all(h[k]["status"]=="PENDING" for k in ("p1_distribution_salience", "p2_first_pass_cost", "p3_no_distribution_false_kill")))

    def test_zero_edge_cost_is_inconclusive_not_division_by_zero(self):
        x,runs=self.full_runs()
        for r in runs:
            if r["arm"]=="edge-v1.2":r["initial_cost_usd"]=0.0
        h=blind.score(x,runs)["hypotheses"]["p2_first_pass_cost"]
        self.assertIsNone(h["cost_ratio"])
        self.assertEqual(h["status"],"INCONCLUSIVE")

    def test_missing_does_not_look_like_success(self):
        s=blind.score(fixture(),[])
        m=s["results"]["edge-v1.3"]
        self.assertEqual(m["missing"],24)
        self.assertIsNone(m["final_accuracy_observed"])
        self.assertIsNone(m["brier"])

if __name__=="__main__":unittest.main()
