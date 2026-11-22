---
name: robot-trajectory-retiming
description: Develop or review the conversion of geometric robot paths into timed trajectories. Diagnose joint or tool limit violations between waypoints, unintended speed valleys, and regressions introduced by smoothing or repeated retiming.
metadata:
  title: Trajectory Retiming and Controller Interpolation
---

# Trajectory Retiming and Controller Interpolation

Take one reproducible geometric path or timed command, its semantic phase boundaries, the active controller's interpolation mode, and the applicable joint and tool limits. Keep copies of the input path, the result of the time parameterizer, and the exact message received by the controller.

1. Identify which stage owns geometry and which owns timing. Record approach, contact, retreat, and transfer boundaries by index. Detect timed input entering a geometry-only stage. When smoothing or path fitting can move waypoints, recheck clearance and task constraints on the resulting path. [Time parameterization and path deviation](https://moveit.picknik.ai/main/doc/examples/time_parameterization/time_parameterization_tutorial.html)
2. Reconstruct the interpolation actually executed. For the Jazzy joint trajectory controller in spline mode, positions at both ends give a linear segment, adding velocities gives a cubic, and adding accelerations as well gives a quintic. An array of zeros is a supplied field. Inspect both endpoints of the received message and the active mode. Derivative-only input, integration and other controllers need their own reconstruction. [Controller trajectory representations](https://control.ros.org/jazzy/doc/ros2_controllers/joint_trajectory_controller/doc/trajectory.html)
   For each polynomial segment, test both endpoints and every interior root of the derivative of the quantity being bounded. For example, acceleration extrema of a quintic require the interior roots of jerk. Check one-sided values at joins. A cubic with an acceleration jump at a knot has no finite global jerk bound there.
3. Audit the joint and tool profiles together. Use the path configuration and actual joint velocity vector to compute tool velocity through the Jacobian. Record the joint, constraint, phase, and timestamp at each limiting event. Compare a local approach slowdown with a transfer slowdown away from contact. Diagnose geometric reversals or IK branch changes before increasing global segment durations.
4. Compare algorithms on the same starts, endpoints, scenes, and budgets. On jointly successful requests, compare execution duration, additional joint travel, peak dynamics, and unexpected speed valleys. Across all requests, count gained and lost successes separately and report planning wall time including failures. Keep sampled collision clearance and analytical joint extrema as distinct results.

**Offline counterexample.** A joint moves one radian in one second with zero velocity at both ends. With cubic Hermite interpolation its normalized position is `3u² - 2u³`. The test below compares endpoint-only validation with the interior extremum for a synthetic speed limit of 1.2 rad/s.

```python
def peak_speed(duration):
    def speed(u):
        return (6 * u - 6 * u * u) / duration

    # Acceleration is zero at u=0.5. Include both endpoints as well.
    return max(abs(speed(u)) for u in (0, 0.5, 1))


limit = 1.2
assert 0.0 <= limit < peak_speed(1.0)
assert peak_speed(1.5) <= limit
print(f"peak at 1 s={peak_speed(1.0):g}, peak at 1.5 s={peak_speed(1.5):g} rad/s")

# Same move in 1 s, also supplying zero acceleration at both ends.
# The quintic position is 10u³ - 15u⁴ + 6u⁵. Speed peaks at u=0.5.
u = 0.5
quintic_peak = 30 * u**2 * (1 - u)**2
assert peak_speed(1.0) == 1.5 <= 1.6 < quintic_peak == 1.875
print(f"1.6 rad/s limit: cubic passes, quintic peaks at {quintic_peak:g} rad/s")
```

**Deliverable.** Identify the first processing stage that produces a violation, provide the offending segment and interpolation parameters, and compare the original and revised curves under the same controller contract. For a feasible command that the robot failed to track, use [Motion Execution and Tracking Validation (optional)](../robot-motion-validation/SKILL.md).
