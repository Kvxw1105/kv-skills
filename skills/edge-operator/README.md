# Edge Operator · 商业行动引擎

**A portable agent skill for finding real demand, pricing outcomes, designing offers, coordinating agents and actually validating business results.**

[中文快速开始](QUICKSTART.md) · [完整提示词](prompts/MASTER_PROMPT.txt) · [思维原子](references/mind-atoms.md) · [角色组合](references/archetype-mixer.md) · [权限配置](references/permission-charter.md) · [MIT License](LICENSE)

> **当前版本：v1.2.0**。这是提示词、知识库、协议和轻量校验脚本组成的 Skill，不是已获得社交账号控制权或支付权限的自治 SaaS。成功交易、已安装代理、API 调用和实际发布必须分别验收。

## Why

Most agents can brainstorm. Fewer reliably trace money from a real buyer to a deliverable, compare costs, choose a strategy, and execute authorized work. Edge Operator turns 96 thinking atoms, 64 role archetypes and 16 role combinations into repeatable **observe → assess → produce → validate → learn** behavior.

- **Marketplace first**: who already pays, what they buy, who controls distribution, what remains after refunds and costs.
- **Hacker-style recombination**: combine existing tools, APIs, manual operations and public research rather than building everything from scratch.
- **Mechanism literacy**: understand unconventional/gray markets and manipulation mechanisms analytically, find legitimate substitutes without pretending third-party harm is profit.
- **Agent coordination**: cloud research, local building, mobile operations, distribution/content and independent verification via explicit handoffs.
- **Distinct public voice**: evidence-grounded, opinionated, human content instead of fictitious credentials, inflated claims or generic AI posts.

## Directory map

| Path | Purpose |
| --- | --- |
| [`SKILL.md`](SKILL.md) | Primary Skill entrypoint and routing |
| [`references/`](references/) | Atomic reasoning library, archetype combinations, playbooks, evaluations, permissions |
| [`prompts/`](prompts/) | Full/short reusable prompts and 6 dedicated agent roles |
| [`templates/`](templates/) | Mission contract, permission charter, opportunity card and handoff |
| [`scripts/`](scripts/) | Dependency-free unit economics, mission validation and test tools |
| [`AGENTS.md`](AGENTS.md) | Agent-facing iteration and repository conventions |
| [`CHANGELOG.md`](CHANGELOG.md) | Release history |

## Evidence-backed upgrade v1.2.0

**21 source records + 16 new research-grade atoms + deterministic truth gate.** Each new atom contains a trigger, observable evidence, decision rule, next action, falsifier and reference IDs. These are additional to the original 96 exploratory atoms. See [research synthesis](references/research-synthesis-2026-11-20.md), [source ledger](references/research-source-ledger.json), [research atoms](references/research-atoms.json) and the [Etsy 2026 policy-shift example](examples/etsy-authenticity-2026/ready-to-use-audit.md).

A verified policy change, a Reddit complaint, and a Fiverr asking price are three different facts; **they do not constitute a paid order**. The packaged `evidence_gate.py` detects several common ways agents misreport payment or execution. It does not validate site authenticity, determine live legal compliance or show improved real-world sales performance.

```bash
python scripts/evidence_gate.py examples/etsy-authenticity-2026/opportunity-evidence.json --json
python -m unittest discover -s scripts -p 'test_*.py' -v
```

## Use it with any agent

**Skills-aware CLI agents:** Clone the public parent repo at <https://github.com/Kvxw1105/kv-skills> and point your agent/skill manager to `skills/edge-operator/SKILL.md`. If using the `skills` CLI, try:

```bash
npx skills add Kvxw1105/kv-skills --skill edge-operator
```

CLI availability and auto-discovery vary by host; the repository source is the authoritative fallback.

**Prompt-only agents (Muse, Grokbot, Mika, NanoMuse, etc.):** Copy `prompts/MASTER_PROMPT.txt` as a long-term instruction where supported, or `prompts/QUICK_START.txt` for constrained contexts. Append one role-specific prompt such as `prompts/CLOUD_SCOUT.txt` or `prompts/PHONE_OPERATOR.txt`. The prompt **does not grant tools, logins, permissions or persistent memory**.

