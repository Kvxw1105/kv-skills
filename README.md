# kv-skills · 心吾技能体系

> **心吾出品的 AI Agent 技能集。**  
> 公开、可用、可安装。每个技能解决一个真实痛点。

---

## 系列一览

| 技能 | 定位 | 核心能力 |
|------|------|---------|
| [**KV Creative Workbench Suite**](skill-suites/kv-creative-workbench/) | 创意决策组合技 | 从问题重构、创意发散、独立收敛到机会验证与决策，支持回流和选择性重跑 |
| [**kv-engineering-reasoning-harness**](skills/kv-engineering-reasoning-harness/) | 工程推理与接力增强器 | 让编码 Agent 核验真实状态、规划任务、控制改动、验证结果并完成跨节点接力 |
| [**kv-insight-engine**](skills/kv-insight-engine/) | 洞察引擎 — 深度思考放大器 | 提纯问题、拉高判断、交付更强方案 |
| [**kv-clarity-mirror**](skills/kv-clarity-mirror/) | 清晰镜 — AI 盲区检查器 | 运行时自检，在交付前捕获最可能翻车的地方 |
| [**kv-sanity-auditor**](skills/kv-sanity-auditor/) | 苛刻产品体验官 | 六视角融合审查 AI 产品的体验完整性 |
| [**kv-ai-comic-style**](skills/kv-ai-comic-style/) | AI三反骨 — 漫画 IP 生产流 | 把 AI / Agent / Workflow / OPC 等概念转成三账号漫画、暗线剧情、视频提示词与图像提示词 |
| [**kv-xuanlight-aesthetic**](skills/kv-xuanlight-aesthetic/) | 玄光美学风格系统 | 将普通视觉需求系统化转译为诗性、神性微光、低清颗粒的玄光视觉语言 |
| [**kv-biji-note-extractor**](skills/kv-biji-note-extractor/) | 得到笔记提取器 | 从知识库批量提取内容并沉淀经验 |
| [**kv-goal-loop**](skills/kv-goal-loop/) | 自主循环执行引擎 | 高层目标 → 计划 → 执行 → 验证 → 评估 → 迭代 |
| [**kv-playful-h5-game-designer**](skills/kv-playful-h5-game-designer/) | 轻趣 H5 游戏设计师 | 移动端轻游戏设计、实现与验收 |

---

## 安装

```bash
npx skillkit add Kvxw1105/kv-skills
```

单独安装工程推理增强器：

```bash
npx skillkit add Kvxw1105/kv-engineering-reasoning-harness
```

ChatGPT 用户也可以直接上传对应目录中的 `skill.zip`。

---

## 工程推理与接力增强器

`kv-engineering-reasoning-harness` 面向 Codex、ChatGPT、Claude Code、Cursor 等编码 Agent。

它解决：

- 项目开始前没有完整侦察，直接写代码；
- Agent 接力时依赖旧总结，导致重复劳动或误改；
- 规划无法验收；
- 调试缺少根因分析；
- 把代码修改、本地验证、commit、push、PR、CI 混成一句“完成”；
- 项目节点结束后无法可靠交接。

核心循环：

```text
核验现状 → 明确目标 → 选择路径 → 最小实现 → 分层验证 → 反方审查 → 状态交接
```

---

## 设计原则

- **具体而非抽象**：每个技能给出可直接执行的检查点，而非泛泛建议。
- **开源生态意识**：发现问题时指出成熟方案，不重复造轮子。
- **组合而不耦死**：每个 Skill 独立安装，同时支持体系组合。
