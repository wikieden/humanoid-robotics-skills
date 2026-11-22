---
name: robot-voice-playback
description: Diagnose robot speech that stutters or drops out during one utterance, or verify interrupted, duplicated or unconfirmed playback across turns and retries.
metadata:
  title: Robot Speech Playback and Continuity
---

# Robot Speech Playback and Continuity

**Speech cuts out during one uninterrupted utterance.** Go directly to the [streaming underrun guide](references/streaming-underruns.md). Trace playable milliseconds and output deadlines to the first observed shortage. With sender-only evidence, identify what the receiver must measure.

For speech that resumes after interruption, repeats, or lacks a completion receipt, use the turn timeline below.

## Turn interruption and delivery

Pick one utterance and state the intended outcome, such as completing one announcement or cancelling an old reply after a user interruption. Identify the logical delivery, turn, target device, audio revision, and expiry. A transport retry can receive a new request identifier while referring to the same logical delivery.

1. Align the turn events: synthesis, dispatch, device receipt, playback start, playback end or cancellation, device acknowledgment, and persisted platform outcome. Use a common timebase or report intervals within each clock. Capture the device playback callback and, if audibility matters, a consented external observation of the output.
2. For interruption, mark the cancelled turn and the successor. Inspect the active player and queued audio on the device. Deliver a delayed chunk for the cancelled turn in an offline fixture. Check that it cannot resume speech or complete the new turn.
3. For reliable delivery, identify the durable deduplication key and its retention through restart. Re-delivery of a completed item should return its stored acknowledgment while it is valid. A payload change under the same identity is a conflict. If the original playback outcome is uncertain after a crash, preserve uncertainty and apply the documented recovery policy.
4. Match acknowledgments to the authenticated device, tenant, delivery and validity interval. Distinguish synthesis success, transport acceptance, device-reported playback completion, and independently observed sound. Check that late or mismatched acknowledgments leave unrelated deliveries untouched.

**Offline case.** A clip ends on the device. Its completion acknowledgment is lost. The player restarts and receives the same unexpired delivery. With a durable completion record, the expected totals are one playback and one logical completion, even when the acknowledgment is transmitted twice. With no durable record, record the crash window as unresolved.

**Deliverable.** Provide a turn-by-turn timeline with observed play counts, duplicate deliveries, cancellation boundaries, and the evidence for each completion. Use a synthetic or consented clip and omit raw private audio from the report.
