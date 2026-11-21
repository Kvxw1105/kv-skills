#!/usr/bin/env python3
"""Edge Operator Agent Kit: safe workspace adapters, no third-party deps.

Project-scoped only. This CLI never changes provider/system prompts or grants tools.
"""
from __future__ import annotations
import argparse
import hashlib
import difflib
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[1]
SKILL_SRC = REPO_ROOT / "skills" / "edge-operator"
VERSION = "1.3.0"

HOSTS = {
    "codex": {"skill": ".agents/skills/edge-operator", "files": ["AGENTS.md"]},
    "claude": {"skill": ".claude/skills/edge-operator", "files": ["CLAUDE.md"]},
    "gemini": {"skill": ".gemini/skills/edge-operator", "files": ["GEMINI.md"]},
    "opencode": {"skill": ".opencode/skills/edge-operator", "files": ["AGENTS.md"]},
    "cursor": {"skill": ".edge-operator/reference/edge-operator", "files": [".cursor/rules/edge-operator.mdc"]},
    "openclaw": {"skill": "skills/edge-operator", "files": ["AGENTS.md", "SOUL.md"]},
}
TAG = "EDGE-OPERATOR-AGENT-KIT"
MANIFEST = ".edge-operator-install.json"

BASELINE = """商业判断触发器（仅用于机会、交易、商业侦察与营销主张，不强行商业化其他任务）：
- 先问：谁在喊？是否有推广佣金或其他利益？区分付费推广、自然模仿和算法放大，未见证据不指控谁是托。
- 谁已经付钱、为什么付、钱最后流到谁手里？为什么轮到我，这个机会有什么隐藏瓶颈或衰减条件？
- 区分宣传/报价/询价/订金/净回款/复购，不准越级，不把模拟结果称为真实收入。
- 小额、可逆行动优先。每个严肃机会保留事前可证伪的判断、数字概率与结算日；结果到账或验收须有回执。
- 正规授权内积极执行。不要假装已有账号、工具、付款能力或第三方许可；有害、欺骗或未授权的动作不执行。
- 对同题任务先用短入口，复杂高成本任务再阅读已安装 edge-operator 的 SKILL.md 和相关资源；无需全量加载思维原子。
""".strip()
SOUL = """只调整商业任务中的思维姿态，不改变现有人格身份：说人话，敢独立判断，发现传播激励和利益错位；不使用神棍口吻，不凭语气制造确定性。对重要结论给证据等级、核查日期和失效条件。"""


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def hash_files(folder: Path) -> dict[str,str]:
    found = {}
    for file in sorted(folder.rglob("*")):
        if file.is_symlink():
            raise ValueError(f"Refusing symlink in managed skill: {file}")
        if file.is_file() and file.name != MANIFEST:
            found[file.relative_to(folder).as_posix()] = sha(file.read_bytes())
    return found


def safety(project: Path, target: Path) -> None:
    # For project files, do not follow any pre-existing symbolic link.
    project = project.absolute()
    if project.is_symlink():
        raise ValueError("Project path is a symlink; use its explicit real path")
    if project != target and project not in target.parents:
        raise ValueError("Target escaped project directory")
    p = project
    for component in target.relative_to(project).parts:
        p = p / component
        if p.is_symlink():
            raise ValueError(f"Refusing symlink target: {p}")


def tags(agent: str):
    return (f"<!-- {TAG}:{agent}:BEGIN -->", f"<!-- {TAG}:{agent}:END -->")


def block(agent: str, skill_rel: str, file: str) -> str:
    start, end = tags(agent)
    if agent == "cursor":
        return ("---\n"
                "description: Edge Operator business evidence and action discipline\n"
                "alwaysApply: false\n"
                "---\n"
                f"{start}\n# Edge Operator: commercial opportunity and execution\n"
                f"{BASELINE}\nWhen deeper tools are needed, read `{skill_rel}/SKILL.md`.\n{end}\n")
    payload = SOUL if file == "SOUL.md" else (BASELINE + f"\nDetailed skill entry: `{skill_rel}/SKILL.md`.")
    return f"{start}\n{payload}\n{end}\n"


def edited_text(existing: str | None, section: str, agent: str) -> str:
    begin, end = tags(agent)
    if existing is None or existing == "":
        return section
    if (begin in existing) != (end in existing):
        raise ValueError("Broken managed block marker; refusing unsafe edit")
    if begin in existing:
        if existing.count(begin) != 1 or existing.count(end) != 1 or existing.index(begin) >= existing.index(end):
            raise ValueError("Duplicate/inverted managed marker")
        start = existing.index(begin)
        finish = existing.index(end) + len(end)
        if existing[finish:finish+1] == "\n": finish += 1
        # The first install determines placement; update only the managed body.
        return existing[:start] + section + existing[finish:]
    return existing.rstrip("\n") + "\n\n" + section


