# Three.js 空间化设计

## 使用原则

Three.js 不是装饰层，而是产品状态的空间表达。

适合：
- 创作工具工作流。
- 品牌入口。
- 数据宇宙。
- 可探索知识空间。

不适合：
- 高频后台操作区。
- 复杂表格。
- 纯信息展示。

## 推荐架构

DOM：标题、表单、按钮、文字。

WebGL：空间、材质、粒子、镜头、沉浸。

同步：
用户动作 → 状态机 → 动画时间轴 → 视觉变化。

## 常用技术

- Three.js Scene / Camera / Renderer。
- ShaderMaterial。
- InstancedMesh。
- GSAP 时间轴。
- CanvasTexture。
- Fresnel 边缘光。
- 降级 Canvas 方案。

禁止只制作发光球、随机粒子背景。
