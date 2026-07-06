# 常见问题与排查

## 1. window.open 拦截器失效

**现象**：点击灰色区块后 `window.__urls` 没有新增 URL。

**原因**：侧边栏切换笔记后 Vue.js 重新渲染组件，可能重置了 `window.open` 引用。

**解决**：每次切换笔记后，立即重新设置拦截器：

```javascript
(window.open = function(url) { window.__urls.push(url); return null; })
  && (window.__urls = [])
  && 're-intercepted'
```

**验证拦截器是否生效**：

```javascript
window.open.toString().substring(0, 80)
// 应返回: "function(url) { window.__urls.push(url); return null; }"
```

## 2. 灰色区块选择器找不到元素

**现象**：`document.querySelector('.cursor-pointer.rounded-lg.bg-gray-F5F6F7')` 返回 null。

**原因**：切换笔记后页面还在渲染中，灰色区块尚未出现。

**解决**：等待 1-2 秒后重试，或用轮询：

```javascript
document.querySelector('.cursor-pointer.rounded-lg.bg-gray-F5F6F7') ? 'found' : 'not found'
```

## 3. 侧边栏点击无反应

**现象**：`document.querySelectorAll('.sider-list-item')[N].click()` 执行后页面内容未切换。

**原因**：使用了错误的选择器。span 索引方式 `span[N*3].click()` 已失效。

**解决**：必须使用 `.sider-list-item` div 的 click()：

```javascript
document.querySelectorAll('.sider-list-item')[N].click()
```

## 4. JS 变量赋值返回 undefined

**现象**：`const x = document.querySelector(...)` 在浏览器 JS 工具中返回 undefined。

**原因**：此环境的浏览器 JS 工具对 `const`/`let` 中间变量赋值的返回值处理有缺陷。

**解决**：使用链式表达式（`&&` 连接）代替中间变量：

```javascript
// 错误：返回 undefined
const el = document.querySelector('.foo');
el.click();

// 正确：链式调用
document.querySelector('.foo') && document.querySelector('.foo').click()
```

## 5. 新标签页被弹窗拦截

**现象**：点击灰色区块后没有新标签打开。

**原因**：浏览器弹窗拦截器阻止了 `window.open()` 创建的标签。

**解决**：不需要依赖弹窗。用 `tabs_create_mcp` 手动创建新标签，再用 `navigate` 导航到拦截到的 URL。

## 6. 原始笔记页内容为空

**现象**：访问 `/post/.../web` 页面后 `main.innerText` 为空。

**原因**：页面是 SPA，内容需要时间加载。

**解决**：导航后等待 1-2 秒再读取内容。如果仍然为空，检查 URL 是否正确（必须以 `/post/` 开头，以 `/web` 结尾）。

## 7. API 直接调用返回 AppNotFound

**现象**：直接 fetch `knowledge-api.trytalks.com` 返回 `{"message":"AppNotFound"}`。

**原因**：API 需要认证上下文（cookie/token），不能直接裸调。

**解决**：放弃 API 路线，改用页面导航方式逐篇提取。这是唯一可靠的路径。

## 8. 页面存在 app-error-page 元素

**现象**：页面 HTML 中有多个 `app-error-page` div 和"重新加载"按钮。

**说明**：这些元素默认隐藏（`display: none`），是错误状态的占位符，与内容提取无关。点击它们不会加载完整原文。

## 9. 异步批量脚本中途卡死（v2.0.0 新增）

**现象**：用 `async/await` + `setTimeout` 写的循环脚本，跑了若干篇后停止执行，`window.__done` 始终未设置。

**原因**：biji.com 是 Vue.js SPA，每次切换笔记都会触发组件重渲染。重渲染会中断 async 函数的执行上下文，导致 setTimeout 回调永远不会被触发。

**解决**：放弃异步批量脚本。改用"一步一确认"策略——每篇笔记的拦截操作拆成 3 个独立的工具调用（切换笔记 → 重设拦截器+点击灰色区块 → 读取 URL）。这是唯一经过验证的可靠方式。

## 10. 侧边栏只显示部分笔记（虚拟滚动）（v2.0.0 新增）

**现象**：`document.querySelectorAll('.sider-list-item').length` 返回 50，但知识库实际有 64 篇笔记。

**原因**：侧边栏使用虚拟滚动（virtual scrolling），只渲染可视区域内的 DOM 元素。

**解决**：找到侧边栏的滚动容器，通过 JS 滚动到底部加载更多项目：

```javascript
var scroller = document.querySelector('.sider-list-item').closest('[class*=overflow]');
scroller.scrollTop = scroller.scrollHeight;
```

等待 1-2 秒后重新检查数量。可能需要多次滚动。

## 11. URL 列表有重复项（v2.0.0 新增）

**现象**：最终收集的 URL 数量多于笔记总数，或提取出的 Markdown 有重复内容。

**原因**：手动补漏时容易把已收集的 URL 再 push 一次。

**解决**：收集完所有 URL 后用 Set 去重：

```javascript
JSON.stringify([...new Set(window.__allUrls)])
```
