---
name: agent-harness-comparison
description: Compare coding or tool-using agent workflows when prompts, tools, context handling, retries or graders may explain a score change. Use for matched experiments, per-task regressions and cost per solved task.
metadata:
  title: Paired Agent Harness Evaluation
---

# Paired Agent Harness Evaluation

Name the change the comparison should isolate, such as tool-result truncation or the retry policy. Record model revision, input fixtures, tool versions, permissions, workspace starting state, time and token budgets, and grader version. When two products expose different or opaque model settings, label the result as a comparison of the complete systems.

## Pair the runs

1. Give each configuration a fresh copy of the same starting state for each task. Decide what counts as success from an observable outcome, such as an artifact passing a check. Set the treatment of timeouts, retries and manual interventions before running. Exclude setup failures only under an explicit rule applied equally to both sides.
2. For a harness-only change keep the model fixed. If both model and harness change and all combinations are supported, run each model under each harness. Repeat a subset with the same configuration to estimate normal outcome variation. Keep independent trials identifiable even when a task is retried.
3. Join results by task and trial ID. Count common passes, common failures, baseline-only passes and candidate-only passes. Inspect traces for the first divergent step in both directions. A failed attempt still consumes tokens and elapsed time. Compute cost per success as total cost of all attempts divided by solved tasks for the declared retry policy. Report it as undefined if none succeed.

**Worked comparison.** In this synthetic fixture each column represents the same task. The runs have equal success rates, yet the candidate fixes a task and breaks another.

```python
baseline = {"edit": True, "build": True, "resume": False, "export": False}
candidate = {"edit": True, "build": False, "resume": True, "export": False}
assert baseline.keys() == candidate.keys()
gained = {task for task in baseline if candidate[task] and not baseline[task]}
lost = {task for task in baseline if baseline[task] and not candidate[task]}
assert gained == {"resume"} and lost == {"build"}
assert sum(candidate.values()) == sum(baseline.values()) == 2
```

**Deliverable.** Return the changed variables, paired outcome table, cost and elapsed time including failures, and traces for a gain and a loss where available. State which cause the experiment can isolate. Report scorer-fixture checks and live agent trials separately.
