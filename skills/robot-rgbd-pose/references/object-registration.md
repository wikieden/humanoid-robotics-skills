# Object Pose Registration Under Partial Visibility

Start with the segmented metric cloud, the object frame and dimensions or reference template, and the downstream use of orientation. A gripper approaching a marked face may need to distinguish two poses that are interchangeable for picking up an unmarked box. If depth scale or frame conversion is in doubt, use the [RGB-D input checks](../SKILL.md#rgb-d-input-checks).

1. **Establish a baseline.** Preserve the original segmented cloud and any available mask and depth samples. Compare a bounding box fitted to the visible points with a fit constrained by known physical dimensions, when available. Missing surfaces bias the visible extent. Record which faces were observed, which dimensions were supplied, and which pose components are still unconstrained.
2. **Generate plausible starting poses.** Use known support planes, principal axes, or a global registration method. Include axis flips and rotations consistent with approximate symmetry. Keep source-to-target transform direction explicit. Include plausible alternatives before local refinement; rerunning ICP from one seed only tests its local basin.
3. **Refine and rank on comparable evidence.** Downsample at successive scales and refine each hypothesis. Report distance thresholds, inlier count, overlap definition, residual units, and the visible region used for scoring. A low inlier RMSE supported by a small patch can favor the wrong pose. Preserve thin distinguishing features during filtering and check their residual separately. Avoid penalizing surfaces hidden from the camera as if they were observed.
4. **Challenge the winning hypothesis.** Compare it with the strongest geometrically distinct alternative. Mask a distinguishing feature, perturb the starting yaw, and repeat across views. If the remaining observations support several orientations, return those hypotheses or the symmetry class. Report full orientation error for tasks that require a particular side, and symmetry-aware error when the task genuinely accepts equivalent poses.

**Offline counterexample.** Compare yaw angles of 0° and 180° for a flat rectangular face. Both hypotheses use the same model outline. Depth samples include an extra point on the top edge, so the observation is sampled unevenly. A printed dot has a known location on the model and adds no depth relief. When its identity is visible, compare its observed position with the predicted position of that same dot. Masking the color cue leaves the depth samples unchanged.

```python
outline = [(x, y) for x in range(-2, 3) for y in range(-1, 2)
           if abs(x) == 2 or abs(y) == 1]
observed_depth = [(-2, -1), (2, -1), (2, 1), (-2, 1), (0, 1)]
model_dot = (0, 1)


def squared_distance(p, q):
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2


def rotate(point, yaw):
    x, y = point
    return (x, y) if yaw == 0 else (-x, -y)


def compare(identified_dot=None):
    geometry_mse, dot_error_sq = {}, {}
    for yaw in (0, 180):
        model = [rotate(p, yaw) for p in outline]
        geometry_mse[yaw] = sum(min(squared_distance(p, q) for q in model)
                                for p in observed_depth) / len(observed_depth)
        if identified_dot is not None:
            dot_error_sq[yaw] = squared_distance(identified_dot, rotate(model_dot, yaw))
    # Exact agreement is appropriate for this noiseless fixture.
    plausible = [yaw for yaw, error in geometry_mse.items()
                 if error == 0 and (yaw not in dot_error_sq or dot_error_sq[yaw] == 0)]
    return geometry_mse, dot_error_sq, plausible


tie = {0: 0.0, 180: 0.0}
for case, observation, expected_error, expected_yaws in [
    ("depth only", None, {}, [0, 180]),
    ("dot identified at top", (0, 1), {0: 0, 180: 4}, [0]),
    ("dot masked", None, {}, [0, 180]),
    ("dot identified at bottom", (0, -1), {0: 4, 180: 0}, [180]),
]:
    result = compare(observation)
    assert result == (tie, expected_error, expected_yaws)
    print(case, *result)
```

**Deliverable.** Show the baseline and proposed estimates on the same captures. Include the leading alternatives, coverage and residuals, feature visibility, and pose errors against an independent reference if available. Report ambiguous and rejected cases in the denominator.
