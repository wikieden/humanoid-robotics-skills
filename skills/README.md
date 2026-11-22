# Robotics Skill Index

English · [简体中文](README.zh-CN.md)

Choose a skill by the engineering question at hand. A single investigation may span categories: start with session ownership for a handoff, inspect input mapping for reversed motion, then check takeover labels before using the recording for training.

## Systems, deployment, and safety

| Engineering question | Skill |
| --- | --- |
| Who owns each joint if a process restarts mid-maneuver? | [ROS 2 architecture](robot-ros2-architecture/SKILL.md) |
| Which devices and DDS traffic can each Pod access? | [Pod deployment](robot-ros2-pod-deployment/SKILL.md) |
| Where did a command or acknowledgment stop between Linux and the MCU? | [Embedded bring-up](robot-embedded-bringup/SKILL.md) |
| What establishes standstill, and what prevents motion after reset? | [Physical safeguards](robot-safety-policy/SKILL.md) |

## Perception, calibration, and navigation

| Engineering question | Skill |
| --- | --- |
| Does a stationary target shift in the base frame when the camera mount turns? | [Sensor extrinsics](robot-sensor-calibration/SKILL.md) |
| Did the offset first appear in the mask, depth, or frame transform? | [RGB-D pose validation](robot-rgbd-pose/SKILL.md) |
| Which observation supports the object's identity and state when part of it is hidden? | [Multimodal object and state grounding](robot-multimodal-grounding/SKILL.md) |
| Do the visible surfaces distinguish two competing orientations? | [Object registration](robot-object-registration/SKILL.md) |
| How should scan matching and loop closure handle a corridor with little geometric information? | [Lidar SLAM algorithm development](robot-slam-development/SKILL.md) |
| How should sensor rays update a rolling map when an obstacle moves or observations stop? | [Local occupancy and traversability map development](robot-local-costmap-development/SKILL.md) |
| How can a robot find a feasible detour, set its speed, and track the resulting path? | [Navigation planner and path tracking development](robot-navigation-planner-development/SKILL.md) |
| Which recorded signal first explains a missed waypoint? | [Navigation replay](robot-navigation-replay/SKILL.md) |
| Can a fresh robot localize on the correct floor after the saved map is reloaded? | [SLAM map and relocalization acceptance](robot-map-relocalization/SKILL.md) |

## Grasping, planning, and motion control

| Engineering question | Skill |
| --- | --- |
| Which grasp permits both approach and retreat with the object? | [Grasp selection](robot-grasp-selection/SKILL.md) |
| Does the controller exceed a limit between valid waypoints? | [Trajectory retiming](robot-trajectory-retiming/SKILL.md) |
| Did the task fail at goal selection, planning, tracking, or contact? | [Motion validation](robot-motion-validation/SKILL.md) |
| Did the simulated object stay supported after release, or did an attachment or scoring shortcut keep it in place? | [Contact task simulation](robot-sim-contact-validation/SKILL.md) |
| Can the humanoid follow the commanded velocity and stay upright across a full trial? | [Locomotion simulation evaluation](robot-locomotion-sim-eval/SKILL.md) |

## Teleoperation and demonstration data

| Engineering question | Skill |
| --- | --- |
| Which operator can command the robot after a handoff? | [Session ownership](robot-teleop-session/SKILL.md) |
| Which mapping reversed the operator's gripper or arm input? | [Controller mapping](robot-teleop-bringup/SKILL.md) |
| Which capture method can supply the labels the intended training objective needs? | [Demonstration capture design](robot-capture-design/SKILL.md) |
| Can the training loader use the converted episodes, and what does the split test? | [Dataset audit](robot-episode-audit/SKILL.md) |
| Which consecutive action windows contain verified human corrections? | [Takeover labels](robot-takeover-audit/SKILL.md) |

## Policy training and evaluation

| Engineering question | Skill |
| --- | --- |
| Does this failure call for new supervision, a parameter update, or an execution fix? | [Policy training and RSI](robot-policy-training/SKILL.md) |
| Which precision fits the memory budget, resumes correctly and reloads for inference? | [Training precision and checkpoint comparison](robot-training-precision/SKILL.md) |
| Can the checkpoint supply usable actions on time, and does it improve task outcomes? | [Policy evaluation](robot-policy-eval/SKILL.md) |

## Robot platform and cloud services

| Engineering question | Skill |
| --- | --- |
| Can the same device recover its identity and connections after a retry? | [Device onboarding](robot-device-onboarding/SKILL.md) |
| Which release and permissions did this device session actually use? | [Agent binding](robot-agent-binding-review/SKILL.md) |
| When a speaker moves to a second device, which knowledge, preferences and conversation fields may follow? | [Shared robot knowledge and session memory](robot-agent-context/SKILL.md) |
| How should the protocol handle a duplicated or late command? | [Task protocol](robot-task-protocol/SKILL.md) |
| For this particular run, where did the earliest receipt go missing? | [Task tracing](robot-task-trace/SKILL.md) |
| Did the device finish, interrupt, or replay the utterance? | [Voice playback](robot-voice-playback/SKILL.md) |
| Which tenants and robots still resolve a withdrawn or superseded revision? | [Action asset release](robot-action-release/SKILL.md) |

## Engineering methods for agents and technical learning

| Engineering question | Skill |
| --- | --- |
| Two agent workflows have the same pass rate. Which tasks did each solve, and at what cost? | [Paired agent harness evaluation](agent-harness-comparison/SKILL.md) |
| How can a learner test one technical claim, review a mistake, and resume at the next unanswered question? | [Technical study labs and review cards](technical-study-lab/SKILL.md) |
