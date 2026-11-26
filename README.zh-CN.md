# 人形机器人开发技能集

[English](README.md) · 简体中文

这套技能集包含 1 个主入口和 59 个专项，共 60 个英文 skill。专项中有 52 个面向人形机器人与移动操作机器人开发，另有 7 个通用方法，涵盖 Agent 工作流评测与执行、技术教学、交互应用、离线归档、技能分发和技术文档发布。每份 Markdown 文档回答一个具体的工程问题，从“夹爪指令在哪一层反了”到“新策略是否值得替换基线”。你可以让 AI 编程助手按步骤排查，也可以在工程评审时直接查阅。

## 用一个入口调用整套技能

从仓库根目录运行下面的命令，把主入口链接到 Codex 和 Claude Code 的用户级目录。请将仓库保存在固定位置。两个助手都从同一份本地仓库按需读取专项及其配套资料，读取这些文件无需联网。

```sh
(
  set -e
  entry="$PWD/skills/robot-dev-skills"
  test -f "$entry/SKILL.md"
  for skills_dir in "$HOME/.agents/skills" "$HOME/.claude/skills"; do
    mkdir -p "$skills_dir"
    target="$skills_dir/robot-dev-skills"
    if [ -e "$target" ] || [ -L "$target" ]; then
      printf 'Already present: %s\n' "$target"
    else
      ln -s "$entry" "$target"
    fi
  done
)
```

新开会话后，在 Codex 输入 `$robot-dev-skills 把这段动捕迁到短腿机器人，支撑脚为什么会滑？`，在 Claude Code 输入 `/robot-dev-skills 把这段动捕迁到短腿机器人，支撑脚为什么会滑？`。入口会读取动作重定向指南，再根据你提供的素材处理问题。

[主入口触发回归用例](tests/robot-dev-skills/cases.md)列出了每个专项的显式问法和自然问法。跨领域问题若希望按本技能集处理，可直接带上入口名，再写现场现象、已有证据和要做的判断。

[专项算法复核](tests/robot-dev-skills/method-checks.md)收录了运动、导航、感知和策略开发的 8 组反例，附原始来源、复跑命令和实测结果。

[机器人资产导入与物理验收](skills/robot-sim-asset-validation/SKILL.md)检查转换后的运动学与物理行为。[仿真故障注入与归因](skills/robot-sim-fault-injection/SKILL.md)先验证故障是否实际生效，再评估恢复。

也可以按单包装法只复制 `robot-dev-skills/`，连同其中的 `references/workflows.md` 一并保留。入口优先读取同级安装的专项或你指定的本地仓库。缺少本地文件时，可从固定的 GitHub 提交读取所选指南。完全离线且只有入口副本时，它会指出还需要哪个包。 晚于固定提交新增的专项，需要使用含该专项的本地仓库，或提供已发布版本的完整提交号。

## 如何使用

克隆仓库，按下表找到对应的 skill，把文件路径和待分析的录制、日志或配置交给助手。例如：

> 请按 `skills/robot-episode-audit/SKILL.md` 检查这段录制。操作员中途接管了两次。请列出哪些连续两步的动作窗口可用于行为克隆，并说明每个接管边界的判断依据。

