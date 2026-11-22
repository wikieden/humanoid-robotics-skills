---
name: robot-agent-binding-review
description: Audit how robot text and voice sessions resolve a device's tenant, agent instance, immutable release, binding revision, and domain authority before dispatching a tool or robot task.
metadata:
  title: Device-to-Agent Release Binding Review
---

# Device-to-Agent Release Binding Review

Choose an authenticated device and one conversation turn. Reconstruct the binding that the runtime actually consumed. Capture pseudonymous identifiers and version digests. Record the configured policy for existing sessions when a binding changes.

1. Trace the text and voice ingress paths separately to the conversation entry point. Identify the source of device identity and tenant ownership, the binding record read at admission, the selected agent instance and release, and the session and turn identifiers. Compare like-for-like requests admitted under the same binding revision.
2. Verify how the session snapshot is stored and used for subsequent turns. Test a binding change while an earlier session is open. Check old and new sessions against the specified pinning or explicit migration policy. If a historical record lacks the release needed for reproducibility, report the ambiguity and follow the documented close or migration path.
3. Trace one proposed tool call to the domain service that owns the resource and makes the authorization decision. Record the target device, tenant, requested capability, decision, and resulting command or denial. A selected agent release establishes behavior identity. The domain service still decides whether that operation is allowed.
4. Check failure handling with synthetic identities. Cover an unavailable binding lookup, a device whose ownership changed, and an unavailable release. Confirm that errors are attributable and that an implicit default does not dispatch an unintended command. Distinguish runtime session completion, durable conversation history, and the device task outcome.

**Offline case.** Under a session-pinning policy, a voice session begins on release A. The device binding is then changed to release B. A fresh text session should resolve B, while another turn in the original session should resolve A or receive the documented explicit closure. Silently changing the old session to B is a binding defect. A tool request for a device outside the session's authorized scope must be denied independently of either release.

**Deliverable.** Return a binding matrix by device, channel, session, and turn. Include the effective release, authorization decision, expected migration behavior, and evidence for the first inconsistent lookup or dispatch.
