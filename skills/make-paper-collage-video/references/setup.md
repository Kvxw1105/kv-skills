# Workspace Setup

A native workspace exposes `project:new`, `project:resume`, `project:preview`, and `project:render` in `package.json`. Use it when available.

When no native workspace exists, run the bundled portable bootstrap script from the Skill directory. It creates a writable workspace with project-state templates and a zero-dependency HTML preview path.

```bash
python <skill-root>/scripts/bootstrap_workspace.py \
  --target <absolute-workspace> --slug <slug> --title "<title>"
```

The portable runtime does not silently install npm packages or claim Remotion rendering. If a native renderer is required, install dependencies in the writable workspace and report any network or system blocker exactly.
