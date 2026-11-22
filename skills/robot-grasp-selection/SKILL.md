---
name: robot-grasp-selection
description: Develop or compare a grasp selector that combines learned scores with gripper geometry, collision checks, and path feasibility through approach and loaded retreat. Use when the top-scoring pose cannot complete the requested pick.
metadata:
  title: Grasp Candidate Filtering and Selection
---

# Grasp Candidate Filtering and Selection

Fix a scene snapshot, object hypothesis, initial robot state, gripper model, and requested task stages. Preserve all proposal IDs, poses, opening widths, and model scores before filtering. Staging ends at the requested scope: a lift, a handoff, and a complete pick-and-place have different completion conditions.

1. Generate proposals on target geometry while preserving surrounding context for collision checks. Use a calibrated transform for each approach axis and finger closing direction. Audit object segmentation near adjacent obstacles: removing target points for expected finger contact must preserve the table, nearby objects, and non-contact parts of the target. Record any allowed contact pairs and the stages where they apply.
2. Reject known violations such as inadequate aperture, collision along approach, or an unreachable pre-grasp pose. For surviving candidates, check IK continuity, gripper closure geometry, lift and retreat. After attachment, use the carried object's geometry and its transform relative to the tool. A pose that clears the gripper at rest can still trap the payload on withdrawal.
3. Track each stage as passed, rejected with a reason, or unchecked. Solver timeout, missing geometry, and a proven collision have different meanings. Rank candidates eligible for the requested stage sequence. If using non-maximum suppression or a top-K budget, inspect whether it removed alternative approach directions before they received a feasibility check.
4. Compare the selector and baseline with identical proposal sets to isolate ranking and filtering. Then compare complete pipelines if candidate generation also changed. Report scenes with any feasible proposal, scenes where the selected proposal passed all checked stages, per-stage rejections, planning latency including failures, and observed grasp retention or placement only when separately measured.

**Offline counterexample.** Two candidates approach the same target. In this synthetic fixture all checks except width clearance have already passed. Widths are in millimeters. The straight retreat corridor requires a 5 mm margin on each side of the payload.

```python
candidates = [
    # ID, model score, clear corridor width, projected payload width
    ("A", 0.96, 45, 42),
    ("B", 0.82, 68, 48),
]
margin_per_side = 5
feasible = [c for c in candidates if c[2] >= c[3] + 2 * margin_per_side]
raw_best = max(candidates, key=lambda c: c[1])
selected = max(feasible, key=lambda c: c[1]) if feasible else None
assert raw_best[0] == "A" and selected[0] == "B"
print(f"score winner={raw_best[0]}, feasible winner={selected[0]}")
```

**Deliverable.** Return the candidate ledger from proposal to first rejection or final selection, an overlay showing approach and retreat, the scene and tool versions, and the most informative rejected high-score candidate. Label simplified clearance checks, full scene planning, simulated execution, and physical task results separately.
