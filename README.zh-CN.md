# 人形机器人开发技能集

[English](README.md) · 简体中文

这套技能集面向开发人形机器人和移动操作机器人的工程师。23 个英文 skill 各用一份 Markdown 文档回答一个具体的工程问题，从“夹爪指令在哪一层反了”到“新策略是否值得替换基线”。你可以让 AI 编程助手按步骤排查，也可以在工程评审时直接查阅。

## 如何使用

克隆仓库，按下表找到对应的 skill，把文件路径和待分析的录制、日志或配置交给助手。例如：

> 请按 `skills/robot-takeover-audit/SKILL.md` 检查这段录制。操作员中途接管了两次。请列出哪些连续两步的动作窗口可用于行为克隆，并说明每个接管边界的判断依据。

如果助手支持从本地技能目录自动发现 `SKILL.md`，可以把各个 `robot-*` 文件夹并列复制到该目录，并保留其中的 `references/` 子目录。这样，skill 之间的交叉引用和配套示例都可以正常打开。

## 按工程问题选择 skill

查看[中文技能索引](skills/README.zh-CN.md)，按工程问题找到对应工作流。

| 分类 | Skill 数量 |
| --- | ---: |
| [系统架构、部署与安全](skills/README.zh-CN.md#系统架构部署与安全) | 4 |
| [感知、标定与导航](skills/README.zh-CN.md#感知标定与导航) | 4 |
| [抓取、规划与运动控制](skills/README.zh-CN.md#抓取规划与运动控制) | 3 |
| [遥操作与示教数据](skills/README.zh-CN.md#遥操作与示教数据) | 4 |
| [策略训练与评测](skills/README.zh-CN.md#策略训练与评测) | 2 |
| [机器人平台与端云服务](skills/README.zh-CN.md#机器人平台与端云服务) | 6 |

## 试一个离线示例

[相机几何示例](skills/robot-sensor-calibration/references/geometry-check.md) 只需 Python 3 和标准库即可运行。两个不同深度的三维点可以投影到同一个像素。示例用一个未参与标定的三维参考点，说明怎样发现这类深度误差。

[停机与重启案例](skills/robot-safety-policy/references/stop-restart-cases.md) 提供五段合成事件记录。可以先从“反馈丢失”一例入手：驱动回复了停机请求，但位置反馈在停稳前中断。用这段记录练习判断哪些结论已经有证据，哪些仍需实测。

## 许可证

技能文档和原创示例采用 [MIT 许可证](LICENSE)。链接中的论文、配置和手册由各自的权利人发布。
