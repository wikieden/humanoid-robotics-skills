---
name: robot-bag-recording
description: Design or audit a continuously running robot data recorder with bounded storage and asynchronous upload. Use when a session must be archived while capture continues, or retention, restart or retry can produce incomplete bags.
metadata:
  title: Continuous Robot Recording, Rotation and Upload
---

# Continuous Robot Recording, Rotation and Upload

Identify the recording unit that can be reopened independently. A split file may have closed while the enclosing session still has mutable metadata. Record the topic allowlist, storage backend, quality of service, session identifier, and whether upload operates on a split or the whole session.

1. Give the writer ownership of the active session. For whole-session upload, seal the requested session, finalize its metadata, open the replacement recording, and hand the sealed identity to the upload worker. If the writer stops and restarts, measure the gap using source sequence numbers or timestamps. A new directory appearing immediately gives no bound on lost messages.
2. Keep compression and network waits off the recording control path. Test capture under a slow or failing upload, including CPU and disk contention. Measure input counts, recorded counts, source gaps and query responsiveness. Track empty or incomplete recordings explicitly instead of scoring a small successful transfer as usable data.
3. Define retention separately for closed splits, sealed sessions and unconfirmed uploads. Keep the open file and any in-use archive stable. When pruning recorded splits, update the reader-visible index to match what exists. If storage fills before an unconfirmed session can be retained, apply and report the chosen loss or stop policy.
4. Retry a sealed session using its stable identity and content digest. Distinguish a partial remote transfer from a confirmed archive. After a restart, reconcile the index with the filesystem and remote receipt. Reopen the delivered archive using the intended bag reader and check topic counts and boundary timestamps.

**Rotation fixture.** Publish a consecutively numbered synthetic topic. Trigger upload twice during capture and interrupt the first transfer. Record which session each caller requested. An explicit retry of the first sealed session should converge on one archive of that content. Check the union of captured sequence numbers across both sides of the rotation, report any gap, and verify that the replacement session stayed writable during the retry.

In this single-topic fixture the counts add up to the number sent. Checking identities still reveals both a missing message and a duplicate.

```python
from collections import Counter

sent = set(range(20, 26))
sealed, replacement = [20, 21, 22], [22, 24, 25]
received = Counter(sealed + replacement)
assert sum(received.values()) == len(sent)
assert sent - received.keys() == {23}
assert {seq for seq, count in received.items() if count > 1} == {22}
```

**Deliverable.** Return a session timeline showing seal, reopen, archive and confirmation, plus capture gaps and retention decisions. For interpreting the resulting trajectories as training samples, use [Episode and Training Dataset Audit (optional)](../robot-episode-audit/SKILL.md).
