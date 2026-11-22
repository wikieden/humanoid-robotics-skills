---
name: robot-multimodal-grounding
description: Verify language-conditioned detections, instance identity, and object state against visible and geometric evidence. Use for wrong-object selection, occluded attributes, conflicting modalities, and stale spatial memory.
metadata:
  title: Multimodal Object and State Grounding
---

# Multimodal Object and State Grounding

Turn a request such as “find the empty container” into testable claims: a container was detected, it is the referenced instance, its interior is visible, and that interior is empty. Associate each claim with a frame, candidate region, query and required evidence. Speech or text provides user intent. The current object state needs an observation.

1. **Preserve the evidence when cropping.** An open-vocabulary detector such as Grounding DINO can propose boxes from text. Keep the source frame, candidate IDs, competing instances, crop coordinates and outputs. Use a full crop, mask, image-text similarity score, or vision-language model according to the property being judged. A shell mask may remove the contents needed to decide whether a container is empty.
2. **Judge each attribute separately.** A high detection score can coexist with an invisible interior. Allow an explicit unknown for state even when identity is certain. Record the visible cue and where it appears. Inspect whether a model's explanation is supported by those pixels.
3. **Bind the modalities to one observation.** For a 3D referent, check instance association, time alignment, depth validity and scale, and the transform at capture. Keep the state and the metric pose independently reportable. For spatial memory, retain the observation time and map revision. Reobserve changeable properties when the stored evidence is too old. Use [RGB-D Pose Validation (optional)](../robot-rgbd-pose/SKILL.md) for geometric inconsistencies.
4. **Test what drives the decision.** Mask the interior, change an irrelevant background, and exchange the positions of two similar instances. Fix the query, crop policy, model revision, and decoding settings. Label visibility independently. Report detection misses, identity swaps, unsupported state claims, and abstentions, both end-to-end and conditional on correct detection.

**Offline example.** In four correctly detected instances, only two interiors are visible. Score answer coverage, accuracy among answered cases, and unsupported assertions. A system that always abstains has undefined accuracy among answered cases.

```python
observable_state = ["empty", "occupied", "unknown", "unknown"]


def score(decisions):
    assert len(observable_state) == len(decisions)
    answered = correct = unsupported = 0
    for reference, decision in zip(observable_state, decisions):
        if decision == "unknown":
            continue
        answered += 1
        correct += decision == reference
        unsupported += reference == "unknown"
    accuracy = correct / answered if answered else None
    return answered / len(decisions), accuracy, unsupported


assert score(["empty", "occupied", "empty", "empty"]) == (1.0, 0.5, 2)
assert score(["empty", "occupied", "unknown", "unknown"]) == (0.5, 1.0, 0)
assert score(["unknown"] * 4) == (0.0, None, 0)
```

**Deliverable.** Return per-instance identity, state, supporting region, time, optional 3D location, and reason for abstention. Include a counterexample that identifies the first error in detection, cropping, cross-modal association, classification, or memory retrieval.
