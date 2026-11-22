---
name: interactive-run-lifecycle
description: Implement or review pause, resume and restart in a game, simulator UI or interactive lab. Use when input repeats, timers advance under a pause overlay, or a callback from an earlier run updates a restarted scene.
metadata:
  title: Pause, Resume and Restart in Interactive Applications
---

# Pause, Resume and Restart in Interactive Applications

List phases in terms of actions they accept. In a small simulator these might be ready, running, paused and finished. Keep the authoritative phase outside the rendering and input adapters. Preserve the phase that was paused so resuming a ready scene does not start the simulation.

| Transition | Reset or preserve | Observable check |
| --- | --- | --- |
| Pause and resume | Preserve run identity, prior phase, remaining simulation timers and scene state | Pause before launch and during motion. Each returns to its own phase. |
| Advance a stage | Preserve run identity and run-wide state, replace stage-local entities | A level or scenario is constructed once even if the UI redraws. |
| Restart the same stage | Allocate a new run generation, reset transient input, subscriptions and callbacks | A delayed completion from the previous generation cannot advance the replacement stage. |

Translate hardware events into named actions. Sample held axes as continuous state. Latch a one-shot press that can begin and end between frames, consume it once, and decide which phase receives actions that arrive together. If individual repeats matter, queue each event rather than coalescing them. Treat menu actions and gameplay inputs separately.

Specify the pause behavior for physics stepping, simulation timers, animations and the UI clock. Keep the resume control responsive. For a remote simulation, verify whether the control pauses the worker or only the view. On teardown cancel timers and detach listeners. Guard late callbacks with both the run and stage identity if an old stage can finish after the next one starts.

**Regression sequence.** Start in ready, pause, resume, and confirm the launch action is still required. Launch with a tap entirely between two frames. Verify one launch. Pause halfway through a timed effect, advance wall time, resume, and check that the remaining simulation time is unchanged. Schedule a completion, restart into the same stage, then deliver the old completion. The new run must still be ready. Repeat with the same view mounted twice to detect duplicate subscriptions.

**Deliverable.** Return the transition table, ownership of clocks and one-shot actions, and results of the regression sequence. Record whether each check exercised the state machine, event adapter or rendered application.
