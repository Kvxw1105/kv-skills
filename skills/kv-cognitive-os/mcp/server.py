"""
kv-cognitive-os MCP server
常驻技能编排服务 - FastMCP stdio

工具：
  get_skill(name)        -> 加载技能完整 SKILL.md
  list_skills(category)  -> 按类筛选索引
  suggest_skills(task)   -> 根据任务描述推荐组合链
  get_reference(skill, ref) -> 加载技能参考文档

数据源：C:\\Users\\kvxkf\\skill-os\\registry.json + 本地技能目录
"""

import json
from pathlib import Path
from typing import Any

from fastmcp import FastMCP

SKILL_OS_ROOT = Path.home() / "skill-os"
REGISTRY_PATH = SKILL_OS_ROOT / "registry.json"

mcp = FastMCP(
    "kv-cognitive-os",
    instructions=(
        "心吾技能体系编排服务。"
        "提供技能索引查询、全文加载和组合推荐。"
        "配合 kv-cognitive-os SKILL.md（常驻注入层）使用。"
    ),
)


def _load_registry() -> dict:
    if not REGISTRY_PATH.exists():
        return {}
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _resolve_skill_path(source: str) -> Path:
    return SKILL_OS_ROOT / source


CATEGORY_MAP = {
    "认知": ["kv-insight-engine", "kv-clarity-mirror", "kv-sanity-auditor",
             "kv-high-pressure-awakening", "elon-musk-cognitive-lens",
             "ding-yuanying-cognitive-lens", "kv-goal-loop"],
    "内容": ["xw-content-engine", "xw-xinwu-voice", "xuanqi-copy-engine",
             "xw-functional-content-forge", "humor-writer",
             "kv-cinematic-intelligence-narrative"],
    "视觉": ["xuanlight-aesthetic", "kv-xuanlight-aesthetic", "beyond-answer-visual-system",
             "huashu-design-cn", "frontend-slides", "make-paper-collage-video"],
    "漫画": ["ai-comic-style", "kv-ai-comic-style", "xw-programmatic-comic-drama",
             "xw-xuanqi-universe"],
    "前端": ["kv-frontend-upgrade-director", "interactive-web-experience-engineer",
             "one-click-web-preview", "playful-h5-game-designer",
             "kv-playful-h5-game-designer"],
    "垂直": ["legal-docx-delivery", "gaokao-volunteer-strategist",
             "shanghai-primary-math-generator", "interactive-ip-profit-director",
             "dbs-unified"],
    "工具": ["kv-biji-note-extractor", "biji-note-extractor", "xw-ai-dev-git-workflow",
             "xw-cloudflare-kimi-bridge-ops", "xw-abec-entitlement-center-ops",
             "kv-goal-loop-chatgpt"],
    "元": ["xw-skill-creator", "xw-skill-source-manager", "xw-skill-release-manager",
           "xw-universal-skill-orchestrator", "xw-profile"],
}

COMPOSITION_PATTERNS = {
    "长文创作": {
        "keywords": ["长文", "公众号", "文章", "写作", "推文", "博客", "深度文", "付费文"],
        "chain": ["kv-insight-engine", "xw-content-engine", "xw-xinwu-voice", "kv-clarity-mirror"],
        "note": "先找真问题，再写，再校准人设，最后自检",
    },
    "短文案": {
        "keywords": ["文案", "标题", "hook", "短视频", "slogan", "金句", "小红书"],
        "chain": ["xuanqi-copy-engine", "xw-xinwu-voice"],
        "note": "文案锻造 + 人设校准",
    },
    "视觉设计": {
        "keywords": ["海报", "视觉", "设计", "封面", "风格", "美学", "配色", "排版"],
        "chain": ["xuanlight-aesthetic", "beyond-answer-visual-system", "frontend-slides"],
        "note": "风格定调 -> 视觉系统 -> 落地",
    },
    "产品开发": {
        "keywords": ["网页", "H5", "前端", "页面", "交互", "组件", "游戏", "小程序"],
        "chain": ["kv-frontend-upgrade-director", "interactive-web-experience-engineer", "one-click-web-preview"],
        "note": "升级方向 -> 工程实现 -> 预览验证",
    },
    "产品审查": {
        "keywords": ["审查", "体验", "验收", "测试", "质量", "检查", "audit"],
        "chain": ["kv-sanity-auditor", "kv-clarity-mirror"],
        "note": "六视角审查 + 盲区扫描",
    },
    "战略思考": {
        "keywords": ["战略", "商业", "变现", "IP", "定价", "模式", "规划", "决策"],
        "chain": ["interactive-ip-profit-director", "dbs-unified", "kv-insight-engine"],
        "note": "变现策略 + 商业思维 + 深度分析",
    },
    "漫画生产": {
        "keywords": ["漫画", "分镜", "连载", "角色", "三反骨", "白卷羊", "玄奇"],
        "chain": ["ai-comic-style", "xw-programmatic-comic-drama", "xw-xuanqi-universe"],
        "note": "风格 -> 分镜 -> 世界观一致性",
    },
    "自主执行": {
        "keywords": ["自动", "循环", "目标", "自主", "不用管", "跑完", "端到端"],
        "chain": ["kv-goal-loop"],
        "note": "启动自主循环，计划->执行->验证->评估->迭代",
    },
}


