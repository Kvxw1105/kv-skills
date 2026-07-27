# 自适应布局契约（Adaptive Layout Contract）

## 目标

让页面在未知窗口、系统缩放、浏览器侧栏、横竖屏和嵌入式容器中保持可用。禁止针对单张截图连续叠加断点补丁。

## 开发前必须定义

| 项目 | 说明 |
|---|---|
| 核心交互最小宽度 | 低于该宽度时必须换布局或滚动 |
| 核心交互最小高度 | 低于该高度时不得继续硬压缩 |
| 理想宽高 | 计算统一 UI 比例的参考画布 |
| 语义布局模式 | 例如竖屏、紧凑横屏、宽松横屏 |
| 降级顺序 | 留白 → 装饰 → 字号/控件 → 重排 → 隐藏非核心信息 → 滚动 |

## 实现原则

1. **页面级结构由真实容器决定。** 使用 `ResizeObserver` 读取应用容器，而非假设浏览器窗口等于可用区域。
2. **使用语义模式。** 模式由宽度、高度、宽高比和最小空间共同决定，不以某款手机或电脑型号命名。
3. **统一尺寸标尺。** 计时器、按钮、槽位、间距和字号共享一个受限的 `--fit`，不得各自使用无关联的 `vw` 公式。
4. **组件级使用 Container Query。** 组件按自己获得的宽度换列或换行，不依赖整页断点。
5. **Grid/Flex 负责分配空间。** 避免通过绝对定位把主要操作区钉在底部。
6. **设定硬下限。** 可点击控件通常不低于 40–44 CSS px；达到下限后必须重排或滚动。
7. **溢出是安全阀。** 空间不足时允许纵向滚动，严禁重叠、裁切和不可达操作。
8. **断点按内容失效点产生。** Media Query 只负责少量页面级外观或宏观结构，不用于逐项修补。

## 推荐模式选择器

```js
function chooseLayout(width, height) {
  const ratio = width / Math.max(height, 1);
  if (width >= 920 && height >= 460 && ratio >= 1.32) return 'spacious';
  if (width >= 660 && height >= 390 && ratio >= 1.12) return 'compact';
  return 'portrait';
}
```

阈值必须根据项目的真实最小内容预算校准，不得直接照抄。

## 统一比例

```js
const fit = Math.max(
  contract.minFit,
  Math.min(1.08, width / contract.idealW, height / contract.idealH)
);
root.style.setProperty('--fit', fit.toFixed(3));
```

```css
.component {
  --control-h: clamp(40px, calc(46px * var(--fit)), 54px);
  --letter-size: clamp(58px, calc(86px * var(--fit)), 100px);
}
```

## 组件查询

```css
.play-panel { container: play / inline-size; }
.letters { grid-template-columns: repeat(5, var(--letter-size)); }
@container play (width < 500px) {
  .letters { grid-template-columns: repeat(3, var(--letter-size)); }
}
```

## 验收矩阵

至少覆盖：

- 320×568、360×700、390×844、430×932；
- 640×360、800×450、900×600；
- 768×1024、1024×768；
- 1280×720、1366×768、1700×864、1920×1080；
- 浏览器 80%、100%、125% 缩放的等效 CSS 视口；
- 侧栏、开发者工具、地址栏变化和横竖屏切换。

自动检查：横向溢出、元素相交、控件低于下限、核心按钮不可见、文字截断和滚动不可达。
