# Robotics Skill Index

English · [简体中文](README.zh-CN.md)

Start with the [robot development entry skill](robot-dev-skills/SKILL.md) or choose one of the 56 specialists below. The collection contains 57 installable skills. A new hardware observation, failure case or worked example belongs with the workflow it improves. Add a separate skill when a different question requires its own evidence and deliverable.

**Simulation and replay.** Build an [algorithm test environment][scene-build], trace a [missed waypoint][nav-replay], verify [contact after release][contact], compare [branches from a snapshot][restore], check [live preview timing][preview], or score [gait tracking and falls][gait]. Each workflow also appears in its engineering category below.

[scene-build]: robot-sim-environment-build/SKILL.md
[nav-replay]: robot-navigation-replay/SKILL.md
[contact]: robot-sim-contact-validation/SKILL.md
[restore]: robot-sim-state-restore/SKILL.md
[preview]: robot-simulation-preview/SKILL.md
[gait]: robot-locomotion-sim-eval/SKILL.md

### Install one skill

Copy the selected folder with its `SKILL.md` and its own `references/` directory when present. The first six files support the entry skill or a named branch. Read the file needed for the task. The last six are optional reading or worked examples. The other 45 packages contain their entire workflow in `SKILL.md`.

| Bundled file | When to use it |
| --- | --- |
| [robot-dev-skills/references/workflows.md](robot-dev-skills/references/workflows.md) | The entry skill uses this directory to select one of the 56 specialists before reading its guide. |
| [robot-episode-audit/references/takeover-labels.md](robot-episode-audit/references/takeover-labels.md) | Label human takeovers and select consecutive expert-action windows. |
| [robot-grasp-selection/references/grasp-algorithms.md](robot-grasp-selection/references/grasp-algorithms.md) | Choose an algorithm when the required output might be an object pose, a gripper pose or an action sequence. |
| [robot-rgbd-pose/references/object-registration.md](robot-rgbd-pose/references/object-registration.md) | Register an existing metric cloud and resolve or report pose ambiguity. |
| [robot-task-protocol/references/task-tracing.md](robot-task-protocol/references/task-tracing.md) | Trace a specific stalled or prematurely completed task through device and cloud receipts. |
| [robot-voice-playback/references/streaming-underruns.md](robot-voice-playback/references/streaming-underruns.md) | Locate a gap within one uninterrupted utterance. |
| [robot-policy-training/references/training-methods.md](robot-policy-training/references/training-methods.md) | Optional research notes on training variants and ablations. |
| [robot-safety-policy/references/stop-restart-cases.md](robot-safety-policy/references/stop-restart-cases.md) | Optional worked cases for interpreting stop, reset and restart traces. |
| [robot-sensor-calibration/references/geometry-check.md](robot-sensor-calibration/references/geometry-check.md) | Optional Python example for transform direction, timing and depth scale. |
| [robot-sim-contact-validation/references/support-check.md](robot-sim-contact-validation/references/support-check.md) | Optional headless support example. Running it requires MuJoCo and NumPy. |
| [robot-sim-environment-build/references/range-stop-bench.md](robot-sim-environment-build/references/range-stop-bench.md) | Optional MuJoCo scene bring-up example with sensor and collision probes and paired controller trials. |
| [robot-motion-retargeting/references/stance-foot-check.md](robot-motion-retargeting/references/stance-foot-check.md) | Optional standard-library example comparing joint copying with stance-constrained IK, including channel order and an unreachable frame. |

Relative links labeled **(optional)** in the English guides lead to sibling skills. The selected package contains its own workflow. To follow a companion link, open it in the full checkout or copy the target package beside the installed one. For example, choosing a grasping algorithm uses the bundled `grasp-algorithms.md`. The companion registration guide in `robot-rgbd-pose` is useful if the follow-up question concerns object orientation.

### Existing installations

Four former skills are now references in their parent packages. Refresh the entire parent folder, including `references/`, update saved prompts, then retire any old copies you manage after checking for local edits.