def atomic_write(dst: Path, content: bytes) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".edge-operator-", dir=str(dst.parent))
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(content)
        os.replace(tmp, dst)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)


def existing_manifest(path: Path) -> dict|None:
    m = path / MANIFEST
    if not m.exists(): return None
    try:
        data = json.loads(m.read_text(encoding="utf-8"))
        if data.get("product") != "edge-operator-agent-kit":
            raise ValueError("Foreign manifest owner")
        return data
    except (ValueError, UnicodeDecodeError) as e:
        raise ValueError(f"Invalid owned-skill manifest at {m}: {e}")


def assert_owned_pristine(target: Path, agent: str) -> None:
    manifest = existing_manifest(target)
    if manifest is None or agent not in manifest.get("agents", []):
        raise ValueError(f"Existing skill directory is not owned by this installer/agent: {target}")
    if manifest.get("hashes") != hash_files(target):
        raise ValueError(f"Managed Skill has local changes; refusing overwrite/removal: {target}")


def create_backup(project: Path, agent: str, rel: str, existing: bytes | None) -> None:
    if existing is None: return
    backups = project / ".edge-operator" / "backups" / agent
    output = backups / rel
    safety(project, output)
    gitignore = project / ".edge-operator" / ".gitignore"
    if not gitignore.exists(): atomic_write(gitignore, b"*\n")
    if not output.exists():
        output.parent.mkdir(parents=True,exist_ok=True)
        atomic_write(output, existing)
    gitignore = project / ".edge-operator" / ".gitignore"


def prepare(args):
    if args.agent not in HOSTS: raise ValueError("Unsupported agent")
    project = Path(args.project).expanduser().absolute()
    if not project.is_dir(): raise ValueError(f"Project/workspace directory does not exist: {project}")
    spec=HOSTS[args.agent]
    target=project/spec["skill"]
    safety(project,target)
    if not (SKILL_SRC/"SKILL.md").exists(): raise ValueError("Expected skills/edge-operator/SKILL.md beside agent-kits")
    # This installer copies a vetted local source tree; refuse source symlink tricks.
    hash_files(SKILL_SRC)
    if target.exists(): assert_owned_pristine(target,args.agent)
    results=[]
    for rel in spec["files"]:
        p=project/rel;safety(project,p)
        previous = p.read_text(encoding="utf-8") if p.exists() else None
        section=block(args.agent,spec["skill"],Path(rel).name)
        if args.agent == "cursor":
            # A dedicated .mdc file is wholly owned by this adapter, not a shared user file.
            if previous is not None and previous != section:
                raise ValueError("Cursor rule already exists or was customized; refusing overwrite")
            contents=section
        else:
            contents=edited_text(previous,section,args.agent)
        if contents != previous: results.append((rel,previous,contents))
    return project,target,results


def cmd_plan(args):
    project,target,results=prepare(args)
    print(f"PLAN agent={args.agent} workspace={project}")
    print(f"  Skill: {'update-owned' if target.exists() else 'copy-new'} {target}")
    for rel,old,new in results:
        print(f"  Context: {'append/update-marked-block' if old else 'create'} {rel} (+{len(new)-(len(old) if old else 0)} chars)")
    if not results: print("  Context unchanged (already current)")
    if getattr(args, "diff", False):
        for rel,old,new in results:
            print("".join(difflib.unified_diff((old or "").splitlines(keepends=True),new.splitlines(keepends=True),fromfile=f"{rel} (before)",tofile=f"{rel} (planned)")))
    print("  No files changed. Run `install` explicitly to apply.")


