---
name: robot-action-release
description: Review publication of reusable robot motion assets, immutable revisions, tenant opt-in, compatibility, concurrent upgrades, withdrawal, and rollback of pinned references.
metadata:
  title: Robot Action Asset Release and Withdrawal
---

# Robot Action Asset Release and Withdrawal

Take one authored action, such as a gesture synchronized with speech. Identify the editable draft, the published artifact, the target robot or controller profile, each tenant's selected version, and the artifact resolved for execution. These are distinct records with different owners and lifetimes.

1. Freeze the draft revision and asset digest when publishing. Check joint names and units, timing, configured limits, supported robot profiles, and referenced media. Record what the validation actually covered. Keep physical execution approval and collision or dynamics validation as separate evidence.
2. Verify the intended tenant audience and immutable version lookup. Publish a second revision in an isolated catalog and resolve an existing tenant's pinned reference again. It should still resolve to the original bytes until an explicit version change succeeds.
3. Exercise concurrent changes from the same prior tenant selection. Record the expected prior revision, operation identity, and committed result. A stale compare-and-swap should trigger a reread. After a lost response, reconcile the original operation before retrying.
4. Check withdrawal semantics against the declared policy. Inventory existing pins, new selections, cached copies, and running executions separately. If withdrawal only blocks new adoption, report affected existing references. An emergency execution block needs its own enforcement path and evidence. For rollback, verify that the selected earlier digest is still available and compatible.

**Offline case.** Tenant A pins revision 1. Revision 2 is published and later withdrawn under a policy that blocks new adoption and preserves existing pins. A still resolves revision 1. Tenant B cannot newly select revision 2. Neither event should rewrite revision 1 or enqueue motion.

**Deliverable.** Return the draft-to-digest provenance, tenant impact table, compatibility evidence, and the observed outcomes of publication, concurrent selection, withdrawal, and rollback.
