import importlib.util
import json
import pathlib
import tempfile
import unittest
from zipfile import ZipFile

p=pathlib.Path(__file__).resolve().parents[1]/"build_release.py"
spec=importlib.util.spec_from_file_location("edge_build_release",p)
release=importlib.util.module_from_spec(spec);spec.loader.exec_module(release)

class ReleaseTest(unittest.TestCase):
    def test_archive_integrity(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=pathlib.Path(tmp)/"kit.zip"
            meta=release.build(p)
            self.assertGreaterEqual(meta["files"],65)
            with ZipFile(p) as z:
                self.assertIsNone(z.testzip())
                self.assertEqual(sum(n.endswith("/SKILL.md") for n in z.namelist()),1)
                self.assertFalse(any("__pycache__" in name or name.endswith(".pyc") for name in z.namelist()))
                self.assertIn("edge-operator-kit/CHECKSUMS.json",z.namelist())
