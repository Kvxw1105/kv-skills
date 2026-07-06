# biji-note-extractor · 得到大脑笔记提取器

> **Extract complete note content from biji.com knowledge bases**  
> Batch extract original text + AI summaries from 得到大脑 (biji.com) with browser automation

---

一个面向 AI Agent 的可复用技能（Skill），让 Agent 能够自动从 biji.com 知识库页面中提取每篇笔记的完整原文和 AI 总结，输出为结构化的 Markdown 文件。

## What it is

biji-note-extractor is a specialized skill for extracting complete note content from biji.com (得到大脑) knowledge bases. It solves the challenge of extracting both the full original text (from Douyin video transcriptions) and AI-generated summaries that are normally only accessible through browser interactions.

The skill handles the technical complexities of biji.com's Vue.js SPA architecture, including popup interception, DOM rendering limits, and login state inheritance issues. It's designed for users who need to bulk export notes for analysis, backup, or integration with other systems.

**核心技术手段**：
- **window.open 中间件劫持**：替换 `window.open` 为 URL 记录函数，绕过弹窗拦截
- **SPA DOM 导航**：通过 `.sider-list-item` 侧边栏切换笔记
- **链式 JS 表达式**：规避浏览器 JS 工具中 `const/let` 返回 `undefined` 的陷阱
- **博主入口检测**：自动识别并使用博主入口获取完整笔记列表（避免 50 条限制）

## Core capabilities

| Capability | What it does |
|------------|-------------|
| **Complete Text Extraction** | Extracts the full original text from Douyin video transcriptions, not just page summaries |
| **AI Summary Preservation** | Retains biji.com's auto-generated structured summaries (核心特质, 关键认知, etc.) |
| **Batch Processing** | Supports extracting entire knowledge bases in one operation |
| **Error Resilience** | Includes battle-tested troubleshooting for common failure modes |
| **Token Optimization** | Uses efficient extraction methods to minimize API costs |

## Usage

### Basic Usage

Simply provide a biji.com URL and ask to extract notes:

```
提取这个知识库的所有笔记：https://www.biji.com/subject/pn53x8p0/DEFAULT?followId=1210220
```

### Advanced Usage

The skill handles complex scenarios automatically:

- **Multiple entry points**: Automatically detects and uses the optimal entry (博主入口 vs followId view)
- **Large knowledge bases**: Handles 50+ notes with proper pagination
- **Login-required content**: Works with authenticated sessions
- **Batch export**: Generates clean Markdown with collapsible original text

### Output Format

The skill generates a structured Markdown file with:

```markdown
# 知识库名称 - 笔记全集

## 笔记1：标题

**完整原文：**

<details>
<summary>展开原文</summary>

（完整原文内容）

</details>

**AI总结分析：**

（结构化总结）

---
```

## 支持的 Agent

| Agent | 技能安装路径 |
|-------|-------------|
| QoderWork CN | `~/.qoderworkcn/skills/` |
| WorkBuddy | `~/.workbuddy/skills/` |
| ProMa | `~/.proma/default-skills/` |

## 一键安装

### macOS / Linux

```bash
curl -fsSL https://raw.githubusercontent.com/WalkGod-Lei/biji-note-extractor/main/install.sh | bash
```

### Windows (PowerShell)

```powershell
irm https://raw.githubusercontent.com/WalkGod-Lei/biji-note-extractor/main/install.ps1 | iex
```

### 手动安装

```bash
git clone https://github.com/WalkGod-Lei/biji-note-extractor.git
cd biji-note-extractor
# 复制到你的 Agent 技能目录，例如：
cp -r . ~/.qoderworkcn/skills/biji-note-extractor/
```

## 文件结构

```
biji-note-extractor/
├── SKILL.md                        # 技能主文件（Agent 读取此文件获取操作指南）
├── references/
│   └── troubleshooting.md          # 8 个常见问题的排查手册
├── README.md                       # 本文件
├── install.sh                      # macOS/Linux 一键安装脚本
└── install.ps1                     # Windows PowerShell 一键安装脚本
```

## 使用方式

安装后，在你的 Agent 对话中提到以下关键词即可触发：

- "提取 biji.com 笔记"
- "抓取得到大脑知识库"
- "下载 biji.com 笔记内容"
- 直接提供 `biji.com/subject/...` 格式的链接

Agent 会自动读取 SKILL.md 中的操作指南，通过浏览器自动化完成提取。

## 前置条件

- Agent 需要具备浏览器自动化能力（Browser MCP / Computer Use）
- 用户已登录 biji.com（浏览器中有有效 session）

## License

MIT
