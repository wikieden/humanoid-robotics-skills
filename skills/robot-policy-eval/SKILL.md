---
name: robot-policy-eval
description: Adapt or compare vision-language-action policies and world action models. Check observation and action contracts, checkpoint loading, action delivery timing, and paired simulation outcomes from reset or a shared handoff.
metadata:
  title: VLA and WAM Policy Evaluation
---

# VLA and WAM Policy Evaluation

Identify the question under test: compatibility with a robot, continuous action delivery, or a change in task performance. Record the robot model, dataset version, checkpoint, inference configuration, control rate, and evaluation setting.

1. Check camera views, language inputs, state ordering, action dimensions, normalization, and action chunk length in the target configuration. Trace the same recorded input from the loader through the policy to the client. Compare the training configuration with the inference service inputs and the client's action decoder.
2. Load the checkpoint in a fresh process with a fixed sample and inference settings. Save the raw actions, denormalized actions, and actions after client-side constraints. Inspect scale errors, saturation, reversed channel order, and substantial clipping.
3. Define the start and end of each timer. Measure model execution time, request round-trip time, and the interval between usable action arrivals at the controller. Divide the number of executable steps by the control frequency to find the time a chunk covers. Five steps at 20 Hz cover 250 ms. Check the queue timeline for starvation, accounting for overlapping chunks, repeated steps, and dropped actions.
4. Match the task, scene, robot, reset conditions, action frequency, trial count, and success criterion across policies. Record the outcome, human interventions, and stop reason for every attempt. Attribute published benchmark scores, completed training runs, offline replay, simulation, and supervised hardware results to their respective sources.

## Pair simulated rollouts

Choose the comparison unit before scoring: a fresh online rollout from reset, or two continuations from the same handoff state. For a policy comparison, each policy must generate its own actions on its own resulting observations. For a downstream execution comparison, a shared recorded prefix can isolate the change. Record the model calls used to create it separately from scored continuations. Verify both arms start from equivalent physical and controller state, including queues, random state and recurrent memory where relevant.

Pin the scene, asset and sensor versions, physics step, renderer settings, camera poses, and action horizon. Read settings back after reset. If the same seed produces different behavior, compare the initial physical state, first rendered observations, first actions, and first physical divergence. Report paired counts (both succeeded, gained, lost, both failed), incomplete pairs, and native partial scores. Score the physical terminal condition separately, for example stable support after gripper withdrawal. Stratify by layout and host when relevant. Distinguish simulated time, wall-clock time, inference and offline video encoding.

**Deliverable.** Provide a comparison table with model and data versions, latency percentiles and sample counts, failure clips, and a reproducible entry point. If the only evidence is a trained checkpoint or offline inference, mark task success rate as unmeasured.
