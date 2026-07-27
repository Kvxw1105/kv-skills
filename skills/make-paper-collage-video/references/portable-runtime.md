# Portable Runtime

The bundled fallback creates project-state files and a self-contained HTML preview without npm, Remotion, or network access.

It supports:

- schema-v4-like recursive asset/group nodes;
- `free`, `supported-subject`, and `registered-environment` labels;
- normalized keyframe interpolation for x, y, scale, rotation, and opacity;
- local image paths embedded as data URIs when building the preview;
- deterministic project validation and production-state reporting.

It does not provide:

- MP4 encoding;
- Chromium/Remotion equivalence;
- automatic matting or segmentation;
- semantic vision approval;
- provider execution or quota accounting.

State these limits. Use the native repository runtime when full rendering and evidence production are required.
