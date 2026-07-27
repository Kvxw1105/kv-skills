# 模块 07：DOM 与 WebGL 双层架构

### 适用

需要沉浸式效果，同时又要保持表单、文字、SEO、可访问性和产品可维护性。

### 提示词

```text
采用 DOM + WebGL 双层架构。

DOM 负责：语义文字、导航、按钮、表单、菜单、表格、焦点、键盘与可访问性。
WebGL/Canvas 负责：空间、情绪、复杂可视化、品牌主视觉和状态空间化。

推荐层级：
- z0：Three.js/Canvas；
- z1：暗角、雾、颗粒、扫描线；
- z2：正常页面内容；
- z3：Toast、命令面板、临时过渡对象。

WebGL 默认 pointer-events:none。只有明确需要拾取的对象使用 Raycaster，并为其提供 DOM 等价操作。

不要把整个 UI 画进 Canvas。保证即使 WebGL 不可用，核心内容与操作仍然存在。
```

---
