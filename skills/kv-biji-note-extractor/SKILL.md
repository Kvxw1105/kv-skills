---
name: kv-biji-note-extractor
description: |
  Extract complete note content (original text + AI summaries) from biji.com (得到大脑) knowledge bases. Use when the user wants to scrape, extract, or download notes from biji.com knowledge base pages, or mentions 得到笔记/得到大脑/biji.com extraction. Also triggers on: 爬取笔记、抓取得到、导出知识库、biji.com 批量下载。
version: 2.0.0
---

# biji.com 笔记提取技能 v2

从得到大脑 (biji.com) 知识库中批量提取笔记的完整原文和 AI 总结分析。

## 适用场景

- 用户要求提取/抓取/下载 biji.com 知识库中的笔记内容
- 用户提供了 biji.com/subject/... 格式的链接
- 需要获取笔记的完整原文（不仅仅是页面上显示的摘要）

## 核心难点

biji.com 是 Vue.js 3 单页应用（Pinia + Vue Router），存在以下关键障碍：

1. **灰色链接区块**：每篇笔记的完整原文在灰色区块中，点击后通过 `window.open()` 在新标签页打开原始笔记页。但浏览器弹窗拦截器会阻止新标签打开。
2. **侧边栏切换**：笔记列表在侧边栏中，需要通过 JS 点击切换，不能用坐标点击。
3. **JS 变量陷阱**：在此环境的浏览器 JS 工具中，`const`/`let` 中间变量赋值返回 `undefined`，必须用链式表达式。
4. **虚拟滚动**：侧边栏使用虚拟滚动（virtual scrolling），DOM 中只渲染约 50 个 `.sider-list-item`，即使实际笔记数量更多。
5. **页面重渲染杀死异步**：每次侧边栏切换笔记后 Vue 组件重新渲染，会中断所有 pending 的 setTimeout/async 回调。

---

## 反模式警告 — 不要走这些弯路

以下方法在实际测试中**全部失败**，不要尝试：

### ❌ 异步批量脚本（async/await + setTimeout 循环）

```javascript
// 不要这样做！页面重渲染会杀死你的回调
(async () => {
  for (let i = 0; i < 64; i++) {
    document.querySelectorAll('.sider-list-item')[i].click();
    await new Promise(r => setTimeout(r, 1000));
    // ... 这里永远不会执行，因为页面重渲染了
  }
})();
```

**失败原因**：Vue 组件重渲染会中断 async 函数的执行上下文，setTimeout 回调不会被触发。实测 64 篇只跑了 12 篇就卡死。

### ❌ 直接调用 API

```javascript
// 不要这样做！CORS 和认证会阻止你
fetch('https://knowledge-api.trytalks.com/v1/web/topic/resource/list/mix?...')
```

**失败原因**：API 需要内部认证上下文（cookie/token + 特殊请求头），从浏览器 JS 环境裸调会返回 `AppNotFound` 或 `Failed to fetch`。XMLHttpRequest 同样失败。

### ❌ 从 Vue/Pinia 实例提取数据

```javascript
// 不要这样做！数据结构不直接暴露笔记 ID
document.querySelector('#app').__vue_app__.config.globalProperties.$pinia._s
```

**失败原因**：Pinia store 内部状态不直接暴露笔记列表，Vue 组件树中也找不到包含所有笔记 ID 的数据源。

### ❌ 递归 setTimeout 链

```javascript
// 不要这样做！和 async/await 一样会被重渲染杀死
window.__processNext = function(i) {
  setTimeout(function() { /* ... */ window.__processNext(i+1); }, 1000);
};
```

**失败原因**：同上，setTimeout 回调在页面重渲染后不会触发。

---

## 正确的执行策略

核心原则：**一步一确认，每步都是独立的工具调用**。

不要试图用聪明的脚本一次搞定。用最朴素的方式逐步推进，每一步都确认结果。虽然慢（64 篇约需 200 次工具调用），但每一步都是确定性的、可验证的。

### 第一步：打开知识库页面

用浏览器工具导航到用户提供的 biji.com/subject/... URL，记录 tabId。

### 第二步：确认笔记数量并处理虚拟滚动

```javascript
document.querySelectorAll('.sider-list-item').length
```

如果返回的数量小于用户说的总数，说明虚拟滚动没有加载全部项目。需要先滚动侧边栏加载更多：

```javascript
// 找到侧边栏的滚动容器并滚动到底部
var scroller = document.querySelector('.sider-list-item').closest('[class*=overflow]');
scroller.scrollTop = scroller.scrollHeight;
```

等待 1-2 秒后再次检查数量。重复直到数量匹配。

### 第三步：初始化 URL 收集器

```javascript
(window.__allUrls = [])
  && (window.__origOpen = window.__origOpen || window.open)
  && (window.open = function(url) { window.__urls.push(url); return null; })
  && (window.__urls = [])
  && 'initialized'
```

### 第四步：逐篇拦截原始 URL

对每篇笔记，执行以下 3 个独立工具调用（不要合并）：

