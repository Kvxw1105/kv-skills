# 10-Second Dynamic Comic Video Workflow

Use when the user wants to feed comic pages into a limited AI video model.

## Principle

Do not ask the model to create a full animation. Ask for a moving comic page.

Core phrase: **像一张会动的漫画页，而不是一段动画片。**

## Shared constraints

- Keep original comic style, character identity, and layout.
- Use 2D micro-animation only: blink, slight head tilt, bubble pop, arrows, icon glow, paper flip, caption fade-in.
- Avoid 3D, live action, cinematic camera spins, anime redesign, large body action, random new characters.
- If voice is weak, use subtitles and sound effects; do not rely on long generated speech.

## Video forms

### 三格定型板
Keep the full three-panel page visible. Animate panel 1 first, then panel 2, then panel 3. Each panel gets only one or two small motions.

Timing:
- 0-2s: problem hook
- 2-6s: contrast/conflict
- 6-9s: answer/mental model
- 9-10s: hold final quote

### 漫画自动下滑
Camera reads the vertical page from top to bottom. Use for dense educational pages.

### 重点格放大
Show the full page, then push into the most suspenseful or useful panel.

### 白卷纸张变答案
Use for 白卷羊: blank paper receives a question, transforms into a roadmap or answer sheet.

### 案件推理板
Use for 白卷羊 or night mode: evidence board, red lines, relationship map, clues, concept nodes.

### 低帧率掉帧动态漫
Use deliberate limited animation, 8-12 fps feeling, hand-flip comic rhythm, hold frames between poses. This is a style choice, not broken-video glitch.

## Segment prompt skeleton

```text
Generate a 10-second vertical 2D dynamic comic video based on the provided comic image. Strictly preserve the original hand-drawn comic style, character design, colors, and layout. Make it feel like a moving comic page, not a full animation.

0-2s: {hook_motion}
2-6s: {conflict_motion}
6-9s: {answer_motion}
9-10s: hold on {final_text}

Only animate: blinking, small gestures, speech bubbles, arrows, icons, paper, light glow, slight camera push. No 3D, no live action, no cinematic redesign, no random character changes, no unreadable Chinese text.
```
