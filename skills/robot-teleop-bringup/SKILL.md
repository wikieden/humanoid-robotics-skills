---
name: robot-teleop-bringup
description: Bring up or troubleshoot dual-arm teleoperation with handheld or XR controllers. Trace swapped arms, reversed gripper motion, or jumps after reconnecting from controller input through IK, driver commands, independent feedback, and recorded data.
metadata:
  title: Dual-Arm Teleoperation Bring-Up and Mapping Validation
---

# Dual-Arm Teleoperation Bring-Up and Mapping Validation

Choose a recording in which only one input changes. Identify which side first diverges from the operator's intent and at what stage. Prefer existing logs, offline tests, or isolated simulation. Physical motion, homing, and replay that sends actuator commands require authorization for the hardware run.

## Identify the active mapping

Record the robot model, gripper model, input software version, control mode, and recording version. Follow the active launch configuration through controller input, arm mapping, inverse kinematics (IK), driver, and recorder. If the same entry point can select simulation or hardware, confirm the backend and end effector loaded for this run.

## Trace one movement

1. Choose a clip with a stationary baseline, such as a single squeeze and release of the left trigger. At each stage, record both sides' values before and after the input, units, timestamps, and signal sources. For different device clocks, establish synchronization or identify a shared event. If only arrival order is available, record end-to-end latency as unknown.
2. For a gripper, compare trigger input, mapped opening target, command received by the driver, and independently measured position. Use the gripper's known open and closed endpoints to interpret the direction. Increasing trigger pressure can correctly map to a smaller opening. A command echo verifies only the command stage.
3. For an arm, use a single-axis translation or rotation to check controller and base frames, left and right transforms, orientation conventions, and absolute or incremental mode. Follow the end-effector target, IK result, joint targets, and measured joints. For a jump on re-enable, compare the reference poses on either side of the transition and inspect the first new target.
4. Use the idle side as a control. If left-only input first changes the right target, inspect side routing or mirroring. If the reversal appears only in the camera view, check independent joint feedback before changing the mapping. For a limit, IK failure, or rejection by the active control mode, record the state and output at that instant.
5. Verify that the recording contains the command actually committed to the actuator and independent feedback. If the raw record is correct but direction changes in the training tensor, continue from the recorded field to the loader using [Teleoperation Episode and Training Dataset Audit (optional)](../robot-episode-audit/SKILL.md).

**Deliverable.** Trace operator intent, input, mapped target, driver command, measured motion, and recorded value in a single table. Include the clip ID, last verified stage, first contradiction, and next check that would distinguish the remaining causes. If only interface documentation is available, identify the minimum signals to collect and leave the physical direction unconfirmed.
