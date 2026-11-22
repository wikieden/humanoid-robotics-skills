# 人形机器人开发技能集

[English](README.md) · 简体中文

这套技能集面向开发人形机器人和移动操作机器人的工程师。14 个英文 skill 各用一份 Markdown 文档回答一个具体的工程问题，从“夹爪指令在哪一层反了”到“新策略是否值得替换基线”。你可以让 AI 编程助手按步骤排查，也可以在工程评审时直接查阅。

## 如何使用

克隆仓库，按下表找到对应的 skill，把文件路径和待分析的录制、日志或配置交给助手。例如：

> 请按 `skills/robot-takeover-audit/SKILL.md` 检查这段录制。操作员中途接管了两次。请列出哪些连续两步的动作窗口可用于行为克隆，并说明每个接管边界的判断依据。

如果助手支持从本地技能目录自动发现 `SKILL.md`，可以把各个 `robot-*` 文件夹并列复制到该目录，并保留其中的 `references/` 子目录。这样，skill 之间的交叉引用和配套示例都可以正常打开。

## 按工程问题选择 skill

| 你要解决的问题 | 对应 skill |
| --- | --- |
| 机器人伸手时感知进程重启，谁负责保持平衡，谁仍有权向机械臂下发指令？ | [人形机器人 ROS 2 架构设计与审查](skills/robot-ros2-architecture/SKILL.md) |
| 每个 Pod 能访问哪些设备和 ROS 2 通信流？替换 Pod 后，队列里的旧指令会怎样？ | [ROS 2 Pod 部署与环境隔离](skills/robot-ros2-pod-deployment/SKILL.md) |
| 板端已受理命令，反馈在哪一层中断了？ | [嵌入式 Linux 与 MCU 联调](skills/robot-embedded-bringup/SKILL.md) |
| 操作员扣动左手扳机，夹爪或机械臂的动作为什么反了？ | [双臂遥操作与映射验证](skills/robot-teleop-bringup/SKILL.md) |
| 哪些录制能被训练加载器读取？当前数据划分能检验哪种泛化能力？ | [遥操轨迹与训练集验收](skills/robot-episode-audit/SKILL.md) |
| 一段混合录制中，哪些动作确实来自接管的操作员？ | [人工接管与专家动作标签验收](skills/robot-takeover-audit/SKILL.md) |
| 任务失败后，该补数据、训练策略，还是修复执行逻辑？ | [VLA、WAM 训练与递归自改进](skills/robot-policy-training/SKILL.md) |
| 控制器能否在当前动作执行完之前收到下一段可用动作？ | [机器人策略评测](skills/robot-policy-eval/SKILL.md) |
| 相机支架转动时，静止目标在机器人坐标系里的位置为什么变了？ | [相机到机器人的外参标定](skills/robot-sensor-calibration/SKILL.md) |
| 抓取目标有偏差，问题出在图像、深度，还是坐标变换？ | [RGB-D 感知与位姿验证](skills/robot-rgbd-pose/SKILL.md) |
| 导航未到点，定位、规划、跟踪和底盘反馈中哪一步最先出现偏差？ | [建图与导航回放](skills/robot-navigation-replay/SKILL.md) |
| 擦拭没有生效，是策略选线有误，还是执行时失去了接触？ | [运动控制与强化学习验证](skills/robot-motion-validation/SKILL.md) |
| 界面显示任务完成，是谁上报的？设备实际做到了哪一步？ | [机器人端云任务追踪](skills/robot-task-trace/SKILL.md) |
| 什么证据能确认机器人已经停稳？如何防止复位后执行旧命令？ | [机器人安全策略与防护验证](skills/robot-safety-policy/SKILL.md) |

## 试一个离线示例

[相机几何示例](skills/robot-sensor-calibration/references/geometry-check.md) 只需 Python 3 和标准库即可运行。两个不同深度的三维点可以投影到同一个像素。示例用一个未参与标定的三维参考点，说明怎样发现这类深度误差。

[停机与重启案例](skills/robot-safety-policy/references/stop-restart-cases.md) 提供五段合成事件记录。可以先从“反馈丢失”一例入手：驱动回复了停机请求，但位置反馈在停稳前中断。用这段记录练习判断哪些结论已经有证据，哪些仍需实测。

## 许可证

技能文档和原创示例采用 [MIT 许可证](LICENSE)。链接中的论文、配置和手册由各自的权利人发布。