def cmd_install(args):
    project,target,changes=prepare(args)
    for rel,old,new in changes:
        create_backup(project,args.agent,rel,old.encode("utf-8") if old is not None else None)
    for rel,old,new in changes:
        atomic_write(project/rel,new.encode("utf-8"))
    # Avoid destructive replacement unless installed source still exactly matches recorded checksums.
    if target.exists(): shutil.rmtree(target)
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copytree(SKILL_SRC,target,symlinks=False,ignore=shutil.ignore_patterns("__pycache__","*.pyc","dist"))
    manifest={"product":"edge-operator-agent-kit","version":VERSION,"agents":[args.agent],"hashes":hash_files(target)}
    atomic_write(target/MANIFEST,(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n").encode("utf-8"))
    print(f"INSTALLED {args.agent}: {target}")
    print("  Existing instruction files preserved; only managed blocks updated.")
    print("  Start a new agent session; installed files do not grant tools or authorization.")


def strip_block(current: str, agent: str) -> str:
    begin,end=tags(agent)
    if begin not in current and end not in current: raise ValueError("No managed instructions in context file")
    if current.count(begin)!=1 or current.count(end)!=1: raise ValueError("Invalid markers")
    a=current.index(begin);b=current.index(end)+len(end)
    if current[b:b+1]=="\n": b+=1
    return (current[:a].rstrip("\n") + "\n" + current[b:].lstrip("\n")).strip("\n")+"\n" if (current[:a].strip() or current[b:].strip()) else ""


def cmd_uninstall(args):
    project=Path(args.project).expanduser().absolute();spec=HOSTS[args.agent]
    target=project/spec["skill"];safety(project,target)
    assert_owned_pristine(target,args.agent)
    changes=[]
    for rel in spec["files"]:
        p=project/rel;safety(project,p)
        if not p.is_file(): raise ValueError(f"Missing expected context file: {p}")
        old=p.read_text(encoding="utf-8")
        if args.agent == "cursor":
            expected=block(args.agent,spec["skill"],Path(rel).name)
            if old != expected: raise ValueError("Cursor rule customized since install; refusing removal")
            changes.append((p,None))
        else:
            new=strip_block(old,args.agent)
            backup=project/".edge-operator"/"backups"/args.agent/rel
            safety(project,backup)
            if backup.is_file():
                prior=backup.read_text(encoding="utf-8")
                if old == edited_text(prior,block(args.agent,spec["skill"],Path(rel).name),args.agent):
                    new=prior  # Byte-identical original when untouched outside managed block.
            if not new.strip():
                new=None  # No remaining user or other-agent content.
            changes.append((p,new))
    for p,new in changes:
        if new is None: p.unlink()
        else: atomic_write(p,new.encode("utf-8"))
    shutil.rmtree(target)
    print(f"UNINSTALLED {args.agent}. Existing user instructions retained; saved backups left intact.")


def cmd_status(args):
    project=Path(args.project).expanduser().absolute();spec=HOSTS[args.agent]
    target=project/spec["skill"];safety(project,target)
    info={"agent":args.agent,"workspace":str(project),"skill_exists":target.is_dir(),"managed":False,"pristine":False,"instructions":{}}
    if target.is_dir():
        m=existing_manifest(target)
        info["managed"] = bool(m and args.agent in m.get("agents",[]))
        info["pristine"] = bool(info["managed"] and m.get("hashes")==hash_files(target))
        info["installed_version"] = m.get("version") if m else None
    for rel in spec["files"]:
        p=project/rel;safety(project,p)
        info["instructions"][rel]=p.is_file() and tags(args.agent)[0] in p.read_text(encoding="utf-8")
    info["all_installed"] = info["managed"] and info["pristine"] and all(info["instructions"].values())
    print(json.dumps(info,ensure_ascii=False,indent=2))
    if not info["all_installed"]: sys.exit(2)


def cmd_export(args):
    project=Path(args.project).expanduser().absolute()
    if not project.is_dir(): raise ValueError("Project directory does not exist")
    output=project/"edge-operator-system-prompt.txt";safety(project,output)
    if output.exists(): raise ValueError("Existing prompt export would be overwritten; choose a clean directory")
    extra=(SKILL_SRC/"prompts"/("MASTER_PROMPT.txt" if args.profile=="full" else "QUICK_START.txt")).read_text(encoding="utf-8")
    payload=("# Edge Operator | prompt-only export (not automatically installed)\n"
             + BASELINE + "\n\n# Additional instructions\n" +extra.strip()+"\n")
    atomic_write(output,payload.encode("utf-8"))
    print(f"EXPORTED {output}\n  Paste into the target application's permitted Custom Instructions/Prompt field; this tool did not modify a provider system prompt.")


def main(argv=None):
    ap=argparse.ArgumentParser(description="Edge Operator Agent Kit: plan, install, status, uninstall, export")
    sub=ap.add_subparsers(dest="command",required=True)
    for cmd in ("plan","install","status","uninstall"):
        p=sub.add_parser(cmd);p.add_argument("--agent",required=True,choices=sorted(HOSTS));p.add_argument("--project",default=".")
        if cmd == "plan": p.add_argument("--diff",action="store_true",help="Preview unified differences without writing")
    p=sub.add_parser("export");p.add_argument("--project",default=".");p.add_argument("--profile",choices=["compact","full"],default="compact")
    args=ap.parse_args(argv)
    dispatch={"plan":cmd_plan,"install":cmd_install,"status":cmd_status,"uninstall":cmd_uninstall,"export":cmd_export}
    try: dispatch[args.command](args)
    except (ValueError,OSError,UnicodeError) as e:
        print(f"ERROR: {e}",file=sys.stderr);sys.exit(1)


if __name__=="__main__": main()
