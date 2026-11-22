---
name: robot-map-relocalization
description: Qualify a 2D or 3D SLAM map for later localization. Use for false loop closures, wrong-floor matches, recovery after tracking loss, and displaced waypoints after a map revision.
metadata:
  title: SLAM Map and Relocalization Acceptance
---

# SLAM Map and Relocalization Acceptance

Start with a question the map must answer on a later run: can a freshly started robot identify the right floor, recover its pose, and resolve a known destination? Reserve an independent traversal or surveyed landmarks before tuning. Record the map revision, calibration, sensor clocks, and mapping or localization mode.

## Build and reload the map

1. Trace the inputs the active estimator consumes. For 2D scan matching, check laser coverage, transforms, and odometry if enabled. For lidar-inertial mapping, inspect IMU alignment, scan timing and deskew during turns. A crisp straight corridor can hide a heading or timing error.
2. Inspect the trajectory before and after loop closure. Use a physical revisit as a positive control and distinct but similar corridors as a negative control. Check for duplicated walls, warped passages, or a wrong loop that collapses two places together. Without independent references, report map consistency and leave absolute accuracy unmeasured.
3. Save the localization artifact, navigable grid, required tiles or estimator state, map frame, origin, orientation, resolution, and floor identity. For a 3D-to-2D projection, inspect narrow openings, ramps, and overhangs. Reload from a clean process. Isolate any writes to dynamic layers so that every trial starts from the declared map.
4. Test an independently located waypoint, virtual wall, or floor transition against the reloaded artifact. A pixel-to-world-to-pixel round trip can pass when both conversions share the same wrong origin. Check the action taken when an old waypoint references a superseded map.

## Score relocalization

Separate initialization from a supplied pose, search around a coarse prior, and unseeded global localization according to supported modes. Vary start, heading, and sensor coverage. Include a similar-looking area and a fresh traversal after a temporary loss. Remove previously recorded localization outputs from replay inputs.

Define position and wrapped-heading tolerances, a minimum dwell, and a timeout before scoring. Check the map and floor identities before comparing local coordinates. Report sustained correct locks, false accepted poses, unresolved trials, and time to sustained correct lock. Keep timeouts in the denominator. Aligning each trial on its own estimated trajectory can erase the error being tested.

**Offline example.** The following synthetic accepted poses arrive one second apart. A correct lock requires two consecutive samples in tolerance on the correct floor. The last pose alone would conceal a transient or wrong-floor match.

```python
from math import hypot

reference = ("upper", 2.0, 1.0, 179)
good = ("upper", 2.03, 1.0, -179)
wrong_floor = ("lower", 2.0, 1.0, 179)


def score(samples):
    floor, x, y, yaw = reference
    streak = 0
    lock_time = None
    false_accept = False
    for second, pose in enumerate(samples):
        valid = False
        if pose is not None:
            f, px, py, heading = pose
            error_deg = abs((heading - yaw + 180) % 360 - 180)
            valid = f == floor and hypot(px - x, py - y) <= 0.1 and error_deg <= 3
            false_accept |= not valid
        streak = streak + 1 if valid else 0
        if streak >= 2 and lock_time is None:
            lock_time = second
    return lock_time, false_accept


assert score([None, good, good]) == (2, False)
assert score([wrong_floor, wrong_floor]) == (None, True)
assert score([None, good, None]) == (None, False)
```

**Deliverable.** Return map build and reload identities, held-out evidence, each start and prior, time to lock, false accepts, and the effect on semantic layers. If localization is stable but the goal is missed, continue with [Navigation Replay (optional)](../robot-navigation-replay/SKILL.md).
