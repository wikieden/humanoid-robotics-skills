# Offline Stance-Foot Retargeting Check

A synthetic five-frame stance clip keeps a source foot planted as the hip advances. The target leg is shorter and uses two named drive channels in knee-first order, with a reversed knee axis and nonzero offsets. Compare copying the source angles with solving the target leg for the same contact. Both methods use the same target root path, channel binding and scorer.

Run this block with Python 3. Coordinates are horizontal distance and height in metres. The planar model has a point foot, a fixed floor and a single bending branch. The solver rejects a goal outside the leg's reach.

```python
from math import acos, atan2, cos, dist, sin

SOURCE = (0.50, 0.45)
TARGET = (0.42, 0.38)
ANCHOR = (0.0, 0.0)


def solve_leg(root, lengths, foot):
    thigh, shin = lengths
    forward = foot[0] - root[0]
    down = root[1] - foot[1]
    knee_cos = (forward**2 + down**2 - thigh**2 - shin**2) / (2 * thigh * shin)
    if not -1 <= knee_cos <= 1:
        return None
    knee = acos(knee_cos)
    hip = atan2(forward, down) - atan2(shin * sin(knee), thigh + shin * cos(knee))
    return hip, knee


def foot_fk(root, lengths, hip, knee):
    thigh, shin = lengths
    return (root[0] + thigh * sin(hip) + shin * sin(hip + knee),
            root[1] - thigh * cos(hip) - shin * cos(hip + knee))


def bind_target(angles):
    hip, knee = angles
    return 0.20 - knee, hip + 0.10  # knee_drive, hip_drive in radians


def read_target_fk(root, row):
    knee_drive, hip_drive = row
    return foot_fk(root, TARGET, hip_drive - 0.10, 0.20 - knee_drive)


copied, fitted = [], []
for hip_x in (-0.10, -0.05, 0.0, 0.05, 0.10):
    source_root = (hip_x, 0.85)
    target_root = (hip_x, 0.70)
    source_q = solve_leg(source_root, SOURCE, ANCHOR)
    source_foot = foot_fk(source_root, SOURCE, *source_q)
    assert dist(source_foot, ANCHOR) < 1e-9
    target_q = solve_leg(target_root, TARGET, source_foot)
    assert target_q is not None
    copied.append(read_target_fk(target_root, bind_target(source_q)))
    fitted.append(read_target_fk(target_root, bind_target(target_q)))


def stance_metrics(points):
    drift = max(abs(x - points[0][0]) for x, z in points)
    penetration = max(max(0.0, -z) for x, z in points)
    return drift, penetration


for label, points in (("angle copy", copied), ("contact IK", fitted)):
    drift, penetration = stance_metrics(points)
    print(f"{label}: drift={drift:.4f} m, penetration={penetration:.4f} m")

assert stance_metrics(copied)[0] > 0.02
assert max(dist(p, ANCHOR) for p in fitted) < 1e-9
assert solve_leg((0.0, 0.85), TARGET, ANCHOR) is None

# At geometric zero the target reader expects (0.20, 0.10).
# An off-neutral channel swap must also be visible to the FK check.
assert bind_target((0.0, 0.0)) == (0.20, 0.10)
row = bind_target(target_q)
assert dist(read_target_fk(target_root, row[::-1]), ANCHOR) > 0.02
print("Reversed channel order detected. Out-of-reach contact rejected.")
```

Observed with Python 3 in a fresh process.

```text
angle copy: drift=0.0316 m, penetration=0.0159 m
contact IK: drift=0.0000 m, penetration=0.0000 m
Reversed channel order detected. Out-of-reach contact rejected.
```

Drift measures horizontal excursion from the first target contact. Penetration measures distance below the floor. Also compare the absolute world anchor, since a foot can be stationary in the wrong place. A floating-base humanoid adds multi-axis joints, contact areas, balance dynamics and controller limits beyond this kinematic check.
