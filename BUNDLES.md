# KV Skills：批量安装与迁移

本仓库是公开 Skill 母库。可使用 `skills` CLI 扫描仓库中的多个 `SKILL.md` 并批量安装。

## 安装到 Codex

```bash
npx skills add Kvxw1105/kv-skills --skill '*' --agent codex --global --yes --full-depth
```

## 同时安装到多个 Agent

```bash
npx skills add Kvxw1105/kv-skills --skill '*' --agent codex --agent claude-code --agent cursor --global --yes --full-depth
```

## 更新

```bash
npx skills update --global --yes
```

## 仓库规则

- 可安装源码统一放在 `skills/`，或组合技母目录下明确的 `skills/` 子目录。
- 组合关系、依赖图和共享协议放在 `skill-suites/` 或 `collections/`。
- 每个 Skill 必须保留独立的 `SKILL.md`。
- 不提交密钥、Cookie、缓存、虚拟环境、测试输出和无再分发许可的资产。

## 总包快照

总包应包含完整源码目录、每个 Skill 的独立 ZIP、`manifest.json`、SHA-256 校验和及 Windows/Linux 安装脚本。GitHub 仓库负责持续更新，总包负责离线迁移和灾备。