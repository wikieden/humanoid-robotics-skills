# Workflow Directory

Choose a package by the engineering question. The package name locates its `SKILL.md` using the lookup order in the entry skill.

## Systems, deployment, and safety

| Question | Package |
| --- | --- |
| Who owns each joint if a process restarts mid-maneuver? | `robot-ros2-architecture` |
| Which devices and DDS traffic can each Pod access? | `robot-ros2-pod-deployment` |
| How can a brief, real capture or generated 3D asset become a repeatable robot algorithm test environment? | `robot-sim-environment-build` |
| Where did a command or acknowledgment stop between Linux and the MCU? | `robot-embedded-bringup` |
| After an interrupted update, which controller, host and model versions are actually active together? | `robot-update-recovery` |
| Why are arm joints still visible while the planner rejects its start state after a gripper feedback gap? | `robot-joint-feedback` |
| What establishes standstill, and what prevents motion after reset? | `robot-safety-policy` |
| A new cover fits at rest. Which two surfaces come closest when its joints move together? | `robot-shell-clearance` |
| What electrical load does a motion impose, and how long would the battery last over the full duty cycle? | `robot-motion-energy` |

## Perception, calibration, and navigation

| Question | Package |
| --- | --- |
| Does a stationary target shift in the base frame when the camera mount turns? | `robot-sensor-calibration` |
| Is a pose error due to RGB-D projection, or do the segmented points support several orientations? | `robot-rgbd-pose` |
| Which observation supports the object's identity and state when part of it is hidden? | `robot-multimodal-grounding` |
| Why does one detector rarely produce a fresh result while the shared camera still meets its frame-rate target? | `robot-edge-vision-scheduling` |
| How should scan matching and loop closure handle a corridor with little geometric information? | `robot-slam-development` |
| How should sensor rays update a rolling map when an obstacle moves or observations stop? | `robot-local-costmap-development` |
| How can a robot find a feasible detour, set its speed, and track the resulting path? | `robot-navigation-planner-development` |
| Which recorded signal first explains a missed waypoint? | `robot-navigation-replay` |
| Can a fresh robot localize on the correct floor after the saved map is reloaded? | `robot-map-relocalization` |

## Grasping, planning, and motion control

| Question | Package |
| --- | --- |
| Which grasp permits both approach and retreat with the object? | `robot-grasp-selection` |
| Can an approved picking capability handle a packaging change or a tighter shelf slot? | `robot-item-onboarding` |
| How can a captured or authored clip be bound to a different humanoid while preserving planted feet and hand contacts? | `robot-motion-retargeting` |
| Does the controller exceed a limit between valid waypoints? | `robot-trajectory-retiming` |
| Which workspace regions produce invalid trajectories or excessive refusals from a particular arm planner? | `robot-planner-workspace-regression` |
| A plan succeeded. Where did dispatch, base-to-arm handoff or measured motion first diverge? | `robot-motion-validation` |
| Did the simulated object stay supported after release, or did an attachment or scoring shortcut keep it in place? | `robot-sim-contact-validation` |
| After restoring a mid-task snapshot, does the same action reproduce the uninterrupted contact and motion? | `robot-sim-state-restore` |
| Did the preview show this run before it finished, and did rendering affect the result? | `robot-simulation-preview` |
| Can the humanoid follow the commanded velocity and stay upright across a full trial? | `robot-locomotion-sim-eval` |
| Does reflecting a policy sample produce the expected motion of the opposite limb? | `robot-policy-symmetry` |

## Teleoperation and demonstration data

| Question | Package |
| --- | --- |
| Which operator can command the robot after a handoff? | `robot-teleop-session` |
| Which mapping reversed the operator's gripper or arm input? | `robot-teleop-bringup` |
| Which capture method can supply the labels the intended training objective needs? | `robot-capture-design` |
| Are the converted episodes usable, and which consecutive takeover actions qualify as expert labels? | `robot-episode-audit` |
| Can the current reader migrate old episodes while preserving unknown times, labels and native stream rates? | `robot-episode-schema-migration` |
| Can a running recorder seal and upload a session while keeping later messages and retries accountable? | `robot-bag-recording` |

## Policy training and evaluation

| Question | Package |
| --- | --- |
| Given mixed feedback, which update should we make this round: train parameters, collect supervision, or repair execution? | `robot-policy-training` |
| Which rollout stage actually caused the failure, and would a matched recovery branch distinguish it from an upstream change? | `robot-rsi-failure-attribution` |
| Which learner states should receive expert queries or takeover corrections, and which targets can those records support? | `robot-rsi-correction-design` |
| Can this RSI generation become the next parent under retention and independent acceptance rules? | `robot-rsi-candidate-promotion` |
| Which precision fits the memory budget, resumes correctly and reloads for inference? | `robot-training-precision` |
| How many GPU-hours and calendar days will the planned multimodal training run require? | `robot-training-capacity` |
| Can a checkpoint supply usable actions on time, and which policy wins on matched trials? | `robot-policy-eval` |

## Robot platform and cloud services

| Question | Package |
| --- | --- |
| Can the same device recover its identity and connections after a retry? | `robot-device-onboarding` |
| Which release and permissions did this device session actually use? | `robot-agent-binding-review` |
| Will both the rule router and the model fallback recognize a new robot intent? | `robot-intent-routing` |
| When a speaker moves to a second device, which knowledge, preferences and conversation fields may follow? | `robot-agent-context` |
| How should a retry affect the task, and which receipt is missing when a run shows completion too early? | `robot-task-protocol` |
| Did a turn replay after interruption, or did the audio queue run dry during continuous speech? | `robot-voice-playback` |
| Which tenants and robots still resolve a withdrawn or superseded revision? | `robot-action-release` |

## Engineering methods for agents and technical learning

| Question | Package |
| --- | --- |
| Two agent workflows have the same pass rate. Which tasks did each solve, and at what cost? | `agent-harness-comparison` |
| Which execution environment actually read the input, ran the job and produced the artifact? | `agent-execution-placement` |
| How can a learner test one technical claim, review a mistake, and resume at the next unanswered question? | `technical-study-lab` |

## Interactive tools and offline archives

| Question | Package |
| --- | --- |
| How can an interactive session resume in the right phase and ignore callbacks from an earlier run? | `interactive-run-lifecycle` |
| Which evaluation trials, details and camera views can a reader still open after going offline? | `offline-evaluation-archive` |

## Skill distribution and technical publishing

| Question | Package |
| --- | --- |
| Can several agent hosts discover the same skill and its resources while preserving user-installed packages? | `skill-distribution` |
| Which translations, exports and bundles still carry an outdated technical claim? | `document-variant-sync` |
