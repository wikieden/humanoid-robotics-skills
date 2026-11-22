# Diagnosing Streaming Speech Underruns

Pick one uninterrupted utterance with a reported gap. Trace its sequence numbers at the synthesis callback, sender, receiver, decoded queue and audio output callback. Compare intervals on one monotonic clock at a time. Record sample format, sample rate, channels, timestamps and any intentional silence.

1. Express queued **playable** audio in milliseconds. For interleaved PCM, use `queued_ms = 1000 * queued_bytes / (channels * bytes_per_sample * sample_rate_hz)`, with the sample rate measured per channel. For compressed audio, use packet duration or decoded sample counts. A configured byte capacity says little about the queue depth at the instant the player needs samples.
2. Plot cumulative playable duration produced and consumed, plus actual receiver queue depth. Separate time to first sound from gaps during continuous playback. Inspect the largest interarrival gaps and the preceding headroom. A producer delivering one second of audio per second on average can drain the queue during a bursty interval.
3. Distinguish causes with matched inputs. Replay the same decoded samples locally, then the same encoded frames through the decoder and receiver, then the original stream. If data arrived on time but the decoded queue emptied, inspect decoding and scheduling. If the queue stayed healthy, inspect the audio callback, format and sample clock. For a transport that conceals loss, record concealment events separately from output underruns. [WebRTC statistics](https://www.w3.org/TR/webrtc-stats/)
4. Change one parameter such as chunking cadence or startup prefill. Replay the same arrival trace and compare missing playback time, gap count and added start latency. End-of-stream drain and an intentional user interruption have their own outcomes. For late audio after an interruption, use [Voice Playback](../SKILL.md#turn-interruption-and-delivery).

**Fixture.** Playback starts with 20 ms queued. Every arrival contributes another 20 ms after the indicated delay. Both traces produce the same amount over the same elapsed time.

```python
def missing_playback_ms(delays):
    queued = 20
    missing = 0
    for elapsed in delays:
        missing += max(0, elapsed - queued)
        queued = max(0, queued - elapsed) + 20
    return missing

assert missing_playback_ms([20, 20, 20, 20]) == 0
assert missing_playback_ms([20, 40, 10, 10]) == 20
```

**Deliverable.** Give the first stage that missed its deadline, the evidence at that boundary, and the measured start-latency versus continuity tradeoff. When only sender traces exist, state which receiver measurement would distinguish the remaining explanations.
