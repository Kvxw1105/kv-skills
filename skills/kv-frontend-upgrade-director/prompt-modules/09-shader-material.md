# 模块 09：Shader 与材质强化

### 适用

模型形状普通，希望通过材质和光感提升质感。

### 提示词

```text
不要依赖增加模型数量来制造复杂度。通过材质层次、Shader 和光源建立体积感。

可使用：
- 顶点噪声或正弦扰动表现呼吸、能量、液体或生长；
- Fresnel 表现边缘光、半透明灵体和能量壳；
- 两到三种受控颜色混合；
- 局部纹路、扫描线、溶解阈值；
- 实体层 + 线框层 + Sprite 光晕；
- ACESFilmicToneMapping 与正确色彩空间；
- 少量雾和景深强化空间。

Uniform 必须映射到真实状态，例如 progress、power、error、success、voiceEnergy、scrollPhase。避免永远只按时间循环。

高亮区域保持有限。禁止满屏 Bloom、过曝白光、塑料感高反射和廉价赛博霓虹。
```

---
