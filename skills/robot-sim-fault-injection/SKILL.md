---
name: robot-sim-fault-injection
description: Verify that an injected robot simulation fault actually takes effect and identify which layer responds. Use for matched clean and faulted runs, skipped injections, fallback backends, or evidence that a recovery handles a specific fault.
metadata:
  title: Simulation Fault Injection and Attribution
---

# Simulation Fault Injection and Attribution

Start with a reproducible simulation case, a fault hypothesis and the decision the experiment needs to support. Choose an event that can be measured at the affected interface, such as detachment while the gripper is still commanded closed.

1. Define the fault contract. Record the affected channel, trigger, magnitude, frame, units and end condition. Use simulation time or a named event for the trigger. Freeze scene, controller, policy, seed and effective backend across the clean and injected arms. For stochastic faults, use a separate random stream or record the actual perturbation sequence. If camera rendering falls back to synthetic observations in one arm, report a separate backend case.
2. Verify delivery before comparing outcomes. Trace the requested setting through schema normalization into the effective configuration and then to a step-stamped measurement on the affected channel. Classify each run as applied, eligible but no application observed, trigger not reached, or unknown due to missing evidence. Keep every run in the activation ledger. A slip scheduled after attachment cannot exercise recovery when the grasp never attaches.
3. Compare first divergence under one fault. Keep a clean control, then add one fault at a time. Measure trigger reach, activation, downstream detection, recovery or stop, and terminal physical outcome. Use a known-applied positive control for the detector and an unreached-trigger case for scoring. Distinguish an injected disturbance, a rule finding and a hypothesized cause. Prefer an independently measured effect when the diagnostic can see the injected-fault label. Run combinations when interactions are the question.
4. Save the replay inputs, effective backend and configuration, time-aligned applied events, per-run outcome and evidence of the first divergence. Report application rate and recovery conditional on application alongside whole-task success. For comparing two policies, show which matched trials actually exercised the affected stage and retain the unconditional outcome counts.

**Offline example.** A grasp never attaches in one configured slip run. Another run drops the object while the gripper remains closed.

```python
def activation(steps):
    if "slip_applied" in steps:
        return "applied"
    if "attachment" in steps:
        return "eligible_without_application_evidence"
    return "trigger_not_reached"


assert activation(["approach", "grasp_missed"]) == "trigger_not_reached"
assert activation(["attachment", "timeout"]) == "eligible_without_application_evidence"
assert activation(["attachment", "slip_applied", "drop"]) == "applied"
```

**Deliverable.** Provide the fault and acceptance criteria, clean and faulted run IDs, trigger and application evidence, first observed divergence, and recovery and task outcomes with denominators. State the simulated grasp and perception mechanisms that produced the result. For preview timing, use [Simulation Preview (optional)](../robot-simulation-preview/SKILL.md).
