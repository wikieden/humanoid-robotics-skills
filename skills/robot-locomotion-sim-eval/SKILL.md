---
name: robot-locomotion-sim-eval
description: Evaluate humanoid walking and velocity-command tracking in simulation. Use for policies that stay upright but drift, shuffle, slip, ignore turns, or change behavior under a different actuator model.
metadata:
  title: Humanoid Locomotion Evaluation in Simulation
---

# Humanoid Locomotion Evaluation in Simulation

State the intended maneuver and its acceptance measures before running the policy. Standing balance, forward tracking, turning, command transitions, and recovery from a push exercise different capabilities. Record a tolerance and evaluation interval for the maneuver, or report measurements without a pass threshold.

1. **Match the simulated plant.** Pin the checkpoint, robot description, body mass and inertia, joint order and sign, action scale and offset, PD gains, torque and speed limits, delays, physics step, policy rate, foot contact geometry, and terrain. Compare the actual evaluation configuration with training. Run changes to the plant as separate experiments.
2. **Build a command matrix.** Include standing, forward and reverse, lateral motion, and turning when supported. Match starting pose, command transitions, duration, terrain, disturbance schedule and seeds across policies. Keep nominal trials separate from stress tests. Save world-frame base pose and time-synchronized commands. For body-frame commands, express measured linear velocity in the matching body or heading frame at the same time; unwrap yaw or use consistent angular velocity for turn tracking.
3. **Trace the first loss of response.** Change the command with other conditions fixed and inspect the observation presented to the policy, its action, the target passed to the actuator, measured joint motion, stance and swing contacts, and base twist. If the action changes but base speed barely changes, inspect saturation, foot clearance and stance slip. A fixed camera with a floor scale helps distinguish body displacement from camera tracking.
4. **Score all attempts.** Report completion, falls and time to fall, survival duration, and tracking error over the observed interval. On completed segments, report steady-state and transition errors separately. Record foot slip during stance, swing clearance, and saturation where observable. Show the attempted count per command and independent seed. Early falls stay in the task denominator even when steady-state tracking is unavailable.

**Offline scoring check.** Three synthetic straight-line trials share a 0.2 m/s command, a 5 s target horizon, and a fixed heading. The first stands still, the second tracks the full command, and the third tracks briefly before falling. Averaging over survivors drops the fall and obscures which trial stood still. This fixture uses distance over observed time. For policy evaluation, also measure time-resolved error.

```python
command = 0.2
horizon = 5.0
trials = [
    # Name, elapsed seconds, forward displacement (m), fell
    ("stationary", 5.0, 0.0, False),
    ("walking",    5.0, 1.0, False),
    ("early fall", 1.0, 0.2, True),
]
passed = []
for name, elapsed, distance, fell in trials:
    mean_speed = distance / elapsed
    tracks = abs(mean_speed - command) <= 0.04
    complete = elapsed >= horizon and not fell
    if complete and tracks:
        passed.append(name)
    print(f"{name}: observed_v={mean_speed:.2f} complete={complete} tracks={tracks}")
assert passed == ["walking"]
```

**Deliverable.** Provide one row per command and trial with plant version, seed, observed tracking interval, falls, and task verdict. Compare the paired gains and losses, show fixed-view evidence for a representative failure, and identify which plant assumptions still need hardware measurement.
