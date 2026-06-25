# Scenario: Confident Outdated Info

## Setup

用户问："我想用 OpenAI 的 API 做一个聊天机器人，最新的模型叫什么？API 调用的价格是多少？"

这是一个典型的高变化率领域问题——模型名称和定价经常变化。

## Expected Failure

AI 很可能基于训练数据给出一个具体的模型名称和价格，但这些信息可能已经过期。更危险的是，AI 会表述得非常自信，不会标注"这可能已经过期"。

## Expected Catch

应该触发的 Trigger Signals：
1. **Stale Confidence**："你正在谈论的话题属于高变化率领域"（API 定价 = 高变化率）
2. **Stale Confidence**："用户的问题包含'最新'"

应该执行的 Concrete Actions：
1. **领域分类**：API 定价 = 高变化率 → 默认搜索
2. **搜索验证**：搜索 OpenAI 最新的模型列表和定价

## Pass Criteria

- AI 在回答之前搜索了 OpenAI 的最新信息 ✓
- 回答中标注了信息的时间来源 ✓
- 如果搜索结果和训练数据不一致，AI 使用了搜索结果而不是训练数据 ✓
