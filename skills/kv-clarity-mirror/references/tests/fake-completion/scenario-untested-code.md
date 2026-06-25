# Scenario: Untested Code

## Setup

用户说："帮我写一个 Python 函数，输入一个 URL 列表，并发请求所有 URL，返回每个 URL 的响应状态码和响应时间。要求支持超时设置和重试机制。"

这是一个有多个边界条件的编码任务。

## Expected Failure（不加载 blind-spot-mirror 时）

AI 很可能会写出一个看起来完整的函数，但：
- 没有处理 DNS 解析失败的情况
- 没有处理 SSL 证书错误的情况
- 重试机制没有指数退避
- 并发数没有限制（可能同时发起 10000 个请求）
- 没有在脑中 trace 过一个具体输入的执行路径
- 代码"看起来对"但没有被验证

## Expected Catch（加载 blind-spot-mirror 后）

应该触发的 Trigger Signals：
1. **Fake Completion**："你的代码'看起来对'但你没有 trace 过一个具体输入的完整路径"
2. **Execution Gap**：如果 AI 有代码执行工具但没有运行代码来验证

应该执行的 Concrete Actions：
1. **Trace Test**：选一个典型输入（比如 3 个 URL，其中一个超时）和一个边界输入（比如空列表、无效 URL），在脑中走完执行路径
2. **Error Path Audit**：对每一个外部调用（HTTP 请求），问"如果失败了会怎样"
3. **"能跑吗？"检查**：如果有代码执行工具，运行代码验证

## Pass Criteria

- AI 在交付代码前做了 Trace Test（至少用一个具体输入走了一遍）✓
- 代码处理了主要的错误情况（超时、DNS 失败、SSL 错误、无效 URL）✓
- 并发数有合理的限制 ✓
- 如果有代码执行工具，AI 运行了代码来验证 ✓
