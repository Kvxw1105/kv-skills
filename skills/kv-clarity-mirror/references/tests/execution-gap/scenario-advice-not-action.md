# Scenario: Advice Not Action

## Setup

用户说："帮我把桌面上的 report.csv 文件中的销售数据按月份汇总，生成一个新的 Excel 文件。"

AI 有文件读写工具和 Excel 工具可用。

## Expected Failure

AI 很可能会回答："你可以按照以下步骤操作：1. 读取 CSV 文件 2. 用 pandas 按月份分组 3. 计算汇总 4. 导出为 Excel"——给了一份操作指南，而不是直接做。

## Expected Catch

应该触发的 Trigger Signals：
1. **Execution Gap**："你有工具可以用，但你选择了描述而不是动手"
2. **Execution Gap**："你的输出是一份'方案'而不是一个'结果'"

应该执行的 Concrete Actions：
1. **工具扫描**：我有文件读写工具和 Excel 工具 → 我可以直接做这件事
2. **动词审计**：如果输出中出现"你可以"、"建议你" → 切换为直接执行

## Pass Criteria

- AI 直接读取了 CSV 文件 ✓
- AI 直接生成了汇总后的 Excel 文件 ✓
- AI 交付的是一个可用的文件，而不是一份操作指南 ✓
