---
name: robot-object-registration
description: Develop and compare point-cloud registration algorithms for partially visible or symmetric objects. Use when selecting coarse pose hypotheses, refining them with ICP, or deciding whether the available geometry resolves orientation.
metadata:
  title: Object Pose Registration Under Partial Visibility
---

# Object Pose Registration Under Partial Visibility

Start with the segmented metric cloud, the object frame and dimensions or reference template, and the downstream use of orientation. A gripper approaching a marked face may need to distinguish two poses that are interchangeable for picking up an unmarked box. For suspected depth-scale or frame errors, check the inputs with [RGB-D Pose Validation](../robot-rgbd-pose/SKILL.md).

1. **Establish a baseline.** Keep the raw mask and depth samples. Compare a bounding box fitted to the visible points with a fit constrained by known physical dimensions, when available. Missing surfaces bias the visible extent. Record which faces were observed, which dimensions were supplied, and which pose components are still unconstrained.
2. **Generate plausible starting poses.** Use known support planes, principal axes, or a global registration method. Include axis flips and rotations consistent with approximate symmetry. Keep source-to-target transform direction explicit. Include plausible alternatives before local refinement; rerunning ICP from one seed only tests its local basin.
3. **Refine and rank on comparable evidence.** Downsample at successive scales and refine each hypothesis. Report distance thresholds, inlier count, overlap definition, residual units, and the visible region used for scoring. A low inlier RMSE supported by a small patch can favor the wrong pose. Preserve thin distinguishing features during filtering and check their residual separately. Avoid penalizing surfaces hidden from the camera as if they were observed.
4. **Challenge the winning hypothesis.** Compare it with the strongest geometrically distinct alternative. Mask a distinguishing feature, perturb the starting yaw, and repeat across views. If the remaining observations support several orientations, return those hypotheses or the symmetry class. Report full orientation error for tasks that require a particular side, and symmetry-aware error when the task genuinely accepts equivalent poses.

**Offline counterexample.** A rectangular face has four visible corners. A half-turn around its center maps the corners onto themselves. A visible mark on just one edge breaks that symmetry. This miniature uses exact half-turns in 2D to isolate ambiguity in yaw.

```python
from math import dist

corners = [(-2, -1), (2, -1), (2, 1), (-2, 1)]


def mean_squared_distance(observed, model):
    return sum(min(dist(p, q) ** 2 for q in model) for p in observed) / len(observed)


for points, expect_tie in [(corners, True), (corners + [(0, 1)], False)]:
    turned = [(-x, -y) for x, y in points]
    correct = mean_squared_distance(points, points)
    alternative = mean_squared_distance(points, turned)
    assert (correct == alternative) == expect_tie
    print(f"observed points={len(points)}, costs={correct:g}, {alternative:g}")
```

**Deliverable.** Show the baseline and proposed estimates on the same captures. Include the leading alternatives, coverage and residuals, feature visibility, and pose errors against an independent reference if available. Report ambiguous and rejected cases in the denominator.
