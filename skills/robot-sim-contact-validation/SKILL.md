---
name: robot-sim-contact-validation
description: Audit physical success in simulated grasping, placement, and wiping tasks. Use when an object follows an empty gripper, appears to float after release, obstacles disappear, or a wipe earns credit without effective contact.
metadata:
  title: Contact Task Validation in Simulation
---

# Contact Task Validation in Simulation

Choose the physical claim and an observation that could disprove it. For placement, a useful claim is that the released object stayed in the target region, supported by the intended surface, after the tool withdrew. Save the native task score alongside this independent verdict.

1. **Freeze the scene.** Record simulator and asset revisions, collision geometry and masks, units, gravity, timestep, solver settings, friction, actuator mode, and any scripted attachments. Verify a known obstacle in the collision representation used by the planner and in the physics scene. A visually rendered table can be absent from either. If a point cloud supplies obstacles, compare a thin obstacle before and after voxelization and filtering.
2. **Identify the source of motion.** Determine whether the robot follows a kinematic replay, tracks commands through modeled actuators, or runs a closed-loop policy. For the payload, record when it is a free body and when a weld, scripted attachment, or other assist is active. A successful transfer with an assist establishes that the assisted sequence ran. Frictional grip strength requires separate evidence.
3. **Score stages from physical signals.** For a parallel-jaw grasp, align target-relative fingertip geometry, contact pairs, measured aperture, lift, and payload motion. During transfer, check slip relative to the tool and contacts with obstacles. After release, verify the attachment is inactive, the object lies within the target region, and the intended surface supports it throughout a declared settling interval. Record displacement and velocity during that interval. For wiping, compute coverage from the actual tool footprint during effective contact and compare with independently observed changes in the surface state.
4. **Run negative controls.** Close the gripper away from the target, remove the intended support in an isolated scene, and move a wiping tool just clear of the surface. The corresponding grasp, supported placement, and cleaning predicates should fail. Record the first transition that incorrectly earned credit. Keep an ordinary positive trial so a broken detector that always rejects is visible.

For a reproducible single-body example, run the [headless support check](references/support-check.md). For a rejected candidate before motion begins, use [Grasp Selection](../robot-grasp-selection/SKILL.md).

**Deliverable.** Return the scene and reset identifiers, active assists, synchronized contact and pose traces, the native score, and a per-stage physical verdict. For dropped samples or an attempt that never reached release, mark the affected stage unobserved. Report positive and negative controls separately from end-to-end task success.
