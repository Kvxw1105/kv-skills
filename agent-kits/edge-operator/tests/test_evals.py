import pathlib
import json
import tempfile
import importlib.util
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("edge_bench",ROOT/"evals/bench.py")
bench=importlib.util.module_from_spec(spec);spec.loader.exec_module(bench)

class BenchTest(unittest.TestCase):
    def test_packets_are_identical_for_each_cohort(self):
        cases,cohorts=bench.get_cases()
        with tempfile.TemporaryDirectory() as tmp:
            out=pathlib.Path(tmp)/"packets"
            bench.packets(out,cases,cohorts)
            self.assertEqual(len(list(out.rglob("*.md"))),len(cases)*len(cohorts))
            data=[(out/cohort/"B01.md").read_text() for cohort in cohorts]
            self.assertEqual(len(set(data)),1)
            self.assertNotIn("模拟/挂牌价称为实收",data[0])
            self.assertNotIn("可逆动作",data[0])
    def test_missing_results_are_counted_as_zeros(self):
        cases,cohorts=bench.get_cases()
        with tempfile.TemporaryDirectory() as tmp:
            file=pathlib.Path(tmp)/"results.jsonl"
            file.write_text(json.dumps({"cohort":"edge","case_id":"B01","adjudicator":"human", "evidence_ref":"mocked.txt",**{k:1 for k in bench.FIELDS}})+"\n")
            res=bench.score(file,cases,cohorts)
            self.assertEqual(res["results"]["edge"]["score_out_of_five"],round(5/len(cases),3))
            self.assertEqual(res["results"]["baseline"]["score_out_of_five"],0)
    def test_self_grading_without_receipts_fails(self):
        cases,cohorts=bench.get_cases()
        with tempfile.TemporaryDirectory() as tmp:
            file=pathlib.Path(tmp)/"bad.jsonl"
            file.write_text(json.dumps({"cohort":"edge","case_id":"B01",**{k:1 for k in bench.FIELDS}}))
            with self.assertRaises(ValueError):bench.score(file,cases,cohorts)
    def test_duplicate_case_fails(self):
        cases,cohorts=bench.get_cases()
        with tempfile.TemporaryDirectory() as tmp:
            file=pathlib.Path(tmp)/"dup.jsonl"
            item={"cohort":"edge","case_id":"B01","adjudicator":"h","evidence_ref":"a",**{k:0 for k in bench.FIELDS}}
            file.write_text(json.dumps(item)+"\n"+json.dumps(item)+"\n")
            with self.assertRaises(ValueError):bench.score(file,cases,cohorts)
