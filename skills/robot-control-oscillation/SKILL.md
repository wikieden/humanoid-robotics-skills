---
name: robot-control-oscillation
description: Diagnose oscillation, overshoot, prolonged settling or possible integral windup in a robot joint or tool control loop. Use when steady or step commands produce repeated motion, residual oscillation or sustained effort clipping.
metadata:
  title: Robot Control Oscillation Diagnosis
---

# Robot Control Oscillation Diagnosis

Start with a repeatable held setpoint or logged step response. Record the controller revision, measured sampling intervals, load, contact state and actuator limits. Take the actual controller setpoint, measured position and velocity, requested and applied effort, and integral state when available. Check feedback gaps and align clocks using timestamps or synchronization events.

1. Find the phase in which oscillation starts. Use a steady-command window and label contact, mode switches, trajectory boundaries and saturation. Measure amplitude and cycle period in that window. Use a deadband based on sensor resolution and observed noise, and break crossing counts at unobserved gaps. For a roughly periodic signal, two sign crossings span about one cycle. Treat a high crossing rate as a screening signal.
2. Check step response against the commanded final setpoint. Measure overshoot relative to the commanded step amplitude. Declare the settling band and required observation interval. If the run ends too soon or feedback has gaps, leave settling unconfirmed. For a cyclic command, report tracking amplitude and phase error against the reference.
3. Separate plausible mechanisms with signals and controlled comparisons. If the oscillation begins in the setpoint, inspect command interpolation and dispatch. If measured effort clips at a known bound and the integrator grows while the command is limited, inspect how the integrator behaves after the error reverses. Clipping alone is insufficient evidence of windup. If vibration begins at contact under the same command, compare matched contact and free-space traces. Check whether oscillations are present in independently measured motion or only in feedback. [ROS 2 PID API and anti-windup](https://control.ros.org/jazzy/doc/api/classcontrol__toolbox_1_1Pid.html)
4. Isolate one change on replay or in simulation. Repeat the same setpoint, load and measurement window with the baseline and candidate. Compare oscillation amplitude, tracking error, settling, effort and saturation duration. Record the first signal that changed and reproduce the prior symptom in an unchanged control.

**Offline example.** A controller can match its final command at the last sample while failing a required settling window. The fixture assumes uniformly sampled, gap-free data.

```python
def settled_in_final_window(response, target, tolerance, samples):
    return len(response) >= samples and all(
        abs(value - target) <= tolerance for value in response[-samples:]
    )


assert not settled_in_final_window([0.9, 1.06, 0.94, 1.0], 1.0, 0.02, 3)
assert settled_in_final_window([0.9, 1.01, 0.99, 1.0], 1.0, 0.02, 3)
```

**Deliverable.** Report the affected joint, window, command, measured response and effort, supported mechanism or missing signal, and the matched control and candidate outcomes. For dispatch, controller handoff and missing motion, use [Motion Execution and Tracking (optional)](../robot-motion-validation/SKILL.md).
