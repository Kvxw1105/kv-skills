import contextlib
import io
import json
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import cli


class AgentKitTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.temp.name)
    def tearDown(self):
        self.temp.cleanup()
    def run_cli(self, *argv, code=0):
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            with self.assertRaises(SystemExit) if code else contextlib.nullcontext() as failure:
                cli.main(list(argv) + ["--project",str(self.root)])
            if code: self.assertEqual(failure.exception.code,code)
        return stdout.getvalue() + stderr.getvalue()
    def test_all_six_install_and_uninstall(self):
        for host in cli.HOSTS:
            with self.subTest(host=host):
                self.run_cli("install","--agent",host)
                self.run_cli("status","--agent",host)
                self.run_cli("uninstall","--agent",host)
                self.assertFalse((self.root/cli.HOSTS[host]["skill"]).exists())
    def test_multiple_agents_same_project_preserve_blocks(self):
        self.run_cli("install","--agent","codex")
        self.run_cli("install","--agent","opencode")
        full=(self.root/"AGENTS.md").read_text()
        self.assertIn("AGENT-KIT:codex:BEGIN",full)
        self.assertIn("AGENT-KIT:opencode:BEGIN",full)
        self.run_cli("uninstall","--agent","codex")
        text=(self.root/"AGENTS.md").read_text()
        self.assertNotIn("AGENT-KIT:codex:BEGIN",text)
        self.assertIn("AGENT-KIT:opencode:BEGIN",text)
        self.run_cli("uninstall","--agent","opencode")
        self.assertFalse((self.root/"AGENTS.md").exists())
    def test_cursor_existing_rule_not_overwritten(self):
        p=self.root/".cursor/rules/edge-operator.mdc"
        p.parent.mkdir(parents=True)
        p.write_text("private rule")
        self.run_cli("install","--agent","cursor",code=1)
        self.assertEqual(p.read_text(),"private rule")
    def test_plan_has_no_effect(self):
        self.run_cli("plan","--agent","codex")
        self.assertEqual(list(self.root.iterdir()),[])
    def test_retains_unmanaged_text(self):
        old="Do not modify other scripts.\n\nExisting user rules.\n"
        f=self.root/"AGENTS.md";f.write_text(old,encoding="utf-8")
        self.run_cli("install","--agent","codex")
        self.assertTrue(f.read_text(encoding="utf-8").startswith(old))
        self.run_cli("uninstall","--agent","codex")
        self.assertIn("Existing user rules.",f.read_text(encoding="utf-8"))
        self.assertNotIn("EDGE-OPERATOR-AGENT-KIT",f.read_text(encoding="utf-8"))
        self.assertEqual(f.read_text(encoding="utf-8"),old)
        self.assertEqual((self.root/".edge-operator/backups/codex/AGENTS.md").read_text(encoding="utf-8"),old)
    def test_idempotent_install(self):
        self.run_cli("install","--agent","claude")
        first=(self.root/"CLAUDE.md").read_bytes()
        self.run_cli("install","--agent","claude")
        self.assertEqual(first,(self.root/"CLAUDE.md").read_bytes())
        self.assertEqual(first.count(b"EDGE-OPERATOR-AGENT-KIT"),2)
    def test_unowned_skill_refused(self):
        p=self.root/".agents/skills/edge-operator";p.mkdir(parents=True)
        (p/"PRIVATE.txt").write_text("do not delete")
        self.run_cli("install","--agent","codex",code=1)
        self.assertTrue((p/"PRIVATE.txt").exists())
        self.assertFalse((self.root/"AGENTS.md").exists())
    def test_modified_managed_skill_protected(self):
        self.run_cli("install","--agent","opencode")
        p=self.root/".opencode/skills/edge-operator/SKILL.md"
        p.write_text(p.read_text()+"\nMY CUSTOMIZATION\n")
        self.run_cli("install","--agent","opencode",code=1)
        self.run_cli("uninstall","--agent","opencode",code=1)
        self.assertIn("MY CUSTOMIZATION",p.read_text())
    def test_symlink_target_refused(self):
        evil=self.root/"AGENTS.md"
        outside=self.root/"outside.txt";outside.write_text("PRIVATE")
        evil.symlink_to(outside)
        self.run_cli("install","--agent","codex",code=1)
        self.assertEqual(outside.read_text(),"PRIVATE")
    def test_marker_corruption_refused(self):
        (self.root/"CLAUDE.md").write_text("<!-- EDGE-OPERATOR-AGENT-KIT:claude:BEGIN -->\n")
        self.run_cli("plan","--agent","claude",code=1)
    def test_prompt_export_explicit_and_not_installed(self):
        self.run_cli("export")
        p=self.root/"edge-operator-system-prompt.txt"
        self.assertIn("谁在喊",p.read_text())
        self.assertFalse((self.root/"AGENTS.md").exists())
        self.run_cli("export",code=1)
    def test_status_missing_is_nonzero(self):
        self.run_cli("status","--agent","gemini",code=2)
    def test_laoshou_baseline_no_blind_accusations(self):
        self.assertIn("区分付费推广、自然模仿和算法放大", cli.BASELINE)
    def test_no_forced_system_prompt_overwrite(self):
        for host in cli.HOSTS:
            self.assertNotIn("system_prompt", " ".join(cli.HOSTS[host]["files"]))
    def test_original_skill_single_entry(self):
        self.assertTrue((cli.SKILL_SRC/"SKILL.md").is_file())
        self.assertEqual(len(list(cli.SKILL_SRC.rglob("SKILL.md"))),1)

if __name__=="__main__":unittest.main()
