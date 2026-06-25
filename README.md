# kv-skills · 心吾技能体系

> **心吾出品的 AI Agent 技能集。**  
> 公开、可用、可安装。每个技能解决一个真实痛点。

---

## 系列一览

| 技能 | 定位 | 核心能力 |
|------|------|---------|
| [**kv-insight-engine**](skills/kv-insight-engine/) | 洞察引擎 — 深度思考放大器 | 提纯问题、拉高判断、交付更强方案 |
| [**kv-clarity-mirror**](skills/kv-clarity-mirror/) | 清晰镜 — AI 盲区检查器 | 运行时自检，在交付前捕获最可能翻车的地方 |
| [**kv-sanity-auditor**](skills/kv-sanity-auditor/) | 苛刻产品体验官 | 六视角融合审查 AI 产品的体验完整性 |

---

## 安装

所有技能支持以下方式安装：

```bash
# 安装全部
npx skillkit add Kvxw1105/kv-skills

# 或安装单个
npx skillkit add Kvxw1105/kv-insight-engine
npx skillkit add Kvxw1105/kv-clarity-mirror
npx skillkit add Kvxw1105/kv-sanity-auditor
```

或用 `skills` CLI：

```bash
npx skills add Kvxw1105/kv-sanity-auditor
```

---

## 体系关系

```
           kv-insight-engine           kv-clarity-mirror
          （能力放大）                  （盲区检查）
                  \                      /
                   \                    /
                    v                  v
                    kv-sanity-auditor
                  （产品体验验收官）

           kv-skill-creator（私人元技能，不在此仓库）
          （创建新技能的心吾版生产工具）
```

- **insight-engine** 帮你把答案做得更深、更强
- **clarity-mirror** 帮你交付前检查盲区
- **sanity-auditor** 帮你验收 AI 产出的体验完整性

三者配合使用：**想深 → 查漏 → 验收质量**。

---

## 设计原则

- **具体而非抽象**：每个技能给出可直接执行的检查点，而非泛泛建议
- **开源生态意识**：发现问题时指出社区已有方案，不重复造轮子
- **交付导向**：问题附带方案，方案附带验收标准
- **质量一致**：共用的 README 结构、命名规范、触发词策略

---

## 作者

**心吾** — AI Agent 技能设计师。  
追求让 Agent 的输出不只在技术上正确，在使用上完整。

---

## License

MIT
