---
name: ai-comic-style
description: create and refine cute chinese educational comic image prompts and multi-page visual scripts for ai/business explainer content. use when the user wants to reverse-engineer or reproduce a consistent hand-drawn pastel comic style from reference images, generate prompts for image models, build a recurring comic series mascot, create social-media carousel pages, or turn topics such as ai basics, prompt engineering, agents, context, loop, harness, opc, personal company, and knowledge products into short comic panels.
---

# AI Comic Style

## Core Output
Produce a complete comic-generation package, not only a loose image prompt.

For each request, return:
1. **Series concept**: topic, target reader, core teaching point.
2. **Visual system**: mascot, page layout, color palette, line style, icon language.
3. **Panel script**: one idea per panel, with action, object, and caption.
4. **Image prompt**: ready to paste into an image generation model.
5. **Quality checklist**: checks for text legibility, character consistency, and originality.

Use `references/design-system.md` for style rules and `references/prompt-templates.md` for prompt structures.
Use `references/workflow.md` when the user asks for an automated or repeatable workflow.

## Style Principle
Create work that is close in feeling to a cute, hand-drawn Chinese social-media explainer comic, but clearly original. Do not copy exact characters, account branding, page numbers, captions, compositions, or distinctive IP. Describe style through general traits: sketchy black outlines, pale mint panels, warm off-white background, cute mascot, simple icons, and short captions.

## Character System
Use a recurring mascot when requested. For the user's current series, use:
- Name: 小小羊
- Species: original cute lamb
- Identifiers: white fluffy wool, curled forelock, one red eye, one green eye, rounded body, small blush, expressive but simple face
- Avoid: exact 喜羊羊 design, horns, costume copying, or any named IP likeness

Keep the mascot consistent across pages by repeating the same identifiers in every page prompt.

## Page Structure
Default to a vertical 9:16 social-media comic page with:
- Top title bubble
- Page label such as `第1页 / 共4页`
- Topic subtitle
- Three horizontal mini-scenes
- Short Chinese caption below each scene
- Pale mint/teal rectangular stage panels
- Thick, slightly wobbly black outlines
- Soft flat colors, tiny stars, arrows, dotted lines, simple icons

For multi-page carousels, keep the title, mascot, palette, and layout stable while changing topic and scene content.

## Content Strategy
Make abstract AI ideas concrete through analogy and action.

Prefer this structure:
1. Misunderstanding or pain point
2. Simple mechanism or mental model
3. Practical example or takeaway

For AI/business topics:
- AI basics: black box → prediction/context → clear input improves answer
- Prompt engineering: vague request → role/goal/format/constraints → useful answer
- AI Agent: chat assistant → tools/context/memory/execution → context-loop-harness
- OPC/personal company: solo workload → AI mini-team → productized knowledge/result

## Text Rules
Chinese text must be short and large enough to read. Use captions under panels instead of dense text inside bubbles when possible.

Recommended limits:
- Main title: 4-8 Chinese characters plus optional English term
- Panel caption: 18-32 Chinese characters
- Speech bubble: 6-18 Chinese characters
- Detailed bubble: only if essential; break into 2-4 short lines

If image text accuracy matters, provide both:
1. a visual prompt with minimal text, and
2. a post-edit text overlay plan listing exact final copy.

## Prompt Assembly
When writing the final image prompt, include these blocks in order:
1. Role and task: create original Chinese educational comic page.
2. Style reference: hand-drawn pastel webcomic traits, not copied.
3. Mascot specification.
4. Page layout specification.
5. Topic and teaching logic.
6. Panel-by-panel scenes and exact captions.
7. Negative constraints: no phone UI, no watermark, no copying exact reference character, no clutter, legible text.

## Quality Checklist
Before finalizing, check:
- The mascot is recognizable and consistent.
- The topic can be understood without external explanation.
- Every panel has one clear action or metaphor.
- Captions are concise and not generic.
- The generated image prompt asks for original composition, not direct imitation.
- Visual density is low enough for mobile viewing.
- Chinese text is short enough for image models to render.
