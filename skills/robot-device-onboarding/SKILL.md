---
name: robot-device-onboarding
description: Qualify a new robot for platform access. Trace hardware identity, activation retries, credential rotation, separate messaging channels, and cloud confirmation after a network change.
metadata:
  title: Robot Device Onboarding and Acceptance
---

# Robot Device Onboarding and Acceptance

Start with a newly provisioned test device and a specific scope: first activation, recovery after interruption, or a network change. Record the firmware and protocol versions, a pseudonymous hardware identity, tenant assignment, and timestamps. Keep credentials and wireless network details out of the evidence.

## Trace identity across a retry

1. Map the durable hardware identity, changeable serial or display label, platform device record, and tenant binding. Identify which system owns each value. Use the durable identity to check whether a second activation updated an existing device or created a duplicate.
2. Separate creation of the device record from credential issuance and local persistence. If the activation response is lost after the record is created, retry through the documented recovery path. Preserve the logical device identity and regenerate request-specific freshness fields as the protocol requires. Verify one device record, the correct tenant, and a usable credential set. The issued bytes can change across retries.
3. Check expiration and refresh using a test clock or fixture. For rotating credentials, exercise loss of the refresh response and a restart during persistence. The device must recover a consistent credential set. Record the documented reactivation path when the previous refresh credential has already been consumed.
4. Verify each required channel independently. On a test broker, observe a harmless state report tied to the authenticated device. On the session channel, observe an authenticated exchange scoped to the same device and tenant. Record denied cross-tenant access using isolated test identities. Keep proof of transport connectivity and proof of application authorization as separate observations.

## First-device acceptance cases

| Case | Evidence that resolves it |
| --- | --- |
| First activation | One durable device identity resolves to the expected tenant. Each required channel completes its own authenticated exchange. |
| Lost activation response | The retry returns the device to service and a lookup finds exactly one device record after both attempts. |
| Expired access credential | The expected refresh or recovery path succeeds across a restart. A partial write does not replace a usable credential pair. |
| Network change | Local provisioning completes, then the same device sends a fresh cloud report identifying the intended network through the approved privacy-preserving indicator. An old heartbeat or a local connection event leaves cloud confirmation open. |

**Deliverable.** Return a state table from provisioning through connected operation, a per-channel verdict, and the earliest missing signal in each failed case. Label simulated credential tests and observed device behavior separately.
