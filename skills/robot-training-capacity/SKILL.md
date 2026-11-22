---
name: robot-training-capacity
description: Size a robot video or multimodal training run from capture hours, sampling, cameras, model input layout and measured throughput. Use when comparing dataset or fleet scenarios and converting them to GPU-hours and elapsed time.
metadata:
  title: Compute Sizing for Robot Model Training
---

# Compute Sizing for Robot Model Training

Choose the decision the estimate must support, such as meeting a training deadline or fitting a data mixture into an allocation. Keep recorded hours, sampled input tokens, effective training passes, active GPU-hours and reserved wall time in separate columns.

1. Start with synchronized scene hours. For each input stream compute retained seconds times sampling rate times tokens per retained sample. Sum only the cameras and modalities consumed by the model. If the input already counts camera-hours, multiplying by view count again overstates work. Include text, action and temporal compression where the actual processor uses them. Check the result against one batch from that processor.
2. Convert the training recipe into consumed examples or tokens. Account for repeated passes, overlapping windows, packing, padding, mixture weights and dropped batches. Declare whether throughput counts padded tokens or useful tokens and use the matching numerator. If memory or sequence shape limits a candidate, carry that condition into the estimate.
3. Prefer measured throughput from a representative distributed run with the intended precision, sequence mix and I/O path. Label whether the rate is per GPU or for the entire group. Divide work by group throughput to obtain active wall time, then multiply by the participating GPU count for active GPU-hours. If using a theoretical estimate, state the architecture-specific FLOPs assumption and calibrate it against a pilot before committing capacity.
4. Apply downtime only for periods the measured rate excludes. Separate occupied GPU-hours, reserved GPU-hours and calendar delay. Queue time delays delivery and may consume no allocation. Budget experimentation, post-training, simulation and serving as separate workloads, showing which overlap and which compete for the same devices.

**Worked estimate.** Five synchronized scene-hours, two cameras sampled at two frames per second, and twelve tokens per frame yield the following one-pass visual workload. The throughput is synthetic and covers the whole four-GPU group during active training.

```python
tokens = 5 * 3600 * 2 * 2 * 12
group_tokens_per_second = 240
active_hours = tokens / group_tokens_per_second / 3600
gpus = 4
active_fraction_of_reservation = 0.8
assert tokens == 864_000
assert active_hours * gpus == 4
assert active_hours / active_fraction_of_reservation * gpus == 5
```

**Deliverable.** Return the input-unit ledger, a low/base/high estimate, the largest uncertainty, and the pilot measurement that would reduce it. Identify which outputs are forecasts and which numbers came from an executed run.
