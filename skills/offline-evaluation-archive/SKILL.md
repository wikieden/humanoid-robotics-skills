---
name: offline-evaluation-archive
description: Preserve an evaluation dashboard and verify offline access to its results, per-trial details and replay media. Use when a snapshot has totals but missing trials, partial camera views or playback that still depends on the original service.
metadata:
  title: Offline Evaluation Archive Verification
---

# Offline Evaluation Archive Verification

Fix the snapshot revision and capture time. Inventory checkpoints, evaluation batches, trials, detail records, expected camera views and media files as separate units. Record the source's expected IDs or pagination boundaries for each. Mark an unknown denominator explicitly. One clip can be referenced by several views, and one trial can have several clips.

1. Save source responses and media manifests with their revision, retrieval status, byte size and digest when available. Keep the original responses alongside normalized tables. Separate a missing detail, an absent media listing, a failed transfer and an integrity failure. Keep newly observed revisions identifiable when updating a snapshot.
2. Join by stable IDs. Reconcile an aggregate score against trials using the published scoring rule, including exclusions and timeouts. Preserve both values when they disagree. Record the latest checkpoint and the latest checkpoint with a completed evaluation separately.
3. Verify bytes, playability and viewer coverage as separate checks. A stored digest records what was saved. Recompute it when checking current integrity and state the fraction read. For media, test decoding or seeking as appropriate. With external requests disabled, follow a real path from the dashboard filter through a trial to a specific view. Try a known missing record as well as a working one. Preserve a visible unavailable state when the source omitted a detail.
4. When new captures arrive, compare revisions by ID and content. Retain the prior capture where a state or score changed. Attribute a revised result to the upstream source until independently reproduced.

**Coverage fixture.** Two files exist for three expected camera views. Only one trial has a complete set. The other trial has playable media and still lacks a detail record.

```python
expected = {"trial-a": {"front", "side"}, "trial-b": {"front"}}
media = {("trial-a", "front"), ("trial-b", "front")}
details = {"trial-b"}
missing_views = {(trial, view) for trial, views in expected.items()
                 for view in views if (trial, view) not in media}
assert missing_views == {("trial-a", "side")}
assert set(expected) - details == {"trial-a"}
assert sum(all((t, v) in media for v in views)
           for t, views in expected.items()) == 1
```

**Deliverable.** Return coverage per unit, a missing-ID manifest, integrity and playback checks with their scope, and the offline user paths exercised. Report the archived scores as source-reported results.
