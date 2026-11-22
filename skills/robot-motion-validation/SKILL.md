---
name: robot-motion-validation
description: Validate forward and inverse kinematics, arm trajectories, or mobile manipulation policies. Use this skill to compare SAC and PPO wiping policies or investigate planner fallback, simulated contact, and tracking errors.
metadata:
  title: Motion Control and Reinforcement Learning Validation
---

# Motion Control and Reinforcement Learning Validation

Trace each attempt through goal generation, planning, execution, and task outcome. Collect the robot's URDF, calibration, control period, constraints, and run record. For policy-driven tasks, also collect the checkpoint, scene, reward definition, and random seed.

1. Check base, end-effector, and tool frames, joint names and order, and position and velocity limits. Verify that the controller and simulator load the same robot description. Compute forward kinematics (FK) for a known joint state. Solve inverse kinematics (IK) for a reachable pose, pass the solution through FK, and report position and orientation residuals separately.
2. For a surface-cleaning comparison, start from the same stain distribution and observations. Save the wipe segment selected by the policy, the planned trajectory, and the solver status. Count joint solves, sequential fallbacks, and infeasible attempts separately. Use the same environment, action representation, and evaluation budget for each policy.
3. Align commanded and observed end-effector trajectories with contact force, surface clearance, and collision events in simulation. Use the measured roller path during effective contact to compute cleaning coverage. Compare planned coverage with observed stain removal.
4. When reviewing hardware logs, identify differences from the simulated execution mode. If the base moves before the arm, compare the time the base reached its goal with the arm start time. Confirm which contact controller was active. Record stop times and human interventions after limit violations or unexpected contact.

**Deliverable.** Use one row per attempt for initial conditions, policy, solver mode, tracking error, contact or cleaning outcome, and termination reason. Identify the earliest divergence and attach the relevant trace or log. Report sample counts separately for the policy environment, physics simulation, and hardware.