@mcp.tool()
def list_skills(category: str = "") -> dict[str, Any]:
    """列出可用技能。可选按类筛选：认知/内容/视觉/漫画/前端/垂直/工具/元"""
    registry = _load_registry()
    skills = registry.get("skills", {})

    results = []
    for name, meta in skills.items():
        if category:
            cat_skills = CATEGORY_MAP.get(category, [])
            if name not in cat_skills:
                continue
        results.append({
            "name": name,
            "visibility": meta.get("visibility", "unknown"),
            "source": meta.get("source", ""),
        })

    return {
        "total": len(results),
        "filter": category or "all",
        "skills": results,
    }


@mcp.tool()
def get_skill(name: str) -> dict[str, Any]:
    """加载指定技能的完整 SKILL.md 内容。传入技能名（如 xw-content-engine）。"""
    registry = _load_registry()
    skills = registry.get("skills", {})

    meta = skills.get(name)
    if not meta:
        candidates = [k for k in skills if name in k or k in name]
        return {
            "error": f"skill not found: {name}",
            "candidates": candidates[:5],
            "hint": "use list_skills() to see all",
        }

    source = meta.get("source", "")
    skill_md_path = _resolve_skill_path(source) / "SKILL.md"

    if not skill_md_path.exists():
        return {
            "error": f"SKILL.md missing: {skill_md_path}",
            "name": name,
            "source": source,
        }

    content = skill_md_path.read_text(encoding="utf-8")

    refs_dir = _resolve_skill_path(source) / "references"
    references = []
    if refs_dir.exists():
        references = [f.name for f in refs_dir.iterdir() if f.suffix == ".md"]

    return {
        "name": name,
        "path": str(skill_md_path),
        "content": content,
        "references": references,
        "visibility": meta.get("visibility", "unknown"),
    }


@mcp.tool()
def suggest_skills(task: str) -> dict[str, Any]:
    """根据任务描述推荐技能组合链。传入自然语言任务描述。"""
    task_lower = task.lower()

    matches = []
    for pattern_name, pattern in COMPOSITION_PATTERNS.items():
        score = sum(1 for kw in pattern["keywords"] if kw in task_lower)
        if score > 0:
            matches.append((score, pattern_name, pattern))

    matches.sort(key=lambda x: -x[0])

    if not matches:
        return {
            "task": task,
            "matches": [],
            "fallback": "no exact match. suggest kv-insight-engine to clarify first.",
        }

    registry = _load_registry()
    results = []
    for score, pname, pattern in matches[:3]:
        chain_detail = []
        for skill_name in pattern["chain"]:
            skill_meta = registry.get("skills", {}).get(skill_name, {})
            skill_md = _resolve_skill_path(skill_meta.get("source", "")) / "SKILL.md"
            chain_detail.append({
                "skill": skill_name,
                "available": skill_md.exists(),
            })
        results.append({
            "pattern": pname,
            "confidence": "high" if score >= 2 else "medium",
            "chain": chain_detail,
            "note": pattern["note"],
        })

    return {"task": task, "recommendations": results}


@mcp.tool()
def get_reference(skill_name: str, ref_name: str) -> dict[str, Any]:
    """加载技能的参考文档。如 get_reference("xw-content-engine", "longform-engine.md")"""
    registry = _load_registry()
    meta = registry.get("skills", {}).get(skill_name)
    if not meta:
        return {"error": f"skill not found: {skill_name}"}

    ref_path = _resolve_skill_path(meta.get("source", "")) / "references" / ref_name
    if not ref_path.exists():
        refs_dir = _resolve_skill_path(meta.get("source", "")) / "references"
        available = []
        if refs_dir.exists():
            available = [f.name for f in refs_dir.iterdir() if f.is_file()]
        return {"error": f"reference not found: {ref_name}", "available": available}

    return {
        "skill": skill_name,
        "reference": ref_name,
        "content": ref_path.read_text(encoding="utf-8"),
    }


if __name__ == "__main__":
    mcp.run()
