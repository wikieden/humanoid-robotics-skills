# 机器人开发技能索引

[English](README.md) · 简体中文

按要解决的工程问题，从 53 个 skill 中选择入口。新的硬件观测、故障案例或算例，放入能用到它的现有流程。遇到需要不同输入证据、给出不同工程结论的问题，再建独立 skill。

**仿真与回放速查。** 从[搭建算法测试环境][scene-build]开始，或直接进入[导航未到点回放][nav-replay]、[释放后的接触验证][contact]、[快照恢复与分支对照][restore]、[实时预览验证][preview]或[步态跟踪与摔倒评测][gait]。下方分类表中可以找到同一入口。

[scene-build]: robot-sim-environment-build/SKILL.md
[nav-replay]: robot-navigation-replay/SKILL.md
[contact]: robot-sim-contact-validation/SKILL.md
[restore]: robot-sim-state-restore/SKILL.md
[preview]: robot-simulation-preview/SKILL.md
[gait]: robot-locomotion-sim-eval/SKILL.md

### 单独安装一个 skill

复制所选 skill 的完整目录，保留 `SKILL.md` 和同包的 `references/`（如有）。下表前五项是对应分支的操作指南，执行该分支时需要阅读。后六项是可选阅读或离线算例。其余 42 个包的全部说明都在各自的 `SKILL.md`。

| 包内资料 | 何时使用 |
| --- | --- |
| [robot-episode-audit/references/takeover-labels.md](robot-episode-audit/references/takeover-labels.md) | 判定接管动作标签和连续专家动作窗口。 |
| [robot-grasp-selection/references/grasp-algorithms.md](robot-grasp-selection/references/grasp-algorithms.md) | 在物体位姿、夹爪位姿和动作序列之间选算法路线。 |
| [robot-rgbd-pose/references/object-registration.md](robot-rgbd-pose/references/object-registration.md) | 从已有公制点云做配准，判定朝向是否可区分。 |
| [robot-task-protocol/references/task-tracing.md](robot-task-protocol/references/task-tracing.md) | 沿端云回执追踪一次卡住或提前显示完成的任务。 |
| [robot-voice-playback/references/streaming-underruns.md](robot-voice-playback/references/streaming-underruns.md) | 定位同一句连续播报中的音频欠载。 |
| [robot-policy-training/references/training-methods.md](robot-policy-training/references/training-methods.md) | 可选阅读：训练路线和消融实验的研究资料。 |
| [robot-safety-policy/references/stop-restart-cases.md](robot-safety-policy/references/stop-restart-cases.md) | 可选练习：判读停止、复位和重新启动的事件记录。 |
| [robot-sensor-calibration/references/geometry-check.md](robot-sensor-calibration/references/geometry-check.md) | 可选算例：用 Python 检查变换方向、时间和深度尺度。 |
| [robot-sim-contact-validation/references/support-check.md](robot-sim-contact-validation/references/support-check.md) | 可选算例：无界面的接触支撑检查，运行需 MuJoCo 和 NumPy。 |
| [robot-sim-environment-build/references/range-stop-bench.md](robot-sim-environment-build/references/range-stop-bench.md) | 可选算例：在 MuJoCo 中检查传感器和碰撞，再对同一场景做两种控制器的回归。 |
| [robot-motion-retargeting/references/stance-foot-check.md](robot-motion-retargeting/references/stance-foot-check.md) | 可选算例：用 Python 标准库比较直接复制关节角与带支撑脚约束的重定向，检查通道顺序和不可达姿态。 |

英文指南中标有 **(optional)** 的相对链接指向同级 skill。单包装好后即可完成本包工作流。需要跟进相邻问题时，可在完整仓库打开链接，也可把目标 skill 的整个目录并排复制。例如选择抓取算法需要本包的 `grasp-algorithms.md`；要进一步检查物体朝向，才需要打开 `robot-rgbd-pose` 的配准指南。

