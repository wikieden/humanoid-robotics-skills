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
2. Overlay detections, masks and valid depth on the source image. Identify the depth producer's units, invalid values and distance convention. ROS REP 118 canonical float depth gives optical-axis Z in metres. Its OpenNI raw format gives millimetres and uses zero for invalid pixels. A vendor range image may instead give distance along the ray. [ROS depth image specification](https://github.com/ros-infrastructure/rep/blob/master/rep-0118.rst)
   Obtain an undistorted ray `d=(x,y,1)` for the pixel using its own stream's camera model. Back-project optical depth as `P=Z*d`, or radial range as `P=r*d/||d||`. For `d=(0.75,0,1)` and `r=1.25 m`, the point is `(0.75,0,1) m`. Treating range as Z yields `(0.9375,0,1.25) m`. Both reproject to the same pixel. Check an independently measured off-axis target. For unregistered streams, transform the depth point into the color optical frame and project it with the color camera model before looking up its mask. Where several points project to the same color pixel, resolve visibility in the color view and flag occluded associations. [ROS camera model fields](https://github.com/ros2/common_interfaces/blob/jazzy/sensor_msgs/msg/CameraInfo.msg)
3. Test pose hypotheses against object geometry. For a box, check oriented bounding box dimensions and axes. For planar work, inspect the target mask, occluders, and work-surface projection separately. If the cloud admits several orientations, follow the registration workflow above to compare them and record any remaining ambiguity.
4. Transform each candidate into the consumer's frame at exposure time. With a reference pose, report translation and rotation error by distance, occlusion, and viewpoint. If the target stays fixed but its reported position changes as the camera mount turns, check the mounting transform and joint-state timestamp. See [Camera-to-Robot Extrinsic Calibration (optional)](../robot-sensor-calibration/SKILL.md).

**Deliverable.** Include the source frame ID, overlay, candidate results with frame, timestamp, and units, and representative failures. Attach execution records for any reported physical grasp or wiping outcome.
