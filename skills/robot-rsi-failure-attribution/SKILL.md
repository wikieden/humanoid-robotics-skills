---
name: robot-rsi-failure-attribution
description: Localize recurring rollout failures during robot recursive self-improvement (RSI). Use when terminal scores, stage counts or recovery replays disagree and the team needs to decide whether to change perception, planning, the policy, the executor or the evaluator.
metadata:
  title: RSI Failure Attribution
---

# RSI Failure Attribution

Start with the parent system revision, allowed development episodes, command and observation traces, and the native success predicate. Deliver one testable explanation of the earliest divergence and one experiment that could refute it.

1. **Find the first broken condition.** Reconstruct the expected transitions and identify a measurable event for each, such as stable object support after the gripper opens. Trace observation → subgoal → proposed action → accepted command → measured state → scorer. A rejected proposal, an executed action that slipped, and a scorer that missed a valid placement call for different fixes. If the terminal video cannot distinguish them, name the missing signal.
2. **Count who reached the stage.** For each revision, report total starts, episodes reaching the stage, passes among those episodes, and end-to-end successes. Count distinct episodes separately from retries. For strictly nested stages the conditional pass rates multiply to the full pass rate. For branching or retrying tasks, use the actual transition ledger. Changing an upstream stage changes the mix of downstream cases. [Compounding Physical RSI, preprint](https://arxiv.org/abs/2611.06654v1)
3. **Try to disprove the explanation.** Replay a known-good trajectory through the evaluator if scoring is suspect. For a recovery change, branch before the intervention. Match physical state, contacts, observations, action queue, recurrent state and random draws where applicable. Run an unchanged control first and record its variability. Matching seed and action prefix alone can conceal a different contact state. Mark unmatched branches as inconclusive for causal attribution.
4. **Choose the next intervention.** Change one component on the matched branch. If both the planner and policy changed, compare old/old, new/old, old/new and new/new when feasible. Separate a handoff-only recovery result from a full rollout starting at reset. Identify who selected the change and what persists to the next round. A within-episode retry belongs in the execution trace. [Original study of repeated robot skill discovery](https://arxiv.org/abs/2609.31760)

**Worked decision.** In a synthetic 20-start test, the parent reaches release 8 times and completes 6 placements. The candidate reaches release 16 times and completes 10. Full success rises from 30% to 50%, while success given release falls from 75% to 62.5%. The four additional release failures are compatible with harder cases reaching release. Compare both revisions from matched pre-release states before assigning the regression to the gripper.

**Handoff.** Return the first divergent event, competing explanation, matched and unmatched trial counts, observation that would distinguish them, and the component worth changing. A diagnosed execution or scoring defect can be fixed directly. A missing learned behavior can proceed to correction design.
