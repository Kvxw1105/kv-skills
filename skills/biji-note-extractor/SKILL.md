---
name: biji-note-extractor
description: |
  Extract complete note content (original text + AI summaries) from biji.com (得到大脑) knowledge bases. Use when the user wants to scrape, extract, or download notes from biji.com knowledge base pages, or mentions 得到笔记/得到大脑/biji.com extraction. Also trigger when user says "提取笔记", "下载笔记", "抓取笔记", "批量导出", "知识库内容", "biji.com 笔记", or provides biji.com/subject/... URLs.
version: 1.0.0
metadata:
  category: data-extraction
  scope: web-scraping
  complexity: high
  requires-browser: true
  ip-prefix: kv
  author: kv
  display-name: biji.com 笔记提取器
  chinese-name: 得到大脑笔记提取器
  compatibility:
    - browser-use-mcp
    - claude-code
    - newmax
  trigger-phrases:
    - "提取 biji.com 笔记"
    - "下载得到大脑笔记"
    - "抓取知识库内容"
    - "批量导出笔记"
    - "biji.com extraction"
    - "得到笔记提取"
    - "知识库笔记下载"
---

# biji.com 笔记提取器

从得到大脑 (biji.com) 知识库中批量提取笔记的完整原文和 AI 总结分析。这是一个高复杂度的浏览器自动化任务，需要处理 SPA 架构、弹窗拦截、登录态继承等技术难点。

## 核心价值

- **完整原文提取**：获取抖音视频语音转文字的完整文案，而非页面摘要
- **AI 总结保留**：保留 biji.com 自动生成的结构化总结（核心特质、关键认知等）
- **批量处理**：支持一次提取整个知识库的全部笔记
- **经验沉淀**：包含真实踩坑经验，避免重复犯错

## 适用场景

当用户提到以下任何情况时，**必须使用此技能**：

**中文触发词**：
- "提取笔记"、"下载笔记"、"抓取笔记"
- "得到大脑"、"biji.com"
- "知识库内容"、"知识库笔记"
- "批量导出"、"批量下载"
- "抖音笔记"、"语音转文字"

**英文触发词**：
- "extract notes from biji.com"
- "download biji.com content"
- "scrape knowledge base"
- "batch export notes"

**URL 模式**：
- `https://www.biji.com/subject/...`
- `https://www.biji.com/post/...`

## 核心难点（必须理解）

biji.com 是 Vue.js 单页应用，存在三个**必须解决**的技术障碍：

### 1. 弹窗拦截问题
- **问题**：每篇笔记的完整原文在灰色区块中，点击后通过 `window.open()` 在新标签页打开
- **影响**：浏览器弹窗拦截器会阻止新标签打开，导致无法获取原文 URL
- **解决方案**：劫持 `window.open` 方法，拦截 URL 而非真正打开窗口

### 2. DOM 渲染限制
- **问题**：侧边栏笔记列表有硬限制，最多渲染 50 条 DOM
- **影响**：直接查询 DOM 只能获取 50 条，无法获取完整笔记列表
- **解决方案**：必须通过博主入口获取完整列表，或使用 API 分页

### 3. 登录态继承问题
- **问题**：iframe 无法继承主页面的登录态，跨域请求被 CORS 阻止
- **影响**：批量加载方案（如 iframe 并行加载）会失败
- **解决方案**：必须逐个用浏览器打开 URL 提取，不能用 iframe

## 提取流程（严格按顺序执行）

### 第一步：打开知识库页面

```javascript
// 用浏览器工具导航到用户提供的 URL
// 记录 tabId，后续操作都基于这个 tabId
```

**关键**：先检查 URL 是否包含 `followId` 参数，这会影响笔记数量限制。

### 第二步：确认笔记数量（最重要的一步！）

**永远不要用 DOM 查询结果作为最终数字！**

正确做法：
1. **截图确认页面全貌** —— 看页面上是否有"共 X 条"的计数器
2. **检查博主入口** —— 如果有"博主"tab，点进去看博主详情页的笔记数（通常没有限制）
3. **对比两个视图** —— followId 视图（URL 带 `followId=xxx`）可能有 50 条硬限制

```javascript
// DOM 查询（仅作参考，不是最终数字）
document.querySelectorAll('.sider-list-item').length

// 正确做法：截图后查看页面上的计数器
// 或者点击"博主"tab 查看博主详情页的笔记数
```

**实战教训**：
- followId 视图：最多 50 条
- 博主入口：通常没有限制
- 如果用户说有 64 条，但 DOM 只有 50 条，**必须从博主入口获取**

详见 [references/lessons-learned.md](references/lessons-learned.md) 的"核心认知：笔记数量的正确获取"章节。

### 第三步：劫持 window.open 拦截 URL

这是**核心技巧**。在页面 JS 环境中替换 `window.open`，使其不真正打开窗口，只记录目标 URL：

```javascript
(window.__origOpen = window.__origOpen || window.open)
  && (window.open = function(url) {
       window.__urls.push(url);
       return null;
     })
  && (window.__urls = [])
  && 'intercepted'
```

