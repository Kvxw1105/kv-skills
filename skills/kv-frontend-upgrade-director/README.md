# KV Frontend Upgrade Director

一个面向 AI 编程 Agent 的前端体验升级与提示词编译 Skill。

它不是固定风格模板，而是一套从产品诊断、业务保护、视觉系统、语义动效、Three.js 空间化、响应式、浏览器验收到经验回流的控制系统。

## 能做什么

- 审计并升级已有网站、SaaS、AI 工具、工作台、后台和 H5；
- 从真实产品任务推导视觉母题，而不是默认套紫蓝科技风；
- 把业务状态转成有来源和去向的语义动效；
- 决定 DOM、CSS、Canvas、Three.js、Shader 与声音各自职责；
- 为 Codex、Cursor、Claude Code、Windsurf、Trae、Kimi、灵光等编译可执行提示词；
- 用项目记忆与模式候选机制持续积累已验证经验。

## 安装

从 `Kvxw1105/kv-skills` 安装：

```bash
npx skills add Kvxw1105/kv-skills --skill kv-frontend-upgrade-director --agent codex --global --yes --full-depth
```

ChatGPT 可上传本目录打包后的 `skill.zip`。

## 快速使用

```text
使用 KV 前端升级总导演，保护现有 API、路由和业务状态，审计并升级这个项目的用户端和工作台。先做两个 Showcase，再扩散共享组件，最后实际浏览器验收。
```

只编译提示词：

```bash
python scripts/compile_prompt.py --profile existing-project --project "My Product" --out upgrade-prompt.md
```

初始化持久项目记忆：

```bash
python scripts/init_frontend_workspace.py --project-root . --project-name "My Product" --project-type "AI workspace"
```

记录经验候选：

```bash
python scripts/record_pattern.py --project-root . --title "DOM 到 WebGL 的跨媒介接力" --problem "内容切换生硬" --solution "临时 DOM 字符飞入空间并由粒子接力" --evidence "桌面与手机核心路径复测通过" --transfer "AI 创作工具、生成式工作台"
```

## 公开与私人边界

本仓库版本只保存可迁移的公开方法。玄启、VideoForge、个人审美偏好、未公开商业策略和具体私有项目结构，应放在私人扩展 Skill 或项目 `.agent/` 记忆中，不回流到公开母体。