**Multi-agent collaboration:** Give one orchestrator the [`mission.json`](templates/mission.json) and an explicit permission charter; workers report their actual outputs in [`task_handoff.md`](templates/task_handoff.md). See [`agent-coordination.md`](references/agent-coordination.md).

## Test locally

```bash
cd skills/edge-operator
python -m unittest discover -s scripts -p "test_*.py" -v
python scripts/validate_mission.py templates/mission.json
python scripts/unit_economics.py templates/example_deal.json --json
python scripts/package.py --out ./dist/skill.zip
```

Python 3 standard library only. The example deal numbers are **illustrative assumptions, not observed revenue**. Unit tests validate code and task contracts only; they do not prove that the instructions improve LLM performance on any named platform.

## Contribute & iterate

1. Fork / clone the parent repository, edit source in `skills/edge-operator/`, then run the tests.
2. For new thinking atoms, add a distinct trigger, evidence requirement, decision/action and failure mode in `references/mind-atoms.md`; avoid renaming vague rhetoric as a new skill.
3. Add a counterexample or regression case to `references/evaluation.md` or `references/demonstrations.md`.
4. Record observable behavior changes and release notes in [`CHANGELOG.md`](CHANGELOG.md); update prompt/Skill content together when a rule changes.
5. Open a pull request with inputs, produced artifacts, verifiable outcomes and limitations. Never include tokens, cookies, third-party private data or individual account credentials.

**Release rule:** do not increase atom counts or report agent capability gains unless backed by actual text/tests. Continuous integration / auto-deployment is **not** included in v1.0.0; run the commands above before publishing updates.

## Scope and boundaries

The goal is aggressive exploration and evidence-based action within actual authority. This project may analyze persuasion, underground economies and adversarial behavior; it does not advocate fraud, unauthorized access, abuse, fabricated proof, harassment or evasion of legitimate enforcement. Human operators remain accountable for permissions, publication, spending and applicable rules.

Licensed under [MIT](LICENSE). Attribution: Kvxw1105, 2026.


## Judgment calibration and finite atom lifecycle (v1.2.0)

The most important change: a commercial agent should **settle its forecasts and retire weak ideas**, rather than only collecting new evidence and increasing the atom count.

- [Calibration loop](references/calibration-loop.md): outside-view reference class, rival hypotheses, probability/falsifier/settlement, freeze SHA, monthly settlement and Brier accuracy review.
- [Direction card](templates/orientation_card.md) and [draft forecast](templates/forecast_example.json): one concise intervention at orientation, another at settlement; no unnecessary approval cascade.
- [Atom lifecycle](references/atom-lifecycle.md) and [uniform registry](references/atom-registry.json): all original 96 are `heuristic`, all 16 RX atoms `research_linked`, none independently field-validated; controlled trials can motivate patch/split/retire review, not auto-impute commercial revenue.
- [Cross-market discovery](references/cross-market-price-discovery.md) with [synthetic price scan](templates/price_scan_example.json): listed quotes and executable bid/ask economics are different evidence types.
- [Process metrics](scripts/ops_metrics.py): falsification latency, independently adjudicated gate false-block rate and *annotated* luck context, with missing-data denominators.

Run from the Skill directory:

```bash
python scripts/calibration.py validate templates/forecast_example.json
python scripts/calibration.py report templates/forecast_example.json
python scripts/atom_review.py
python scripts/price_scan.py templates/price_scan_example.json
python scripts/ops_metrics.py templates/ops_metrics_example.json
python -m unittest discover -s scripts -p 'test_*.py' -v
python scripts/package.py --out ./dist/skill.zip
```

**Limitations:** Scores currently have zero real settlements, sample prices are synthetic, no Agent-vs-Agent controlled A/B was run, and there is no automatic monthly scheduler or signed forecast registry. Local SHA detects changes in an existing frozen record but cannot independently prove its creation time. Git history can supply a more credible external timestamp when the file is committed before the event resolves.

Calibration sharing between agents: [portable JSON contract](references/interoperability.md). Do not claim drop-in compatibility with another team's schema until an explicit mapping has been tested.

Full rationale and critique-by-critique responses: [external review response](references/review-response-2026-11-20.md).
