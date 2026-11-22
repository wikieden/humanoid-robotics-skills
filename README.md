# Humanoid Robotics Skills

English · [简体中文](README.zh-CN.md)

This collection contains 35 English-language agent skills. It includes 33 workflows for humanoid and mobile manipulation robotics and two general workflows for evaluating agents and teaching technical topics. Each skill is a Markdown workflow for a specific engineering decision, from tracing a reversed gripper command to deciding whether a new robot policy should replace its baseline.

## Use a skill

Clone the repository, open the skill that matches your question, and give your agent the relevant inputs. For example:

> Follow `skills/robot-takeover-audit/SKILL.md` to review this recording. One operator took control twice. Show which two-step action windows are eligible for behavior cloning and identify the evidence for each boundary.

The workflows can also be read directly by a human reviewer. To use an agent that discovers `SKILL.md` files from a local skills directory, copy the skill folders listed in the index there as siblings, including their `references/` subdirectories. This preserves the relative links between skills.

## Choose a workflow

Browse the [skill index](skills/README.md) to choose a workflow by engineering question.

| Category | Skills |
| --- | ---: |
| [Systems, deployment, and safety](skills/README.md#systems-deployment-and-safety) | 4 |
| [Perception, calibration, and navigation](skills/README.md#perception-calibration-and-navigation) | 9 |
| [Grasping, planning, and motion control](skills/README.md#grasping-planning-and-motion-control) | 5 |
| [Teleoperation and demonstration data](skills/README.md#teleoperation-and-demonstration-data) | 5 |
| [Policy training and evaluation](skills/README.md#policy-training-and-evaluation) | 3 |
| [Robot platform and cloud services](skills/README.md#robot-platform-and-cloud-services) | 7 |
| [Engineering methods for agents and technical learning](skills/README.md#engineering-methods-for-agents-and-technical-learning) | 2 |

## Try an offline example

The [camera geometry example](skills/robot-sensor-calibration/references/geometry-check.md) runs with Python 3 and the standard library. It shows how two different depth values can map to the same pixel and how a held-out 3D landmark exposes the error. The [stop and restart cases](skills/robot-safety-policy/references/stop-restart-cases.md) give five synthetic event traces for reviewing evidence without connecting to hardware.

## License

The skill documents and original examples are available under the [MIT License](LICENSE). Linked papers, configurations, and manuals are published by their respective owners.
