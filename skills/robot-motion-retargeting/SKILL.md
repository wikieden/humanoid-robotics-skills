---
name: robot-motion-retargeting
description: Bind a motion asset to a humanoid rig and retarget human mocap, character animation, or another robot's clip to target joint and root trajectories. Use for skeleton mapping, rest-pose or axis mismatches, foot skating, and hand-to-prop contact errors.
metadata:
  title: Robot Motion Asset Binding and Retargeting
---

# Robot Motion Asset Binding and Retargeting

Identify what must survive the transfer. For a greeting, that might be the raised hand, its facing direction and the beat at which it peaks. For a step while carrying a tray, it might be the stance sole's location on the floor and the hands' poses relative to the tray. Use these relationships to choose constraints and score the exported clip.

## Import the clip and bind the target

1. Preserve the source clip, usage rights, frame interval and asset revision. For BVH, read the hierarchy, offsets, channel order and frame time. For an FBX or glTF/GLB animation, identify the selected take or animation, skeleton and tracks. For a robot trajectory, read joint names, units, timestamps and root convention from its producer. Record missing, occluded or low-confidence landmarks when starting from video-derived motion.
2. Calibrate a known source pose against the target robot's reference configuration. Record length units, handedness, forward/up axes, local versus world transforms, rotation order and quaternion layout. Check whether root translation lives on a scene node, pelvis or separate base track. Apply it once. Declare how an in-place clip, floating-base clip or base-locked gesture should move in the target world.
3. Save a binding table tied to the source skeleton revision and the target URDF/MJCF or equivalent model revision. Give each mapped landmark its target link or joint chain, parent frame, neutral offset, axis/sign, allowed degrees of freedom and fallback for missing channels. An elbow hinge with aligned axes can use `q_target = q_target_neutral + sign * (q_source - q_source_neutral)`. Resolve multi-axis rotations in the calibrated local frames before solving for the available robot joints. Flag duplicate assignments, passive joints and unmapped required effectors.
4. Check the visual rig independently of joint commands. Attach each rigid shell piece to its link with its local mount transform. For a skinned mesh, inspect joint indices, per-vertex weights and inverse bind transforms in the format's convention. Probe neutral, left-only and right-only poses. Compare a wrist or sole landmark from target forward kinematics (FK) with its visual marker. If the joint-frame marker follows the intended arc but the shell or skin drifts, fix the mesh binding first. For a held prop, record the hand socket transform and the attachment and release frames. [glTF skinning specification](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html#skins)

## Retarget the motion

| Transfer | Baseline | What to preserve or reject |
| --- | --- | --- |
| An authored gesture between similar mechanisms | Map calibrated joint deltas by name and retain the original timing. | Verify direction, side, peak pose and whether the target elbow or wrist can reproduce the gesture. |
| Human or different-proportion skeleton to robot | Fit scaled task-space landmarks with constrained inverse kinematics (IK). Warm-start from the preceding target pose. Use orientation only where the source supports it. | Respect target joint and coupled limits, avoid self-collision, and record tracking residuals. A shorter arm may require torso motion or a declared unreachable frame. [General Motion Retargeting](https://arxiv.org/abs/2510.02252) |
| Locomotion or interaction with an object | Mark stance, swing, grasp and release intervals. Anchor a stance sole in its support frame and a grasp point in the object's frame. Solve root and joint motion together when the controller supports a moving root. | Keep an intentional pivot or slide in the contact specification. Allow the swing foot to lift. Report competing hand and foot constraints and the frames at which either becomes infeasible. |

Keep a simple joint-copy baseline for comparison. Fix the target proportions and floor height once per calibrated setup. Fitting scale or translating the root independently at every frame can hide a bad map or create foot skating. Use confidence to reduce the influence of an inferred landmark. If a required contact cannot be met within limits, identify the offending interval and the residual or relax a documented lower-priority objective.

## Export and verify the target asset

- Export the root track, named target joint channels, timestamps, contact intervals and event markers at the consumer's expected rate. Preserve clip duration and event order when resampling. Interpolate orientations on the shortest consistent quaternion arc and recompute velocities on the final timeline. Check start, end and any loop or blend seam for jumps. Reopen the artifact through the intended loader and inspect its decoded joint order, units and root layout. [Example controller motion-reference format](https://github.com/NVlabs/GR00T-WholeBodyControl/blob/main/docs/source/references/motion_reference.md)
- Run FK on the decoded clip. Measure peak and typical hand position and orientation errors in the task frame, maximum horizontal stance-foot drift from touchdown, vertical penetration, joint-limit excess and speed peaks. Keep swing and stance samples separate. Compare the same clip and intervals against the baseline. Retain the worst frame, unresolved channels and rejected frames in the result. The [offline stance-foot example](references/stance-foot-check.md) isolates the effect of changing limb lengths.
- Where tracking or balance matters, replay the reference through the target controller in closed-loop simulation. Record actual contacts, timing, saturation, tracking error and falls. A posed skeleton verifies geometry. An actuated run supplies evidence about tracking under that simulated plant.

**Deliverable.** Return the original clip identity, versioned binding table, target robot and controller profile, derived motion asset, export settings and verification results. Bind the derived asset to that target profile so a model or mapping change triggers revalidation. For publishing, tenant selection or withdrawal of the verified revision, continue with [Action Asset Release (optional)](../robot-action-release/SKILL.md).
