---
name: robot-navigation-planner-development
description: Design or modify global search, local replanning, speed profiling, and path tracking for mobile robots. Use when choosing a planner state space, adding obstacle detours, or connecting a route to a wheeled or legged motion controller.
metadata:
  title: Navigation Planner and Path Tracking Development
---

# Navigation Planner and Path Tracking Development

Declare the platform command interface first. A differential base accepts forward speed and yaw rate. A holonomic base can also accept lateral speed. For a humanoid, identify whether the consumer accepts a bounded body twist or explicit footsteps, and obtain its feasible turning and stopping envelope. Carry the map revision, route revision, frame and measurement time across the planner and tracker boundary.

## Build a reproducible search baseline

1. On a frozen costmap, implement or reuse Dijkstra with nonnegative edge costs, explicit unknown-cell policy, and a footprint collision test. Define metric edge lengths for axial and diagonal moves. Reject a diagonal that cuts a blocked corner. Keep this search as an oracle on small maps.
2. Add A* using a lower bound in the same units as edge cost. For length plus nonnegative penalties, minimum cost per metre times straight-line distance is admissible. Compare feasibility and total cost with Dijkstra on the same graph. Equal-cost paths can contain different waypoints. Record node expansions and solve time. [Nav2 NavFn planner](https://docs.nav2.org/rolling/configuration_and_development/configuration_guide/planners_plugins/configuring_navfn/)
3. Choose a heading-aware lattice or Hybrid A* if orientation, a minimum turning radius, or reverse motion changes reachability. Collision-check the swept footprint along motion primitives, including in-place turns when the model supports them. Test an opening that admits the robot at only one orientation.

**Closed-set regression.** For optimal graph A* with nonnegative costs, use `h(goal)=0` and finish when the goal is removed from the minimum-`g+h` queue with its current best cost. Permanently closing expanded states requires a consistent heuristic as a general guarantee. Check `h(u) ≤ cost(u,v) + h(v)` on every directed edge, or reopen an expanded state when a cheaper path reaches it if the heuristic is only known to be admissible. [A* search with inconsistent heuristics](https://ijcai.org/proceedings/2009/111)

On the directed edges `S→A:3, S→B:1, B→A:1, A→G:3`, set `h(B)=4` and all other estimates to zero. Each estimate is a lower bound, but the edge B→A violates consistency. A permanent closed set returns cost 6. Reopening A yields S→B→A→G at cost 5, matching Dijkstra. Keep this graph alongside grid cases when changing the queue or heuristic.

## Replan around a local obstacle

Match the current pose to forward progress on the route. At a self-crossing, use heading and prior arc length to disambiguate the branch. Search a bounded region for a detour to a reachable point downstream. Allow a wider or global search when that region has no solution. Report a blocked route if neither search succeeds.

Splice the detour where its position and heading agree with the retained route. If smoothing in Frenet coordinates, use a reference with a locally unique projection and verify curvature at both joins. Recheck the swept footprint after smoothing and after the splice on the current map revision. On a failed check, retain a still-valid collision-checked candidate or request a new plan. Invalidate work that finishes after its goal has been replaced.

## Turn geometry into executable motion

- **Speed profile.** For a forward segment with curvature `k`, cap speed by `sqrt(a_lat / abs(k))` where curvature is nonzero. Apply a backward braking pass from the terminal speed, then a forward acceleration pass from the measured initial speed. If the initial state already exceeds the stopping envelope, report infeasibility. Include observation age, control delay and actuator response in the required stopping distance. Handle reverse segments and zero-distance turns explicitly.
- **Tracking.** For a differential base, start with pure pursuit. For lookahead point `(x, y)` in the base frame, use `k = 2y / (x² + y²)` and `yaw_rate = v * k` away from a zero-length target. Regulated pure pursuit adds velocity and collision constraints. Consider model predictive path integral control (MPPI) when scoring short-horizon motion under dynamics is worth the computation. Roll out the actual motion model, reject infeasible trajectories, and validate the emitted command after weighting and limiting. Record deadline misses as well as cross-track error.
- **Legged handoff.** If the interface accepts twist, limit the reference to the gait controller's verified envelope and use measured velocity and support feedback when tracking progress. For explicit footsteps, use a state containing stance foot, side and pose. Expand alternating step primitives inside the reach envelope, require observed support area, and check swing and body clearance. Compare two scenes on the same body route, one with a reachable next support and one with a gap exceeding step reach. The second must yield a blocked step sequence.

## Minimal regression for a short stop

This Python example isolates the backward pass on a forward path. Two paths have identical curvature at their midpoint. Moving the stop closer changes the midpoint speed limit.

```python
from math import isclose, sqrt


def braking_envelope(curvature, lengths, speed_limit, lateral_accel, braking):
    caps = [
        min(speed_limit, sqrt(lateral_accel / abs(k))) if k else speed_limit
        for k in curvature
    ]
    caps[-1] = 0.0
    for i in reversed(range(len(lengths))):
        reachable = sqrt(caps[i + 1] ** 2 + 2 * braking * lengths[i])
        caps[i] = min(caps[i], reachable)
    return caps


curve = [0.0, 1.0, 0.0]  # 1/m
short = braking_envelope(curve, [0.2, 0.05], 2.0, 0.64, 1.0)
long = braking_envelope(curve, [0.2, 1.0], 2.0, 0.64, 1.0)
assert isclose(short[1], sqrt(0.1)) and isclose(long[1], 0.8)
assert isclose(short[0], sqrt(0.5)) and short[-1] == 0.0
```

**Deliverable.** Return the state and action space, objective, footprint and unknown-space rules, failure behavior, and a regression for the changed stage. Compare planners on the same map and start/goal set. Compare trackers separately on the same timed path, dynamics and command limits. Report feasible routes, swept clearance, solve latency, terminal error, and interventions at the evidence level actually exercised. For an end-to-end missed waypoint, use [Navigation Replay (optional)](../robot-navigation-replay/SKILL.md).
