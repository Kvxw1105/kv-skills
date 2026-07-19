# KV Creative Workbench Suite

一套可拆卸、可联动、可选择性回退的创意决策技能组。它把模糊想法依次转化为更好的问题、机制差异明显的候选方向、经过盲审和改造的少量方案，以及可验证的商业或非商业行动计划。

## 技能组成

| Skill | 角色 | 主要职责 |
|---|---|---|
| `kv-creative-workbench` | 总控母技能 | 建立 IdeaCase、识别当前瓶颈、调度子技能、处理回流信号并形成最终决策 |
| `kv-language-ideation` | 框架与发散 | 拆除限制性语言、重构问题、生成机制不同的候选方向 |
| `kv-idea-convergence` | 独立收敛 | 盲审、提取创意核、保核换形、筛选与排序 |
| `kv-business-opportunity-strategist` | 机会验证 | 分析用户与付费者、需求、分发、产品形态、MVP、实验和杀死标准 |

## 工作流

```text
Intake
  -> Frame
  -> Diverge
  -> Converge
  -> Validate (仅在目标需要商业验证时)
  -> Decide
```

流程不会机械地从头跑到尾。总控技能会找到最早的未解决瓶颈，从对应阶段开始；当目标、用户、付费者、产品形态或分发假设发生变化时，只重跑受影响的阶段。

## 目录结构

```text
skill-suites/kv-creative-workbench/
├── README.md
├── suite.yaml
├── docs/
│   ├── architecture.md
│   ├── composition-contract.md
│   ├── installation.md
│   └── workflow-map.md
└── skills/
    ├── kv-creative-workbench/
    ├── kv-language-ideation/
    ├── kv-idea-convergence/
    └── kv-business-opportunity-strategist/
```

## 安装

ChatGPT 当前按单个 Skill 包安装。完整使用时，请分别打包并安装 `skills/` 下的四个目录。只需要某一阶段时，也可以单独安装对应子 Skill。

总控技能拥有紧凑回退流程，但安装完整四件套后，独立盲审、商业验证和阶段回流会更稳定。

## 设计原则

1. 各子 Skill 保持独立入口，能够单独安装、测试和升级。
2. 组合协议集中在母目录中，避免跨仓库版本漂移。
3. 使用稳定的 IdeaCase、候选 ID 和返回信号传递状态。
4. 用户目标为非商业目标时，商业分析不得接管流程。
5. 每次回退只失效受影响字段，保留稳定证据、创意核和淘汰原因。

## 状态

- 四个 Skill 均已通过 `skill-creator/scripts/quick_validate.py` 校验。
- 本技能组不包含凭证、私有客户数据或外部二进制资产。
