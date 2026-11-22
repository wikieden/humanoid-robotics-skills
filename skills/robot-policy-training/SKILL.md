---
name: robot-policy-training
description: Design, run, or audit a robot policy training round for a vision-language-action policy (VLA), a world-action model (WAM), or rollout-driven recursive self-improvement (RSI). Use when choosing supervision, scoping a parameter update, resuming training, or deciding whether a candidate should become the next baseline.
metadata:
  title: Robot Policy Training and Recursive Self-Improvement
---

# Robot Policy Training and Recursive Self-Improvement

Start with one decision the experiment must support. An example is whether conditioning on a predicted future improves placement success at the same control rate. Record the baseline checkpoint and runtime, target task and embodiment, available observations and labels, development budget, evaluation unit, and acceptance criterion. Use RSI as a repeatable feedback loop around a VLA, WAM, planner, or execution system. Name what will change in this round.

## Choose the update from the available evidence

| Observation | Candidate update | Comparison that tests the explanation |
| --- | --- | --- |
| Aligned demonstrations cover the intended behavior, but the policy issues poor actions | Supervised fine-tuning (SFT) of an action head, adapter, or full VLA. Declare the action representation and loss, such as action-token prediction or continuous flow matching. | Frozen baseline versus the update, with the same processor, task mix, and runtime. Check held-out action error and closed-loop success. |
| The action depends on a future contact or object state, and time-aligned trajectories contain valid future observations | Train a WAM with a future-image or latent-feature target alongside action supervision. Specify the prediction horizon, trainable world and action modules, and loss weights. | Compare action-only conditioning with predicted-future conditioning at matched data and compute. An oracle using observed futures can diagnose headroom offline. |
| Repeated development failures expose a specific stage, and verified corrective experience exists | Start an RSI round. Update the action policy for a motor error, the external planner for a wrong subgoal, or the execution logic for a stale command. | Hold the other layers fixed. If both planner and policy changed, cross old/new planner with old/new policy under the same runtime. |

For recent approaches to paired corrections, latent subgoals, and world-model rollouts, consult the [research notes](references/training-methods.md) when the observations and supervision match.

## Prepare one reproducible run

1. **Freeze the split before windowing.** Deduplicate complete source recordings and group related sessions, objects, or layouts according to the generalization claim. Keep development feedback and candidate selection separate from the sealed acceptance set. Trace each source to its allowed use. A test rollout used to change a prompt, recovery rule, or checkpoint choice becomes development evidence.
2. **Inspect one real training batch.** Decode the camera views, language, state, and action chunk using the actual training processor. Check frames, units, absolute versus delta actions, camera order, episode tails, padding and supervision masks, and training-only normalization statistics. Compare the same observation with the inference processor. For WAMs, verify future targets stay within the episode. Run inference with future target fields removed and only inputs available at decision time. See [Episode Audit (optional)](../robot-episode-audit/SKILL.md).
3. **Prove the intended update on a short run.** Record the parent weight digest, code and config revision, seed, effective batch size, optimizer-step budget, hardware allocation, and dataset fingerprint. Inspect optimizer membership and gradient norms by module, then compare actual parameters before and after an optimizer step. Check frozen tensors for drift and log action and world losses separately when applicable. For a multimodal planner, compare decisions on real versus shuffled or masked images and inspect decision-token loss separately from formatting tokens. This tests whether better text loss reflects better use of observations.
4. **Test what the checkpoint restores.** Export weights with architecture/config, processor, action schema, normalization, and any required world encoder. Cold-load the export in a clean process and reproduce a fixed-input prediction with controlled noise and a declared numerical tolerance. For a resumable run, also restore optimizer, scheduler, mixed-precision scaler if used, RNG, global step, and sampler position. Compare the next sample IDs and learning rate with an uninterrupted run, including across distributed ranks.

## Turn a failure into a bounded RSI round

- Record the earliest observable failed stage, how many trials reached it, the committed action, its source, and the native outcome. Preserve failed attempts and timeouts in the full-task denominator. If the recordings show failure but contain no verified corrective action, collect a targeted correction, investigate the runtime, or use the sample as outcome supervision for a compatible objective.
- Match the learning objective to the data. For behavior cloning, mask policy and recovery-hold actions in mixed recordings. Paired corrections can supply positive and negative segments. Offline RL requires attributable transitions, rewards and terminals plus a method appropriate to the logged action coverage. Mark imagined transitions explicitly and validate world-model contact and failure predictions against independent observed transitions before expanding their use. See [Takeover Label Audit (optional)](../robot-episode-audit/references/takeover-labels.md).
- Track the parent, candidate, exact changed component, evidence motivating the change, data added, and cost. Once validation selects a candidate, freeze the checkpoint, adapters, prompt, tools, action transforms, normalization and runtime together. Clear episode-local memory between independent trials. Preserve the previous baseline for comparison and rollback.

## Decide whether to inherit the candidate

Pair baseline and candidate on the same initial layouts, seeds, task conditions, controller, and timing budget. Use independent task outcomes and include previously successful tasks. Report both-success, gained, lost, and both-failed counts, incomplete pairs, total attempts, interventions, stops, and timing. Net success change on complete pairs is `(gained - lost) / complete_pairs`. Inspect per-task regressions and uncertainty at the independent layout or session level before pooling repeated trials. Use [Policy Evaluation (optional)](../robot-policy-eval/SKILL.md) for action scaling, clipping, and whether the controller receives actions on time.

**Round record.** Deliver the run manifest, split IDs, parameter-update and reload evidence, per-trial comparison, and a decision to inherit the candidate, retain the baseline, or collect missing evidence. State the highest level actually tested: optimizer update, offline inference, simulation, or supervised hardware. Assign a parent for the next round only after applying the predeclared acceptance and retention criteria.
