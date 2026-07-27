---
name: xuanlight-aesthetic
description: use for translating visual ideas into the xuanlight aesthetic, a low-resolution sacred fantasy style system. trigger when the user asks for xuanlight, oriental ink-wash fantasy, wuxia or xianxia mood prompts, data soulism, sacred light, low-resolution grain, poetic ruins, dreamlike rooms, manga panels, cover or kv prompts, style iteration, or reusable image-generation prompt systems in chinese or english.
---

# Xuanlight Aesthetic

## Core definition

Translate visual ideas into **玄光美学 / Xuanlight Aesthetic**: a visual system built from dark spacious worlds, sacred subtle light, solitary subjects, low-resolution grain, oriental negative space, and poetic restraint.

Use this skill to produce image-generation prompts, style systems, prompt libraries, cover/KV directions, manga-panel directions, and iterative visual branches.

The central sentence is:

> 幽暗天地中，被神性微光照见的孤独灵魂。  
> a solitary soul revealed by sacred subtle light in a dark and spacious world.

## Non-negotiable visual DNA

Preserve most of these traits unless the user explicitly asks otherwise:

- dark base: ink black, deep indigo, blue-gray, cold gray
- sacred light: moon disc, star wheel, heavenly beam, glowing soul-core, window light, distant city light
- solitude: one subject, few subjects, empty scene, or solitary object
- negative space: sparse composition, large breathing room, poetic emptiness
- low-resolution texture: film grain, digital noise, xuan-paper texture, soft blur, scan noise
- soft optical quality: bloom, halation, subtle chromatic aberration, gentle glow
- restrained emotion: quiet, fateful, lonely, sacred, sublime, post-apocalyptic tenderness
- high-end restraint: avoid clutter, overdesign, commercial poster loudness, cheap fantasy effects

## Branch selection

Choose one or combine two branches:

1. **玄光·水墨 / Xuanlight Ink**: oriental ink-wash, paper texture, misty mountains, sparse landscape, moon-white and mist-blue palette.
2. **玄光·仙途 / Xuanlight Pilgrimage**: wuxia/xianxia, cultivator, swordsman, pilgrim, mountain path, destiny light, spiritual journey.
3. **玄光·灵核 / Xuanlight Soulcore**: data soulism, translucent consciousness-form, glowing chest core, memory fragments, ai-age spirituality.
4. **玄光·废墟 / Xuanlight Ruins**: distant city, black reflective water, ruins, afterglow, lonely skyline, gentle end-of-world feeling.
5. **玄光·梦室 / Xuanlight Room**: old room, window light, television glow, memory trace, private dream, intimate quietness.
6. **玄光·漫画 / Xuanlight Panels**: cinematic panels, sequential emotion, sparse dialogue space, consistent light source and grain.

Load `references/branches.md` when branch details matter.

## Standard workflow

1. Identify the requested output type: single image, cover, KV, character concept, scene, series, comic, or style document.
2. Translate the request into xuanlight language:
   - who or what is being revealed by light?
   - what is the sacred light source?
   - what kind of emptiness surrounds the subject?
   - which branch or branch blend is strongest?
3. Decide density:
   - **minimal**: large negative space, few objects, almost no ornament.
   - **balanced**: one clear subject, simple environment, controlled symbolic detail.
   - **narrative**: more scene context, but each frame still has one emotional focus.
4. Produce layered prompts:
   - abstract prompt: reusable style principle.
   - generic prompt: reusable prompt for similar scenes.
   - concrete prompt: directly usable for the current image.
5. Provide chinese and english when useful, especially for image models.
6. Add negative prompts and parameter notes if the user is preparing generation.
7. Suggest iteration directions if the user is exploring a style system.

Load `references/workflows.md` for cover, series, manga, or scale workflows.

## Default output format

Use this format unless a shorter answer is clearly better:

1. **风格判断 / style interpretation**
2. **关键词 / keywords** in chinese and english
3. **抽象版提示词 / abstract prompt**
4. **通用版提示词 / generic prompt**
5. **具体版提示词 / concrete prompt**
6. **负面词 / negative prompt**
7. **参数与比例建议 / parameters and aspect ratio**
8. **可迭代方向 / iteration directions**

Load `references/prompt-library.md` for reusable prompt blocks.

## Aspect ratio rules

- **1:1**: use central, iconic, meditative composition. Good for avatar, square cover, single mood image.
- **4:5 or 9:16**: emphasize vertical destiny axis: sacred light above, subject below. Good for mobile covers, posters, character visuals.
- **16:9 or 21:9**: emphasize distance, horizon, skyline, mountain range, or cinematic scale. Good for KV, banners, worldbuilding scenes.
- **comic panels**: use one emotional beat per panel. Keep light source, grain, palette, and subject identity consistent.

## Avoid list

Actively prevent these failure modes:

- making every image a female swordsman
- cheap xianxia glamour, ornate armor, decorative overload
- generic cyberpunk ui, neon clutter, excessive holograms
- glossy plastic 3d render, over-sharp hd cleanliness
- commercial poster loudness, high saturation, visual crowding
- generic anime face, cute face template, too much facial detail
- losing the sacred light logic or low-resolution sacred texture

## Reference files

- `references/style-principles.md`: visual DNA, color, texture, emotional rules.
- `references/branches.md`: the six branch system and branch risks.
- `references/prompt-library.md`: chinese and english prompt blocks.
- `references/workflows.md`: scale, cover, series, and manga workflows.
- `references/examples.md`: example user requests and output skeletons.
- `references/iteration-log.md`: versioning and evolution template.
