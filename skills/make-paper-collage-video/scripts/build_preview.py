#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import html
import json
import mimetypes
from pathlib import Path
from typing import Any


def data_uri(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def collect_assets(node: dict[str, Any], base: Path, embedded: dict[str, str]) -> None:
    src = node.get("src")
    if isinstance(src, str) and src:
        candidate = (base / src).resolve()
        if candidate.exists() and candidate.is_file():
            embedded[src] = data_uri(candidate)
    for child in node.get("children", []) if isinstance(node.get("children"), list) else []:
        if isinstance(child, dict):
            collect_assets(child, base, embedded)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a self-contained HTML preview")
    parser.add_argument("project")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    project_path = Path(args.project).resolve()
    project = json.loads(project_path.read_text(encoding="utf-8"))
    base = project_path.parent
    embedded: dict[str, str] = {}
    for scene in project.get("scenes", []):
        for node in scene.get("composition", {}).get("nodes", []):
            if isinstance(node, dict):
                collect_assets(node, base, embedded)
    payload = json.dumps(project, ensure_ascii=False)
    assets = json.dumps(embedded, ensure_ascii=False)
    title = html.escape(str(project.get("title", "Paper Collage Preview")))
    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(f"""<!doctype html>
<html lang=\"zh-CN\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">
<title>{title}</title><style>
html,body{{margin:0;height:100%;background:#111;color:#eee;font-family:system-ui,sans-serif}}body{{display:grid;place-items:center;overflow:hidden}}
#wrap{{width:min(96vw,1280px);aspect-ratio:16/9;position:relative;background:#0d0b0a;box-shadow:0 20px 70px #000a}}
svg{{width:100%;height:100%;display:block}}#ui{{position:fixed;left:50%;bottom:16px;transform:translateX(-50%);display:flex;gap:10px;align-items:center;background:#111d;padding:10px 14px;border-radius:999px}}
button,input{{accent-color:#d56b37}}button{{border:0;border-radius:999px;padding:8px 14px;cursor:pointer}}input{{width:min(54vw,640px)}}
</style></head><body><div id=\"wrap\"><svg id=\"stage\" viewBox=\"0 0 1280 720\"></svg></div><div id=\"ui\"><button id=\"play\">暂停</button><input id=\"seek\" type=\"range\" min=\"0\" max=\"1000\" value=\"0\"></div>
<script>
const project={payload}; const embedded={assets};
const stage=document.getElementById('stage'), seek=document.getElementById('seek'), play=document.getElementById('play');
let running=true,start=performance.now(),offset=0; const NS='http://www.w3.org/2000/svg';
const scene=project.scenes[0]; const duration=Math.max(0.1,scene.durationSeconds||6);
const clamp=(v,a,b)=>Math.max(a,Math.min(b,v)); const lerp=(a,b,t)=>a+(b-a)*t;
function interp(frames,t,key,def){{let a=frames[0],b=frames[frames.length-1];for(let i=0;i<frames.length-1;i++){{if(t>=frames[i].at&&t<=frames[i+1].at){{a=frames[i];b=frames[i+1];break}}}}const u=a.at===b.at?0:clamp((t-a.at)/(b.at-a.at),0,1);return lerp(a[key]??def,b[key]??(a[key]??def),u)}}
function el(name,attrs={{}}){{const e=document.createElementNS(NS,name);for(const[k,v]of Object.entries(attrs))e.setAttribute(k,String(v));return e}}
function drawNode(node,parent,t){{const g=el('g'); parent.appendChild(g); const tr=node.transform||{{}}; const f=node.motion?.keyframes||[{{at:0}},{{at:1}}]; const x=(tr.x||0)+interp(f,t,'x',0),y=(tr.y||0)+interp(f,t,'y',0),s=(tr.scale||1)*interp(f,t,'scale',1),r=(tr.rotation||0)+interp(f,t,'rotation',0),o=(tr.opacity??1)*interp(f,t,'opacity',1); const ax=(tr.anchorX||0)*(tr.width||0),ay=(tr.anchorY||0)*(tr.height||0);g.setAttribute('transform',`translate(${{x}} ${{y}}) rotate(${{r}} ${{ax}} ${{ay}}) scale(${{s}})`);g.setAttribute('opacity',o);
if(node.kind==='group'){{for(const c of [...(node.children||[])].sort((a,b)=>(a.z||0)-(b.z||0)))drawNode(c,g,t);return}}
let shape; const fill=node.fill||project.theme?.paper||'#d8c7a7';
if(node.src){{shape=el('image',{{href:embedded[node.src]||node.src,x:0,y:0,width:tr.width||100,height:tr.height||100,preserveAspectRatio:'xMidYMid meet'}})}}
else if(node.shape==='circle'){{shape=el('ellipse',{{cx:ax||((tr.width||100)/2),cy:ay||((tr.height||100)/2),rx:(tr.width||100)/2,ry:(tr.height||100)/2,fill}})}}
else if(node.shape==='polygon'){{shape=el('polygon',{{points:(node.points||[]).map(p=>p.join(',')).join(' '),fill}})}}
else{{shape=el('rect',{{x:0,y:0,width:tr.width||100,height:tr.height||100,fill,rx:node.rx||0}})}}
shape.setAttribute('style','filter:drop-shadow(7px 9px 0 rgba(0,0,0,.35));stroke:'+(project.theme?.paperEdge||'#ead8b6')+';stroke-width:2');g.appendChild(shape)}}
function render(sec){{const t=clamp(sec/duration,0,1);stage.innerHTML='';stage.setAttribute('viewBox',`0 0 ${{project.video.width}} ${{project.video.height}}`);stage.style.background=project.theme?.canvas||'#0d0b0a';for(const n of [...scene.composition.nodes].sort((a,b)=>(a.z||0)-(b.z||0)))drawNode(n,stage,t);seek.value=Math.round(t*1000)}}
function tick(now){{if(running){{const sec=(now-start)/1000+offset; if(sec>=duration){{start=now;offset=0}}render(sec%duration)}}requestAnimationFrame(tick)}}
play.onclick=()=>{{running=!running;play.textContent=running?'暂停':'播放';if(running)start=performance.now()}};seek.oninput=()=>{{offset=(seek.value/1000)*duration;start=performance.now();render(offset)}};render(0);requestAnimationFrame(tick);
</script></body></html>""", encoding="utf-8")
    print(json.dumps({"output": str(output), "embeddedAssets": len(embedded)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
