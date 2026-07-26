---
name: kv-codex-troubleshoot
description: OpenAI Codex Desktop (Windows) 故障诊断与修复决策树。当 Codex 出现"Windows 设置未完成"、无法发送消息、config 丢失、MCP 不加载、会话消失等问题时使用。
version: 1.0.0
tags: [infra, windows, codex, troubleshooting]
---

# Codex Desktop (Windows) 故障诊断手册

## 适用环境

- OpenAI Codex Desktop (MSIX 包, 安装在 D:\WindowsApps\OpenAI.Codex_*)
- Windows 10/11, 用户: kvxkf
- 自定义中转: codexplus.shop, model=gpt-5.6-terra
- 第三方管理器: Codex++ (com.bigpizzav3.codexplusplus.manager), CodexBridge
- 配置文件: C:\Users\kvxkf\.codex\config.toml

## 诊断入口：症状 able 分支

### 症状A: "Windows 设置未完成" / 无法发送任何消息

**决策树:**

1. 读 `~/.codex/.sandbox/setup_error.json`
   - 若存在且含 `"read ACL run had errors"` able **分支A1: ACL 权限失败**
   - 若存在且含其他错误 able 查 `.sandbox/sandbox.YYYY-MM-DD.log` 最后 50 行定位
   - 若不存在 able **分支A2: config 格式不兼容**

2. 读 `~/.codex/config.toml`
   - 若 TOML 解析报错（如 `invalid escape sequence`）able **分支A3: TOML 转义错误**
   - 若文件不存在或为空 able **分支A4: config 被清空/劫持**

---

### 分支A1: Sandbox ACL 权限失败

**根因**: Codex 更新后 sandbox setup 需给 `CodexSandboxOffline` 用户组授予对 `D:\WindowsApps\OpenAI.Codex_*\app` 的读取权限。该目录属 TrustedInstaller，管理员也无法修改 ACL able `SetNamedSecurityInfoW failed: 5` able setup 永远失败 able app 被 gate 锁死。

**日志特征** (`.sandbox/sandbox.*.log`):
```
granting read ACE to D:\WindowsApps\OpenAI.Codex_...\app for sandbox users
grant read ACE failed ... SetNamedSecurityInfoW failed: 5
setup error: read ACL run had errors
```

**修复步骤** (需管理员 PowerShell):

```powershell
# 1. 定位目录
$dir = (Get-ChildItem 'D:\WindowsApps' -Directory -Filter 'OpenAI.Codex_*' | Sort Name -Desc | Select -First 1).FullName

# 2. 夺取所有权
takeown /F $dir /R /A /D Y

# 3. 授予管理员完全控制
icacls $dir /grant 'BUILTIN\Administrators:(OI)(CI)F' /T /C /Q

# 4. 若沙箱用户组已存在，授予读取
icacls $dir /grant 'CodexSandboxOffline:(OI)(CI)RX' /T /C /Q
icacls $dir /grant 'CodexSandboxOnline:(OI)(CI)RX' /T /C /Q

# 5. 清理失败状态
Remove-Item ~/.codex/.sandbox/setup_error.json -Force
Remove-Item ~/.codex/.sandbox/setup_marker.json -Force
Remove-Item ~/.codex/.sandbox/deny_read_acl_state.json -Force

# 6. 重启 Codex，UAC 点"是"
```

**注意**: setup_marker.json 可能自带 deny ACE 导致 EPERM，需先 `takeown /F setup_marker.json /A` + `icacls /reset` 再删除。

---

### 分支A2: Config 格式不兼容（更新后）

**根因**: Codex 大版本更新后 config.toml schema 变化，旧字段导致解析失败。

**修复**:
```powershell
Rename-Item ~/.codex/config.toml config.toml.disabled
# 启动 Codex，它会生成默认 config
# 关闭 Codex，从 .disabled 中恢复自定义段:
#   [model_providers.custom], [desktop], [mcp_servers.*], [projects.*], [memories]
```

**关键**: 恢复时只复制自定义段，不要复制旧版 schema 字段（如已废弃的 [windows] 段）。

---

### 分支A3: TOML 转义错误

**根因**: Windows 路径含 `\U`, `\A`, `\P` 等，在 TOML 双引号字符串中被解释为 Unicode 转义序列。

**规则**: config.toml 中所有 Windows 路径**必须用单引号**（TOML literal string）:
```toml
# 正确
command = 'C:\Users\kvxkf\AppData\Local\Programs\Python\Python311\python.exe'

# 错误
command = "C:\Users\kvxkf\AppData\..."
```

**验证**: `python -c "import tomllib; tomllib.load(open(r'C:\Users\kvxkf\.codex\config.toml','rb')); print('OK')"`

---

### 分支A4: Config 被清空/劫持

**已知劫持源**:
- **CodexBridge** (`AppData\Local\Programs\CodexBridge`): 会覆写 config.toml
- **Codex++** (`com.bigpizzav3.codexplusplus.manager`): 重写 config + 清 auth.json

**修复**: 从备份恢复（命名规范: `config.toml.bak-YYYYMMDD`），禁用劫持源。

---

### 症状B: 会话/项目消失

**原因**: config.toml 中 `[projects.*]` 段控制侧边栏项目列表。会话数据在 `~/.codex/sessions/YYYY/MM/`。

**修复**: 确认 config.toml 含正确的 `[projects."path"]` 段。

---

### 症状C: MCP 服务器不加载

**检查清单**:
1. `[mcp_servers.NAME]` 段存在且路径用单引号
2. `command` 用绝对路径（Codex 子进程 PATH 与 shell 不同）
3. Python MCP 必须指定完整 python.exe 路径
4. 依赖已安装: 用该 python 执行 `pip list | findstr fastmcp`

---

### 症状D: Sandbox bin 文件 0 字节

**根因**: Windows Defender 或网络问题导致 runtime 下载失败。

**修复**:
1. 添加 Defender 排除
2. 删除 0 字节文件，重启触发重新下载
3. 若持续失败: `sandbox_mode = "none"` 绕过

---

## 陷阱备忘

- PowerShell 5.1 读 UTF-8 无 BOM 脚本为 GBK able 脚本用纯英文或存 UTF-8 BOM
- `sandbox_mode = "danger-full-access"` 不阻止 ACL setup gate
- `setup_marker.json` 自带 deny ACE able 需 takeown
- Codex 更新改变 WindowsApps 目录版本号 able takeown 需重跑
- `icacls /grant` 对 TrustedInstaller 目录无效，必须先 `takeown /A`