单独安装时，把选中 skill 的完整文件夹复制到助手的技能目录。保留包内的 `references/`，按当前任务打开对应指南。同级 skill 是可选延伸阅读；整套并列安装时也能离线打开这些链接。[单包资料清单](skills/README.zh-CN.md#单独安装一个-skill)

## 按工程问题选择 skill

查看[中文技能索引](skills/README.zh-CN.md)，按工程问题找到对应工作流。

新增 7 项流程，覆盖动作资产绑定与重定向、生成式仿真环境搭建、关节反馈恢复、多组件升级、端侧视觉调度、机械臂工作空间回归和连续录包。另有四个旧入口并入现有技能，已安装用户可查阅[迁移表](skills/README.zh-CN.md#已安装用户迁移)。

| 分类 | 专项 skill 数量 |
| --- | ---: |
| [系统架构、部署与安全](skills/README.zh-CN.md#系统架构部署与安全) | 11 |
| [感知、标定与导航](skills/README.zh-CN.md#感知标定与导航) | 9 |
| [抓取、规划与运动控制](skills/README.zh-CN.md#抓取规划与运动控制) | 12 |
| [遥操作与示教数据](skills/README.zh-CN.md#遥操作与示教数据) | 6 |
| [策略训练与评测](skills/README.zh-CN.md#策略训练与评测) | 7 |
| [机器人平台与端云服务](skills/README.zh-CN.md#机器人平台与端云服务) | 7 |
| [通用工程方法：Agent 评测与技术学习](skills/README.zh-CN.md#通用工程方法agent-评测与技术学习) | 3 |
| [交互工具与离线归档](skills/README.zh-CN.md#交互工具与离线归档) | 2 |
| [技能分发与技术文档发布](skills/README.zh-CN.md#技能分发与技术文档发布) | 2 |

## 机器人递归自改进（RSI）

在外部开发任务上重复 R1–R3。候选通过独立验证，就成为下一轮父版本；候选在必须保留的任务上退化，就沿用父版本；证据不足，就补采能区分不同解释的观测或纠正动作。

| 阶段 | 怎么做 | 进入下一步的依据 |
| --- | --- | --- |
| R0 · 审计来源 | 确定父版本，追溯数据、权重、提示词和恢复逻辑的来源。选样前，以完整录制或布局为单位划分开发、独立验证和封存验收数据。 | 记录每份数据允许的用途、此前是否参与调优或选版，以及尚待核实的来源。 |
| R1 · 定位失败 | 在外部任务上运行父版，依次检查观测、子目标、提议动作、实际指令、物理结果和评分。分别统计到达各阶段的局数和其中通过的局数。 | 找出首次分歧，设计一个从相同状态出发、能推翻当前归因的对照实验。[失败归因](skills/robot-rsi-failure-attribution/SKILL.md) |
| R2 · 生成候选 | 针对策略实际遇到的状态采集专家标注，把观测结果归到实际执行的动作。按归因更新规划器、动作策略或执行逻辑中的一项，记录预算。 | 交付可复现的候选、父版本和改动依据。[纠正数据设计](skills/robot-rsi-correction-design/SKILL.md) · [策略训练](skills/robot-policy-training/SKILL.md) |
| R3 · 决定是否继承 | 父版和候选在相同预算下做独立配对试验，分别统计新增成功和旧任务退化，按事先约定的收益与保留门槛判断。跨轮定期与同一固定基线比较。 | 决定继承候选、保留父版或补充证据。被拒绝的候选也保留记录。[配对评测](skills/robot-policy-eval/SKILL.md) · [候选晋级](skills/robot-rsi-candidate-promotion/SKILL.md) |
| R4 · 验证迁移并冻结 | 核对目标本体的相机坐标系、动作单位、控制频率和每局重置行为。把基线与候选的权重、提示词、工具、恢复逻辑、控制器和运行环境一起冻结。 | 为实际进入验收的两套系统保存版本清单，并在新进程中验证重载。 |
| R5 · 封存验收 | 首次验收前锁定指标和失败处理方式，完整保留成功、失败与干预记录。分别报告仿真、实机和官方成绩。 | 给出冻结系统的迁移结果。RoboDojo 禁止使用其布局上的 rollout 反馈迭代调优。[官方评测协议](https://robodojo-benchmark.com/leaderboard/protocol?lang=en) |

## 试一个离线示例

[相机几何示例](skills/robot-sensor-calibration/references/geometry-check.md) 只需 Python 3 和标准库即可运行。两个不同深度的三维点可以投影到同一个像素。示例用一个未参与标定的三维参考点，说明怎样发现这类深度误差。

[停机与重启案例](skills/robot-safety-policy/references/stop-restart-cases.md) 提供五段合成事件记录。可以先从“反馈丢失”一例入手：驱动回复了停机请求，但位置反馈在停稳前中断。用这段记录练习判断哪些结论已经有证据，哪些仍需实测。

## 许可证

技能文档和原创示例采用 [MIT 许可证](LICENSE)。链接中的论文、配置和手册由各自的权利人发布。
