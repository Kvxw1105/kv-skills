# 单文件预览打包

## Vite 推荐配置

将以下原则合并到项目的 `vite.config.ts`：

```ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  base: "./",
  plugins: [react()],
  build: {
    cssCodeSplit: false,
    assetsInlineLimit: 100_000_000,
    rollupOptions: {
      output: {
        inlineDynamicImports: true,
        manualChunks: undefined,
      },
    },
  },
});
```

注意：

- 单入口项目才能可靠使用 `inlineDynamicImports`。
- 避免运行时动态导入远程资源。
- npm 依赖应被 Vite 打入构建产物，不使用 CDN。
- 字体和图片尽量通过本地 import 引入，使其被内联。

## 打包命令

构建后执行：

```bash
python scripts/make_single_html.py dist 主题名-直接预览.html
python scripts/check_single_html.py 主题名-直接预览.html
```

Skill 的脚本路径可能不同，实际调用时使用该 Skill 目录中的脚本绝对路径。

## 失败处理

若检测到动态 JavaScript 分块：

1. 调整 Vite 配置为单入口内联动态导入。
2. 移除不必要的 `import()`。
3. 重新构建并打包。

若应用确实依赖多个文件、Web Worker、WASM 或浏览器不允许的 `file://` 能力：

- 仍提供一个可打开的降级单文件预览；
- 同时提供完整构建包；
- 明确指出只有哪一项高级能力需要网站环境；
- 不把用户默认引导到命令行。
