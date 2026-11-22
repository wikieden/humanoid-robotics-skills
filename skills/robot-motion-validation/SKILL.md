---
name: robot-motion-validation
description: Trace a successful robot motion plan through dispatch, controller handoff, and measured tracking. Use when the arm starts early, a controller acknowledges a command but motion is missing, or the tool path diverges during execution.
metadata:
  title: Motion Execution and Tracking Validation
---

# Motion Execution and Tracking Validation

Start with one accepted trajectory and the measured motion from the same attempt. Identify the trajectory revision, joint order, units, tool frame, robot model, control period and active controller. If only the plan is available, record which execution signal is missing.

1. Align the accepted reference, submitted trajectory, controller acceptance, applied setpoints and independent joint feedback. Preserve timestamps and clock domains. On mobile manipulators, include measured base arrival, the condition that releases the arm, arm dispatch and the first measured arm motion. Without a common clock or synchronization bound, use causal ordering and leave cross-clock delay unmeasured.
2. Compare the commanded and measured joints or tool pose at the same trajectory time and in the same frame. Use forward kinematics with the loaded model to reconstruct tool motion when only joint feedback exists. Mark that pose as derived. Record position and orientation errors separately. Preserve missing feedback as a gap.
3. Find the earliest divergence. If execution used a fallback segment, retain both the accepted and dispatched references. If the setpoints match but feedback lags, inspect activation time, active mode and tracking limits. Align controller switches, contact onset, stops and interventions with that first divergent sample.

**Worked case.** A plan succeeds and the base action returns success. A synchronized trace shows arm motion began while the base was still moving outside the handoff tolerance. The first discrepancy lies at the base-to-arm transition. If arm feedback is absent, the same trace can establish dispatch order only.

**Deliverable.** Return a timeline for each attempt, the first observed mismatch (or first missing signal), peak tracking error with its timestamp, and the stop or completion evidence. Label simulation and hardware results separately.

For IK or a planner that returns an invalid path, use [Workspace Regression (optional)](../robot-planner-workspace-regression/SKILL.md). For a command that exceeds limits between valid waypoints, use [Trajectory Retiming (optional)](../robot-trajectory-retiming/SKILL.md). Use [Contact Task Simulation (optional)](../robot-sim-contact-validation/SKILL.md) to assess physical contact or cleaning coverage, and [Policy Evaluation (optional)](../robot-policy-eval/SKILL.md) to compare policies on matched trials.
