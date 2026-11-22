---
name: robot-rsi-correction-design
description: Design the next feedback collection round for a robot policy after a failure has been localized. Use when deciding which learner states to revisit, whether a takeover, expert query or outcome supplies a usable label, and how to spend a limited correction budget.
metadata:
  title: RSI Correction Data Design
---

# RSI Correction Data Design

Start from a failure family, examples from the current policy, the deployment observation/action contract and a collection budget. Deliver a sampling and labeling plan that can produce a trainable batch for a named objective.

| Available evidence | Use in this round |
| --- | --- |
| Failure clip with a verified terminal outcome | Tag the failing state and outcome. Request a correction at the decision point. A clip without a known target action can still supervise a compatible outcome estimator. |
| Expert queried on the exact learner observation | Keep the expert action as a counterfactual imitation target with its time, action convention and source. Record the action actually executed separately. Associate the observed next state and reward with that executed action. Record an explicit expert preference or a declared ranking rule before using the pair for preference learning. [DAgger](https://proceedings.mlr.press/v15/ross11a.html) |
| Operator takes over and a corrected segment runs | Preserve proposed policy commands, executed operator actions, intervention onset, handback and resulting state. For recovery imitation, form windows from contiguous expert targets. A replaced action and a later correction make a contrastive pair only when their decision context and alignment support it. [Paired-correction technical report](https://arxiv.org/abs/2611.08577v3) |
| Attributable transitions or a validated action-conditioned simulator | Outcome- or advantage-conditioned updates can use executed experience with suitable reward or value labels. Tag imagined transitions and check reward-critical contacts and failures against held-out observed transitions. [RECAP](https://www.pi.website/download/pistar06.pdf) · [VLAW](https://proceedings.mlr.press/v306/guo26i.html) |

1. Fix the unit before sampling, for example an independent recording, failure prefix or layout. Group duplicates and sibling clips before splitting. Sample recurrent failures, nearby successes and previously solved cases. Set aside independent validation groups before requesting labels. Record queried, answered, executed and excluded counts, and label minutes or simulator calls. [Failure-directed robot data collection](https://arxiv.org/abs/2609.38905)
2. At each selected state save the observation at decision time, actor, proposed action, label source, committed action, timestamp and mask. For delayed commands or cached chunks, trace the offset actually consumed. For a stale or ambiguous pairing, recollect the state or mask the target. Keep the parent data mix and correction budget visible.
3. Test the collection strategy against a matched alternative, such as uniform sampling at the same annotation budget. To test a training objective instead, give both objectives the same recordings and labels. Run a one-batch loader/target check before training. A fitted correction or a newly feasible plan is an intermediate result. Test closed-loop outcomes on independent tasks before reusing the candidate.

**Worked decision.** In one synthetic log the policy proposed and executed “open” while a queried expert labelled the same observation “hold”. The object fell. The imitation row can target “hold”. The observed transition is attached to “open”. The log supplies no measured outcome for “hold”. Expert labels on either side of a controller-only hold cannot form a contiguous expert action chunk.

**Handoff.** Return eligible recording IDs or synthetic placeholders, intended use by label type, rejected spans and reasons, split unit, sampling budget and a matched comparison. Use the ordinary training guide to fit and reload the chosen update.
