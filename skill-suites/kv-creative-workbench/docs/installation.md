# Installation and release

## ChatGPT

ChatGPT installs one Skill package at a time. Package each directory below independently:

```text
skills/kv-creative-workbench
skills/kv-language-ideation
skills/kv-idea-convergence
skills/kv-business-opportunity-strategist
```

Install all four for the complete workflow. The controller should be installed last when the interface makes installation order visible, although the packages have no filesystem-time dependency on that order.

## Local agents

Local Skill managers can index the mother directory and expose each child directory as an individual Skill. `suite.yaml` is metadata for suite-aware managers; it is not required by ChatGPT runtime.

## Validation

Run the official validator against every child directory:

```bash
python /path/to/skill-creator/scripts/quick_validate.py skills/<skill-name>
```

Package each child separately. Do not upload a ZIP containing multiple `SKILL.md` entrypoints through the single-Skill ChatGPT upload flow.

## Versioning

Increment the suite version when composition contracts, shared schemas, routing rules, or required member versions change. A child Skill may release independently when its public contract remains compatible.
