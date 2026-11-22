---
name: robot-edge-vision-scheduling
description: Diagnose model starvation, late detections or stale outputs when several perception tasks share an edge accelerator. Use when a system meets its aggregate frame-rate target but one model rarely runs.
metadata:
  title: Scheduling Multiple Vision Models on an Edge Accelerator
---

# Scheduling Multiple Vision Models on an Edge Accelerator

For each operating mode, list each enabled model, minimum useful inference cadence, maximum result age, measured runtime, and whether the budget is a soft average or a hard deadline. Measure camera capture, input queueing, accelerator service time and result publication separately. Display refresh and tracker updates can continue between detections.

1. Record a scheduling decision for every due model. Include frame identity, due time, reason for admission or deferral, estimated cost, actual cost and last fresh inference time. Check a time interval long enough to include the slowest model's required refresh.
2. Test one non-preemptible model whose execution time exceeds the nominal per-frame share. A strict fit test can defer it forever. For a soft average budget, reserve service over several frames or permit bounded overruns with explicit accounting. For a hard frame deadline, reduce the workload, use another execution path, or report infeasibility. A fixed “first eligible model” rule can still starve a peer when several are due together.
3. Change modes with a frame queued and a model in flight. Tag results with model, mode generation and source-frame time. Decide whether consumers can accept results from the previous mode. Under overload, measure maximum time between fresh results, deadline misses and dropped inputs per model. Include packaging or preprocessing time when it competes for the same budget.

**Scheduling fixture.** An indivisible job costs three synthetic time units and receives two units of soft budget per tick. Resetting unused budget every tick gives it zero service. Carryover makes it runnable without changing its cost.

```python
credit = runs = 0
for _ in range(6):
    credit += 2
    if credit >= 3:
        credit -= 3
        runs += 1
assert runs == 4 and credit == 0
```

This fixture checks average service for one model. Add competing models and real execution times before claiming fairness or a deadline guarantee.

**Deliverable.** Provide the schedule trace, per-model age and cadence, the first missed requirement, and the smallest policy or workload change that resolves it.