### 已安装用户迁移

四个旧 skill 已并入现有入口。更新时请连同 `references/` 复制完整的入口目录，修改已保存的提示词，再检查并清理自己安装的旧副本，保留个人修改。

| 旧 skill（链接固定到上一公开版本） | 现行入口 | 直达专项指南 |
| --- | --- | --- |
| [`robot-takeover-audit`](https://github.com/wikieden/humanoid-robotics-skills/blob/1e4d404b36adf7d1b84f526ed12ef41fd8b97aac/skills/robot-takeover-audit/SKILL.md) | `robot-episode-audit` | [接管标签与连续动作窗口](robot-episode-audit/references/takeover-labels.md) |
| [`robot-object-registration`](https://github.com/wikieden/humanoid-robotics-skills/blob/1e4d404b36adf7d1b84f526ed12ef41fd8b97aac/skills/robot-object-registration/SKILL.md) | `robot-rgbd-pose` | [点云配准与朝向消歧](robot-rgbd-pose/references/object-registration.md) |
| [`robot-task-trace`](https://github.com/wikieden/humanoid-robotics-skills/blob/1e4d404b36adf7d1b84f526ed12ef41fd8b97aac/skills/robot-task-trace/SKILL.md) | `robot-task-protocol` | [端云任务追踪](robot-task-protocol/references/task-tracing.md) |
| [`robot-streaming-audio`](https://github.com/wikieden/humanoid-robotics-skills/blob/1e4d404b36adf7d1b84f526ed12ef41fd8b97aac/skills/robot-streaming-audio/SKILL.md) | `robot-voice-playback` | [流式语音播放欠载](robot-voice-playback/references/streaming-underruns.md) |

## 系统架构、部署与安全

| 要回答的问题 | Skill |
| --- | --- |
| 机器人伸手时感知进程重启，谁负责保持平衡，谁仍有权下发关节指令？ | [ROS 2 架构设计与审查](robot-ros2-architecture/SKILL.md) |
| 每个 Pod 能访问哪些设备、收到哪些 DDS 消息？ | [Pod 部署与环境隔离](robot-ros2-pod-deployment/SKILL.md) |
| 如何把场景描述、实拍视频或生成的 3D 资产搭成可复现的机器人算法测试环境？ | [仿真环境搭建与算法回归](robot-sim-environment-build/SKILL.md) |
| 板端服务已受理命令，反馈在哪一层中断？ | [嵌入式与 MCU 联调](robot-embedded-bringup/SKILL.md) |
| 升级中断后，主机、控制器和模型分别运行哪个版本，这个组合能否继续工作？ | [整机多组件升级与恢复](robot-update-recovery/SKILL.md) |
| 手臂关节仍有实测反馈，为什么夹爪短暂断流后规划器就拒绝起始状态？ | [关节反馈时效与恢复](robot-joint-feedback/SKILL.md) |
| 什么证据能确认停稳，复位后如何防止旧指令引起运动？ | [安全策略与防护验证](robot-safety-policy/SKILL.md) |
| 外壳静态装得下，多个关节一起运动时，哪两处表面最先靠近？ | [运动外壳间隙审查](robot-shell-clearance/SKILL.md) |
| 某个动作会产生多大电气负载，按实际任务中动静交替的比例，电池能用多久？ | [执行器负载与电池续航估算](robot-motion-energy/SKILL.md) |

## 感知、标定与导航

| 要回答的问题 | Skill |
| --- | --- |
| 相机支架转动时，静止目标在基座坐标系里也跟着移动吗？ | [传感器外参标定](robot-sensor-calibration/SKILL.md) |
| 偏差来自 RGB-D 投影，还是已有分割点云本身就支持多个候选朝向？ | [三维目标位姿与点云配准](robot-rgbd-pose/SKILL.md) |
| 机器人认对了物体，但关键区域被遮挡，它凭什么判断物体状态？ | [多模态目标与状态判断](robot-multimodal-grounding/SKILL.md) |
| 摄像头帧率达标，为什么共享加速器上的某个检测模型迟迟没有新结果？ | [端侧多视觉模型调度](robot-edge-vision-scheduling/SKILL.md) |
| 长走廊里哪些方向的位姿估不准？前端配准和后端回环约束怎么设计？ | [激光 SLAM 算法开发](robot-slam-development/SKILL.md) |
| 障碍物移走或传感器掉帧时，滚动地图如何更新占据状态和通行性？ | [局部占据地图与通行性算法开发](robot-local-costmap-development/SKILL.md) |
| 如何搜索可通行路径、绕开局部障碍，并给底盘或步态控制器下发可执行的参考？ | [导航规划与路径跟踪算法开发](robot-navigation-planner-development/SKILL.md) |
| 导航未到点，定位、规划、跟踪和底盘反馈中哪一步先出现异常？ | [建图与导航回放](robot-navigation-replay/SKILL.md) |
| 地图保存并重载后，机器人能否从新起点在正确楼层重新定位？ | [SLAM 地图与重定位验收](robot-map-relocalization/SKILL.md) |

## 抓取、规划与运动控制

| 要回答的问题 | Skill |
| --- | --- |
| 哪个抓取候选既能接近，又能带着物体撤离？ | [抓取候选选优](robot-grasp-selection/SKILL.md) |
| 商品换包装或换到更窄的货位后，原有抓取能力还能复用到什么范围？ | [新品与包装变更准入](robot-item-onboarding/SKILL.md) |
| 如何把动捕或已有动作绑定到另一台人形机器人的骨架，并检查支撑脚滑动和手部接触偏差？ | [动作资产绑定与重定向](robot-motion-retargeting/SKILL.md) |
| 路点均达标，控制器插值后的速度或加速度是否超限？ | [轨迹定时与插值](robot-trajectory-retiming/SKILL.md) |
| 机械臂规划器在哪些工作空间区域返回无效轨迹，或频繁拒绝已知可行的请求？ | [机械臂规划器工作空间回归](robot-planner-workspace-regression/SKILL.md) |
| 规划成功后，指令下发、底盘到手臂的交接、实测运动，最先在哪一步出现偏差？ | [运动执行与跟踪验证](robot-motion-validation/SKILL.md) |
| 仿真松爪后，物体确实得到支撑，还是被残留约束固定在原位？ | [接触任务仿真验收](robot-sim-contact-validation/SKILL.md) |
| 从任务中途的快照恢复后，同一动作还能复现连续运行时的接触和运动吗？ | [仿真快照恢复与分支验证](robot-sim-state-restore/SKILL.md) |
| 预览是否在本次仿真结束前就显示了新画面，开启渲染会不会改变结果？ | [仿真实时预览验证](robot-simulation-preview/SKILL.md) |
| 人形机器人能否在整段试验中保持站立，并跟随指定速度行走和转向？ | [人形步态仿真评测](robot-locomotion-sim-eval/SKILL.md) |
| 把策略样本左右镜像后，另一侧肢体是否真的朝预期方向运动？ | [机器人策略左右镜像验证](robot-policy-symmetry/SKILL.md) |

## 遥操作与示教数据

| 要回答的问题 | Skill |
| --- | --- |
| 接管之后，哪位操作员的指令还会被执行端接受？ | [遥操作会话与控制权](robot-teleop-session/SKILL.md) |
| 操作员扣左侧扳机，夹爪或机械臂的动作在哪一层反了？ | [遥操作输入映射](robot-teleop-bringup/SKILL.md) |
| 要训练这个动作，第一视角视频、手持工具和机器人遥操作各能提供哪些标签？ | [示教采集方案设计](robot-capture-design/SKILL.md) |
| 转换后的轨迹能否用于训练，接管前后哪些连续动作窗口可以作为专家标签？ | [示教轨迹与接管标签验收](robot-episode-audit/SKILL.md) |
| 新版读取器能否读懂历史示教记录，保留未知时间、缺失标签和原始采样率？ | [示教记录元数据迁移](robot-episode-schema-migration/SKILL.md) |
| 连续录包时怎样封口上传一段数据，并查清轮转间隙有没有漏消息、重传有没有重复归档？ | [连续录包、轮转与上传](robot-bag-recording/SKILL.md) |

## 策略训练与评测

| 要回答的问题 | Skill |
| --- | --- |
| 这次失败该补数据、更新参数，还是修执行逻辑？ | [策略训练与递归自改进](robot-policy-training/SKILL.md) |
| 哪种训练精度能装进显存、正确续训，并在新进程中重载推理？ | [训练精度与检查点对照](robot-training-precision/SKILL.md) |
| 这批多机位训练数据需要多少 GPU 卡时，实际排期要多久？ | [机器人训练算力估算](robot-training-capacity/SKILL.md) |
| 新权重能否按时供给可执行动作？在同一组任务条件下哪个策略表现更好？ | [机器人策略对照评测](robot-policy-eval/SKILL.md) |

## 机器人平台与端云服务

| 要回答的问题 | Skill |
| --- | --- |
| 激活响应丢失或设备换网后，如何确认同一台设备恢复服务？ | [设备接入验收](robot-device-onboarding/SKILL.md) |
| 这次设备会话实际使用了哪个 Agent 版本和哪些权限？ | [设备与 Agent 版本绑定](robot-agent-binding-review/SKILL.md) |
| 新增机器人意图后，关键词规则和模型兜底两条路径都能正确处理吗？ | [机器人意图路由与回归验证](robot-intent-routing/SKILL.md) |
| 用户换到另一台机器人时，哪些知识、偏好和对话内容可以带过去？ | [机器人共享知识与会话记忆](robot-agent-context/SKILL.md) |
| 重发命令应如何推进状态？线上任务提前显示完成时，哪条回执缺失？ | [任务协议与端云追踪](robot-task-protocol/SKILL.md) |
| 播报被打断或重播了吗？连续播放中途卡顿时，哪一层先供不上音频？ | [语音播报与连续播放诊断](robot-voice-playback/SKILL.md) |
| 动作换版或撤回后，哪些租户和机器人仍引用旧版？ | [动作资产发布与撤回](robot-action-release/SKILL.md) |

## 通用工程方法：Agent 评测与技术学习

| 要回答的问题 | Skill |
| --- | --- |
| 两种 Agent 工作流通过率相同，各自解决了哪些任务，每个成功任务花了多少成本？ | [Agent 工作流配对评测](agent-harness-comparison/SKILL.md) |
| 任务究竟在哪个执行环境里读取输入、运行并产生了交付文件？ | [Agent 任务执行位置验证](agent-execution-placement/SKILL.md) |
| 怎么把一个技术问题做成小实验，把真实错答变成复习卡，下次从断点继续学？ | [技术学习实验与复习卡](technical-study-lab/SKILL.md) |

## 交互工具与离线归档

| 要回答的问题 | Skill |
| --- | --- |
| 交互应用如何从暂停前的阶段恢复，并在重启后丢弃旧回调？ | [暂停、恢复与重启](interactive-run-lifecycle/SKILL.md) |
| 评测站点离线后，还有哪些试验明细和机位视频能从看板点开？ | [离线评测归档核验](offline-evaluation-archive/SKILL.md) |

## 技能分发与技术文档发布

| 要回答的问题 | Skill |
| --- | --- |
| 多种 Agent 助手能否发现同一套 skill 及其资源，同时保留用户已有的同名文件？ | [跨助手技能分发](skill-distribution/SKILL.md) |
| 技术结论更正后，哪些译本、导出文件和交付压缩包里还留着旧说法？ | [技术文档多版本同步](document-variant-sync/SKILL.md) |
