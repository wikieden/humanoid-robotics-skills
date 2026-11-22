---
name: robot-agent-context
description: Design or test what an agent may retrieve or remember when users, sites or devices change. Use for shared knowledge revisions, personal preferences, revocation, and cross-device conversation handoff.
metadata:
  title: Shared Robot Knowledge and Session Memory
---

# Shared Robot Knowledge and Session Memory

Start with two devices serving the same agent release. Define who is speaking, where the device is operating, and whether the person is known. Resolve the applicable tenant, agent instance, site, device and principal from the session authority before assembling context.

| Context | Establish at read time | On device or speaker change |
| --- | --- | --- |
| Published knowledge | Effective revision, tenant, site and publication state | Retrieve again under the destination scope. Carry the source revision in the citation. |
| Personal preference | Identified subject, permitted purpose and devices, current consent version | Apply only if the destination also has a current grant. A guest starts without personal preferences. |
| Conversation state | Active session, speaker and turn generation | Start a fresh session or transfer explicitly selected fields under the handoff policy. |

Filter retrieval candidates by scope before ranking. Check the winning passages again before delivery if publication can change mid-turn. Version preference writes and deletion records so that an older summary job cannot recreate a forgotten preference. Record the policy decision and pseudonymous passage or preference identifiers when testing.

## Exercise a handoff

Use synthetic speakers, devices and distinct fact markers. Give both devices one shared fact, give the first device a site-specific fact, and grant one speaker a preference for an explicit purpose. Query each scope with the same wording. Inspect which markers actually reached the response builder, as well as the answer. An omitted phrase alone gives little evidence about what context the model received.

Withdraw a passage after retrieval and before delivery. Revoke a preference before its delayed summary is saved. For an authorized move between devices, bind a short-lived handoff to the intended subject, instance and destination, consume it atomically, and test a repeated delivery. Resume only the agreed fields and re-check their current scope. Record separately whether the system identified the speaker, retrieved the right facts, and transferred the authorized state.

**Deliverable.** Provide the scope matrix, expected and observed markers for each transition, and the first read, write or delivery that violates it. Report the highest layer exercised, such as a storage fixture, retrieval service or end-to-end device interaction. For the release chosen at session admission, use [Device-to-Agent Release Binding Review (optional)](../robot-agent-binding-review/SKILL.md).
