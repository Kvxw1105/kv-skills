#!/usr/bin/env python3
"""Package a portable, source-complete offline kit with local Skill and installer."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import argparse
import hashlib
import json

KIT = Path(__file__).resolve().parent
ROOT = KIT.parents[1]
EXCLUDED = {"__pycache__", ".pytest_cache", ".git", ".venv", "dist"}

def build(dst:Path)->dict:
    inclusions=[ROOT/"skills"/"edge-operator",KIT]
    files=sorted(p for directory in inclusions for p in directory.rglob("*")
                 if p.is_file() and not any(k in EXCLUDED for k in p.relative_to(ROOT).parts)
                 and p.suffix not in (".pyc", ".pyo", ".zip"))
    entries={str(f.relative_to(ROOT)).replace("\\", "/"):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
    assert len([p for p in entries if p.endswith("/SKILL.md")])==1, "One Skill entrypoint required"
    for p in files:
        if p.is_symlink(): raise ValueError("Rejecting symbolic link in bundle")
    dst.parent.mkdir(parents=True,exist_ok=True)
    with ZipFile(dst,"w",ZIP_DEFLATED,compresslevel=9) as zipfile:
        for path in files: zipfile.write(path,"edge-operator-kit/"+path.relative_to(ROOT).as_posix())
        zipfile.writestr("edge-operator-kit/CHECKSUMS.json",json.dumps({"version":"1.3.2","files":entries},indent=2,ensure_ascii=False)+"\n")
    with ZipFile(dst) as zipfile:
        assert zipfile.testzip() is None
        manifest=json.loads(zipfile.read("edge-operator-kit/CHECKSUMS.json"))
        for file,digest in manifest["files"].items():
            assert hashlib.sha256(zipfile.read("edge-operator-kit/"+file)).hexdigest()==digest
    return {"version":"1.3.2","files":len(files),"archive":str(dst)}

if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("--out",type=Path,default=Path("dist/edge-operator-agentkit.zip"))
    print(json.dumps(build(parser.parse_args().out),indent=2))
