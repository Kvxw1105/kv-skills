# Research Notes for Humor Writer

This note distills humor theory, English-language comedy practice, Chinese crosstalk practice, sitcom/sketch patterns, internet meme dynamics, and computational humor findings into operational guidance for the skill.

## 1. Theories worth operationalizing

### Incongruity / resolution
Humor often begins when the audience's expected frame is disrupted and then reinterpreted. In writing terms: setup activates frame A; punchline reveals frame B; the reader enjoys the quick mental reclassification.

Operational use:
- Build a normal reading first.
- Hide a second possible reading.
- Reveal the second reading as late as possible.

### Benign violation
A line becomes funny when it violates a norm but the audience still experiences the violation as safe, acceptable, playful, or psychologically distant.

Operational use:
- Increase violation for edge.
- Increase benign cues for safety: affection, self-targeting, absurdity, obvious exaggeration, distance, consent, or low stakes.

### Superiority and status
Many jokes involve a status drop: a boast collapses, a serious person becomes petty, a machine acts needy, or the speaker exposes their own incompetence.

Operational use:
- Prefer self-status drops or situation-status drops.
- Avoid status attacks on vulnerable targets.

### Relief
Humor can release social pressure around anxiety, awkwardness, workload, embarrassment, or taboo.

Operational use:
- Name the tension lightly.
- Do not deny the real problem.
- Add a small absurd image, then return to the practical point.

### General Theory of Verbal Humor / script opposition
For verbal jokes, a useful linguistic lens is to identify opposing scripts: normal/abnormal, literal/metaphorical, high/low, professional/petty, human/machine, epic/trivial.

Operational use:
- Define the two scripts before writing.
- Choose the logical mechanism that connects them: pun, false analogy, faulty syllogism, literalization, exaggeration, or frame blend.

## 2. English comedy patterns

- **Rule of three**: two beats establish the pattern; the third beat breaks or intensifies it.
- **Deadpan**: the sentence sounds practical while the meaning is absurd.
- **Callback**: a phrase returns later with changed meaning.
- **Game of the scene**: identify the first unusual thing and heighten it logically.
- **Yes-and**: accept the premise and add information rather than cancel the scene.
- **Character commitment**: the funniest line often comes from a character sincerely defending a ridiculous worldview.

## 3. Chinese comedy patterns

- **说学逗唱** is a useful capability map, but for text generation the most transferable parts are 说, 学, 逗: narration, imitation, teasing.
- **包袱** is not a random punchline; it depends on setup, delay, and release.
- **三番四抖** provides a repeat/escalate/release structure.
- **捧哏/逗哏** maps well to dialogue: one voice pushes absurdity, the other voice provides resistance and rhythm.
- **现挂** maps to chat replies: use a detail from the immediate context so the humor feels live.
- **谐音梗** works when the pun is already close to the user's phrase; otherwise it becomes cheap.

## 4. Meme and internet humor

Internet humor depends heavily on shared context. A meme is not just a joke format; it is a cultural unit that spreads, mutates, and gains meaning through repeated use in a community.

Operational use:
- Ask whether the target audience will recognize the reference.
- If not, use meme cadence without requiring meme knowledge.
- Avoid stale, generic meme templates unless the user specifically requests them.

## 5. Computational humor warning

Recent Chinese and cross-lingual humor research repeatedly shows that humor generation and explanation remain difficult for language models, especially culturally dense Chinese humor, crosstalk, homophones, and internet memes. Therefore this skill should force the model to reason through mechanism, audience, and timing instead of directly generating a punchline.

## 6. Design implication for this skill

The skill must make the model answer these questions before writing:

1. Who is laughing with whom?
2. What is being violated?
3. Why is it still safe?
4. What expectation is created?
5. What exact word or image creates the final turn?
6. Which scene constraints limit the joke?
7. Is the output actually sendable by a real person?

## 7. Source map

- Philosophy and theory: Stanford Encyclopedia of Philosophy-style summaries of humor theories; Raskin and Attardo's verbal humor theory; incongruity, relief, and superiority traditions.
- Benign violation: Peter McGraw and Caleb Warren's theory and later discussion.
- Chinese crosstalk: xiangsheng descriptions, 包袱, 说学逗唱, 捧哏/逗哏, 现挂, and crosstalk generation research.
- Computational humor: crosstalk generation papers, Chinese humor understanding datasets, Chinese meme explanation research, and recent script-opposition humor generation work.
- Improv/sketch practice: Second City / UCB-style yes-and, game of the scene, heightening, and character commitment.
