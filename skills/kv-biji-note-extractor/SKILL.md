---
name: kv-biji-note-extractor
description: |
  Extract complete note content (original text + AI summaries) from biji.com (得到大脑) knowledge bases. Use when the user wants to scrape, extract, or download notes from biji.com knowledge base pages, or mentions 得到笔记/得到大脑/biji.com extraction. Also triggers on: 爬取笔记、抓取得到、导出知识库、biji.com 批量下载。
version: 3.1.0
---

# biji.com 笔记提取技能 v3

> **设计说明（v3.1.0）**：本技能的核心执行流程（下方「完整执行流程」第一步至第八步）经过反复验证，是**默认采用的主干方案**，请勿轻易替换。v3.1.0 的实战中还摸索出几条**可选优化**（见文末「可选优化方案」），能进一步提速/降复杂度，但属于**可选参考**，按现场情况决定是否采用——原设计依然成立、依然可用。

从得到大脑 (biji.com) 知识库中批量提取笔记的完整原文和 AI 总结。

## 适用场景

- 用户要求提取/抓取/下载 biji.com 知识库中的笔记内容
- 用户提供了 biji.com/subject/... 格式的链接
- 需要获取笔记的完整原文和 AI 总结

## 核心架构（v3 验证通过）

**快速通道**（推荐，约 10 次工具调用完成全部提取）：

```
XHR 劫持捕获认证头 → API 批量获取笔记列表+AI总结 → iframe 并行加载获取原文 → 清洗 → 组装
```

**Fallback**（仅当快速通道失败时使用）：
逐篇点击侧边栏 + window.open 劫持 + 新标签页读取。约 200 次工具调用，仅在 API 变更时使用。

---

## 完整执行流程（含可执行代码）

### 第一步：导航到知识库页面

用浏览器 `navigate` 工具打开用户提供的 URL，记录 `tabId`。

### 第二步：确认笔记数量

```javascript
document.querySelectorAll('.sider-list-item').length
```

如果数量不足，滚动侧边栏加载更多：
```javascript
var s = document.querySelector('.sider-list-item').closest('[class*=overflow]');
s.scrollTop = s.scrollHeight;
```

### 第三步：XHR 劫持 — 捕获认证头

这是核心技巧。拦截页面自己的 XMLHttpRequest，捕获完整的认证请求头：

```javascript
(function() {
  window.__capturedHeaders = {};
  window.__capturedRequests = [];
  var origOpen = XMLHttpRequest.prototype.open;
  var origSetHeader = XMLHttpRequest.prototype.setRequestHeader;
  var origSend = XMLHttpRequest.prototype.send;
  
  XMLHttpRequest.prototype.open = function(method, url) {
    this.__url = url; this.__method = method; this.__headers = {};
    return origOpen.apply(this, arguments);
  };
  XMLHttpRequest.prototype.setRequestHeader = function(name, value) {
    this.__headers[name] = value;
    window.__capturedHeaders[name] = value;
    return origSetHeader.apply(this, arguments);
  };
  XMLHttpRequest.prototype.send = function(body) {
    if (this.__url && this.__url.includes('knowledge-api')) {
      window.__capturedRequests.push({
        method: this.__method, url: this.__url,
        headers: Object.assign({}, this.__headers), body: body
      });
    }
    return origSend.apply(this, arguments);
  };
  return 'XHR interceptor installed';
})()
```

### 第四步：触发页面自己的 API 请求

点击侧边栏笔记，让页面发出带认证头的 XHR 请求：

```javascript
document.querySelectorAll('.sider-list-item')[1].click()
```

### 第五步：读取捕获的认证头

```javascript
JSON.stringify(Object.keys(window.__capturedHeaders))
```

应包含：`Authorization`, `Xi-Csrf-Token`, `X-Request-ID`, `x-d`, `Xi-App-Client-Source`, `X-Appid`, `X-Av` 等。

### 第六步：API 批量获取笔记列表 + AI 总结

**获取笔记列表**（需要同时传 `follow_id` 和 `topic_id`，缺一不可）：

从 URL 参数中提取 `followId`，从 API 响应中提取 `topic_id`。

