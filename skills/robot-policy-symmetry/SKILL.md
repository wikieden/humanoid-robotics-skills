---
name: robot-policy-symmetry
description: Derive and test left-right mirror transforms for robot policy observations, actions and augmentation. Use when mirrored examples look plausible but produce the wrong limb motion, command direction or base orientation.
metadata:
  title: Left-Right Symmetry in Robot Policies
---

# Left-Right Symmetry in Robot Policies

Pin the model actually loaded by training, the observation layout and the action decoder. Name the reflection plane and origin. Pair links by physical role. Read joint and actuator order from the loaded model and transform joint axes into a common frame before comparing them. A naming convention alone cannot establish which way a hinge rotates.

1. Derive a map for each field. For an orthogonal reflection matrix `S` through the origin, polar vectors such as linear velocity transform as `S v`. Axial vectors such as angular velocity transform as `det(S) S w`. Reflect rotations as `S R Sᵀ` when the source and destination frames use the same reflection. Account for mirrored link-local basis conventions when they differ. Compare orientations as rotations so equivalent quaternion signs agree.
2. For hinge angles and velocities, pair the joint indices and derive signs from the mirrored rotation axes. For action offsets around a rest pose, decode to physical targets, reflect, and encode against the destination rest pose and scale. Include previous actions, contact channels, commands and stacked history where the policy consumes them.
3. Test that reflecting twice restores a sample. Then use an independent forward-kinematics check. Run the original pose and its mirrored joint pose, reflect the observed endpoint of the first, and compare it with the paired endpoint of the second. Inspect link orientations as well as positions. Use off-neutral poses and single-joint perturbations. Report a known asymmetric component with its own residual and rationale.
4. Apply augmentation only where the task and environment also admit the reflection. Swap side-specific goals or labels as needed. For a handed tool or asymmetric fixture with no valid mirrored task, exclude that case. Record kinematic consistency and policy rollout performance separately.

**Counterexample.** In this planar fixture the local hinge axes on both copies point out of the page. Swapping joints with the wrong sign passes the round-trip test but sends the endpoint to the wrong side of the mirror.

```python
from math import cos, sin, dist

def reflect_joints(pair, sign):
    left, right = pair
    return sign * right, sign * left

def tip(q):
    return cos(q), sin(q)

pose = (0.4, -0.1)
for sign in (1, -1):
    assert reflect_joints(reflect_joints(pose, sign), sign) == pose
x, y = tip(pose[0])
assert dist(tip(reflect_joints(pose, -1)[1]), (x, -y)) < 1e-12
assert dist(tip(reflect_joints(pose, 1)[1]), (x, -y)) > 0.1
```

**Deliverable.** Return the model revision, field-wise permutation and sign conventions, the largest geometric residual with its witness pose, and the task cases eligible for augmentation.
