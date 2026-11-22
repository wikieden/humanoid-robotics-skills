# Synthetic Camera Geometry Check

Run this Python 3 example offline. The synthetic camera and mount axes are aligned. The camera origin is 0.10 m along the mount's positive X axis. The mount origin in the base frame is (0.40, 0.20, 0.00) m. At exposure the mount has rotated +90 degrees about base Z. The reference landmark is at (0.40, 0.50, 1.00) m in the base frame.

```python
from math import cos, dist, isclose, radians, sin


def point_in_base(point_camera, mount_yaw_deg, camera_offset_m):
    x, y, z = point_camera
    x += camera_offset_m
    angle = radians(mount_yaw_deg)
    return (0.40 + cos(angle) * x - sin(angle) * y,
            0.20 + sin(angle) * x + cos(angle) * y, z)


def project(point):
    x, y, z = point
    return (320 + 500 * x / z, 240 + 500 * y / z)


def back_project(pixel, depth_m):
    u, v = pixel
    return ((u - 320) * depth_m / 500, (v - 240) * depth_m / 500, depth_m)


pixel = (420, 240)
reference_base = (0.40, 0.50, 1.00)
point = back_project(pixel, 1.0)
wrong_depth = back_project(pixel, 2.0)
assert project(point) == project(wrong_depth) == pixel

cases = [
    ("at exposure", point, 90, 0.10, 0.0),
    ("inverted mounting offset", point, 90, -0.10, 0.20),
    ("stale mount pose", point, 0, 0.10, 0.18 ** 0.5),
    ("doubled depth", wrong_depth, 90, 0.10, 1.04 ** 0.5),
]
for label, camera_point, yaw, offset, expected_m in cases:
    error_m = dist(point_in_base(camera_point, yaw, offset), reference_base)
    assert isclose(error_m, expected_m, abs_tol=1e-9)
    print(f"{label}: {error_m:.3f} m")
```

Both depth values reproject to the same pixel. The independent landmark exposes the depth error. The inverted-offset and stale-pose cases perturb one input each so that a frame-convention error can be distinguished from use of the wrong joint state.
