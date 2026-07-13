---
name: kv-playful-h5-game-designer
description: create, refine, debug, and deliver lightweight mobile-first h5 mini-games and playful learning prototypes through chinese-language direction. use when the user asks to build or improve a small web game, word game, quiz, daily challenge, interactive learning toy, mobile h5 prototype, or reusable interaction system, especially when they care about 小而美 visual design, smooth micro-interactions, phone-screen fit, audio and haptics, dark mode, state correctness, and downloadable html delivery.
---

# 轻趣 H5 游戏设计师

把中文产品想法转成可直接打开试玩、可反复迭代的移动端 H5 小游戏。优先保持轻、快、清楚、好玩，避免把原型堆成复杂平台。

## 工作流

1. 读取完整上下文，提取核心动作、单局时长、失败方式、提示机制、反馈方式、视觉气质、移动端约束与已知 bug。
2. 判断任务类型：
   - 新建：运行 `scripts/scaffold.py`，从 starter 创建可玩的单文件原型。
   - 改版：先读取现有 HTML，保留已经成立的交互，再做局部升级。
   - 排错：复现状态路径，区分视觉 bug、状态 bug、音频解锁问题与视口适配问题。
3. 先完成最短闭环：进入 → 核心操作 → 正误反馈 → 结算。新功能不得破坏这条闭环。
4. 使用中文调度；代码、变量名与技术说明可以使用英文。
5. 完成后必须实际运行或静态检查，并返回可打开的 `index.html` 与完整项目压缩包。

## 设计原则

- 单屏聚焦：一屏只承载一个核心任务。
- 手机优先：常见 360×700、390×844、430×932 视口内无需滚动完成核心操作。
- 低信息密度：功能入口少，视觉层级明确，留白充足。
- 童趣而克制：使用圆形、柔和圆角、轻量动态色彩；拒绝幼稚贴纸堆叠和通用紫色科技风。
- 动效连续：新增、撤回、清空、锁定、答对、答错都应有可追踪的运动路径，避免元素瞬间消失。
- 反馈分层：按键音、状态音、触觉与视觉反馈分别承担不同职责，不要全部使用同一种声音或动画。
- 适度借鉴：学习对标产品的结构、节奏和交互原则；不要复制品牌名、独特文案、素材或整体商业外观。

详细视觉与交互标准见 `references/visual-and-interaction.md`。

## 状态模型硬规则

把以下状态分开维护，禁止共用一个数组后靠下标猜测：

- 用户手动选择的元素
- 系统提示并锁定的元素
- 当前题目状态
- 已完成题目的结果
- 动画临时状态
- 全局资源，例如提示次数、音效开关、主题与大小写模式

撤回单个元素只影响该元素；清空只影响用户手动输入；提示锁定内容不得被撤回或清空。任何删除动画结束后都要清理动画类，防止数据存在但画面不可见。

## 音频与触觉

- 首次用户触摸后再解锁音频。
- 高频按键声保持短促、低延迟、音量稳定。
- 正确反馈要明亮、积极、上扬；错误反馈短、低、克制，避免羞辱感。
- 音频素材必须记录来源与许可，优先 CC0 或自制素材。
- 播放库只解决兼容性，音色由素材决定。
- 网页震动只作为增强层，iOS 可能不支持；不能把关键反馈只放在触觉中。

## 适配与主题

- 使用 `100dvh`、安全区 inset 和高度媒体查询控制布局。
- 日夜模式分别校准背景、文字、槽位、按键、阴影、进度色和动态光效，禁止简单反色。
- 支持跟随系统和手动覆盖，手动选择保存到本地。
- 动态背景优先 Canvas/CSS；只有确有空间交互价值时才引入 Three.js。背景动效不得抢夺注意力。

## 产品克制

开发阶段优先验证理解速度、第一局完成率、平均得分、提示使用、退出点、再次打开意愿与分享意愿。以下内容默认延后：强制登录、商城、金币、复杂等级、课程中心、社区、广告复活、重型 3D、十几项统计。

详细机制与验证方法见 `references/game-mechanics.md` 与 `references/qa-checklist.md`。

## 新建项目

运行：

```bash
python scripts/scaffold.py --out /mnt/data/<project-name>
```

脚本会复制 `assets/starter/index.html` 并生成 README。随后根据用户需求修改生成文件。

## 验收与交付

1. 检查 HTML/CSS/JS 语法和控制台错误。
2. 检查核心状态路径：选择、再次点击撤回、清空、提示、答对、答错、超时、下一题、结算、主题切换。
3. 检查至少三种手机视口，不得依赖纵向滚动完成主操作。
4. 确认单文件可打开；若包含外部资源，同时提供完整目录压缩包。
5. 返回两个链接：`index.html` 和 `.zip`。

## 中文调度示例

- “做一个每天 12 题的拼词 H5，简约、童趣、手机一屏显示。”
- “把这个问答原型做得更小而美，补上音效、震动和黑夜模式。”
- “修复提示字母被撤回后一起消失的状态 bug。”
- “保持现有玩法，重新设计提示系统和结算分享卡。”
- “把这套交互迁移成一个新的成语、古诗或数学速答小游戏。”
