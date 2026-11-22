# Humanoid Robotics Skills

English · [简体中文](README.zh-CN.md)

A collection of English-language agent skills for engineers working on humanoid and mobile manipulation robots. Each skill is a Markdown workflow for a specific engineering decision, from tracing a reversed gripper command to deciding whether a new robot policy should replace its baseline.

## Use a skill

Clone the repository, open the skill that matches your question, and give your agent the relevant inputs. For example:

> Follow `skills/robot-takeover-audit/SKILL.md` to review this recording. One operator took control twice. Show which two-step action windows are eligible for behavior cloning and identify the evidence for each boundary.

The workflows can also be read directly by a human reviewer. To use an agent that discovers `SKILL.md` files from a local skills directory, copy the `robot-*` folders there as siblings, including their `references/` subdirectories. This preserves the relative links between skills.

## Choose a workflow

| Engineering question | Skill |
| --- | --- |
| The board accepted a command. Where did feedback stop? | [Embedded Linux and MCU bring-up](skills/robot-embedded-bringup/SKILL.md) |
| Which stage reversed the operator's gripper or arm input? | [Dual-arm teleoperation](skills/robot-teleop-bringup/SKILL.md) |
| Which recordings can the training loader use, and what does the split test? | [Episode and dataset audit](skills/robot-episode-audit/SKILL.md) |
| Which actions came from an operator during a takeover? | [Expert action label audit](skills/robot-takeover-audit/SKILL.md) |
| Should this failure lead to better data, a policy update, or an execution fix? | [VLA, WAM, and recursive self-improvement training](skills/robot-policy-training/SKILL.md) |
| Can the controller receive usable action chunks in time? | [Policy evaluation](skills/robot-policy-eval/SKILL.md) |
| Why does a stationary target shift when the camera mount turns? | [Camera-to-robot calibration](skills/robot-sensor-calibration/SKILL.md) |
| Is the grasp target wrong in the image, in depth, or in the robot frame? | [RGB-D pose validation](skills/robot-rgbd-pose/SKILL.md) |
| Where did localization, planning, tracking, or base feedback first diverge? | [Navigation replay](skills/robot-navigation-replay/SKILL.md) |
| Did the policy choose a poor trajectory, or did execution lose contact? | [Motion control and RL validation](skills/robot-motion-validation/SKILL.md) |
| Which service reported completion, and what did the device actually do? | [Cloud-to-robot task tracing](skills/robot-task-trace/SKILL.md) |
| What evidence establishes standstill and prevents old commands from restarting motion? | [Robot safety policy and safeguard verification](skills/robot-safety-policy/SKILL.md) |

## Try an offline example

The [camera geometry example](skills/robot-sensor-calibration/references/geometry-check.md) runs with Python 3 and the standard library. It shows how two different depth values can map to the same pixel and how a held-out 3D landmark exposes the error. The [stop and restart cases](skills/robot-safety-policy/references/stop-restart-cases.md) give five synthetic event traces for reviewing evidence without connecting to hardware.

## License

The skill documents and original examples are available under the [MIT License](LICENSE). Linked papers, configurations, and manuals are published by their respective owners.
