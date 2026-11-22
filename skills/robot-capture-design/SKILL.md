---
name: robot-capture-design
description: Choose how to collect demonstrations for a learning objective. Use when deciding between human video, an instrumented handheld tool, robot teleoperation, or a paired pilot before buying equipment or collecting at scale.
metadata:
  title: Demonstration Capture Design
---

# Demonstration Capture Design

Start with one decision the future policy must make. For inserting a peg, recognizing the opening, choosing a wrist displacement, and detecting contact require different labels. Write down the model input and target at decision time, their units and frames, and how missing values will be represented.

## Match the source to the label

| Source | What it can directly record | What must be established separately |
| --- | --- | --- |
| First-person human video | Visible sequence, viewpoint, object and scene changes | Camera motion, occluded contact and robot actions need additional evidence. Mark inferred labels with their provenance. |
| Instrumented handheld tool | Tool pose, opening or contact if the corresponding sensors are present | Calibrate tool-to-robot geometry, axes, timing and controller conventions. Check whether the demonstrated motion is reachable. |
| Robot teleoperation or intervention | Issued commands, observed states and task outcomes if all are logged | Distinguish commanded action, executed motion, and control authority around a takeover. |

Plan the smallest paired recording that could overturn the choice. Give simultaneous views one event ID and independent clock information. Use a visible or sensed event to estimate time offset and check it again later for drift. For separate human and robot demonstrations of the same task, share a task or scene ID and keep distinct event IDs. Preserve that distinction when splitting data.

## Decide from a pilot

Run the intended target builder on each source. For each action dimension count measured, derived and missing labels. Inspect one derived trajectory at reversals and contact. Keep a validity mask, calibration revision and label source alongside it. Count usable episodes per operator-hour and include calibration, alignment and rejected takes in the cost.

**Worked decision.** In a synthetic pilot of ten successful drawer openings, eight episodes have usable tool-pose tracks and six have usable gripper-width tracks. Between four and six episodes can have both. Join the episode IDs and intersect their valid time windows to count usable action chunks. All ten videos may still supervise visible task phases. Filling a missing width with zero would teach a false closed-gripper command.

**Deliverable.** Return a source-by-target matrix, the paired pilot design, usable synchronized coverage, and the cheapest source that meets the declared target and error budget. For already converted episodes, use [Episode and Training Dataset Audit (optional)](../robot-episode-audit/SKILL.md).
