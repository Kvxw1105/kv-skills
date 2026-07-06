---
name: kv-biji-note-extractor
description: |
  Extract complete note content (original text + AI summaries) from biji.com (得到大脑) knowledge bases. Use when the user wants to scrape, extract, or download notes from biji.com knowledge base pages, or mentions 得到笔记/得到大脑/biji.com extraction. Also triggers on: 爬取笔记、抓取得到、导出知识库、biji.com 批量下载。
version: 3.0.0
---

# biji.com 笔记提取技能 v3

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
| `topic_id` | `resource/list/mix` API 响应中的 `current_directory.topic_id` |
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

## Learnings

_Accumulated from real usage. Each entry records a pattern discovered during iteration._

- **2026-07-06 (v3.0.0)**: XHR 劫持是正确路线。拦截 `XMLHttpRequest.prototype.setRequestHeader` 可捕获完整认证头（Authorization + CSRF Token 等 9 个），然后用这些头直接调 API 批量获取数据。裸调 API 会失败（CORS + 无认证），但带捕获头的重放调用 100% 成功。
- **2026-07-06 (v3.0.0)**: iframe 并行加载（5路 × 6秒/批）比逐页导航快 3-4 倍，且比新标签页更可靠（继承父页面认证上下文）。实测 24 篇笔记分 5 批共 30 秒完成。
- **2026-07-06 (v3.0.0)**: `follow/account/posts` API 必须同时传 `follow_id`（从 URL 参数获取）和 `topic_id`（从 resource/list API 响应获取），缺一不可。单独传 `follow_id` 会返回"知识库不存在"。
- **2026-07-06 (v3.0.0)**: 清洗正则必须用 URL-char-only 字符集 `[a-zA-Z0-9?&=%.\-_~:/...]+`，绝不能用 `\S+`。后者会匹配 URL 后面紧连的中文字符，导致正文被误删。
- **2026-07-06 (v3.0.0)**: 短原文（200-700字）不等于截断。短视频的语音转文字自然就这么短。不要用长度阈值判断完整性，应让用户确认。
- **2026-07-06 (v3.0.0)**: SPA 页面中的异步批量脚本（async/await + setTimeout）100% 会被 Vue 重渲染杀死。唯一可靠的浏览器端批量方式是同步 XHR 循环（在单条 JS 执行内完成，不涉及异步回调）。
- **2026-07-06 (v2.0.0)**: 浏览器 JS 工具中 `const`/`let` 赋值返回 `undefined`，必须用 `&&` 链式表达式。
- **2026-07-06 (v2.0.0)**: 推荐将数据导出步骤交给子 Agent，避免主会话上下文膨胀。
