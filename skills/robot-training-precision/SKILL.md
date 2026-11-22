---
name: robot-training-precision
description: Compare full-precision or mixed-precision adapter training with a quantized frozen base. Use when memory savings, throughput, resumability and inference export determine which configuration to keep.
metadata:
  title: Training Precision and Checkpoint Comparison
---

# Training Precision and Checkpoint Comparison

Identify the limiting resource and the quality criterion before launching a comparison. Specify storage and compute dtypes for frozen weights, trainable adapters, gradients and optimizer states. A label such as “8-bit training” leaves all four ambiguous.

1. **Match the workload.** Pin the base revision, processor, adapter targets and initialization, device topology, example order, augmentation seeds, optimizer, learning-rate schedule and number of updates. Match microbatch size, accumulation and padding for the precision-only comparison. If memory savings enable a larger microbatch, run that as a second experiment. Record actual nonpadding tokens or valid action targets per update.
2. **Measure the same interval.** Warm both runs, synchronize the accelerator at timing boundaries, reset peak memory counters, and declare whether data loading and checkpoint writes fall inside the timer. Report useful examples or tokens per second and both peak allocated and reserved memory when supported. Retain failed or out-of-memory configurations with their stopping point.
3. **Fork at a checkpoint.** For each precision, compare continuous training with stop-and-resume in a fresh process. Check the next sample IDs and update index, adapter weights, optimizer, scheduler and random state. Verify the frozen base and quantization scales resolve to the same values in both branches. Compare subsequent losses and parameter deltas with a declared tolerance. Use an isolated copy for cold reload so a base-weight cache or a live adapter cannot hide a missing dependency.
4. **Load the inference export separately.** Restore the intended base, adapter and processor using the deployment loader. Run fixed held-out inputs and compare predictions against the same training run before export. Score both precision candidates on a common held-out task and report the evaluation unit. Reproducing a saved prediction checks export fidelity. A robot task claim also requires evaluation at the claimed execution level.

**Worked decision.** Suppose two synthetic runs pass resume and reload. One uses 20 GiB at 48 examples/s and the other 14 GiB at 36 examples/s, with equivalent measured validation quality. With an 18 GiB budget only the second fits. With 24 GiB and a throughput objective the first wins. If the smaller run cannot reproduce its next batch after resume, record its memory result and leave its suitability for resumable training open.

**Deliverable.** Give a row per configuration with workload identity, timer scope, peak memory, throughput, held-out score, resume result and cold-load result. State the resource budget under which the selection holds.