| Former skill at its last published revision | Current entrypoint | Direct reference |
| --- | --- | --- |
| [`robot-takeover-audit`](https://github.com/wikieden/humanoid-robotics-skills/blob/1e4d404b36adf7d1b84f526ed12ef41fd8b97aac/skills/robot-takeover-audit/SKILL.md) | `robot-episode-audit` | [Takeover labels and contiguous windows](robot-episode-audit/references/takeover-labels.md) |
| [`robot-object-registration`](https://github.com/wikieden/humanoid-robotics-skills/blob/1e4d404b36adf7d1b84f526ed12ef41fd8b97aac/skills/robot-object-registration/SKILL.md) | `robot-rgbd-pose` | [Object registration and pose ambiguity](robot-rgbd-pose/references/object-registration.md) |
| [`robot-task-trace`](https://github.com/wikieden/humanoid-robotics-skills/blob/1e4d404b36adf7d1b84f526ed12ef41fd8b97aac/skills/robot-task-trace/SKILL.md) | `robot-task-protocol` | [Cloud-to-robot task tracing](robot-task-protocol/references/task-tracing.md) |
| [`robot-streaming-audio`](https://github.com/wikieden/humanoid-robotics-skills/blob/1e4d404b36adf7d1b84f526ed12ef41fd8b97aac/skills/robot-streaming-audio/SKILL.md) | `robot-voice-playback` | [Streaming speech underruns](robot-voice-playback/references/streaming-underruns.md) |

## Systems, deployment, and safety

| Engineering question | Skill |
| --- | --- |
| Who owns each joint if a process restarts mid-maneuver? | [ROS 2 architecture](robot-ros2-architecture/SKILL.md) |
| Which devices and DDS traffic can each Pod access? | [Pod deployment](robot-ros2-pod-deployment/SKILL.md) |
| How can a brief, real capture or generated 3D asset become a repeatable robot algorithm test environment? | [Simulation environment construction](robot-sim-environment-build/SKILL.md) |
| Where did a command or acknowledgment stop between Linux and the MCU? | [Embedded bring-up](robot-embedded-bringup/SKILL.md) |
| After an interrupted update, which controller, host and model versions are actually active together? | [Multi-component update recovery](robot-update-recovery/SKILL.md) |
| Why are arm joints still visible while the planner rejects its start state after a gripper feedback gap? | [Joint feedback freshness and recovery](robot-joint-feedback/SKILL.md) |
| What establishes standstill, and what prevents motion after reset? | [Physical safeguards](robot-safety-policy/SKILL.md) |
| A new cover fits at rest. Which two surfaces come closest when its joints move together? | [Moving shell clearance review](robot-shell-clearance/SKILL.md) |
| What electrical load does a motion impose, and how long would the battery last over the full duty cycle? | [Actuator load and battery runtime](robot-motion-energy/SKILL.md) |

## Perception, calibration, and navigation

| Engineering question | Skill |
| --- | --- |
| Does a stationary target shift in the base frame when the camera mount turns? | [Sensor extrinsics](robot-sensor-calibration/SKILL.md) |
| Is a pose error due to RGB-D projection, or do the segmented points support several orientations? | [3D object pose and registration](robot-rgbd-pose/SKILL.md) |
| Which observation supports the object's identity and state when part of it is hidden? | [Multimodal object and state grounding](robot-multimodal-grounding/SKILL.md) |
| Why does one detector rarely produce a fresh result while the shared camera still meets its frame-rate target? | [Edge vision model scheduling](robot-edge-vision-scheduling/SKILL.md) |
| How should scan matching and loop closure handle a corridor with little geometric information? | [Lidar SLAM algorithm development](robot-slam-development/SKILL.md) |
| How should sensor rays update a rolling map when an obstacle moves or observations stop? | [Local occupancy and traversability map development](robot-local-costmap-development/SKILL.md) |
| How can a robot find a feasible detour, set its speed, and track the resulting path? | [Navigation planner and path tracking development](robot-navigation-planner-development/SKILL.md) |
| Which recorded signal first explains a missed waypoint? | [Navigation replay](robot-navigation-replay/SKILL.md) |
| Can a fresh robot localize on the correct floor after the saved map is reloaded? | [SLAM map and relocalization acceptance](robot-map-relocalization/SKILL.md) |

## Grasping, planning, and motion control

| Engineering question | Skill |
| --- | --- |
| Which grasp permits both approach and retreat with the object? | [Grasp selection](robot-grasp-selection/SKILL.md) |
| Can an approved picking capability handle a packaging change or a tighter shelf slot? | [Item and packaging qualification](robot-item-onboarding/SKILL.md) |
| How can a captured or authored clip be bound to a different humanoid while preserving planted feet and hand contacts? | [Motion asset binding and retargeting](robot-motion-retargeting/SKILL.md) |
| Does the controller exceed a limit between valid waypoints? | [Trajectory retiming](robot-trajectory-retiming/SKILL.md) |
| Which workspace regions produce invalid trajectories or excessive refusals from a particular arm planner? | [Manipulator workspace regression](robot-planner-workspace-regression/SKILL.md) |
| A plan succeeded. Where did dispatch, base-to-arm handoff or measured motion first diverge? | [Motion execution and tracking](robot-motion-validation/SKILL.md) |
| Did the simulated object stay supported after release, or did an attachment or scoring shortcut keep it in place? | [Contact task simulation](robot-sim-contact-validation/SKILL.md) |
| After restoring a mid-task snapshot, does the same action reproduce the uninterrupted contact and motion? | [Simulation snapshot and branch verification](robot-sim-state-restore/SKILL.md) |
| Did the preview show this run before it finished, and did rendering affect the result? | [Live simulation preview verification](robot-simulation-preview/SKILL.md) |
| Can the humanoid follow the commanded velocity and stay upright across a full trial? | [Locomotion simulation evaluation](robot-locomotion-sim-eval/SKILL.md) |
| Does reflecting a policy sample produce the expected motion of the opposite limb? | [Left-right policy symmetry](robot-policy-symmetry/SKILL.md) |

## Teleoperation and demonstration data

| Engineering question | Skill |
| --- | --- |
| Which operator can command the robot after a handoff? | [Session ownership](robot-teleop-session/SKILL.md) |
| Which mapping reversed the operator's gripper or arm input? | [Controller mapping](robot-teleop-bringup/SKILL.md) |
| Which capture method can supply the labels the intended training objective needs? | [Demonstration capture design](robot-capture-design/SKILL.md) |
| Are the converted episodes usable, and which consecutive takeover actions qualify as expert labels? | [Episode and takeover label audit](robot-episode-audit/SKILL.md) |
| Can the current reader migrate old episodes while preserving unknown times, labels and native stream rates? | [Episode metadata migration](robot-episode-schema-migration/SKILL.md) |
| Can a running recorder seal and upload a session while keeping later messages and retries accountable? | [Continuous bag recording and rotation](robot-bag-recording/SKILL.md) |

## Policy training and evaluation

| Engineering question | Skill |
| --- | --- |
| Does this failure call for new supervision, a parameter update, or an execution fix? | [Policy training and RSI](robot-policy-training/SKILL.md) |
| Which rollout stage actually caused the failure, and would a matched recovery branch distinguish it from an upstream change? | [RSI failure attribution](robot-rsi-failure-attribution/SKILL.md) |
| Which learner states should receive expert queries or takeover corrections, and which targets can those records support? | [RSI correction data design](robot-rsi-correction-design/SKILL.md) |
| Can this RSI generation become the next parent under retention and independent acceptance rules? | [RSI candidate promotion and frozen acceptance](robot-rsi-candidate-promotion/SKILL.md) |
| Which precision fits the memory budget, resumes correctly and reloads for inference? | [Training precision and checkpoint comparison](robot-training-precision/SKILL.md) |
| How many GPU-hours and calendar days will the planned multimodal training run require? | [Robot training compute sizing](robot-training-capacity/SKILL.md) |
| Can a checkpoint supply usable actions on time, and which policy wins on matched trials? | [Policy evaluation](robot-policy-eval/SKILL.md) |

## Robot platform and cloud services

| Engineering question | Skill |
| --- | --- |
| Can the same device recover its identity and connections after a retry? | [Device onboarding](robot-device-onboarding/SKILL.md) |
| Which release and permissions did this device session actually use? | [Agent binding](robot-agent-binding-review/SKILL.md) |
| Will both the rule router and the model fallback recognize a new robot intent? | [Intent routing and catalog regression](robot-intent-routing/SKILL.md) |
| When a speaker moves to a second device, which knowledge, preferences and conversation fields may follow? | [Shared robot knowledge and session memory](robot-agent-context/SKILL.md) |
| How should a retry affect the task, and which receipt is missing when a run shows completion too early? | [Task protocol and incident tracing](robot-task-protocol/SKILL.md) |
| Did a turn replay after interruption, or did the audio queue run dry during continuous speech? | [Speech playback and continuity](robot-voice-playback/SKILL.md) |
| Which tenants and robots still resolve a withdrawn or superseded revision? | [Action asset release](robot-action-release/SKILL.md) |

## Engineering methods for agents and technical learning

| Engineering question | Skill |
| --- | --- |
| Two agent workflows have the same pass rate. Which tasks did each solve, and at what cost? | [Paired agent harness evaluation](agent-harness-comparison/SKILL.md) |
| Which execution environment actually read the input, ran the job and produced the artifact? | [Agent execution placement](agent-execution-placement/SKILL.md) |
| How can a learner test one technical claim, review a mistake, and resume at the next unanswered question? | [Technical study labs and review cards](technical-study-lab/SKILL.md) |

## Interactive tools and offline archives

| Engineering question | Skill |
| --- | --- |
| How can an interactive session resume in the right phase and ignore callbacks from an earlier run? | [Pause, resume and restart](interactive-run-lifecycle/SKILL.md) |
| Which evaluation trials, details and camera views can a reader still open after going offline? | [Offline evaluation archive verification](offline-evaluation-archive/SKILL.md) |

## Skill distribution and technical publishing

| Engineering question | Skill |
| --- | --- |
| Can several agent hosts discover the same skill and its resources while preserving user-installed packages? | [Distributing a skill collection](skill-distribution/SKILL.md) |
| Which translations, exports and bundles still carry an outdated technical claim? | [Synchronizing document variants](document-variant-sync/SKILL.md) |
