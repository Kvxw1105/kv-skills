# Three.js 空间化与高质感实现

## 使用门槛

只有当空间、材质、镜头、实时数据或品牌世界观能显著提升理解和记忆时使用 Three.js。纯信息展示、复杂表格、长表单和后台高频操作优先 DOM。

## 场景设计顺序

1. 先定义空间母题和视觉权威；
2. 将产品状态映射到对象、轨道、镜头和材质；
3. 再选择 Scene、Camera、Geometry、Material、Light 与 Post-processing；
4. 设计移动端、reduced-motion 和失败降级；
5. 最后做性能预算和浏览器验证。

## 成熟技巧

- 使用 Group 管理可独立运动的场景子系统；
- 使用 `InstancedMesh` 渲染重复刻度、节点和碎片；
- 使用 `CanvasTexture` 生成动态文字、标签和程序纹理；
- 使用 ShaderMaterial 实现 Fresnel、溶解、流动、呼吸与状态着色；
- 对摄像机、对象和 Uniform 使用帧率独立插值；
- 控制 DPR、纹理尺寸、粒子数量、透明叠层和 Draw Call；
- 尽量使用单一主光源和少量辅助光，避免满屏 Bloom；
- Three.js 场景与 DOM 共享业务状态，禁止各自维护一套流程。

## 常见失败

- 发光球加随机粒子冒充高级；
- 所有元素持续运动；
- 只为首屏截图服务，实际操作时遮挡和卡顿；
- 加载巨大模型、纹理和字体，却无降级；
- 手机端完整复制桌面场景；
- 把 post-processing 当作材质设计替代品。

## 性能基线

先测真实目标设备。根据设备分级降低 DPR、粒子、细分、阴影、后处理和更新频率。页面不可见时暂停或降频。销毁场景时释放 Geometry、Material、Texture、RenderTarget 和监听器。
