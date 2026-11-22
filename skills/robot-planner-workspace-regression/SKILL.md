---
name: robot-planner-workspace-regression
description: Test arm planning interfaces across their workspace. Use when a planner works near the neutral pose but rejects feasible requests, jumps between inverse-kinematics branches or reports unsafe or incorrect trajectories near boundaries.
metadata:
  title: Workspace Regression for Manipulator Planners
---

# Workspace Regression for Manipulator Planners

Pin the robot model, environment, start-state generator, frames, planner settings and random seeds. Use an isolated planning interface. Distinguish sampling of the joint domain from coverage of tool positions and orientations. A redundant arm can reach one tool pose from configurations with very different clearance.

1. Build a repeatable sample set from single-joint limits, boundary combinations and low-discrepancy or seeded joint configurations. Separate invalid starts and deliberately difficult cases. Track tool-space cells, orientation bins and distinct arm postures. Include both arms where supported. Report the tested region and counts so a small smoke run is recognizable.
2. Construct paired local requests around valid starts. Use forward kinematics of a nearby valid joint configuration to provide a witness for the target pose. For an IK result, pass the returned joints through forward kinematics and report translation and rotation residuals against that target. A reachable endpoint alone does not witness a collision-free path or an exact Cartesian line. If claiming a route exists, retain an independently checked reference path for that task type.
3. Invoke the public planning interface that the application uses. Independently check returned trajectories for finite values, timestamps, endpoint errors, joint and coupled limits, joint discontinuities, and collisions between waypoints at a declared checking resolution. Retain a test whose endpoints clear but whose interpolated motion intersects an obstacle.
4. Score valid success, explained rejection, unexplained failure and invalid success separately. Break results down by planner, workspace region and posture. For requests with verified feasible routes, report the fraction solved. A planner that explicitly refuses every request can have zero invalid successes and still be unusable.

**Counterexample.** On six synthetic requests with known feasible paths, the planner returns four trajectories and two explicit refusals. One returned trajectory violates a coupled limit. Valid success is three of six, invalid success is one of six, and explained rejection is two of six. The four success flags alone would conceal both the constraint violation and the coverage loss.

**Deliverable.** Return the sampling manifest, coverage and outcome table, and a reproducible witness for each invalid success. Keep planning-only results separate from tracking and hardware execution.
