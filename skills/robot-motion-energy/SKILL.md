---
name: robot-motion-energy
description: Estimate electrical load and battery runtime from robot motion traces. Use when comparing gaits, postures or payloads, or when a simulation report gives joint torque without battery-side measurements.
metadata:
  title: Estimating Actuator Load and Battery Runtime
---

# Estimating Actuator Load and Battery Runtime

Define the task and operating cycle. Include durations spent idle, holding a load, moving and recovering. Record the achieved motion, payload, supply voltage, actuator revision and whether each trace was simulated or measured. Compare motions at matched task outcomes and report falls or early stops alongside estimates computed from completed trials.

1. Establish the measurement boundary for every signal. Pair torque and angular speed at the same shaft and time. If the model produces joint-side torque and the motor constant is motor-side, account for gearing, direction and transmission losses. Check whether the reported effort is commanded, limited or actually applied.
2. Separate motion work from winding losses. For a constant-matched simple motor model, estimate current from torque and copper loss from current squared times resistance. At zero speed a holding joint can draw current. Use the actuator's winding/current convention and speed-dependent loss data where available. Keep electronics, sensors, compute and conversion losses as explicit terms.
3. Treat braking according to the drive and battery behavior. Credit returned energy only when supported by the actual power path. At each timestamp sum loads on the common bus before computing system peaks. Winding currents, peak currents at different times, and current measured at the battery describe different quantities.
4. Integrate pack power over time for energy per task. For mission runtime, weight pack power by time in each mode and divide usable watt-hours by that mean power. Record the assumed usable energy, duty mix and measurement interval. Report peak electrical demand and per-joint RMS current separately. A modeled heat source in watts needs thermal measurements or a thermal model before it can support a temperature prediction.

**Counterexample.** A joint alternates between equal positive and negative current. Its signed mean current is zero while copper loss remains positive. A separate synthetic duty cycle illustrates runtime from pack-level power.

```python
currents_a = (2.0, -2.0)
resistance_ohm = 0.5
mean_copper_w = sum(i * i * resistance_ohm for i in currents_a) / len(currents_a)
assert sum(currents_a) == 0 and mean_copper_w == 2.0
mean_pack_w = (1 * 12 + 3 * 4) / 4
assert 18 / mean_pack_w == 3  # hours from 18 usable Wh
```

**Deliverable.** Provide energy per completed task, survivor and failure counts, time-weighted mission runtime, peak bus demand where observable, and the most consequential uncertainty. Label the result as modeled, bench-calibrated or measured on the operating robot.
