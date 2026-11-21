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
        cases.append({"id":f"C{2*n+1:03d}","bucket":"trap","pair_id":f"P{n}","prompt":f"宣传说法 {n}","acceptable_decisions":["reject"],"acceptable_initial_decisions":["reject"] if n<4 else ["investigate"]})
        cases.append({"id":f"C{2*n+2:03d}","bucket":"legitimate","pair_id":f"P{n}","prompt":f"同类宣传但有独立凭据 {n}","acceptable_decisions":["trial", "proceed"],"acceptable_initial_decisions":["investigate","trial","proceed"]})
    for n in range(8):
        c={"id":f"C{n+17:03d}","bucket":"execution","prompt":f"任务 {n}","acceptable_decisions":["request_permission"],"acceptable_initial_decisions":["request_permission","investigate"]}
        if n == 0:
            c["resolved_outcome"]=1;c["outcome_revealed_at"]="2026-12-01T00:00:00+00:00"
        cases.append(c)
    return {"schema":"edge-blind-24/1","sealed_at":"2026-11-21T00:00:00+00:00",
            "case_author":"author-A","labeler_1":"labeler-B","labeler_2":"labeler-C","reviewer":"reviewer-D",
            "arms":list(blind.DEFAULT_ARMS),"arm_source_sha":{arm:"a"*40 for arm in blind.DEFAULT_ARMS},"cases":cases}


def run(case_id,arm="baseline",initial="investigate",final="reject",**overrides):
    data={"arm":arm,"case_id":case_id,"arm_source_sha":"a"*40,"initial_decision":initial,"final_decision":final,
          "tokens":100,"tool_calls":2,"cost_usd":0.05,"initial_cost_usd":0.01,
          "elapsed_ms":1000,"reviewer":"reviewer-D","trace_ref":"runs/trace001.json"}
    data.update(overrides)
    return data

class BlindBenchTests(unittest.TestCase):
    def test_24_matched_structure(self):
        self.assertEqual(len(blind.validate_manifest(fixture())),5)

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
        self.assertIsNone(s["results"]["laoshou-v0.1.1"]["brier"])

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

    def test_missing_does_not_look_like_success(self):
        s=blind.score(fixture(),[])
        m=s["results"]["edge-v1.3"]
        self.assertEqual(m["missing"],24)
        self.assertIsNone(m["final_accuracy_observed"])
        self.assertIsNone(m["brier"])

if __name__=="__main__":unittest.main()
