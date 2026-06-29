# Prompt Templates

## Bright comic page template

```text
Create an original Chinese educational comic page. Keep it in a cute hand-drawn 2D knowledge-comic style: warm off-white paper background, pale mint horizontal panels, thick slightly wobbly black outlines, soft flat colors, small stars/arrows/icons, clean mobile-readable Chinese text.

Character: {character_spec}
Series title: “{series_title}”
Page badge: “{page_number}/{total_pages}”
Subtitle: “{subtitle}”
Format: vertical 9:16, three stacked horizontal mini-panels. Put one short Chinese caption under each panel.

Panel 1: {panel_1_visual}
Caption 1: “{caption_1}”
Panel 2: {panel_2_visual}
Caption 2: “{caption_2}”
Panel 3: {panel_3_visual}
Caption 3: “{caption_3}”

Bottom takeaway: “{takeaway}”
Negative constraints: no 3D, no photorealism, no dense paragraphs, no watermark, no phone screenshot UI, no copied IP, no tiny unreadable Chinese text, preserve character identity.
```

## Four-page carousel arc

```text
Create 4 separate vertical 9:16 Chinese educational comic pages. Use the same character, title system, palette, panel structure, and caption voice across all pages.

Page 1: hook / pain point.
Page 2: misconception / why it fails.
Page 3: method / workflow / mental model.
Page 4: summary / checklist / shareable quote.
```

## Character-specific prompt snippets

白卷羊:
```text
白卷羊, original white fluffy sheep, curled forelock, one green eye and one red eye, light blush, soft rounded body, holding a pen/blank page/scroll, smart warm explainer. Do not call it 小小羊.
```

懒团团:
```text
懒团团, original cloud-like white fluffy sheep/团子, soft round body, warm tea-brown half-lidded eyes with visible eye whites and small highlights, lazy-smart smirk, black coffee mug, remote/device, green beanbag, blue workflow arrows. Do not use pure black hollow eyes, no red-green heterochromia, no random green eyes, no horror feeling.
```

灰策狼:
```text
灰策狼, original gray strategist wolf, green eyes, monocle with gold chain, white shirt, dark vest, green tie, strategy notebook, calm sharp result-oriented business temperament. Cute but not childish, not scary.
```

## Dark poster template

```text
Create a dark high-tension poster for the AI三反骨 universe. Use deep black background, red/blue energy strokes, gritty hand-drawn sketch lines, brush splatter, tech/data motifs, arrows, charts, and dramatic promotional poster energy.

Composition: {c_position_character} is center C-position, largest and most dominant. Place {left_character} left and {right_character} right as supporting characters. Match bottom labels exactly to left-center-right positions: {left_label} / {center_label} / {right_label}. Keep all characters recognizable.

Main title: “AI三反骨”. Use no long text. Keep safe margins for cover/background use.
```

## Repair prompt

```text
Revise the generated image while preserving composition and style. Fix only: {issues}. Preserve: {preserve}. Improve: character consistency, Chinese text clarity, panel spacing, and mobile readability.

For 懒团团 specifically, enforce warm tea-brown half-lidded eyes with visible eye whites; remove pure black hollow eyes and random green/brown switching.
```
