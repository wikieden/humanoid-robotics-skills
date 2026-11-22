---
name: robot-trajectory-retiming
description: Develop or review the conversion of geometric robot paths into timed trajectories. Diagnose joint or tool limit violations between waypoints, unintended speed valleys, and regressions introduced by smoothing or repeated retiming.
metadata:
  title: Trajectory Retiming and Controller Interpolation
---

# Trajectory Retiming and Controller Interpolation

Take one reproducible geometric path or timed command, its semantic phase boundaries, the active controller's interpolation mode, and the applicable joint and tool limits. Keep copies of the input path, the result of the time parameterizer, and the exact message received by the controller.

1. Identify which stage owns geometry and which owns timing. Record approach, contact, retreat, and transfer boundaries by index. Detect timed input entering a geometry-only stage. When smoothing or path fitting can move waypoints, recheck clearance and task constraints on the resulting path. [Time parameterization and path deviation](https://moveit.picknik.ai/main/doc/examples/time_parameterization/time_parameterization_tutorial.html)
2. Reconstruct the interpolation actually executed. Inspect which positions, velocities, and accelerations reach the active controller and the selected interpolation mode. For a cubic Hermite segment, test position at the endpoints and interior roots of velocity, velocity at the endpoints and interior roots of acceleration, and acceleration on both sides of joins. A cubic can have a jump in acceleration at a knot. A finite jerk inside each segment gives no global jerk bound at that knot. [Controller trajectory representations](https://control.ros.org/jazzy/doc/ros2_controllers/joint_trajectory_controller/doc/trajectory.html)
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
```

**Deliverable.** Identify the first processing stage that produces a violation, provide the offending segment and interpolation parameters, and compare the original and revised curves under the same controller contract. A numerically feasible command still needs separate execution evidence. For broader task outcomes, use [Motion Control Validation](../robot-motion-validation/SKILL.md).
