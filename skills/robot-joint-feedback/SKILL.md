---
name: robot-joint-feedback
description: Design or diagnose joint-state publication when a gripper or other joint intermittently stops reporting. Use when a pose display still works but a whole-robot planner loses its start state, or late replies revive an old observation session.
metadata:
  title: Joint Feedback Freshness and Recovery
---

# Joint Feedback Freshness and Recovery

Identify which joints each consumer requires. An arm visualization may use a partial set. Collision checking may need the gripper as well. Record each joint's measurement time and validity, plus the session or generation that produced it. Republishing an aggregate message must preserve the ages of its component measurements.

1. Trace three timelines independently: motion commands, feedback acquisition, and the lifetime of the client's request to keep receiving feedback. Mark the last genuine measurement and the moment the complete state became unusable. A late renewal acknowledgment is different from a late sensor sample.
2. Define separate decisions for using a measurement and keeping an observation session alive. A stale joint immediately makes its dependent planning state unavailable. During a bounded recovery interval, continue the supported feedback transaction and require a new valid sample for the active generation before restoring completeness. If the device protocol couples refresh with actuation, verify the documented behavior before enabling retries.
3. Bind renewals and cancellation to the current generation. Bound outstanding requests and retire late replies. A delayed response must neither create another motion goal nor restart a cancelled or replaced session. Record why the session ended so a client exit can be distinguished from a transient reply gap.

**Replay a discriminating trace.** Keep the arm reports fresh throughout. Begin with no gripper sample, observe a valid sample, let it expire during a short gap, then deliver fresh feedback. The complete planning state should appear, disappear and return while the valid arm-only view persists. Cancel the session and deliver an old reply. It must not restore the complete state. Repeat with the client gone and with only the opposite gripper reporting. Count motion goals as well as state publications.

The following fixture isolates the gripper's contribution to completeness. All timestamps are on one synthetic clock and the arm reports remain valid.

```python
def usable(active_generation, sample, now, max_age):
    if active_generation is None or sample is None:
        return False
    generation, measured_at = sample
    return generation == active_generation and 0 <= now - measured_at <= max_age

assert usable(2, (2, 10), 12, 3)
assert not usable(2, (2, 10), 15, 3)
assert usable(2, (2, 16), 17, 3)
assert not usable(None, (2, 17), 18, 3)
assert not usable(3, (2, 17), 18, 3)
```

**Deliverable.** Return the per-joint validity trace, the first consumer affected, session exit or recovery reason, and any extra motion goals. Distinguish observed state, planner success, and executed movement.
