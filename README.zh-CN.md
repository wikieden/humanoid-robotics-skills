# 人形机器人开发技能集

[English](README.md) · 简体中文

这套技能集包含 1 个主入口和 53 个专项，共 54 个英文 skill。专项中有 46 个面向人形机器人与移动操作机器人开发，另有 7 个通用方法，涵盖 Agent 工作流评测与执行、技术教学、交互应用、离线归档、技能分发和技术文档发布。每份 Markdown 文档回答一个具体的工程问题，从“夹爪指令在哪一层反了”到“新策略是否值得替换基线”。你可以让 AI 编程助手按步骤排查，也可以在工程评审时直接查阅。

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

也可以按单包装法只复制 `robot-dev-skills/`，连同其中的 `references/workflows.md` 一并保留。入口优先读取同级安装的专项或你指定的本地仓库。缺少本地文件时，可从固定的 GitHub 提交读取所选指南。完全离线且只有入口副本时，它会指出还需要哪个包。

## 如何使用

克隆仓库，按下表找到对应的 skill，把文件路径和待分析的录制、日志或配置交给助手。例如：

> 请按 `skills/robot-episode-audit/SKILL.md` 检查这段录制。操作员中途接管了两次。请列出哪些连续两步的动作窗口可用于行为克隆，并说明每个接管边界的判断依据。

单独安装时，把选中 skill 的完整文件夹复制到助手的技能目录。保留包内的 `references/`，按当前任务打开对应指南。同级 skill 是可选延伸阅读；整套并列安装时也能离线打开这些链接。[单包资料清单](skills/README.zh-CN.md#单独安装一个-skill)

## 按工程问题选择 skill

查看[中文技能索引](skills/README.zh-CN.md)，按工程问题找到对应工作流。

新增 7 项流程，覆盖动作资产绑定与重定向、生成式仿真环境搭建、关节反馈恢复、多组件升级、端侧视觉调度、机械臂工作空间回归和连续录包。另有四个旧入口并入现有技能，已安装用户可查阅[迁移表](skills/README.zh-CN.md#已安装用户迁移)。

| 分类 | 专项 skill 数量 |
| --- | ---: |
| [系统架构、部署与安全](skills/README.zh-CN.md#系统架构部署与安全) | 9 |
| [感知、标定与导航](skills/README.zh-CN.md#感知标定与导航) | 9 |
| [抓取、规划与运动控制](skills/README.zh-CN.md#抓取规划与运动控制) | 11 |
| [遥操作与示教数据](skills/README.zh-CN.md#遥操作与示教数据) | 6 |
| [策略训练与评测](skills/README.zh-CN.md#策略训练与评测) | 4 |
| [机器人平台与端云服务](skills/README.zh-CN.md#机器人平台与端云服务) | 7 |
| [通用工程方法：Agent 评测与技术学习](skills/README.zh-CN.md#通用工程方法agent-评测与技术学习) | 3 |
| [交互工具与离线归档](skills/README.zh-CN.md#交互工具与离线归档) | 2 |
| [技能分发与技术文档发布](skills/README.zh-CN.md#技能分发与技术文档发布) | 2 |

## 试一个离线示例

[相机几何示例](skills/robot-sensor-calibration/references/geometry-check.md) 只需 Python 3 和标准库即可运行。两个不同深度的三维点可以投影到同一个像素。示例用一个未参与标定的三维参考点，说明怎样发现这类深度误差。

[停机与重启案例](skills/robot-safety-policy/references/stop-restart-cases.md) 提供五段合成事件记录。可以先从“反馈丢失”一例入手：驱动回复了停机请求，但位置反馈在停稳前中断。用这段记录练习判断哪些结论已经有证据，哪些仍需实测。

## 许可证

技能文档和原创示例采用 [MIT 许可证](LICENSE)。链接中的论文、配置和手册由各自的权利人发布。