```javascript
(function() {
  var h = window.__capturedHeaders;
  var xhr = new XMLHttpRequest();
  // follow_id 从 URL 参数获取，topic_id 从 resource/list API 响应获取
  xhr.open('POST', 'https://knowledge-api.trytalks.com/v1/web/follow/account/posts', false);
  // 设置所有捕获的请求头
  Object.keys(h).forEach(function(k) { xhr.setRequestHeader(k, h[k]); });
  xhr.setRequestHeader('X-Request-ID', Date.now().toString());
  xhr.send(JSON.stringify({follow_id: FOLLOW_ID, topic_id: TOPIC_ID, page: 1, page_size: 100}));
  var data = JSON.parse(xhr.responseText);
  var posts = data.c.posts;
  window.__allNotes = posts.map(function(p) {
    return { id: p.post_id_str, title: p.post_name };
  });
  return JSON.stringify({total: window.__allNotes.length});
})()
```

**批量获取每篇笔记的 AI 总结**：

```javascript
(function() {
  var h = window.__capturedHeaders;
  var notes = window.__allNotes;
  var results = [];
  for (var i = 0; i < notes.length; i++) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'https://knowledge-api.trytalks.com/v1/web/topic/post/detail', false);
    Object.keys(h).forEach(function(k) { xhr.setRequestHeader(k, h[k]); });
    xhr.setRequestHeader('X-Request-ID', Date.now().toString() + i);
    xhr.send(JSON.stringify({topic_id: -1, topic_id_alias: 'pn53x8p0', post_id: notes[i].id}));
    var d = JSON.parse(xhr.responseText).c;
    results.push({id: notes[i].id, title: d.post_name, summary: d.post_summary || ''});
  }
  window.__allDetails = results;
  return JSON.stringify({total: results.length, withSummary: results.filter(function(r){return r.summary}).length});
})()
```

### 第七步：iframe 并行加载获取原文

每次并行 5 个 iframe，每个等待 6 秒：

```javascript
(function() {
  var notes = window.__allNotes;
  var batchSize = 5;
  window.__iframeResults = {};
  
  function loadBatch(start) {
    if (start >= notes.length) { window.__iframeDone = true; return; }
    var end = Math.min(start + batchSize, notes.length);
    var iframes = [];
    for (var i = start; i < end; i++) {
      var iframe = document.createElement('iframe');
      iframe.style.display = 'none';
      iframe.id = 'batch-iframe-' + i;
      iframe.src = 'https://www.biji.com/post/pn53x8p0/' + notes[i].id + '/web';
      document.body.appendChild(iframe);
      iframes.push({index: i, iframe: iframe});
    }
    setTimeout(function() {
      for (var j = 0; j < iframes.length; j++) {
        var item = iframes[j];
        try {
          var doc = item.iframe.contentDocument || item.iframe.contentWindow.document;
          var main = doc.querySelector('main');
          if (main) { window.__iframeResults[item.index] = main.innerText; }
        } catch(e) { window.__iframeResults[item.index] = '__ERROR__'; }
        item.iframe.remove();
      }
      loadBatch(end);
    }, 6000);
  }
  loadBatch(0);
  return 'batch iframe loading started for ' + notes.length + ' notes';
})()
```

等待完成（笔记数 / 5 × 6 秒）后检查：
```javascript
JSON.stringify({done: window.__iframeDone, count: Object.keys(window.__iframeResults).length})
```

### 第八步：清洗 + 组装

用 Python 脚本处理（比浏览器 JS 更可靠）：

```python
import re

def clean_note(text):
    # 去除"得到大脑"前缀
    if text.startswith('得到大脑'): text = text[4:]
    # 去除标题+抖音链接（URL-char-only 正则，不吞中文正文）
    url_match = re.search(r'原链接：https?://[a-zA-Z0-9?&=%.\-_~:/\[\]@!$\'()*+,;]+', text)
    if url_match: text = text[url_match.end():]
    # 去除尾部噪声
    for marker in ['当前网页无法显示', '当前知识库由于作者设置']:
        idx = text.find(marker)
        if idx >= 0: text = text[:idx]
    return text.strip()
```

组装 Markdown：
```markdown
## 笔记N：标题

**完整原文：**
（清洗后的原文）

**AI总结分析：**
（API 返回的 summary）

---
```

---

## 关键参数速查

| 参数 | 来源 |
|------|------|
| `follow_id` | URL 参数 `followId=...` |
| `topic_id` | 从 `GET topic/detail?id_alias=<alias>&source=web` 的响应中取（响应 JSON 里含数字 `topic_id`，如 `297888`）；历史上也曾来自 `resource/list/mix` 的 `current_directory.topic_id`，但该端点已失效，以当前页面真实调用为准（见「可选优化方案」的抓包法） |
| `topic_id_alias` | URL 路径中的 `pn53x8p0` 等 |
| 笔记页 URL | `https://www.biji.com/post/{alias}/{post_id}/web` |

