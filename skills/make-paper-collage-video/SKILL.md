---
name: make-paper-collage-video
description: Create, resume, revise, validate, and deliver editable paper-collage or layered cutout videos with semantic contracts, registered composition groups, rhythmic storyboards, parallax motion, evidence-backed quality checks, and recoverable production state. Use for paper-cutout videos, historical collage, layered illustration, parallax explainers, recurring-character stories, topology-sensitive composites, or any existing project containing production.json. Also use to diagnose whether a result is true articulated cut-paper animation or merely a full AI image being panned or zoomed.
---

# Make Paper Collage Video

Create recoverable layered-video projects while keeping concept, rights, cost, style, and final creative judgment under human control.

## Choose the execution path

1. Inspect the current directory.
2. If `package.json` exposes `project:new`, `project:resume`, `project:preview`, and `project:render`, use the native workspace commands.
3. Otherwise create a writable portable workspace:

```bash
python <skill-root>/scripts/bootstrap_workspace.py --target <absolute-workspace> --slug <slug> --title "<title>"
```

4. Run the portable validator before claiming the project is ready:

```bash
python <skill-root>/scripts/validate_project.py <workspace>/projects/<slug>/project.json
```

5. Build a self-contained HTML preview when native Remotion rendering is unavailable:

```bash
python <skill-root>/scripts/build_preview.py \
  <workspace>/projects/<slug>/project.json \
  --output <workspace>/dist/<slug>/preview.html
```

Never generate inside an immutable Skill cache. Work only in a user-writable directory.

## Preserve the medium boundary

Read `references/code-cutpaper-boundary.md` before choosing the asset strategy.

- **Layered collage** may use complete illustrated masters and registered derivatives for parallax and local movement.
- **Articulated code cut-paper** requires independently movable vector or paper parts, explicit pivots, occlusion order, and local joint motion.
- Do not call a full AI illustration with camera movement “cut-paper animation.”
- If reliable extraction is unavailable, keep the master rigid and reduce local motion rather than inventing damaged layers.

## New-project workflow

### 1. Prepare one compact concept decision

Read `references/planning.md`, `references/approval-gates.md`, and `references/semantic-contracts.md`.

Resolve:

- audience and purpose;
- duration and scene count independently;
- `draft`, `balanced`, or `full-depth` production profile;
- visual language and reusable asset plan;
- provider choices and material cost;
- rights and factual risks;
- whether the project is collage or articulated code cut-paper.

Ask for one explicit approval covering concept, storyboard, budget, and unresolved providers. Do not make paid or external provider calls before approval.

### 2. Lock a rhythmic storyboard

Give the film one arc and one shared motion language. Every scene must have:

- one named blueprint;
- at least three ordered beats;
- a composition plan using `free`, `supported-subject`, or `registered-environment`;
- establish, action/peak, and final proof moments;
- a final proof at or after normalized time `0.82`;
- visible assertions describing what the pixels must prove.

### 3. Lock semantic contracts before critical generation

Classify every asset as decorative, identity-critical, topology-critical, mechanism-critical, or diagram-critical. Critical assets require reusable contracts and named evidence targets.

For coupled assets:

1. create or import one complete master;
2. derive all registered members and masks from the master;
3. preserve canvas, origin, registration id, and source-master id;
4. never generate touching members independently.

### 4. Approve one representative style proof

Create only enough material to judge the style and motion. A coupled proof must use the actual registered group, not a fake masked surrogate. Inspect alpha masks, checkerboard isolates, tight crops, motion-stress frames, and relationship crops.

### 5. Produce in recoverable batches

Use `production.json` as the resume source of truth. Group work by scene, location, or recoverable asset family. Preserve provider provenance and generation attempts. Do not erase rejected or abandoned attempts when quota was consumed.

### 6. Validate both assets and composites

Read `references/quality-motion.md` and `references/project-contract.md`.

An asset passing edge checks does not prove the composite relationship. Review both scopes:

- asset integrity, silhouette, negative space, and background leakage;
- support contact, front occlusion, shared motion, registration alignment, semantic continuity, and final readability.

### 7. Preview, revise, and render

Native workspace:

```bash
npm run project:resume -- <slug>
npm run project:preview -- <slug>
npm run project:render -- <slug>
```

Portable workspace:

```bash
python <skill-root>/scripts/portable_status.py <workspace>/projects/<slug>/production.json
python <skill-root>/scripts/build_preview.py <workspace>/projects/<slug>/project.json --output <workspace>/dist/<slug>/preview.html
```

A portable HTML preview is not an MP4 render. State the renderer actually used. Never report Remotion validation or Chromium rendering unless it was run.

## Resume existing work

1. Read `production.json` once.
2. Continue from `control.mode`, `nextCommand`, or the first remaining work item.
3. Do not repeat approvals already recorded.
4. Preserve unrelated files and Git changes.
5. End only at a human gate, completion, or a genuine blocker with one required action.

## Delivery requirements

Deliver the artifacts that actually exist. Prefer:

- preview or final video;
- contact sheet and proof images;
- `project.json`, `storyboard.json`, and `production.json`;
- quality report and renderer provenance;
- project directory or ZIP.

Separate technical acceptance from creative approval. Local final delivery does not authorize publication.

## Resources

- `references/setup.md` — native and portable workspace setup
- `references/planning.md` — duration, profiles, beats, and proof moments
- `references/approval-gates.md` — human decisions, cost, rights, and publication
- `references/semantic-contracts.md` — identity, topology, mechanism, and diagram contracts
- `references/quality-motion.md` — asset/composite review and motion rules
- `references/project-contract.md` — files, states, composition tree, and validation routing
- `references/code-cutpaper-boundary.md` — collage versus true articulated code cut-paper
- `references/portable-runtime.md` — capabilities and limits of the bundled fallback
- `scripts/bootstrap_workspace.py` — initialize a writable portable workspace
- `scripts/validate_project.py` — deterministic project-contract checks
- `scripts/build_preview.py` — generate a self-contained HTML preview
- `scripts/portable_status.py` — read the current production state
