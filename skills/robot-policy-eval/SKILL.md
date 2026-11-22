---
name: robot-policy-eval
description: Adapt or compare vision-language-action policies and world action models. Check observation and action contracts, checkpoint loading in a fresh process, action delivery timing, and task performance.
metadata:
  title: VLA and WAM Policy Evaluation
---

# VLA and WAM Policy Evaluation

Identify the question under test: compatibility with a robot, continuous action delivery, or a change in task performance. Record the robot model, dataset version, checkpoint, inference configuration, control rate, and evaluation setting.

1. Check camera views, language inputs, state ordering, action dimensions, normalization, and action chunk length in the target configuration. Trace the same recorded input from the loader through the policy to the client. Compare the training configuration with the inference service inputs and the client's action decoder.
2. Load the checkpoint in a fresh process with a fixed sample and inference settings. Save the raw actions, denormalized actions, and actions after client-side constraints. Inspect scale errors, saturation, reversed channel order, and substantial clipping.
3. Define the start and end of each timer. Measure model execution time, request round-trip time, and the interval between usable action arrivals at the controller. Divide the number of executable steps by the control frequency to find the time a chunk covers. Five steps at 20 Hz cover 250 ms. Check the queue timeline for starvation, accounting for overlapping chunks, repeated steps, and dropped actions.
4. Match the task, scene, robot, reset conditions, action frequency, trial count, and success criterion across policies. Record the outcome, human interventions, and stop reason for every attempt. Attribute published benchmark scores, completed training runs, offline replay, simulation, and supervised hardware results to their respective sources.

**Deliverable.** Provide a comparison table with model and data versions, latency percentiles and sample counts, failure clips, and a reproducible entry point. If the only evidence is a trained checkpoint or offline inference, mark task success rate as unmeasured.
