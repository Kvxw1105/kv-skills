#!/usr/bin/env python3
"""Generate deterministic v1.2 sidecar metadata for all 96+16 atoms.
This tool must not silently reset field-test metadata after initial release.
Run only to verify/reconcile additions, not as a general overwrite operation.
"""
import json
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
legacy=(ROOT/'references/mind-atoms.md').read_text(encoding='utf-8')
legacy_pairs=re.findall(r'(?m)^- \*\*([A-L]\d{2})\s+([^*]+)\*\*',legacy)
research=json.loads((ROOT/'references/research-atoms.json').read_text(encoding='utf-8'))['research_atoms']
if len(legacy_pairs)!=96 or len({a for a,_ in legacy_pairs})!=96:
    raise SystemExit('Expected exactly 96 unique legacy atoms')
if len(research)!=16 or len({x['id'] for x in research})!=16:
    raise SystemExit('Expected exactly 16 unique research atoms')
registries=[]
for aid,name in legacy_pairs:
    registries.append({'id':aid,'name':name.strip(),'origin':'original_heuristic',
                       'evidence_tier':'heuristic','lifecycle':'candidate',
                       'source_ids':[], 'observed_trial_n':0, 'last_reviewed':None,
                       'note':'Useful hypothesis; not independently validated as a commercial-performance enhancer.'})
for a in research:
    registries.append({'id':a['id'],'name':a['name'],'origin':'research_2026_11_20',
                       'evidence_tier':'research_linked','lifecycle':'candidate',
                       'source_ids':a['source_ids'],'observed_trial_n':0,'last_reviewed':None,
                       'note':'Sources support a mechanism/context; no controlled evidence of incremental sales or model improvement.'})
path=ROOT/'references'/'atom-registry.json'
if path.exists():
    # Do not discard trial history, patch/split decisions or reviews during upgrades.
    previous=json.loads(path.read_text(encoding='utf-8'))
    byid={x['id']:x for x in previous['atoms']}
    for e in registries:
        if e['id'] in byid:
            orig=byid[e['id']]
            e.update({k:v for k,v in orig.items() if k in ('evidence_tier','lifecycle','observed_trial_n','last_reviewed','note','lineage')})
obj={'schema_version':'1.2','count_note':'96 historical heuristic atoms + 16 source-linked research atoms. Zero field-validated atoms at initial release.','atoms':registries}
path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('registered',len(registries),'atoms, preserving any known lifecycle state')
