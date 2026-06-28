# Prompt Templates

## 1. Single Page Template

Use this when generating one page.

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

## 2. Four-Page Carousel Template

Use this when the user wants a series.

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

## 3. Topic-to-Comic Script Template

Use this before image generation.

```text
Topic: {topic}
Audience: {audience}
Goal: explain {concept} in a simple but not childish way.
Mascot: 小小羊, original red-green-eyed lamb.

Return a 3-panel comic script:
1. Misunderstanding / pain point
2. Mental model / mechanism
3. Practical example / takeaway

For each panel, provide:
- Visual metaphor
- Character action
- Props/icons
- Exact caption, max 32 Chinese characters
- Speech bubble text, max 18 Chinese characters if needed
```

## 4. Quality Repair Prompt

Use this after an image is generated and needs refinement.

```text
Revise the generated comic while preserving the existing style, mascot identity, and overall composition.
Fix only these issues: {issues_to_fix}.
Keep: cute hand-drawn pastel style, thick sketchy black outlines, pale mint panels, warm off-white background, 小小羊 with one red eye and one green eye, curled forelock, clean mobile-readable layout.
Do not change: {elements_to_preserve}.
Improve: Chinese text legibility, panel spacing, character consistency, visual clarity, and caption accuracy.
```
