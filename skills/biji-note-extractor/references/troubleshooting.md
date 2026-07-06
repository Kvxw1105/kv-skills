# 常见问题与排查

## 1. window.open 拦截器失效

**现象**：点击灰色区块后 `window.__urls` 没有新增 URL。

**原因**：侧边栏切换笔记后 Vue.js 重新渲染组件，可能重置了 `window.open` 引用。

**解决**：每次切换笔记后，立即重新设置拦截器：

```javascript
(window.__origOpen = window.__origOpen || window.open)
  && (window.open = function(url) { window.__urls.push(url); return null; })
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

**解决**：放弃 API 路线，改用页面导航方式逐篇提取。

## 8. 页面存在 app-error-page 元素

**现象**：页面 HTML 中有多个 `app-error-page` div 和"重新加载"按钮。

**说明**：这些元素默认隐藏（`display: none`），是错误状态的占位符，与内容提取无关。点击它们不会加载完整原文。

## 9. 笔记数量不匹配（50 vs 64）

**现象**：用户说有 64 篇笔记，但 DOM 查询只返回 50 条。

**原因**：
- biji.com 侧边栏有硬限制，最多渲染 50 条 DOM
- followId 视图（URL 带 `followId=xxx`）可能有数量限制
- 博主入口通常没有限制

**解决**：
1. 先截图确认页面全貌，看页面上是否有"共 X 条"的计数器
2. 检查博主入口 —— 点击"博主"tab，看博主详情页的笔记数
3. 如果博主入口显示 64 条，从博主入口进入获取全部笔记

**关键教训**：永远不要用 DOM 查询结果作为最终数字！

详见 [lessons-learned.md](lessons-learned.md) 的"核心认知：笔记数量的正确获取"章节。

## 10. iframe 方案失败

**现象**：尝试在主页面内用 iframe 并行加载多个笔记 URL，但返回错误"当前知识库由于作者设置，不支持访问"。

**原因**：
- iframe 无法继承主页面的登录态
- biji.com 有跨域限制
- 认证上下文（httpOnly cookie）无法传递给 iframe

**解决**：放弃 iframe 方案，改用逐个打开的方式提取。

**教训**：
- 不要假设 iframe 能继承认证状态
- 先小规模测试方案可行性，再批量执行
- 跨域问题在 SPA 中很常见

## 11. API 直接调用失败（CORS/认证）

**现象**：尝试直接 fetch `knowledge-api.trytalks.com`，但被 CORS 阻止或返回 `{"message":"AppNotFound"}`。

**原因**：
- API 需要认证上下文（httpOnly cookie），JavaScript 无法读取
- 即使拿到 csrfToken，也无法完整认证
- 浏览器直接请求会被同源策略阻止

**解决**：放弃 API 直接调用路线，改用页面导航方式（打开原始笔记页提取内容）。

**关键 API 端点**（仅供参考，不要直接调用）：
- `follow/account/posts` —— 获取关注者的笔记列表
- `topic/post/list` —— 获取单篇笔记详情
- `topic/list/manager` —— 获取知识库笔记列表（博主视图），支持分页参数 `page=1&size=50`

## 12. 滚动侧边栏无效果

**现象**：滚动侧边栏后，DOM 条目数没有增加。

**原因**：biji.com 侧边栏使用 Vue 的虚拟列表实现，不是懒加载。50 条就是全部渲染的 DOM。

**解决**：
- 不要期望通过滚动加载更多
- 如果笔记数接近 50，主动检查博主入口
- 博主入口通常没有数量限制
