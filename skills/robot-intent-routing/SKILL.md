---
name: robot-intent-routing
description: Add or change a spoken or typed robot intent in a hybrid rule and model classifier. Use when paraphrases miss a new label, overlapping phrases trigger the wrong task, or a classifier update changes which requests reach dispatch.
metadata:
  title: Robot Intent Routing and Catalog Regression
---

# Robot Intent Routing and Catalog Regression

Define each intent's stable ID, meaning, required slots, and disposition such as conversation, clarification, task proposal or cancellation of the current request. Record which intents each route supports. A social response and a physical task can share a noun and require different outcomes.

1. Compare the intent registry against rule outputs, model fallback instructions, response schema and downstream handlers. If a label is deliberately rule-only, record that in the comparison. Exercise the fallback directly or use a paraphrase that misses every rule. An exact-keyword test never reaches that branch.
2. Add a minimal pair around each important boundary. For a guide robot, “lead me to the display” requests motion, while “describe the display” can be answered in place. Also try a quoted command, a negated request, a word containing a short trigger, and two actionable intents in one turn. Declare how ties and contextual cancellations are resolved. Decisions that depend on the insertion order of equal-priority rules need a test.
3. Exercise an unknown label, missing slot, timeout and unavailable classifier. Record the route selected and whether any task proposal was emitted. Permit a bounded clarification or a conversational response according to product policy. Keep a conversational cancellation distinct from a protective stop. The execution boundary still checks the device capability and current authority.
4. Compare catalog versions on the same held-out utterances and session contexts. Report per-intent misses, unintended action proposals, abstentions, fallback usage and latency. Use a stub to test routing and failure handling, then label any live-model evaluation separately.

**Catalog fixture.** A new label can be present in the schema and the handler table while a fallback model's instructions omit it. This check uses an explicit manifest of labels supplied to that classifier.

```python
fallback_intents = {"describe", "guide", "clarify"}
schema = {"describe", "guide", "clarify"}
handlers = {"describe", "guide", "clarify"}
prompt_manifest = {"describe", "clarify"}
assert fallback_intents <= schema & handlers
assert fallback_intents - prompt_manifest == {"guide"}
```

**Deliverable.** Return the catalog diff, branch-specific test utterances and expected dispositions, plus one trace from ingress to the proposed action or clarification. Record dispatch and physical completion separately when they are in scope.
