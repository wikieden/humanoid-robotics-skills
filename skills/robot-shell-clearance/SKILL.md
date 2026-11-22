---
name: robot-shell-clearance
description: Check a robot enclosure, cover or guard revision for mechanical interference and closing gaps across joint travel and recorded motion. Use when a new shell fits at rest but may meet a neighboring part in motion.
metadata:
  title: Moving Shell Clearance Review
---

# Moving Shell Clearance Review

Start with the two surfaces that can approach each other. Record the shell revision, link attachments, joint axes and stops, and which geometry represents the exposed surface. Visual meshes and simplified collision bodies often have different dimensions. For a guard surrounding a moving part, inspect both the internal running clearance and the accessible opening, and label them separately.

1. Establish a reference pose and distance units. Verify the distance query on one separated and one overlapping pair with known geometry. Identify rigid seams, moving interfaces and manufacturing clearances. Keep rigidly joined parts out of the list of closing gaps while retaining assembly overlaps that need review.
2. Sweep each affected joint over its specified range. Save the nearest surface pair, distance, and joint configuration at a local minimum. Include intermediate poses. Repeat with coupled joints in plausible combinations and with recorded task motion. A single-joint sweep with all other joints at neutral can miss an interference during a turn.
3. Compare the same poses before and after the shell change. For a small or sign-changing gap, refine the interval or use continuous collision detection where supported. Inspect the witness points on the exposed geometry. Account for mesh approximation, assembly variation and flex when judging whether a clearance is resolved. A sampled minimum bounds what the sampled poses showed.
4. Return geometric interference, accessible closing gaps and untested configurations separately. Record the part or mounting change and replay the witness pose against the revision. Use the application's risk assessment and physical inspection for access and safeguarding decisions. See [Robot Safety Policy (optional)](../robot-safety-policy/SKILL.md).

**Small check.** In this synthetic planar section a rotating tab approaches a fixed wall. Its endpoints both clear while an intermediate pose intersects. All lengths are in the same arbitrary unit.

```python
from math import radians, sin

def signed_gap(angle):
    return 3 - 4 * sin(radians(angle))

assert all(signed_gap(angle) > 0 for angle in (0, 180))
gap, angle = min((signed_gap(a), a) for a in range(181))
assert gap == -1 and angle == 90
```

**Deliverable.** Give a before/after table with the limiting surface pair, witness pose, signed distance or distance convention, sampling method, uncertainty and outstanding physical checks.
