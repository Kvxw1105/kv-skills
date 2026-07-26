# kv-cognitive-os 安装指南

## 各 Agent 安装方式

### QoderWork

SKILL.md 安装：
```
mklink /J "%USERPROFILE%\.qoderworkcn\skills\kv-cognitive-os" "C:\Users\kvxkf\skill-os\public\kv-skills\skills\kv-cognitive-os"
```

MCP 注册（在 QoderWork 设置 → 连接器 → 自定义 MCP）：
```json
{
  "name": "kv-cognitive-os",
  "config": {
    "command": "python",
    "args": ["C:\\Users\\kvxkf\\skill-os\\public\\kv-skills\\skills\\kv-cognitive-os\\mcp\\server.py"]
  }
}
```

### Codex CLI

SKILL.md 安装（追加到全局指令）：
```
type "C:\Users\kvxkf\skill-os\public\kv-skills\skills\kv-cognitive-os\SKILL.md" >> "%USERPROFILE%\.codex\instructions.md"
```

MCP 注册（~/.codex/config.toml）：
```toml
[mcp_servers.kv-cognitive-os]
command = "python"
args = ["C:\\Users\\kvxkf\\skill-os\\public\\kv-skills\\skills\\kv-cognitive-os\\mcp\\server.py"]
```

### Claude Code

SKILL.md 安装（追加到全局 CLAUDE.md）：
```
type "C:\Users\kvxkf\skill-os\public\kv-skills\skills\kv-cognitive-os\SKILL.md" >> "%USERPROFILE%\.claude\CLAUDE.md"
```

MCP 注册（~/.claude/claude_desktop_config.json 或 settings）：
```json
{
  "mcpServers": {
    "kv-cognitive-os": {
      "command": "python",
      "args": ["C:\\Users\\kvxkf\\skill-os\\public\\kv-skills\\skills\\kv-cognitive-os\\mcp\\server.py"]
    }
  }
}
```

### Proma

SKILL.md 安装：
```
mklink /J "%USERPROFILE%\.proma\default-skills\kv-cognitive-os" "C:\Users\kvxkf\skill-os\public\kv-skills\skills\kv-cognitive-os"
```

MCP：Proma 使用 claude-agent-sdk，MCP 配置方式取决于 Proma 的 settings.json 中 mcpServers 字段。

### Cursor / Windsurf / Trae

SKILL.md 安装（项目级）：
将 SKILL.md 内容追加到项目根目录的 .cursorrules 或 AGENTS.md。

MCP：在各 Agent 的 MCP 配置中添加 stdio server，command 和 args 同上。

## 验证

安装后在任意 Agent 中测试：
1. 问一个需要深度思考的问题 → 观察是否触发"重构"行为
2. 说"帮我写一篇公众号" → 观察是否主动提及技能链
3. 调用 list_skills() → 应返回 41 个技能
4. 调用 get_skill("kv-insight-engine") → 应返回完整 SKILL.md 内容

## 卸载

删除 junction / 移除 instructions 中追加的内容 / 移除 MCP 配置即可。
A 层和 B 层完全解耦，移除任一部分不影响另一部分。
