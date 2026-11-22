---
name: robot-task-protocol
description: Design or test command and receipt semantics for multi-stage robot tasks, including pause, resume, advance, retries, out-of-order controls, and task-versus-command completion.
metadata:
  title: Long-Running Robot Task Protocol Acceptance
---

# Long-Running Robot Task Protocol Acceptance

Start with one execution and a short route or sequence. Identify the parent execution ID, the logical ID of each control operation, and the stage identifier or revision used to guard a transition. Assign a new logical ID to a new operation and retain the original ID for retransmission.

1. Build a transition table covering allowed source state, precondition, next state, side effect, and terminal receipt. Make resume semantics explicit: continuing the interrupted stage and advancing to the next one produce different behavior. Specify the outcome of advancing at the last stage.
2. Trace receipts on two timelines. A control receipt answers whether a particular pause, resume, or advance took effect. The parent execution has its own progress, failure, and final completion. A message broker acknowledgment establishes transport progress only.
3. Replay duplicate and out-of-order controls against the same starting state. Verify idempotency at the consumer that performs the side effect and where the platform applies the receipt. Check what survives a device restart. Guard stale advances with the expected stage or equivalent revision. Define how simultaneous operations are serialized or rejected.
4. Record the observed terminal state and side-effect count for each command and for the parent. On reconnect, reconcile durable progress and cached results before issuing another start. For a concrete incident spanning cloud and device logs, continue with [Cloud-to-Robot Task Tracing](../robot-task-trace/SKILL.md).

**Offline case.** A three-stage task is at stage 1. Command A advances from stage 1 to stage 2. Its receipt is lost and A is retransmitted. A new command B then arrives with stage 1 as its required starting point. The device should still be at stage 2, with one advance, a consistent result for A, no effect from B, and the parent task still active.

**Deliverable.** Provide the transition table, the command and execution timelines, the terminal-state reconciliation rule, and a failing or passing trace for each retry, concurrency, and ordering case.
