---
name: robot-slam-development
description: Design or change a lidar SLAM estimator. Use for scan matching, lidar-inertial odometry, keyframe insertion, geometric degeneracy, or loop constraints in a pose graph.
metadata:
  title: Lidar SLAM Algorithm Development
---

# Lidar SLAM Algorithm Development

Choose the state from the sensor mounting and motion. A level planar scanner on a level base can use an SE(2) pose and a scan-to-submap matcher. For a tilting torso or motion across slopes, test whether deskewed 3D lidar with IMU propagation resolves motion that the planar model discards. Keep a planar baseline on the subset where its assumptions hold.

## Implement the front end

1. Define the scan reference time, per-point time units, IMU clock offset, and extrinsic direction. Write a transform test using an off-axis point and a known turn. For a moving sensor mount, interpolate its kinematic transform at acquisition time. Publish continuous local odometry and the global correction as separate transforms.
2. For a 2D matcher, predict a pose and search around it on an existing occupancy submap. For a 3D lidar-inertial estimator, propagate pose, velocity and covariance through the scan with the IMU, bring the returns to a common timestamp, then match against the previous local map. Initialize gravity and biases for the selected state model. Include each measurement once when feeding back the correction.
3. For point-to-plane matching, use the signed distance `nᵀ(Rp + t − q)` from transformed return `p` to the plane at `q` with unit normal `n`. Gate associations by distance and plane quality, robustly weight residuals, and check the analytic Jacobian against finite differences using the same perturbation convention. A small residual beside a long wall can coexist with an unconstrained translation along it.
4. Inspect the weak directions of the measurement information matrix before adding priors or damping. Scale rotation and translation to a declared characteristic length before comparing eigenvalues. In a weak direction, retain the prediction and its uncertainty or declare degraded tracking. Insert an accepted scan or keyframe only after matching. Record overlap, motion since the last insertion, and update time so the insertion policy can be tuned on a fixed recording.

## Add the back end

Anchor one pose to remove the free global transform. Add relative-motion edges with an explicit covariance convention. With poses mapping local points into the map and measurement `Zij` mapping frame j into frame i, use the tangent-space residual `Log(Zij⁻¹ Ti⁻¹ Tj)`. A two-pose graph constructed from one known relative transform should have zero residual at the known solution.

Retrieve loop candidates outside the recent keyframe window, then verify geometry, overlap, and ambiguity before inserting a loop edge. Include two similar corridors that never meet. Log the candidate, verification result, and optimized displacement. Apply accepted graph corrections to global poses and map products under one revision so a controller can continue using continuous odometry.

## Minimal regression for a corridor

Run this Python example with the standard library. Each row encodes a surface-normal constraint `nx * dx + ny * dy = b`. The example isolates the translation block with fixed correspondences and known orientation.

```python
from math import isclose


def solve_translation(rows):
    xx = sum(nx * nx for nx, ny, b in rows)
    xy = sum(nx * ny for nx, ny, b in rows)
    yy = sum(ny * ny for nx, ny, b in rows)
    xb = sum(nx * b for nx, ny, b in rows)
    yb = sum(ny * b for nx, ny, b in rows)
    det = xx * yy - xy * xy
    if det <= 1e-12 * (xx + yy) ** 2:
        return None
    return (yy * xb - xy * yb) / det, (xx * yb - xy * xb) / det


corridor = [(0, 1, -0.2), (0, -1, 0.2)]
assert solve_translation(corridor) is None
dx, dy = solve_translation(corridor + [(1, 0, 0.3)])
assert isclose(dx, 0.3) and isclose(dy, -0.2)
```

**Deliverable.** Return the state and frame contract, residual or factor changed, and the regression. Compare the baseline and candidate on identical timestamped inputs. Run front-end-only odometry first, then enable loop closures on the same trajectory. Report segment drift against an independent reference when available, false and missed loops, tracking losses, and per-scan latency. For a saved map and fresh localization session, use [Map and Relocalization Acceptance (optional)](../robot-map-relocalization/SKILL.md). For a worked example of local submaps and global constraints, see the [Cartographer algorithm walkthrough](https://google-cartographer-ros.readthedocs.io/en/latest/algo_walkthrough.html).