**注意**：每次侧边栏切换笔记后页面会重新渲染，需**重新设置拦截器**。

### 第四步：逐篇拦截原始 URL

对每篇笔记（索引 0 到 N-1）：

1. 切换笔记：`document.querySelectorAll('.sider-list-item')[N].click()`
2. **重新设置 window.open 拦截器**（关键！）
3. 点击灰色区块：`document.querySelector('.cursor-pointer.rounded-lg.bg-gray-F5F6F7').click()`
4. 读取拦截到的 URL：`JSON.stringify(window.__urls)`

URL 格式为 `/post/{subjectId}/{postId}/web`。

**批量处理技巧**：用循环脚本一次处理 5 篇，减少重复操作。

### 第五步：批量提取完整原文

用浏览器导航工具 (`browser_open` + `navigate`) 逐个访问拦截到的 URL：

```
https://www.biji.com{intercepted_path}
```

在每个原始笔记页上读取内容：

```javascript
document.querySelector('main').innerText
```

页面结构为：标题 → 原链接（抖音） → 完整原文正文。

**Token 优化**：用 `browser_save_file` 直接保存到本地文件，避免通过 tool result 传输大量文本。

### 第六步：提取 AI 总结

AI 总结在主知识库页面的 main 区域中，切换笔记后可直接读取：

```javascript
document.querySelector('main').innerText
```

内容包含 emoji 标记的分类（💪 核心特质、🔍 关键认知等）。

**批量收集技巧**：可以在侧边栏切换所有笔记，一次性收集所有 AI 总结到数组中。

### 第七步：组装输出

将完整原文 + AI 总结写入 markdown 文件，每篇笔记格式：

```markdown
## 笔记N：标题

**完整原文：**

（从原始笔记页提取的完整正文）

**AI总结分析：**

（从主页面提取的 AI 总结）
```

**输出优化**：使用 `<details>` 标签折叠原文，使文档更易读。

## 关键 DOM 选择器

| 元素 | 选择器 | 用途 |
|------|--------|------|
| 侧边栏笔记列表项 | `.sider-list-item` | 切换笔记、计数 |
| 灰色链接区块（含完整原文入口） | `.cursor-pointer.rounded-lg.bg-gray-F5F6F7` | 获取原文 URL |
| 笔记标题 | `.note-title` | 提取标题 |
| AI 总结内容 | `.note-content` | 提取总结 |
| 主内容区 | `main` | 读取页面内容 |
| 博主 tab | `[class*="blogger"]` 或通过文本查找 | 获取完整笔记列表 |

## 常见陷阱

详见 [references/troubleshooting.md](references/troubleshooting.md)，包含 12 个常见问题的解决方案。

**最关键的 3 个陷阱**：
1. **不要用 DOM 计数作为最终数字** —— 必须截图确认或从博主入口获取
2. **不要用 iframe 批量加载** —— 无法继承登录态，会失败
3. **每次切换笔记后必须重新设置拦截器** —— 页面会重新渲染

## 实战经验与最佳实践

详见 [references/lessons-learned.md](references/lessons-learned.md)，包含：

- **提取前检查清单** —— 确认笔记总数、入口来源、分页情况、认证状态
- **批量提取策略** —— 为什么 iframe 方案失败、正确的逐个提取方法
- **API 拦截经验** —— 关键端点、分页参数、CORS 限制
- **错误处理原则** —— 什么时候该停止尝试、如何识别平台硬限制
- **Token 优化技巧** —— 用 browser_save_file、Agent 并行处理
- **失败模式速查表** —— 假完成、工具盲区、执行鸿沟等

## 注意事项

- 原文来自抖音视频语音转文字，存在同音字转录误差，**保持原文不改**
- 原始笔记页包含一个抖音原链接，可记录但不需要访问
- 每次切换笔记后 window.open 拦截器会失效，**必须重新设置**
- 用 `browser_open` 创建新标签页访问原始笔记，避免弹窗拦截问题
- **先验证假设，再执行** —— 不要用 DOM 查询结果作为最终数字
- **小规模测试，再批量执行** —— 先用 1-2 篇笔记测试方案可行性
- **及时止损，不要死磕** —— 连续 3 次失败就换方案

## Learnings

_Accumulated from real usage. Each entry records a pattern discovered during iteration._

- **2026-07-06 (v1.1.0)**: followId 视图有 50 条硬限制，博主入口没有。必须从博主入口获取完整列表。
- **2026-07-06 (v1.1.0)**: iframe 方案无法继承登录态，会失败。必须逐个用浏览器打开 URL。
- **2026-07-06 (v1.1.0)**: DOM 查询结果只是当前渲染数量，不是总数。必须截图确认或从博主入口获取。
- **2026-07-06 (v1.1.0)**: 批量处理时用循环脚本一次处理 5 篇，比逐个处理快 3 倍。
- **2026-07-06 (v1.1.0)**: 用 browser_save_file 保存大文本，避免通过 tool result 传输，节省 Token。