## 常见陷阱

详见 [references/troubleshooting.md](references/troubleshooting.md)。

## 注意事项

- 原文来自抖音视频语音转文字，存在同音字转录误差，保持原文不改
- 短原文（200-700字）不等于截断 — 短视频的语音转文字自然就这么短
- 清洗正则 必须用 URL-char-only 字符集，不能用 `\S+`（会吞掉紧连的中文正文）
- `follow/account/posts` API 必须同时传 `follow_id` 和 `topic_id`，缺一不可
- iframe 比新标签页更可靠（继承父页面认证上下文）
- 推荐用子 Agent 处理数据导出，避免主会话上下文过长

---

## 可选优化方案（v3.1.0 实战验证，仅供参考，非必须）

> 以下是 2026-07-16 一次完整实战（98 篇全量提取）中摸索出的几条**可选提速/降复杂度手段**。它们与上面的主干流程**不冲突**：主干流程依然成立、可直接照做；下面这些只是"在某些运行载体下能更顺手"的备选。**请不要因此直接删改主干流程**——主干是经反复验证的稳妥方案，新手段只是给你多一个选择。

### 可选 A：列表接口直接带 AI 总结（省掉逐篇 detail 调用）

实战发现，`follow/account/posts` 的响应里每篇 post 已经内联了 `post_summary`（完整 Markdown AI 总结）与 `post_cleaned_summary`（HTML 版）。**如果你的运行环境抓到的列表响应里已有 `post_summary`**，就可以跳过主干第六步"批量获取每篇 AI 总结"那段逐篇 `topic/post/detail` 的循环（98 篇能省掉近 100 次 API 调用），翻页拉列表时就能同时拿到「标题 + AI总结 + 抖音原链接」。
- *为什么是可选*：早期/不同的知识库数据结构未必都内联 summary，主干的"逐篇 detail"更通用稳妥；先确认响应里有 `post_summary` 字段，再决定是否跳过。

### 可选 B：用网络抓包确认真实接口，别只靠记忆

`resource/list/mix`、`resource/list`、`topic/detail`(POST) 这些旧端点实测已 404。最稳妥的做法（也适用于任何接口不明的页面）：先开网络监控、刷新页面，直接看页面自己发了哪些请求：
1. `GET topic/detail?id_alias=<alias>&source=web` → 响应含 `topic_id`（数字，如 `297888`）。
2. `POST follow/account/posts` → 完整列表（含标题/总结/链接）。
- 用抓包看到的事实替代"猜端点"，准确率 100%，也更省试错时间。这与主干第二步"确认参数来源"是同一意图，只是手段更直观测。

### 可选 C：分块驱动 iframe（规避长脚本被 SPA 重渲染打断）

主干第七步用"单条长 `setTimeout` 链"批量加载 iframe，在部分 SPA 上会因重渲染中断。实战中更稳的写法：把批量拆成"**每块一个自包含 async IIFE**"（`创建 N 个 iframe → await setTimeout → 读 innerText → return JSON`），由**外部脚本（如 Python）逐块循环调用并落盘**，带断点续传（已成功的 id 跳过）。
- 优点：每个 `evaluate` 调用独立、短生命周期，不会因页面重渲染而整段丢失；98 篇分 17 块、每块 6 篇、每块等 7 秒，全部 98/98 成功，约 2 分钟。
- *为什么是可选*：主干的"单条长脚本"在多数情况下也能跑通（v3.0.0 实测 24 篇成功）；仅当遇到长脚本中途中断时才需要切到分块法。

### 可选 D：iframe 等待时间留冗余 + 对少量篇目重试

批量等 7 秒时，可能有 1-2 篇原文还没加载完（会拿到"当前网页无法显示"占位）。对返回噪声占位/空文本的少数篇目，用 **9-10 秒单独重试**一轮即可补全。个别笔记页面会返回"当前知识库存在敏感信息，不支持访问"——多为瞬时/加载超时，重试基本能拿到真文；若确实持续受限，保留其 AI 总结并标注"原文不可得"，不要整篇丢弃。

### 可选 E：运行载体 —— Kimi WebBridge 可作为便捷载体

本技能只需要"在目标页面执行任意 JS + 能抓包"。除了自己用浏览器 CDP/调试端口，也可以直接用 **Kimi WebBridge**（常驻守护进程控制用户浏览器、天然带登录态）：其 `evaluate`（支持 async/await）跑 XHR 劫持与 iframe 批量，`network` 做抓包，一条 curl 即可，省去自己起 Chrome 调试端口/CDP proxy 的麻烦。
- *注意*：无论哪种载体，`navigate` 刷新页面都会清空注入的 `window.__*` 变量——刷新后需重装拦截器、重新点击笔记捕获认证头。

