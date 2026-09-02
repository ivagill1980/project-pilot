# 参与贡献 / Contributing

感谢你愿意改进 Project Pilot。

这个项目 99% 的内容是**一个 Markdown 文件**（`SKILL.md`），所以贡献门槛极低：
改文字、提想法、补案例，都算贡献。

---

## 三条总原则

1. **这是提示词工程，不是软件开发。** 没有构建、没有测试套件、没有依赖。
   但正因为如此，**每一句话都会被 Agent 当指令执行**，措辞要精确、可判定，避免文学化表达。
2. **加规则之前先问：它是否改变 Agent 的可观察行为？**
   不会改变行为的描述性文字，请放进 `README.md` 或指南页，不要塞进 `SKILL.md`。
3. **`SKILL.md` 越长，被截断和稀释的风险越高。**
   新增大段内容时，优先考虑拆到 `references/` 子文件并在 `SKILL.md` 中按需引用。

---

## 关于外部模式标签（Pattern Router）

`SKILL.md` 的 Pattern Router 一节引用了
[Augmented Coding Patterns](https://github.com/lexler/augmented-coding-patterns)（作者 [@lexler](https://github.com/lexler)）
的模式**名称**作为策略标签。规则：

- ✅ 可以引用名称作为行为策略索引
- ❌ 不得复制、翻译、改写其模式正文、示例或文档
- ❌ 不得把这些标签当作术语输出给用户（它们是 Agent 内部标签）
- 📌 新增任何外部标签时，必须同步更新根目录的 **`CREDITS.md`**（含触发情境与上游链接）
- ⚠️ 上游目前**未声明许可证**（默认保留全部权利）。新增引用前请三思；
  长期方向是逐步替换为自有的策略名称，实现零外部依赖

## 你可以贡献什么

| 类型 | 说明 |
| --- | --- |
| 🐛 行为缺陷 | Agent 没按 SKILL.md 的规矩做（例如绕路没写 RETURN TO、凭感觉填进度） |
| ✍️ 措辞改进 | 指令有歧义、太啰嗦、或太弱导致 Agent 不遵守 |
| 🌏 中英双语 | 命令别名、HUD 文案、错误提示的对齐与补全 |
| 📚 案例 | 真实的新建项目 / 老项目 Rescue 对话样本（**务必脱敏**） |
| 🧩 模板 | `.project-pilot/` 各状态文件的模板 |
| 🔧 工具 | 把确定性工作脚本化（进度汇总、状态校验、drift 扫描） |
| 🎨 指南页 | `project-pilot-guide.html` 的修正与补充（单文件、零依赖，请保持） |

---

## 改动 `SKILL.md` 的流程

1. Fork 本仓库，从 `main` 切分支：

   ```bash
   git switch -c feat/short-description
   ```

2. 只改你真正要改的部分。保持现有章节结构与标题层级不动。
3. 自查清单：

   - [ ] 新规则**可观察**——能说清"Agent 做了什么就算遵守了"
   - [ ] 新规则**可判定**——不含"适当""尽量""视情况"这类无法验证的措辞
   - [ ] 没有和现有 12 条 Core Invariants 冲突；若冲突，请明确指出冲突点
   - [ ] 中英文命令别名成对出现（命令表里出现的新命令，中英都要有）
   - [ ] 没有引入外部依赖、网络调用或构建步骤
   - [ ] 若涉及版本号，同步更新 frontmatter 的 `version` 与 `CHANGELOG.md`

4. 提交信息遵循 [Conventional Commits](https://www.conventionalcommits.org/zh-hans/v1.0.0/)：

   ```text
   feat: add return-target reminder for background agents
   fix: make progress rounding rule unambiguous
   docs: clarify the difference between PARTIAL and AT RISK
   ```

5. 发 PR，并在描述里写清楚：

   - **改动前** Agent 会怎么做（最好附真实对话片段）
   - **改动后** 期望 Agent 怎么做
   - 你如何验证的（实际跑过哪些项目/场景）

---

## 提交新案例

案例放在 `examples/`，一个案例一个 Markdown 文件：

```text
examples/
├── greenfield-saas-mvp.md
└── brownfield-rescue-ecommerce.md
```

每个文件请包含：背景、关键对话片段、Project Pilot 的输出、结果、以及"如果没用它会怎样"。
**脱敏是硬性要求**：公司名、路径、凭据、真实业务数据一律替换。

---

## 安全

如果你发现某个指令会导致 Agent 执行破坏性操作（删库、重写历史、清理工作区、
在无确认的情况下改生产环境），请**不要开公开 issue**，直接通过仓库的
Security Advisory 私下报告。

---

## 许可证

贡献即表示你同意你的代码/文字以本项目相同的 [MIT License](./LICENSE) 发布。
