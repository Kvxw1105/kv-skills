# 模块 18：浏览器验收与防假完成

### 适用

任何 Agent 完成开发后。

### 提示词

```text
不要只看源码。启动项目并用真实浏览器完成定向验收。

至少测试：
1. 首次进入；
2. 核心成功路径；
3. 输入为空或错误路径；
4. 快速重复点击；
5. 完成后再次执行；
6. 桌面和手机；
7. 一个矮屏；
8. 键盘焦点；
9. prefers-reduced-motion；
10. 外部资源失败；
11. 控制台和网络错误；
12. scrollWidth <= clientWidth。

所有结论标记为 observed、reproduced、inferred、existing、regression 或 fixed_verified。

只有实际复测通过，才能写“已修复”。浏览器不可用时，明确写“未进行真实浏览器验收”，不要用静态代码检查冒充实测。
```

---
