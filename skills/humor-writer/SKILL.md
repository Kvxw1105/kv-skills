---
name: humor-writer
description: generate, rewrite, diagnose, and calibrate funny chinese or english text for chat replies, social posts, essays, ads, speeches, sketches, sitcom-style dialogue, stand-up-style bits, crosstalk-inspired banter, meme-style captions, playful roasts, self-deprecating lines, and warm social humor. use when the user asks for humorous, witty, funny, playful, absurd, sharp, teasing, meme-like, deadpan, comedic, or less formulaic writing; when a draft feels stiff, ai-like, too cold, too serious, or not actually funny; or when the user needs multiple humor intensity levels matched to audience, platform, relationship, and risk.
---

# Humor Writer

## Operating principle

Treat humor as engineered social tension, not as decoration. A funny line needs a recognizable reality, a controlled violation of expectation, and a safe landing for the audience. Do not merely add emojis, puns, or "cold jokes" unless that matches the brief.

## Default workflow

1. **Diagnose the scene**
   - Identify language, platform, audience relationship, purpose, persona, risk level, and length.
   - If details are missing, make reasonable assumptions instead of stalling. Only ask a question when the missing context could cause social harm or completely change the output.

2. **Choose the humor engine**
   - Use one or two primary engines from `references/humor-mechanisms.md`: mismatch, reversal, status play, escalation, over-specificity, literalization, callback, analogy, role logic, benign violation, understatement, anti-climax, wordplay, or crosstalk-style misrecognition.
   - Avoid stacking too many engines in a short reply; it makes the joke feel written rather than lived.

3. **Build the joke beat**
   - Anchor: ordinary shared reality.
   - Tilt: a surprising interpretation, status shift, false logic, or image.
   - Button: the last phrase carries the comedic hit. Do not explain the joke afterward.

4. **Calibrate safety and relationship**
   - Prefer punching up, punching sideways, self-deprecation with dignity, or attacking the situation.
   - Avoid demeaning protected traits, private trauma, body shaming, coercive sexual humor, workplace harassment, and humiliation disguised as wit.
   - For public or professional settings, use low-violation humor: observational, self-aware, situational, lightly absurd.

5. **Produce useful variants**
   - Unless the user requests a single answer, give 3-7 variants with labels such as: 温和、欠一点、逗比、毒舌但不冒犯、职场可用、朋友圈感、英文自然版.
   - When rewriting, keep the user's intent and core facts; improve comic timing, specificity, and final-word impact.

6. **Polish against ai-flavor**
   - Avoid template crutches: repeated "不是...而是...", over-neat parallelism, motivational slogans, generic internet slang, excessive emoji, and explaining why a sentence is funny.
   - Prefer concrete nouns, human defects, small embarrassments, timing, and one unexpected image.
   - Make the final line sound like something a person would actually send.

## Task modes

### A. Create a humorous reply
Return several versions by intensity. Make the safest usable version first, then sharper versions.

### B. Rewrite a stiff draft
Keep the message's practical purpose. Remove lecture tone. Add one comic turn near the end rather than sprinkling jokes everywhere.

### C. Generate social or content writing
Use a hook, rhythm, contrast, examples, and a closing button. For long text, use recurring callbacks rather than isolated jokes.

### D. Generate dialogue, sketch, sitcom, or crosstalk-inspired text
Use character logic before jokes. Each character should misunderstand, overcommit, or protect status in a distinct way. For crosstalk-inspired text, use 捧/逗 rhythm, repeated misunderstanding, and 三番四抖 when space allows.

### E. Diagnose why a joke is not funny
Evaluate: target, setup clarity, surprise, safety, specificity, rhythm, final word, cultural reference, and whether the line sounds forced.

## Output templates

For short reply requests:

```markdown
可以这样回：
1. [safe version]
2. [playful version]
3. [sharper version]
4. [absurd version]

我最推荐第 [n] 条，因为 [brief reason].
```

For humor diagnosis:

```markdown
问题不在于不够搞笑，而在于：
- [specific issue]
- [specific issue]

改法：
原句：[draft]
新版：[rewrite]
为什么更好：[one concise explanation]
```

For longer comedy writing:

```markdown
# [title]
[hook with tension]
[escalation through 2-4 concrete beats]
[turn/reframe]
[callback or final button]
```

## References to load when needed

- Load `references/humor-mechanisms.md` for humor types, principles, and writing levers.
- Load `references/scenario-playbook.md` for scene-specific choices, risk levels, and tone mapping.
- Load `references/examples.md` when the user wants examples, variants, or a style demonstration.
- Load `references/research-notes.md` only when the user asks about theory, methodology, or why a humor tactic works.
