# 小小羊讲AI：风格提示词、设计思路与自动工作流

## 1. 风格倒推

这类图的核心不是“画得复杂”，而是“用极低视觉负担解释一个抽象概念”。它的风格由五个层面组成：

1. **画风**：手绘感、粗黑线、轻微抖动线条、低细节、软萌角色。
2. **版式**：竖版 9:16，顶部标题，中间 3 个横向分镜，每格下方一句解释。
3. **配色**：暖白背景，浅薄荷绿分镜底色，黄色星星/强调，柔和红绿蓝点缀。
4. **叙事**：先误解，再机制，最后例子/结论。
5. **传播性**：一眼能懂，字幕短，图标多，信息密度低，适合手机滑动阅读。

## 2. 小小羊角色设定

- 名字：小小羊
- 形象：原创白色小羊，圆润、柔软、弱攻击性。
- 识别点：一只红眼，一只绿眼；头顶一撮卷毛；小脸有淡淡腮红。
- 气质：好奇、认真、会解释复杂概念。
- 禁区：不要直接复制喜羊羊或任何现有 IP 的五官、角、衣服、比例和标志性姿态。

## 3. 单页通用提示词

```text
Create an original Chinese educational comic page inspired by the provided reference style, but do not copy any exact character, layout, caption, logo, or branding.

Style: cute hand-drawn pastel social-media explainer comic, thick slightly wobbly black outlines, warm off-white background, pale mint/teal horizontal panel boxes, soft flat colors, tiny yellow stars, dotted arrows, simple icons, lots of white space, mobile-readable composition.

Main character: an original cute lamb named 小小羊. White fluffy wool, curled forelock, one red eye and one green eye, small blush, rounded body, soft cute expression. Keep the character consistent and clearly original, not a copy of any existing cartoon IP.

Page format: vertical 9:16. Top cloud title bubble: “小小羊讲AI”. Small yellow pill label: “第{page_number}页 / 共{total_pages}页”. Subtitle: “{topic_title}”. Use 3 stacked horizontal mini-scenes. Each scene sits inside a pale mint/teal rectangular panel. Place a short Chinese caption under each scene. Make Chinese text legible.

Topic: {topic_title}
Teaching point: {core_explanation}

Scene 1: {scene_1_visual}
Caption 1: “{caption_1}”

Scene 2: {scene_2_visual}
Caption 2: “{caption_2}”

Scene 3: {scene_3_visual}
Caption 3: “{caption_3}”

Negative constraints: no phone screenshot UI, no watermark, no photorealism, no cluttered background, no copied reference character, no dense paragraphs, no tiny unreadable Chinese text.
```

## 4. 四页组图通用结构

```text
Create a 4-page Chinese educational comic carousel called “小小羊讲AI”. The pages must share the same original mascot, palette, page structure, line style, and caption voice.

Global style: cute hand-drawn pastel webcomic, thick sketchy black outlines, warm off-white background, pale mint/teal panels, soft flat colors, small stars, arrows, dotted lines, simple AI/business icons, clear mobile readability.

Mascot: 小小羊, an original white fluffy lamb with curled forelock, one red eye and one green eye, small blush, rounded body. Consistent across all pages. Do not copy any existing cartoon IP.

Page 1 topic: {page_1_topic}
- Panel 1: {p1_panel1_visual}; Caption: “{p1_caption1}”
- Panel 2: {p1_panel2_visual}; Caption: “{p1_caption2}”
- Panel 3: {p1_panel3_visual}; Caption: “{p1_caption3}”

Page 2 topic: {page_2_topic}
- Panel 1: {p2_panel1_visual}; Caption: “{p2_caption1}”
- Panel 2: {p2_panel2_visual}; Caption: “{p2_caption2}”
- Panel 3: {p2_panel3_visual}; Caption: “{p2_caption3}”

Page 3 topic: {page_3_topic}
- Panel 1: {p3_panel1_visual}; Caption: “{p3_caption1}”
- Panel 2: {p3_panel2_visual}; Caption: “{p3_caption2}”
- Panel 3: {p3_panel3_visual}; Caption: “{p3_caption3}”

Page 4 topic: {page_4_topic}
- Panel 1: {p4_panel1_visual}; Caption: “{p4_caption1}”
- Panel 2: {p4_panel2_visual}; Caption: “{p4_caption2}”
- Panel 3: {p4_panel3_visual}; Caption: “{p4_caption3}”

Generate pages as separate images, not one crowded poster.
```

## 5. 自动工作流

```text
你是“小小羊讲AI”漫画工作流。
请把我给你的主题转成一组原创中文教育漫画。
工作流程：
1. 先压缩主题，写出这组漫画真正要讲清楚的一句话。
2. 再设计3段式讲述：误区/痛点 → 机制/模型 → 例子/行动。
3. 输出每页的分镜脚本：画面、道具、角色动作、字幕、气泡文字。
4. 再输出可直接给图像模型使用的完整提示词。
5. 最后用清单检查：风格一致、角色一致、文字够短、构图不拥挤、与参考图相近但不照搬。

固定风格：竖版9:16，暖白背景，浅薄荷绿横向分镜，粗黑手绘线条，柔和扁平色，少量星星/虚线箭头/图标，中文短字幕。
固定主角：原创小羊“小小羊”，白色绒毛，头顶卷毛，一只红眼一只绿眼，圆润可爱，不能照搬任何现有卡通IP。
```
