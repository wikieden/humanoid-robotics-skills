---
name: robot-navigation-replay
description: Use recorded sensor data, maps, and navigation logs to reproduce localization drift, obstacle avoidance errors, or missed goals and trace the fault from SLAM through planning, tracking, and base feedback.
metadata:
  title: Mapping and Navigation Replay
---

# Mapping and Navigation Replay

Fix the map version, robot model, start pose, goal, and time window for one failed attempt. Identify the active navigation backend from its launch configuration. If planner output is visible, trace the path, velocity, and base feedback. For an SDK-only interface, start by aligning status events with base acknowledgments.

1. Inventory the laser scans or point clouds, odometry, transforms (TF), goals, velocities, and execution states present in the recording. Identify whether the stack was mapping or localizing. Check the extrinsics and the continuity of the map-to-odometry-to-base transform chain at the time of failure. State how far the recording supports replay if a required topic is missing.
2. Replay with the recorded clock, map, and parameters in an environment isolated from the robot. Verify that floor data, points of interest, exclusion zones, and obstacle layers align in a common frame. For a localization jump, inspect raw sensor data and transforms first.
   If a nearby obstacle moves in the base frame as a camera mount turns while both the base and obstacle are stationary, compare the sensor timestamp with the joint state used for its transform. Use the [extrinsic calibration workflow](../robot-sensor-calibration/SKILL.md) to test the rigid mounting offset separately.
3. Where localization is stable, trace the global path, local avoidance output, tracking velocity, odometry response, and terminal action state in order. If the path is valid but tracking velocity is zero, inspect local obstacles, controller state, and the recorded stop reason. For an SDK backend, identify which events the interface exposes.
4. Change one parameter at a time on the same recorded interval and compare the time and location of the first divergence. Fixed-input rosbag replay can test perception and decision outputs. Use closed-loop simulation or a physical trial to measure how a change affects the resulting trajectory.

**Deliverable.** Give the recording interval, map version, launch configuration, and replay entry point. Identify the first abnormal signal, supporting evidence, and missing observations. For repeated goal attempts, give successes out of total attempts, goal tolerance, and failure categories.
