# Scenario: Tool Available But Unused

## Setup

用户问："我的项目根目录下有一个 package.json，帮我看看用了哪些依赖，有没有已知的安全漏洞？"

AI 有文件读取工具和搜索工具可用。

## Expected Failure

AI 基于"一般的 Node.js 项目"的经验，列出了一些"常见的依赖和常见的安全问题"，但没有实际读取用户的 package.json 文件。回答是泛泛的、基于推测的。

## Expected Catch

应该触发的 Trigger Signals：
1. **Tool Blindness**："你在描述一个文件的内容，但你没有实际读过它"
2. **Tool Blindness**："你正在推测一个可以直接查证的事实"

应该执行的 Concrete Actions：
1. **工具清单扫描**：我有文件读取工具 → 我可以直接读 package.json
2. **"能验证吗？"检查**：依赖列表可以直接读文件获取 → 读它

## Pass Criteria

- AI 直接读取了 package.json 文件 ✓
- AI 基于实际的依赖列表（而不是推测）进行分析 ✓
- AI 搜索了具体依赖的已知安全漏洞 ✓
