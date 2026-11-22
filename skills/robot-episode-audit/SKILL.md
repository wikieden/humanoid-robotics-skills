---
name: robot-episode-audit
description: Audit converted robot episodes for time alignment, action semantics, split leakage and loader compatibility, or identify which human takeover frames and consecutive action chunks qualify as expert labels for behavior cloning or HG-DAgger.
metadata:
  title: Teleoperation Episode and Training Dataset Audit
---

# Teleoperation Episode and Training Dataset Audit

**Takeover labels.** For a request about expert actions around a control transfer, go directly to the [takeover label audit](references/takeover-labels.md). Return committed-action sources and eligible windows for the requested horizon and masking rule. Video alone can support an intervention annotation while leaving action provenance unknown.

## Batch and loader audit

Start with one episode that can be traced back to its raw recording, then apply the checks across the batch. Collect the source manifest, robot and camera configuration, converter version, target modality definitions, and training loader entry point. Use the recording ID to connect the fields written during capture to the converter output.

1. Locate a distinctive action, such as a gripper closing, in both the source recording and the converted episode. For each camera, compare video timestamps, state samples, command times, and the onset of observed motion. Record dropped frames, duplicate timestamps, the alignment method, and the largest measured offset.
2. Check joint order, units, arm assignment, gripper polarity, absolute versus incremental commands, and episode boundaries. Trace one raw value into the training tensor. For first-person human video, identify which supervision signals are available and how any retargeted actions were generated.

   - If fields share a name, compare the writer, samples, and converter for each robot, hardware revision, and schema version. A gripper value of 0.5 could mean half-open or 0.5 rad. Check the writer's conversion formula and known open and closed endpoints. Retain the raw data and keep batches with unresolved units separate until the mapping is established.
   - For mixed-control recordings, apply the takeover label audit before counting expert samples.

3. Map each source recording to its resulting episodes. Count accepted and excluded episodes and record the reasons for exclusion. Deduplicate by source recording, then check for session, scene, or object overlap across splits according to the evaluation goal. Every clip from the same recording should retain its source ID.
4. Use the intended training configuration to read an actual batch from each of the training and validation splits. Inspect images, states, action chunks, padding masks, and the ends of short episodes. Verify that normalization statistics were computed on the training split and reused for validation or testing.

**Deliverable.** Supply the batch version, provenance and split manifest, example failures, loader command, and observed tensor shapes. State whether the batch loads for training, which generalization claims the split supports, and how the batch should be handled given the findings.