---

## Learnings

_Accumulated from real usage. Each entry records a pattern discovered during iteration._

### 主干设计（v3.0.0，经验证，默认沿用）

- **2026-07-06 (v3.0.0)**: XHR 劫持是正确路线。拦截 `XMLHttpRequest.prototype.setRequestHeader` 可捕获完整认证头（Authorization + CSRF Token 等 9 个），然后用这些头直接调 API 批量获取数据。裸调 API 会失败（CORS + 无认证），但带捕获头的重放调用 100% 成功。
- **2026-07-06 (v3.0.0)**: iframe 并行加载（5路 × 6秒/批）比逐页导航快 3-4 倍，且比新标签页更可靠（继承父页面认证上下文）。实测 24 篇笔记分 5 批共 30 秒完成。
- **2026-07-06 (v3.0.0)**: `follow/account/posts` API 必须同时传 `follow_id`（从 URL 参数获取）和 `topic_id`（`topic_id` 的获取以当前页面真实调用为准，旧 `resource/list` 端点已失效，见可选 B），缺一不可。单独传 `follow_id` 会返回"知识库不存在"。
- **2026-07-06 (v3.0.0)**: 清洗正则必须用 URL-char-only 字符集 `[a-zA-Z0-9?&=%.\-_~:/...]+`，绝不能用 `\S+`。后者会匹配 URL 后面紧连的中文字符，导致正文被误删。
- **2026-07-06 (v3.0.0)**: 短原文（200-700字）不等于截断。短视频的语音转文字自然就这么短。不要用长度阈值判断完整性，应让用户确认。
- **2026-07-06 (v3.0.0)**: SPA 页面中的异步批量脚本（async/await + setTimeout）有被 Vue 重渲染打断的风险；若遇此问题，可改用主干的同步 XHR 循环（在单条 JS 执行内完成），或参考可选 C 的分块驱动法。
- **2026-07-06 (v2.0.0)**: 浏览器 JS 工具中 `const`/`let` 赋值返回 `undefined`，必须用 `&&` 链式表达式。
- **2026-07-06 (v2.0.0)**: 推荐将数据导出步骤交给子 Agent，避免主会话上下文膨胀。

### 可选优化（v3.1.0，实战验证，按需采用）

- **2026-07-16 (v3.1.0) [可选A] 列表接口可能直接内联 AI 总结**：`follow/account/posts` 响应中每篇 post 常已带 `post_summary` 与 `post_cleaned_summary`。若响应确含该字段，可跳过逐篇 `topic/post/detail` 取总结的循环，翻页即同时拿到标题+总结+链接（98 篇约省百次调用）。是否采用以实际响应为准，主干的逐篇 detail 仍作为通用兜底。
- **2026-07-16 (v3.1.0) [可选B] 接口不明时优先抓包**：`resource/list/mix` 等旧端点已 404。与其猜，不如开网络监控刷新页面，直接看真实请求：`GET topic/detail?id_alias=<alias>&source=web` 给 `topic_id`（数字）；`POST follow/account/posts` 给完整列表。抓包所得即事实，准确率最高。
- **2026-07-16 (v3.1.0) [可选C] 分块驱动 iframe 更抗打断**：长 `setTimeout` 链可能被 SPA 重渲染中断。改为"每块一个自包含 async IIFE + 外部脚本逐块循环落盘（断点续传）"，每个 evaluate 调用短生命周期。98 篇分 17 块、每块 6 篇、每块等 7 秒，98/98 成功，约 2 分钟。仅在主干长脚本失效时切换。
- **2026-07-16 (v3.1.0) [可选D] iframe 等待留冗余 + 重试**：批量等 7 秒偶尔有 1-2 篇未加载完（占位噪声），用 9-10 秒单独重试可补全。个别篇返回"敏感信息不支持访问"多为瞬时，重试基本可取回；持续受限则保留 AI 总结并标注原文不可得。
- **2026-07-16 (v3.1.0) [可选E] 运行载体可选 Kimi WebBridge**：需要"执行任意 JS + 抓包"时，Kimi WebBridge 常驻守护进程（带登录态）比手动起 CDP proxy 更省事；`evaluate` 跑劫持/iframe，`network` 抓包。注意刷新页面会清空注入变量，需重装拦截器与重抓头。
