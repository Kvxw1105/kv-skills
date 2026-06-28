# Automated Workflow: Topic to 小小羊 Comic

## Workflow Goal

Turn any AI/business/knowledge-product topic into a consistent 3-panel or 4-page 小小羊 educational comic.

## Step 1: Intake

Ask or infer:

- Topic
- Target reader
- Desired depth: beginner / practitioner / advanced
- Output count: one page / four-page carousel / long series
- Whether exact Chinese captions are required

If unclear, default to: beginner-to-practitioner audience, 4-page carousel, concise captions.

## Step 2: Concept Compression

Rewrite the topic into one sentence:

“这组漫画要让读者明白：{core_point}。”

Then create a 3-step teaching arc:

1. Common misconception
2. Correct mental model
3. Actionable takeaway

## Step 3: Page Planning

For one page: use 3 panels.

For four pages: use this structure:

1. Basic definition
2. Why it matters / how to use it
3. Advanced mechanism / system view
4. Business or personal application

## Step 4: Script Writing

For every panel, output:

- Visual action
- Props/icons
- Caption
- Optional speech bubble

Keep captions short. Prefer visual metaphors over definitions.

## Step 5: Image Prompt Generation

Convert the script into the Single Page Template or Four-Page Carousel Template in `prompt-templates.md`.

Always include:

- Originality constraint
- Mascot identity
- Layout system
- Panel-by-panel visual description
- Exact captions
- Negative constraints

## Step 6: QA Checklist

Check before generation:

- Is the concept clear without external context?
- Does each panel do one job?
- Are captions short enough?
- Does the prompt maintain the mascot identity?
- Does the prompt avoid copying the reference image too literally?
- Is the output mobile readable?

## Step 7: Iteration Loop

After image generation, inspect:

- Wrong or garbled Chinese text
- Inconsistent eye colors or mascot design
- Overcrowded panels
- Missing captions
- Too much realism
- Excessive similarity to reference

Then run the Quality Repair Prompt with targeted fixes.

## Reusable Agent Command

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
