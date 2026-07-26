# Skill 协作与交接

## 职责边界

- 产品范围、业务冻结、实施顺序：全栈产品升级总导演；
- 产品常识和缺失状态：产品审计；
- 视觉原型、Token、Showcase：UI 艺术总监/设计 Skill；
- HTML/CSS/JS/React/Three.js 实现：前端体验工程；
- 浏览器实测和证据：浏览器审计；
- 单文件预览和交付：预览 Skill；
- 最终假完成检查：清晰镜。

只有实际读取或调用才算联动。不可用时使用本 Skill 内置参考降级，不伪造调用。

## 交接卡

```yaml
handoff:
  project: <name>
  mode: <audit-upgrade/direct-build/prompt-compile>
  primary_user: <user>
  primary_job: <job>
  protected_contracts: [<api/route/auth/data>]
  main_archetype: <A-F>
  visual_thesis: <sentence>
  showcase_routes: [<route1>, <route2>]
  changed_files: [<paths>]
  browser_evidence: [<evidence>]
  tests_run: [<commands>]
  unverified: [<items>]
  rollback: <method>
  pattern_candidates: [<ids>]
```

后续 Agent 优先读取此卡、`.agent/` 和 Git diff，不重新长篇扫描整个项目。
