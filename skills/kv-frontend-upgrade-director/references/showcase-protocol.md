# Showcase 驱动升级

## 为什么先做 Showcase

大型项目直接全站改造会放大错误方向、CSS 污染和回归。先完成两个代表页面，用最小成本验证视觉系统、组件状态、密度和响应式。

## 两个代表页面

1. **表达页**：品牌入口、登录、核心任务或结果页。验证视觉母题、首屏、CTA 和情绪。
2. **效率页**：高密度工作台、列表、表单或编辑器。验证 Shell、共享组件、状态、键盘和信息密度。

## Showcase 必须覆盖

- 桌面与 390px 手机；
- 浅色与深色（若产品支持）；
- 默认、hover、active、focus-visible、disabled、loading、success、error、destructive；
- 加载、空、失败和恢复；
- 一条核心成功路径。

## 扩散顺序

视觉 Token → Application Shell → 共享组件 → Showcase → 浏览器验证 → 扩散共享页面 → 定向回归。

不要逐页面贴补丁。相同问题优先修 Token、组件或布局骨架。
