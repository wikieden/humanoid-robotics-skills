---
name: robot-rgbd-pose
description: Validate 3D object poses from RGB-D images or segmented metric point clouds. Use for depth and frame errors, coarse registration and ICP refinement, or competing orientations of partially visible or symmetric objects.
metadata:
  title: 3D Object Pose Validation and Registration
---

# 3D Object Pose Validation and Registration

**Segmented point cloud.** Start directly with [object registration](references/object-registration.md) when the input is already a metric cloud. Use the registration workflow to compare initial poses, refine with ICP, and return the alternatives that the visible geometry supports. For a cloud-only request, the cloud, its units and frame are sufficient to begin.

## RGB-D input checks

Collect a color image and depth image from the same instant, their alignment, camera intrinsics, extrinsics or timestamped transforms, and the frame, units, and target type expected downstream. If depth or calibration is missing, identify which 2D results can still be verified.

1. Determine whether the consumer needs a class label, mask, point cloud, or oriented pose. For semantics, trace the crop and recognition result. For a spatial target, trace depth projection, geometry estimation, and the output frame.
2. Overlay detections, masks, and valid depth on the source image. Check optical axes, depth scale, and color-depth registration. Back-projecting a pixel and projecting it into the same camera checks the implementation's internal consistency. A depth-scale error can cancel in that calculation. Check metric depth against an independently measured distance and color-depth registration against a feature visible in both streams.
3. Test pose hypotheses against object geometry. For a box, check oriented bounding box dimensions and axes. For planar work, inspect the target mask, occluders, and work-surface projection separately. If the cloud admits several orientations, follow the registration workflow above to compare them and record any remaining ambiguity.
4. Transform each candidate into the consumer's frame at exposure time. With a reference pose, report translation and rotation error by distance, occlusion, and viewpoint. If the target stays fixed but its reported position changes as the camera mount turns, check the mounting transform and joint-state timestamp. See [Camera-to-Robot Extrinsic Calibration (optional)](../robot-sensor-calibration/SKILL.md).

**Deliverable.** Include the source frame ID, overlay, candidate results with frame, timestamp, and units, and representative failures. Attach execution records for any reported physical grasp or wiping outcome.
