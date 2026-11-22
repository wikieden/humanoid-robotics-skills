---
name: robot-simulation-preview
description: Verify that a live robot simulation preview shows the active run while it is running and that enabling rendering preserves the reported outcome. Use for viewer integration, stale frames or disagreement between telemetry and video.
metadata:
  title: Live Simulation Preview Verification
---

# Live Simulation Preview Verification

Select one deterministic short scenario with an observable phase change and one variant with a single injected fault. Record the initial state, seed, simulator and controller revisions. Give each launch a unique run ID, including repeats with the same seed.

1. Keep the simulation worker authoritative for state, events and terminal outcome. Stamp frames and events with the run ID and producing step or simulation time. Record arrival and terminal publication on one observer clock. A viewer heartbeat shows a connection is alive. Frame progress requires distinct producing steps.
2. Observe from launch through termination. Capture at least two advancing steps before the terminal result is published. Read the run ID from the publisher data. With a static camera, match the fault event to simulation time and inspect the adjacent frames. A fault can be real even when it occurs between displayed frames. Report that gap.
3. Run the ordinary and faulted scenarios twice each, with preview off and on. Compare within each pair using the same physics stepping, policy inputs and seeds. Record phase order, anomaly type, terminal state and task metrics. Declare tolerances for nondeterministic quantities before running. Report wall-clock overhead separately from simulated duration. Check whether rendering changes the clock the controller actually consumes.
4. Slow or reconnect a viewer. With a latest-frame feed, tolerate skipped pictures and show the age of the last frame. Recover persistent events and the terminal result from the worker's run record. On the next run, expire the previous frame. For a viewer that only supports one run, make that scope explicit before interpreting a concurrent test.

**Regression fixture.** A frame from the previous run, a repeated frame and a frame first delivered after completion can all look current. This example counts distinct producing steps seen before the result.

```python
def live_steps(run_id, terminal_arrival, frames):
    return {step for run, step, arrival in frames
            if run == run_id and arrival < terminal_arrival}

frames = [("old", 12, 1), ("new", 2, 3), ("new", 2, 4), ("new", 8, 11)]
assert live_steps("new", 10, frames) == {2}
assert live_steps("new", 10, frames + [("new", 5, 6)]) == {2, 5}
```

**Deliverable.** Return the four run records, evidence of live frame progress and fault alignment, any result differences, and measured rendering overhead. To investigate the physical interaction itself, use [Contact Task Simulation](../robot-sim-contact-validation/SKILL.md).
