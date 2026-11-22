---
name: robot-update-recovery
description: Qualify an update that spans robot system software, controller firmware or model assets. Use when download, activation and recovery follow different paths, or a partial upgrade can leave incompatible versions active.
metadata:
  title: Multi-Component Robot Update Recovery
---

# Multi-Component Robot Update Recovery

Build a row for each target before judging a release. Identify the current version, expected candidate, staging location, component that activates it, independent source of the active version, and available recovery path. A controller with two firmware slots and a host using a recovery image need different failure tests.

1. Draw the compatible combinations of old and new components. Select an update order that keeps intermediate combinations operable or puts the robot into its documented maintenance state. Record the entry conditions, exclusive owner and conditions for leaving maintenance. A model load may also depend on the running runtime or calibration revision.
2. Trace staging and activation separately. For resumable transfers track the contiguous verified prefix and image identity. Exercise an exact duplicate, a partially overlapping retry, a gap, a changed image and an interrupted transfer using a disposable target. Accept overlap only when it belongs to the same verified bytes. Keep final artifact verification and boot or load confirmation as separate events.
3. Exercise failure before activation, after selection but before health confirmation, and after one component has changed while another is pending. On restart, read the active component versions through their normal owners. Verify health, compatible operation and the retained recovery artifact before declaring the bundle active. Record targets that only have a planned or partially implemented recovery path.

**Recovery fixture.** Model a strictly ordered transfer of a ten-byte image. If six bytes were verified before an acknowledgment was lost, a matching retry covering bytes four through seven extends the contiguous prefix to eight. A chunk beginning at byte nine still leaves a gap. Restarting the process with an eight-byte staged prefix must not change its report of the currently running version.

**Deliverable.** Return a per-target state table for download, verified staging, activation, health confirmation and recovery. Include the observed active combination after each interruption, and label the evidence from a state-machine fixture, isolated target or board test.