**调用 1 — 切换笔记并保存上一篇 URL**：
```javascript
// 如果是第一篇，不需要 push
window.__allUrls.push("上一篇的URL") && document.querySelectorAll('.sider-list-item')[N].click()
```

**调用 2 — 重设拦截器并点击灰色区块**：
```javascript
(window.open = function(url) { window.__urls.push(url); return null; })
  && (window.__urls = [])
  && (document.querySelector('.cursor-pointer.rounded-lg.bg-gray-F5F6F7').click())
  && 'ok'
```

**调用 3 — 读取拦截到的 URL**：
```javascript
JSON.stringify(window.__urls)
```

URL 格式为 `/post/{subjectId}/{postId}/web`。

**为什么必须分 3 步？** 因为点击侧边栏后页面需要时间重渲染，灰色区块必须等渲染完成后才能点击。合并成一步会导致灰色区块找不到元素。

### 第五步：URL 去重

收集完所有 URL 后，检查重复：

```javascript
JSON.stringify([...new Set(window.__allUrls)])
```

### 第六步：批量提取完整原文

用子 Agent 或浏览器导航工具 (`tabs_create_mcp` + `navigate`) 逐个访问拦截到的 URL：

```
https://www.biji.com{intercepted_path}
```

在每个原始笔记页上读取内容（导航后等待 2 秒）：

```javascript
document.querySelector('main').innerText
```

页面结构为：标题 → 原链接（抖音） → 完整原文正文。

如果 `main.innerText` 为空，重试一次（SPA 加载可能需要更多时间）。

### 第七步：提取 AI 总结

回到主知识库页面，逐篇切换侧边栏笔记，读取 main 区域内容：

```javascript
// 切换笔记
document.querySelectorAll('.sider-list-item')[N].click()
// 等待渲染后读取
document.querySelector('main').innerText
```

内容包含 emoji 标记的分类（💡 核心观点、🎯 策略方法、💎 关键需求、🔑 核心要点等）。

**虚拟滚动注意**：如果笔记数超过 ~50 篇，侧边栏的虚拟滚动只会渲染前 50 个项目的 DOM。提取 AI 总结时需要分批：先提取前 50 篇的总结，然后滚动侧边栏加载剩余项目，再提取剩余的。

### 第八步：组装输出

将完整原文 + AI 总结写入 markdown 文件，每篇笔记格式：

```markdown
## 笔记N：标题

**完整原文：**

（从原始笔记页提取的完整正文）

**AI总结分析：**

（从主页面提取的 AI 总结）

---
```

---

## 关键 DOM 选择器

| 元素 | 选择器 |
|------|--------|
| 侧边栏笔记列表项 | `.sider-list-item` |
| 灰色链接区块（含完整原文入口） | `.cursor-pointer.rounded-lg.bg-gray-F5F6F7` |
| 笔记标题 | `.note-title` |
| AI 总结内容 | `.note-content` |
| 主内容区 | `main` |

## 常见陷阱与排查

详见 [references/troubleshooting.md](references/troubleshooting.md)。

## 注意事项

- 原文来自抖音视频语音转文字，存在同音字转录误差，保持原文不改
- 原始笔记页包含一个抖音原链接，可记录但不需要访问
- 每次切换笔记后 window.open 拦截器会失效，必须重新设置
- 用 `tabs_create_mcp` 创建新标签页访问原始笔记，避免弹窗拦截问题
- 收集完 URL 后务必去重，手动补漏时容易产生重复项
- 推荐用子 Agent 处理第六步（批量提取原文），避免主会话上下文过长

---

## Learnings

_Accumulated from real usage. Each entry records a pattern discovered during iteration._

- **2026-07-06 (v2.0.0)**: SPA 页面中的异步批量脚本（async/await + setTimeout）100% 会被 Vue 重渲染杀死。唯一可靠的方式是"一步一确认"——每步作为独立工具调用。实测 64 篇笔记用 async 脚本只跑了 12 篇就卡死，改用逐步调用后 100% 成功。
- **2026-07-06 (v2.0.0)**: biji.com API（knowledge-api.trytalks.com）无法从浏览器 JS 环境直接调用，无论用 fetch 还是 XHR，无论是否带 credentials。API 有内部认证机制，只能通过页面交互间接获取数据。
- **2026-07-06 (v2.0.0)**: 侧边栏使用虚拟滚动，DOM 中只渲染 ~50 个项目。超过 50 篇的知识库需要先滚动侧边栏加载剩余项目，否则无法访问后面的笔记。
- **2026-07-06 (v2.0.0)**: 浏览器 JS 工具中 `const`/`let` 赋值返回 `undefined`，必须用 `&&` 链式表达式。这是工具层面的限制，不是 JS 本身的行为。
- **2026-07-06 (v2.0.0)**: 手动补漏时容易产生 URL 重复。收集完所有 URL 后必须用 `Set` 去重，否则会导致重复提取和文件内容重复。
- **2026-07-06 (v2.0.0)**: 推荐将"批量提取原文"步骤交给子 Agent 处理。64 篇笔记的原文提取会产生大量工具调用，在主会话中执行会导致上下文膨胀。子 Agent 可以独立处理并在完成后返回结果。
