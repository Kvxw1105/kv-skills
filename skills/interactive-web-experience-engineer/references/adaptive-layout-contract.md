# 自适应布局契约

## 开发前填写

- 最小可用宽度和高度；
- 理想宽高；
- 最大内容宽度；
- 核心区域最低尺寸；
- 是否必须单屏；
- 允许的滚动方式；
- 触控目标下限；
- 非核心内容的隐藏顺序。

## 语义布局模式

按内容空间划分，不按具体设备品牌划分：

- `portrait`：竖屏单列；
- `compact`：紧凑横屏或双区；
- `spacious`：宽屏多区；
- `scroll-safe`：低于最低高度或宽度时保持可用并滚动。

宽度决定宏观区域关系，高度控制密度和安全降级。不得因为矮屏退回一个更高的手机布局。

## 技术规则

- 页面级：Grid、Flexbox、少量 Media Query。
- 组件级：Container Query、`minmax()`、`auto-fit`、`clamp()`。
- 复杂嵌入或单屏游戏：必要时使用 ResizeObserver。
- Grid/Flex 子项设置 `min-width: 0; min-height: 0`。
- 使用 `100dvh` 和 safe-area inset。
- 核心内容不使用 `overflow:hidden`。
- 绝对定位不承担主要布局。

## 统一尺寸标尺

所有组件共享空间、字号和控件令牌。不要让计时器、按钮、卡片分别按无关联的 `vw` 变化。

```css
.app-shell {
  --fit: 1;
  --space: clamp(8px, 1.4cqmin, 18px);
  --control-h: clamp(40px, 6cqmin, 54px);
  --title-size: clamp(24px, 4cqmin, 48px);
}
```

## 降级顺序

减少外边距 → 减少装饰间距 → 缩小非核心文字 → 组件换行 → 区域重排 → 隐藏说明和装饰 → 开启安全滚动。

达到触控和可读下限后禁止继续缩小，更不能整体 `transform: scale()`。

## 诊断顺序

1. 读取真实 viewport 和根容器 rect。
2. 计算顶部、底部、主内容、间距和内边距的最低空间预算。
3. 检查固定宽高、min-size、overflow、flex-shrink、grid 轨道和断点同时命中。
4. 修空间模型，不为单张截图增加特例。
