# Project Pilot

> 给 AI 编码 Agent 的**项目控制层**：让大型、长期、甚至已经混乱的项目始终保持
> **「全局可见 + 单点聚焦」**。

![Version](https://img.shields.io/badge/version-0.8.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Format](https://img.shields.io/badge/format-Agent%20Skills%20%2F%20SKILL.md-orange)
![PRs](https://img.shields.io/badge/PRs-welcome-brightgreen)
![Stack](https://img.shields.io/badge/deps-none-lightgrey)

[English](./README_EN.md) · [可视化指南](./project-pilot-guide.html) · [更新日志](./CHANGELOG.md) · [参与贡献](./CONTRIBUTING.md)

---

## 目录

- [它解决什么问题](#它解决什么问题)
- [核心模型](#核心模型)
- [自适应推进](#自适应推进)
- [每轮导航 HUD](#每轮导航-hud)
- [三种模式](#三种模式)
- [安装](#安装)
- [命令速查](#命令速查)
- [它会在项目里留下什么](#它会在项目里留下什么)
- [状态词汇表](#状态词汇表)
- [证据与知识维护](#证据与知识维护)
- [和其他方案的区别](#和其他方案的区别)
- [仓库结构](#仓库结构)
- [适用场景 / 不适用场景](#适用场景--不适用场景)
- [路线图](#路线图)
- [参考来源与致谢](#参考来源与致谢)
- [许可证](#许可证)

---

## 它解决什么问题

Agent 在长周期项目里失败，通常不是因为写不好代码，而是因为**失去了坐标**：

| 症状 | 本质 |
| --- | --- |
| 做了一堆局部正确的事，但与最终目标脱节 | 局部执行与全局目标断开 |
| 隔几天回来，不知道自己做到哪了 | 没有可恢复的持久状态 |
| 老项目越改越乱，文档说一套代码是另一套 | 声明状态 ≠ 观测状态 |
| UI / API / schema 都在，功能却跑不通 | 假完成（False Completion） |
| 为了一个小问题绕出去，再也回不来 | 绕路没有返回点（Return Target） |
| 进度"感觉做了一半"，但说不出依据 | 进度不是从证据算出来的 |

Project Pilot 不改你的技术栈，也不生成代码。它给 Agent 加一层**项目控制纪律**：
一次只推进一件事，但每一刻都把这件事放回整张地图里显示。

> **One Thing in Context**
> 一次只执行一件事，同时始终显示这件事在整个项目中的位置，以及它如何推动项目前进。

---

## 核心模型

工作被建模成四层稳定层级，进度由叶子节点逐级向上汇总：

```text
PROJECT
└── PHASE
    └── MILESTONE
        └── TASK
            └── STEP   ← 唯一活跃执行点
```

设计要点：

- **高层地图全局可见，细节按需展开**——只深度规划当前或下一个里程碑，避免维护一份 500 步的死计划。
- **只有一个活跃执行点**——后台 Agent 可以并行，但用户面向的主线坐标必须唯一且稳定。
- **进度来自证据**——每个节点的状态必须由构建 / 测试 / 运行时行为等证据支撑，不允许凭感觉填百分比；产品、探索和恢复进度分开统计。

### 自适应推进

每个当前节点先标记工作类型：

- `DELIVERY`：向已接受的产品结果推进；
- `EXPLORATION`：用实验、原型或基准减少关键不确定性；
- `RECOVERY`：恢复可信的基线、验证信号或项目控制面。

下一步由四个属性决定：不确定性、反馈成本、可逆性和耦合度。目标清楚且反馈便宜时做小交付切片；假设未证实且实验便宜时先探索；高耦合、回退昂贵或有安全影响时先定义边界与恢复路径。探索否定了路线也算有效进展，但不会伪装成产品完成度。

---

## 每轮导航 HUD

每一次实质性项目推进，Agent 都会在回答顶部给出固定结构的导航头：

```text
🎯 PROJECT
上线一个可注册、分析财报、生成报告并可收费的 MVP
Overall: 38%

📍 YOU ARE HERE
Discovery → Product Definition → Target User → Step 1/3

🧪 WORK TYPE
EXPLORATION

🧭 WHY THIS MATTERS
目标用户决定数据流程、报告深度和产品边界。先定它可以避免架构提前发散。

🔨 NOW
选择第一类目标用户。

✅ DONE WHEN
- 目标用户写入项目基线
- 能据此定义首个核心用户旅程
```

绕路时额外显示返回点：

```text
↩ RETURN TO
MVP → Dashboard → Chart Rendering → Step 4
```

默认配重：**10–20% 全局定位 + 80–90% 当前工作**。隐藏无关细节，但绝不隐藏目的地和你所在的位置。

---

## 三种模式

| 模式 | 触发时机 | 做什么 |
| --- | --- | --- |
| **BUILD** | 新项目，或状态基本连贯 | `Orient → Map → Select → Align → Act → Verify → Record → Navigate` 循环推进 |
| **RECONCILE** | 怀疑项目在漂移，但还没烂透 | 冻结"未经验证的断言"，比对期望 vs 观测，识别漂移并分级（NORMAL / RECONCILE / RESCUE） |
| **RESCUE** | 老项目接管、严重漂移、反复修不好、计划过期 | 项目考古：`observe → verify → reconstruct → diagnose → rebaseline → stabilize → continue` |

### Rescue 模式的两条硬规矩

1. **先观察，再动手。** 除非是必须立即止血的生产事故且用户明确要求，考古阶段一律只读，不改代码。
2. **从验证过的现实重建基线。** 老计划作为历史保留（移至 `plans/abandoned/`），新基线从今天验证过的现实出发。

Rescue 会按固定优先级止血：

```text
1. 阻止数据 / 安全 / 生产损害
2. 恢复可信的 build / test / CI 信号
3. 收尾危险的半成品功能
4. 解决关键路径上的阻塞
5. 修复项目地图与持久知识
6. 回到产品交付
```

### 漂移检测清单

Rescue 会逐项检查：计划漂移、文档漂移、架构漂移、范围漂移、TODO 漂移、
**假完成**、验证漂移、决策漂移。

---

## 安装

本项目是标准的 [Agent Skills](https://github.com/anthropics/skills) 格式，
必需文件只有 `SKILL.md`；`references/` 与 `examples/` 提供按需读取的模式工作流、状态 schema、病因诊断、证据与知识维护细则。
Skill 本身**无依赖、无构建步骤、无网络调用**。

### Codex CLI

```bash
# 用户级：所有项目可用
git clone https://github.com/ivagill1980/project-pilot.git ~/.codex/skills/project-pilot

# 项目级：随仓库提交，团队共享
mkdir -p .codex/skills
cp -r project-pilot .codex/skills/
```

### 其他 Agent

SKILL.md 是跨 Agent 的通用格式，放到对应目录即可，无需任何修改：

| Agent | 用户级路径 | 项目级路径 |
| --- | --- | --- |
| Codex CLI | `~/.codex/skills/` | `.codex/skills/` |
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| WorkBuddy | `~/.workbuddy/skills/` | `.workbuddy/skills/` |

> 目录名即技能名，目录内必须直接包含 `SKILL.md`。
> 安装后**重启 / 新建会话**，Agent 会重新扫描技能目录。

### 验证

```bash
ls ~/.codex/skills/project-pilot/SKILL.md
```

然后直接对 Agent 说一句人话即可触发，不需要记命令：

- 「接管并梳理一下这个项目」
- 「我乱了」
- 「继续」

---

## 命令速查

全部支持自然语言等价说法，不必记英文。

| 命令 | 作用 |
| --- | --- |
| `继续` / `continue` | 接受当前推荐路径，推进到下一个安全动作 |
| `我乱了` / `where am I?` | **空间恢复**：重建并展示目标、进度、路线、当前坐标、返回点、最近完成项、下一步 |
| `看全局` / `zoom out` | 展示阶段/里程碑级全局地图、风险、关键路径 |
| `看当前` / `zoom in` | 聚焦当前任务与步骤、相关文件、阻塞项、验收门槛 |
| `为什么` / `why` | 只解释当前动作为什么存在、解锁了什么 |
| `我不懂` / `explain simpler` | 用更简单的语言重讲当前步骤，不改计划 |
| `换一个` / `alternative` | 提供最多三条实质不同的路线，含推荐与权衡 |
| `先放着` / `park it` | 丢进 Parking Lot，注意力回到主线 |
| `接管项目` / `rescue` / `梳理项目` | 进入 RESCUE 模式，开始项目考古 |
| `校准` / `reconcile` | 比对期望状态与现实，但不自动重建整张路线图 |
| `重新基线` / `rebaseline` | 从当前现实出发建立新基线 |
| `暂停` / `checkpoint` | 写入检查点，让新会话以最小代价恢复 |
| `今天收尾` / `wrap up` | 跑 Learning Loop：总结、沉淀、更新状态、写检查点、给出干净的再入点 |

决策负担也有规矩：需要决策时，给出**一个推荐默认值 + 最多两个备选**，
说明推荐理由和对地图的影响，`继续` 即可接受。

---

## 它会在项目里留下什么

若项目中尚无等价约定，Skill 会在 `.project-pilot/` 下维护一组持久控制文件：

```text
.project-pilot/
├── STATE.md          # 目标、当前坐标、下一步、健康度
├── MAP.md            # Phase → Milestone → Task → Step 层级与状态
├── HEALTH.md         # 项目控制健康（与产品完成度分开统计）
├── RECOVERY.md       # Rescue 期间的证据、矛盾、稳定化里程碑
├── PARKING_LOT.md    # 暂存灵感，不静默占用主线范围
├── DECISIONS.md      # 决策日志
├── SESSION_LOG.md    # 会话日志
├── plans/
│   ├── active/
│   ├── completed/
│   └── abandoned/    # 老计划作为历史保留，不静默覆盖
└── snapshots/
```

若仓库已有 `AGENTS.md`、`docs/` 等约定，Skill 会优先复用现有结构，不制造重复的 competing 结构。

状态 schema（YAML 摘要）：

```yaml
project:  { name, final_goal, success_criteria, mode, progress_policy, baseline_id, baseline_date, overall_progress, product_progress, exploration_progress, recovery_progress }
location: { phase, milestone, task, step, work_type, return_to }
current:  { purpose, done_when, blockers, assumptions, evidence_required, next_action }
health:   { build, tests, ci, docs_alignment, architecture_alignment }
recent:   { completed, decisions, discoveries, evidence }
```

> 需要把项目状态提交进 Git 就提交；不想污染仓库就加进 `.gitignore`。
> 本仓库的默认 `.gitignore` 忽略了 `.project-pilot/`。

---

## 状态词汇表

进度必须由证据推导，不允许拍脑袋填百分比。

| 标记 | 状态 | 含义 |
| --- | --- | --- |
| ✅ | `VERIFIED` | 有证据证明已完成 |
| ◐ | `PARTIAL` | 已实质实现但未完成 |
| ⚠ | `AT RISK` | 存在但不可靠、正在漂移或被阻塞 |
| ✕ | `BROKEN` | 已知不可用 |
| ○ | `NOT STARTED` | 有意未开始 |
| ? | `UNKNOWN` | 证据不足 |

规则：

- 父节点百分比由子节点汇总，`UNKNOWN` 不得被静默当作已完成。
- 无权重信息时，同层级等权，并明确声明当前采用的权重策略。
- **不知道就写 `UNKNOWN`**，并为影响规划的关键未知建立调查步骤。
- 每个重要完成声明都要记录来源、版本 / 环境 / 场景范围、限制和复验触发条件。
- 运行证据说明“现在发生了什么”，不能单独决定“这是否满足目标”；实现、要求和评价方法要分别检查。

证据优先级（冲突时自上而下）：

```text
运行行为 / 生产证据（用于判断当前行为） > 测试 / CI / 类型检查 / lint > 当前代码与配置
  > 近期已接受的提交 > 已接受的 ADR / 规格 > 维护中的文档 > 旧 roadmap / TODO > 假设与记忆
```

这条顺序只回答“系统现在怎样”。“系统应该怎样”仍由用户当前目标和最新可信的需求 / 验收标准决定；可重复的错误行为不能因为容易观测就被当成正确基线。

## 证据与知识维护

主入口只保留核心约束与交互契约；进入某种模式或需要维护持久知识时，再按需读取对应文件：

- [references/build-mode.md](./references/build-mode.md)：BUILD 模式的 `B0`–`B7`、规划规则、决策负载与验收细则；
- [references/reconcile-mode.md](./references/reconcile-mode.md)：RECONCILE 模式的 `R0`–`R5`；
- [references/rescue-mode.md](./references/rescue-mode.md)：RESCUE 考古 `S1`–`S9`、漂移检测器与触发启发式；
- [references/diagnosis.md](./references/diagnosis.md)：可观察症状 → 病因 → 应对，区分固有障碍与用法错误；
- [references/team.md](./references/team.md)：多人协作与交接：控制状态写给不在场的人看；
- [references/state-schema.md](./references/state-schema.md)：`STATE` / `MAP` / `EVIDENCE` / `HEALTH` / `RECOVERY` / `PARKING_LOT` 字段定义；
- [references/multi-agent.md](./references/multi-agent.md)：后台与并行 Agent 的编排规则；
- [references/output-patterns.md](./references/output-patterns.md)：四种响应形态模板；
- [references/pattern-router.md](./references/pattern-router.md)：内部策略标签（可选，含第三方署名）；
- [references/decision-policy.md](./references/decision-policy.md)：工作类型与推进方式选择；
- [references/evidence-record.md](./references/evidence-record.md)：证据记录、验收样例、门禁可信度、独立复核与冲突报告；
- [references/knowledge-maintenance.md](./references/knowledge-maintenance.md)：事实、假设、决策、临时状态的分类与记忆清理。

`examples/` 存放完整对话案例。

---

## 状态文件：模板与校验

`.project-pilot/` 的字段定义在 `references/state-schema.md`，落地靠脚本而不是靠自觉：

```bash
python scripts/project_state.py init .project-pilot      # 从 templates/ 生成七个状态文件
python scripts/project_state.py validate .project-pilot  # 校验字段、枚举、节点 id、依赖与证据
python scripts/project_state.py progress .project-pilot  # 沿 parent 链把进度汇聚上去
python scripts/project_state.py drift .                  # 扫描仓库：文档死链与过期 TODO
python scripts/project_state.py selftest                 # 用已知好/坏样例自检工具本身
```

校验器把能机械判定的部分变成机制：必填字段与枚举、日期与进度范围、节点 id 唯一、
`depends_on` 目标存在且无环、`parent` 目标存在且不成环、证据记录必须带 `recheck_when`。
其中最关键的一条是**没有证据 id 的 `VERIFIED` 节点直接报错**——进度声明不再能靠感觉填写。

`progress` 则把不变量 3 那句"父进度由子节点算出"真正实现：沿 `MAP.md` 的 `parent` 链建树，
容器取子节点的加权平均（权重规则由 `progress_policy` 决定），`unknown` 子节点不计入均值而非
当成 0，容器自己填的进度若与子节点汇聚结果不符会被告警——**子节点才是事实来源**。
`--json` 供其他工具消费。
退出码 `0` 表示干净，`1` 表示有错；`--strict` 把警告也算错。仅用标准库，Python 3.8+。

---

## 和其他方案的区别

| | TODO / 任务列表 | 一次性规划 Prompt | **Project Pilot** |
| --- | --- | --- | --- |
| 产出 | 任务清单 | 一份文档 | 持续维护的项目控制状态 |
| 全局定位 | 无 | 生成时有，之后消失 | **每轮显示在顶部** |
| 进度来源 | 手动勾选 | 估算 | **证据推导** |
| 中断恢复 | 靠记忆 | 重读文档 | **`我乱了` 一键重建坐标** |
| 老项目接管 | 不适用 | 容易照抄过期文档 | **只读考古 + 重新基线** |
| 范围控制 | 无 | 无 | **Parking Lot + Return Target** |

---

## 仓库结构

```text
project-pilot/
├── SKILL.md                  # 技能本体：Agent 读取的全部指令（唯一必需文件）
├── project-pilot-guide.html  # 中文可视化指南，单文件、零依赖，浏览器直接打开
├── README.md                 # 本文件
├── README_EN.md              # English README
├── CHANGELOG.md              # 遵循 Keep a Changelog
├── CONTRIBUTING.md           # 贡献指引
├── CREDITS.md                # 第三方模式名称归属与上游授权状态
├── references/                # 按需读取：模式工作流、状态 schema、证据与知识维护
│   ├── build-mode.md
│   ├── reconcile-mode.md
│   ├── rescue-mode.md
│   ├── diagnosis.md
│   ├── team.md
│   ├── state-schema.md
│   ├── multi-agent.md
│   ├── decision-policy.md
│   ├── evidence-record.md
│   ├── knowledge-maintenance.md
│   ├── output-patterns.md
│   └── pattern-router.md      # 可选增强：含第三方模式名称署名
├── examples/                  # 完整对话案例
│   ├── greenfield-saas-mvp.md
│   └── brownfield-rescue-ecommerce.md
├── templates/                 # .project-pilot/ 七个状态文件的起步模板
├── scripts/                   # 状态工具：init / validate / selftest（仅标准库）
├── LICENSE                   # MIT
└── .gitignore
```

想先建立直觉，直接打开 `project-pilot-guide.html`：核心模型、HUD、三种模式、
命令、状态文件、对话演示都在里面。

---

## 适用场景 / 不适用场景

**适合**

- 多阶段、长周期、规模较大的项目
- 接手别人（或半年前的自己）留下的 brownfield 项目
- 容易被打断、需要低成本重返的长期工作
- 需要"可信进度"而不是"感觉差不多"的场合
- 多个后台 Agent 并行时的外层编排与收口

**不适合**

- 一次性脚本、单文件小改动
- 纯问答、纯查资料
- 已经很小且完全在脑子里的任务——此时导航头是纯噪音

---

## 路线图

v0.2 已完成：

- [x] 按不确定性、反馈成本、可逆性和耦合度选择交付 / 探索 / 恢复路径
- [x] 为重要完成声明增加可追溯、可复验的证据记录
- [x] 分开产品、探索和恢复进度，明确实现行为与目标要求的冲突
- [x] 增加按需读取的决策、证据和知识维护 reference

v0.3 已完成：

- [x] 常驻核心与按需 reference 分离：模式工作流、状态 schema、输出模板与案例移出 `SKILL.md`
- [x] 验收加固：门禁可信度（新门禁必须先证明能失败）、独立复核、阶段目标对账
- [x] 新增不变量 14：作者态与生成物分离，控制状态入库且不被重建删除

v0.4 已完成：

- [x] 新增 `references/diagnosis.md`：把症状归因到固有障碍或用法错误，再选应对
- [x] HUD 分级：阶段切换用全量，连续微步用三行紧凑头（字段不减少）
- [x] 处置阈值与显式回滚：改前先提交，2–3 次不改善就回退重来
- [x] 评审交接：大交付先做拆分 pass，按可独立评审的单元交付
- [x] 核心规则改为指向目标的正面表述（不变量 2 / 5 / 11 标题同步调整）

v0.5 已完成：

- [x] `templates/` 七个状态文件起步模板，`init` 一条命令生成
- [x] `scripts/project_state.py validate`：字段、枚举、日期、进度、节点 id、依赖环、证据链全部机检
- [x] 无证据的 `VERIFIED` 节点直接报错；通过测试但未证明过门禁能失败会告警
- [x] `selftest`：9 个已知好/坏样例自检校验器本身

v0.6 已完成：

- [x] `references/team.md`：多人协作与交接，控制状态写给不在场的人看
- [x] 学习回路补上"回读"：会话日志不再是只写不读，复发项升级为机制
- [x] 子代理返回契约：有界结果 + 证据指针，不回收原始过程
- [x] 卡住时的两条出路：playground 直接试假设 / 多方案共用同一道门禁
- [x] RESCUE 考古新增历史挖掘（热点与变更耦合），指标只提名、不决定

v0.7 已完成：

- [x] MAP 节点新增 `parent`（层级归属，与 `depends_on` 的次序关系分开）
- [x] `scripts/project_state.py progress`：沿 parent 链汇聚进度，支持 `equal` / `weighted` / `milestone-weighted`
- [x] `unknown` 子节点不计入均值；容器自称的进度与汇聚不符会告警
- [x] 校验器新增：`parent` 必须存在、parent 不成环；selftest 扩到 18 项（含 6 个汇聚算术用例）

v0.8 已完成：

- [x] `drift` 子命令：扫描仓库的文档死链（markdown 链接 + HTML href/src）与过期 TODO
- [x] 精度按"宁可漏报不要误报"调校：TODO 必须是注解而非正文，点号标识符不算路径，引号内数据不算注解
- [x] `references/rescue-mode.md` 新增覆盖表：10 类漂移里哪几类机器可判、哪几类必须人读
- [x] selftest 扩到 33 项（新增 15 个扫描用例，含 5 个反例）

后续方向（欢迎 PR，见 [CONTRIBUTING.md](./CONTRIBUTING.md)）：

- [ ] `.project-pilot/` 各状态文件的可复制模板
- [ ] 可选的 init / 校验脚本，把确定性工作从 Agent 手里卸下来
- [ ] 更细的进度权重策略（关键路径加权）
- [ ] 更完整的中英文命令别名覆盖
- [ ] 更多 Rescue 真实案例与对照样本

---

## 设计意图

Project Pilot 算成功的标准是：

> 用户停一天、一周、甚至一个月再回来，项目叙事不断线；
> 局部工作始终与最终目标保持连接；
> 一个混乱的仓库可以依据验证过的现实重新进入。

它要让一个大项目**感觉可导航**，而不是让它**看起来很小**。

---

## 参考来源与致谢

`references/pattern-router.md`（由 `SKILL.md` 按需引用）中的「模式路由器（Pattern Router）」一节，策略标签来自
[**Augmented Coding Patterns**](https://github.com/lexler/augmented-coding-patterns)（作者 [@lexler](https://github.com/lexler)），
一个关于「用 LLM 开发软件」的模式与反模式集合，在线阅读：<https://lexler.github.io/augmented-coding-patterns/>

本项目**只引用模式名称**作为 Agent 内部的策略索引，未复制、未翻译、未转载其任何正文内容。
完整的引用清单（含每个模式的触发情境与上游链接）见 [CREDITS.md](./CREDITS.md)。

> 📌 **使用范围**：本 skill 定位为个人本地使用，不做二次分发。
> 事实记录：截至 2026-09-02，上游仓库未声明任何许可证（GitHub API `license` 为 `null`，
> 根目录无 `LICENSE` 文件），按 GitHub 服务条款默认**保留全部权利**。
> 归属清单与完整说明见 [CREDITS.md](./CREDITS.md)。

除 `references/pattern-router.md` 与 `references/diagnosis.md` 引用的模式名称外，本项目其余内容
（14 条 Core Invariants、三种模式、`.project-pilot/` 约定、命令集、HUD 格式）
以及 `project-pilot-guide.html` 均为本项目原创。

---

## 许可证

[MIT](./LICENSE) © 2026 Project Pilot contributors

第三方模式名称的归属与上游授权状态见 [CREDITS.md](./CREDITS.md)。
