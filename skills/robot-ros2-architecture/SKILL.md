---
name: robot-ros2-architecture
description: Design or review a humanoid ROS 2 architecture. Trace perception, state estimation, planning, teleoperation, control, and safety across node, process, Pod, and hardware boundaries. Use for interface design, timing budgets, control ownership, and restart behavior.
metadata:
  title: Humanoid ROS 2 Architecture Design and Review
---

# Humanoid ROS 2 Architecture Design and Review

Start from a maneuver and a fault. For example, the robot reaches with one arm while balancing, then the perception process restarts. What data does balance still receive? Who owns the arm commands? What evidence permits the task to resume? Record whether the platform is legged or wheeled, its support mode, the control interfaces, and which controller owns stabilization.

## Design a new stack

1. Trace one observation to one physical command. Include capture time, estimator output, planner or policy proposal, command arbitration, controller update, drive acceptance, and independently measured joint state. Identify where the loop closes. Place high-rate stabilization and its fallback on components that can meet the timing and availability requirements when perception, inference, or networking stalls.
2. Assign authority for each resource during idle, autonomous execution, teleoperation, and recovery. Cover arm, gripper, torso, neck, and base or legs where present. Whole-body control can couple resources that appear independent at the task level. Specify who grants ownership, rejects overlapping commands, and handles an old trajectory when ownership changes.
3. Write an interface table with producer, consumer, type, units, frame, timestamp source, expected rate or latency, maximum usable sample age, and fault behavior. Use topics for streams, services for bounded request/reply, and actions for goals with feedback, cancellation, and a terminal result. A cancellation acknowledgment still needs a defined physical completion condition. For each important DDS connection, compare offered and requested QoS, including reliability, durability, and queue depth; check freshness separately. [ROS 2 QoS](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Quality-of-Service-Settings.html)
4. Draw two views. The ROS graph shows nodes, endpoints, TF authorities, controller claims, and public interfaces versus vendor or algorithm adapters. The deployment view maps those nodes to executors, processes, containers, Pods, hosts, devices, and restart units. Give a reason for co-location, such as latency or shared lifecycle, and describe which functions fail together. For articulated cameras, verify the transform chain at exposure time across moving head, torso, and wrist joints.
5. Allocate a timing budget along the chosen path. Include executor and callback contention, transport, inference, controller scheduling, and missed cycles. Measure under representative sensor and compute load. For legged operation, identify what a planner stall or controller restart does to support and balance. The robot-specific safe response may require an active lower-level controller. [Controller manager documentation](https://control.ros.org/jazzy/doc/ros2_control/controller_manager/doc/userdoc.html)

## Review an existing stack

Read package manifests, interface definitions, launch includes, remaps, controller configuration, and the actual Pod or service manifests. Reconstruct the deployed graph from the selected launch arguments and overlays. Mark each finding as design intent, source/configuration evidence, observed runtime behavior, or measured hardware outcome.

| Review question | Evidence and discriminating check |
| --- | --- |
| Can two command sources reach the same joints? | Trace both paths through the final arbiter, including direct driver interfaces. In simulation, switch owner with an old action still pending and check which generation the drive receives. |
| Can the graph look healthy while data is unusable? | Inspect endpoint types and QoS, sample timestamps, TF authority and age, and controller state. A visible joint-state topic with repeated old samples can coexist with a healthy process. |
| Can a sensor or inference restart interrupt stabilization? | Map the shared executor, process, Pod, and host dependencies. Use a recorded interruption or isolated simulation to check feedback continuity and the controller's fallback. |
| Does activation or recovery replay a stale trajectory? | Trace startup dependencies, lifecycle activation, controller switching, reset and goal cancellation. Identify the event that grants fresh authority after feedback returns. |

**Deliverable.** For design, return the two views, an interface and ownership table, and the acceptance test for the critical path. For review, report each finding with its source or trace, affected maneuver, failure consequence, and smallest confirming test. Give separate conclusions for graph correctness, timing, and physical behavior. For a release or environment change, continue with [ROS 2 Pod Deployment and Isolation (optional)](../robot-ros2-pod-deployment/SKILL.md).
