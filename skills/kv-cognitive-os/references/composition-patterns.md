# 组合模式库

本文件是 suggest_skills 工具的知识源，也是人类可读的组合参考。

## 模式列表

### ① 长文创作

触发词：长文、公众号、文章、写作、推文、博客、深度文、付费文

链路：kv-insight-engine → xw-content-engine → xw-xinwu-voice → kv-clarity-mirror

逻辑：先用洞察引擎找到"真正要写什么"，再用内容引擎搭结构出初稿，然后人设校准语气，最后自检交付。

### ② 短文案

触发词：文案、标题、hook、短视频、slogan、金句、小红书

链路：xuanqi-copy-engine → xw-xinwu-voice

逻辑：文案引擎负责结构和冲击力，人设校准负责"像心吾说的"。

### ③ 视觉设计

触发词：海报、视觉、设计、封面、风格、美学、配色、排版

链路：xuanlight-aesthetic → beyond-answer-visual-system → frontend-slides

逻辑：玄光美学定调性，视觉系统做展开，最终用前端落地成可见物。

### ④ 产品开发

触发词：网页、H5、前端、页面、交互、组件、游戏、小程序

链路：kv-frontend-upgrade-director → interactive-web-experience-engineer → one-click-web-preview

逻辑：先定升级方向和体验目标，再工程实现，最后一键预览验证。

### ⑤ 产品审查

触发词：审查、体验、验收、测试、质量、检查、audit

链路：kv-sanity-auditor → kv-clarity-mirror

逻辑：六视角全面审查 + 盲区扫描，双重门禁。

### ⑥ 战略思考

触发词：战略、商业、变现、IP、定价、模式、规划、决策

链路：interactive-ip-profit-director + dbs-unified → kv-insight-engine

逻辑：变现策略和商业思维并行输入，洞察引擎做最终提纯。

### ⑦ 漫画生产

触发词：漫画、分镜、连载、角色、三反骨、白卷羊、玄奇

链路：ai-comic-style → xw-programmatic-comic-drama → xw-xuanqi-universe

逻辑：风格和生产流定义 → 分镜剧本 → 世界观一致性校验。

### ⑧ 自主执行

触发词：自动、循环、目标、自主、不用管、跑完、端到端

链路：kv-goal-loop

逻辑：启动自主循环引擎，计划→执行→验证→评估→迭代，直到目标达成。

## 扩展规则

新增组合模式时：
1. 在本文件添加模式描述
2. 在 mcp/server.py 的 COMPOSITION_PATTERNS 字典添加对应条目
3. 在 SKILL.md 的"组合链"章节添加一行

保持 SKILL.md 中的链不超过 8 条。超过时考虑合并或按使用频率淘汰。
