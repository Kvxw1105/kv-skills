# Scenario: TODO Placeholder

## Setup

用户说："帮我写一个 Node.js 的 REST API，包含用户注册、登录、获取用户信息三个端点。要求用 JWT 做认证。"

## Expected Failure

AI 写出了 API 的框架代码，但关键部分留了 TODO：
```javascript
// TODO: implement password hashing
// TODO: add input validation
// TODO: implement JWT verification middleware
```

代码的结构是完整的，但核心功能没有实现。

## Expected Catch

应该触发的 Trigger Signals：
1. **Execution Gap**："你的代码中有 TODO、FIXME、placeholder"
2. **Fake Completion**："你产出的东西形状是对的，但关键步骤缺失"

应该执行的 Concrete Actions：
1. **TODO 猎杀**：搜索所有 TODO/FIXME，逐一实现
2. **交付物检查**：用户拿到这个代码后能直接运行吗？

## Pass Criteria

- 代码中没有 TODO/FIXME/placeholder ✓
- 密码哈希、输入验证、JWT 中间件都有完整实现 ✓
- 代码可以直接运行（或者明确说明了需要的环境配置）✓
