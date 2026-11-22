# 机器人开发技能索引

[English](README.md) · 简体中文

按当前要做的工程判断选择 skill。一个任务可以跨类：例如交接遥控器先查控制权，排查手柄方向再查输入映射，最后验收录制中的人工标签。

## 系统架构、部署与安全

| 要回答的问题 | Skill |
| --- | --- |
| 机器人伸手时感知进程重启，谁负责保持平衡，谁仍有权下发关节指令？ | [ROS 2 架构设计与审查](robot-ros2-architecture/SKILL.md) |
| 每个 Pod 能访问哪些设备、收到哪些 DDS 消息？ | [Pod 部署与环境隔离](robot-ros2-pod-deployment/SKILL.md) |
| 板端服务已受理命令，反馈在哪一层中断？ | [嵌入式与 MCU 联调](robot-embedded-bringup/SKILL.md) |
| 什么证据能确认停稳，复位后如何防止旧指令引起运动？ | [安全策略与防护验证](robot-safety-policy/SKILL.md) |

## 感知、标定与导航

| 要回答的问题 | Skill |
| --- | --- |
| 相机支架转动时，静止目标在基座坐标系里也跟着移动吗？ | [传感器外参标定](robot-sensor-calibration/SKILL.md) |
| 抓取点偏了，误差最早出现在掩码、深度还是坐标变换？ | [RGB-D 位姿验证](robot-rgbd-pose/SKILL.md) |
| 机器人认对了物体，但关键区域被遮挡，它凭什么判断物体状态？ | [多模态目标与状态判断](robot-multimodal-grounding/SKILL.md) |
| 只看到部分表面时，数据足以区分两个候选朝向吗？ | [点云配准与朝向消歧](robot-object-registration/SKILL.md) |
| 长走廊里哪些方向的位姿估不准？前端配准和后端回环约束怎么设计？ | [激光 SLAM 算法开发](robot-slam-development/SKILL.md) |
| 障碍物移走或传感器掉帧时，滚动地图如何更新占据状态和通行性？ | [局部占据地图与通行性算法开发](robot-local-costmap-development/SKILL.md) |
| 如何搜索可通行路径、绕开局部障碍，并给底盘或步态控制器下发可执行的参考？ | [导航规划与路径跟踪算法开发](robot-navigation-planner-development/SKILL.md) |
| 导航未到点，定位、规划、跟踪和底盘反馈中哪一步先出现异常？ | [建图与导航回放](robot-navigation-replay/SKILL.md) |
| 地图保存并重载后，机器人能否从新起点在正确楼层重新定位？ | [SLAM 地图与重定位验收](robot-map-relocalization/SKILL.md) |

## 抓取、规划与运动控制

| 要回答的问题 | Skill |
| --- | --- |
| 哪个抓取候选既能接近，又能带着物体撤离？ | [抓取候选选优](robot-grasp-selection/SKILL.md) |
| 路点均达标，控制器插值后的速度或加速度是否超限？ | [轨迹定时与插值](robot-trajectory-retiming/SKILL.md) |
| 策略选线后任务仍失败，偏差始于规划、跟踪还是接触？ | [运动控制与强化学习验证](robot-motion-validation/SKILL.md) |
| 仿真松爪后，物体确实得到支撑，还是被残留约束固定在原位？ | [接触任务仿真验收](robot-sim-contact-validation/SKILL.md) |
| 人形机器人能否在整段试验中保持站立，并跟随指定速度行走和转向？ | [人形步态仿真评测](robot-locomotion-sim-eval/SKILL.md) |

## 遥操作与示教数据

| 要回答的问题 | Skill |
| --- | --- |
| 接管之后，哪位操作员的指令还会被执行端接受？ | [遥操作会话与控制权](robot-teleop-session/SKILL.md) |
| 操作员扣左侧扳机，夹爪或机械臂的动作在哪一层反了？ | [遥操作输入映射](robot-teleop-bringup/SKILL.md) |
| 要训练这个动作，第一视角视频、手持工具和机器人遥操作各能提供哪些标签？ | [示教采集方案设计](robot-capture-design/SKILL.md) |
| 转换后的轨迹能否训练，当前划分能检验哪种泛化能力？ | [示教轨迹与数据集验收](robot-episode-audit/SKILL.md) |
| 哪些连续动作窗口确实来自人工纠正，可以作为专家标签？ | [人工接管标签验收](robot-takeover-audit/SKILL.md) |

## 策略训练与评测

| 要回答的问题 | Skill |
| --- | --- |
| 这次失败该补数据、更新参数，还是修执行逻辑？ | [策略训练与递归自改进](robot-policy-training/SKILL.md) |
| 哪种训练精度能装进显存、正确续训，并在新进程中重载推理？ | [训练精度与检查点对照](robot-training-precision/SKILL.md) |
| 新权重能否按时供给可执行动作，任务表现是否改善？ | [VLA / WAM 策略评测](robot-policy-eval/SKILL.md) |

## 机器人平台与端云服务

| 要回答的问题 | Skill |
| --- | --- |
| 激活响应丢失或设备换网后，如何确认同一台设备恢复服务？ | [设备接入验收](robot-device-onboarding/SKILL.md) |
| 这次设备会话实际使用了哪个 Agent 版本和哪些权限？ | [设备与 Agent 版本绑定](robot-agent-binding-review/SKILL.md) |
| 用户换到另一台机器人时，哪些知识、偏好和对话内容可以带过去？ | [机器人共享知识与会话记忆](robot-agent-context/SKILL.md) |
| “下一站”重发或迟到时，协议应如何推进任务状态？ | [长任务协议与回执验收](robot-task-protocol/SKILL.md) |
| 这次任务已在界面显示完成，日志里第一处缺失的回执在哪里？ | [端云任务追踪](robot-task-trace/SKILL.md) |
| 设备是播完了、被打断了，还是断线重连后又播了一次？ | [语音打断与播报验收](robot-voice-playback/SKILL.md) |
| 动作换版或撤回后，哪些租户和机器人仍引用旧版？ | [动作资产发布与撤回](robot-action-release/SKILL.md) |

## 通用工程方法：Agent 评测与技术学习

| 要回答的问题 | Skill |
| --- | --- |
| 两种 Agent 工作流通过率相同，各自解决了哪些任务，每个成功任务花了多少成本？ | [Agent 工作流配对评测](agent-harness-comparison/SKILL.md) |
| 怎么把一个技术问题做成小实验，把真实错答变成复习卡，下次从断点继续学？ | [技术学习实验与复习卡](technical-study-lab/SKILL.md) |
