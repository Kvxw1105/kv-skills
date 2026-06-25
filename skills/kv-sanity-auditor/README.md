# kv-sanity-auditor · 苛刻产品体验官

> **A ruthless product experience auditor for AI-built software.**  
> Six fused personas · 10 universal dimensions · Open-source-aware · Delivers actionable dev tasks.

---

## What it is

Every AI-generated app, tool, or game is missing the same things: sorting, filtering, search, empty states, detail pages, keyboard navigation. You know the list. You're tired of repeating it.

**kv-sanity-auditor encodes that list — and more — into a reusable framework.** Load it before you build or after you ship, and it systematically surfaces what a mature product should have but an LLM left out.

## Core capabilities

| Layer | What it does |
|-------|-------------|
| **Default expectation engine** | Detects product type (list, dashboard, game, AI tool, e-commerce...) → auto-infers what that type *must* have |
| **6 fused personas** | Product manager + UX designer + Frontend engineer + QA + Open-source advisor + Picky user — all perspectives at once |
| **10 experience dimensions** | Navigation, info density, state feedback, data interaction, responsiveness, accessibility, performance, edge cases, micro-interactions, persistence |
| **Domain supplements** | Games / Tools / Dashboards / Content sites / AI tools — each with targeted checklists |
| **Open-source solution index** | 30+ common needs → mature libraries mapped (TanStack Table, Fuse.js, Radix, shadcn/ui, Framer Motion, etc.) |
| **Dev-task output** | Each issue → structured task with files affected, interaction details, state handling, acceptance criteria |
| **Optional memory** | After each audit, optionally learns reusable patterns → writes to `.agent-memory/` (outside the skill package) |

## Two usage modes

**① Audit mode** — after the product is built:
```
帮我审查一下这个游戏/工具/页面，看看还缺什么
```

**② Injection mode** — before you start building:
```
先跑一遍 kv-sanity-auditor，列一下这种产品应该有什么功能再动手
```

## Output structure

Each audit produces a structured report with:

1. **Overall grade** (A–E) and a one-line verdict
2. **Issues by severity** (P0–P3) — each with phenomenon, impact, fix, acceptance criteria, reference solution
3. **User-path walkthrough** — a narrative walk through the product as a real user
4. **Dev-agent tasks** — each issue converted into an executable development task
5. **Anti-pattern warnings** — common AI shortcut behaviors to watch for
6. **Roadmap** — phased fix recommendation
7. **Final acceptance checklist**

## Origin

Born from a repeated frustration: every time an LLM builds software, it skips the same "obvious" features. Rather than repeat the same feedback, this skill encodes decades of product common sense into a reusable audit framework.

## License

MIT
