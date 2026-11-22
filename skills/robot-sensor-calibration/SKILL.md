---
name: robot-sensor-calibration
description: Estimate or verify a rigid camera-to-robot transform after a mount change, when targets have a consistent spatial offset, or when pose errors depend on head or wrist motion. Covers fixed and articulated camera mounts.
metadata:
  title: Camera-to-Robot Extrinsic Calibration
---

# Camera-to-Robot Extrinsic Calibration

Start with the downstream question. For a grasp target, the relevant measurement may be point error in the robot base frame at working distance. For image registration, it may be pixel error in a second camera. Record the frame, operating range, metric, and any task tolerance before choosing a fit.

## Identify what is rigid

Use the convention `p_target = T_target_from_source @ p_source` for homogeneous column vectors. Record axis conventions, length units, and the exact frames used by the producer and consumer. An optical frame and a camera housing frame can have different axes.

- **Body-mounted camera.** Estimate the transform from the camera to its rigid parent. If the consumer uses a world or odometry frame, compose the robot pose at image capture time.
- **Head- or wrist-mounted camera.** Estimate the camera-to-mount transform once per physical mounting configuration. Compute `T_base_from_camera(t) = T_base_from_mount(t) @ T_mount_from_camera` using the joint state at exposure. A base-to-camera pose measured at one joint angle is valid at that pose.

## Fit and test the candidate

1. Pair the images with their intrinsics, distortion model, depth units, target dimensions, and timestamped robot poses as applicable. Confirm camera settings and physical target dimensions for this capture. If the target moved with a tool, record which link carried it and whether the target-to-tool offset was measured or must also be estimated.
2. Pick the estimator that matches the observations. For independently measured 3D point pairs in the two frames, fit a rigid transform using well-separated, non-collinear correspondences. If only a floor plane is observable, report the unresolved in-plane translation and rotation about the plane normal.
   For OpenCV eye-in-hand calibration with a stationary target, supply gripper-to-base and target-to-camera poses. The returned transform maps camera coordinates into the gripper frame. The `AX=XB` formulation needs at least two relative motions about nonparallel axes (at least three poses). With all rotations about z, adding any z offset to the unknown translation leaves `(R_A−I)t_X` unchanged. A small residual can coexist with a wrong mount height. Inspect axis diversity and the singular values of the stacked `R_A−I` translation system. Near-parallel axes amplify noise. Capture a second rotation axis and validate the full transform on independent targets. [OpenCV hand-eye calibration](https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html)
3. Reserve complete target poses or capture sequences before fitting or rejecting outliers. Compare the current and candidate transforms on the same held-out observations. Use an independently located target for metric accuracy. If only repeated observations of an unknown stationary target are available, report repeatability and leave absolute accuracy open.
4. Report image residuals in pixels, point residuals in physical length units, and orientation errors in degrees or radians when reference orientations exist. Give the sample count, typical and worst errors, plus the distances and views tested. On a moving mount, evaluate multiple mount poses. If error grows with joint speed, investigate timestamp alignment before changing the rigid transform.

**Deliverable.** Provide the candidate transform with direction, units, rigid parent, capture IDs, fit and holdout sets, residuals, and the downstream tolerance used for the decision. Identify any unobservable degrees of freedom. With no independent accuracy reference or task tolerance, report the measurements and the acceptance question that remains open.

For an offline check of transform direction, stale mount poses, and depth scale, run the [synthetic calibration example](references/geometry-check.md). For object-specific pose ambiguity after calibration, use [RGB-D Perception and Pose Validation (optional)](../robot-rgbd-pose/SKILL.md).
