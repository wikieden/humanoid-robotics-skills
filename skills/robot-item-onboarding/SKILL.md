---
name: robot-item-onboarding
description: Decide whether an existing picking capability can handle a new SKU, packaging revision or shelf position. Use for capability reuse, package changes, look-alike checks, scoped rollout and withdrawal.
metadata:
  title: Item and Packaging Qualification for Robotic Picking
---

# Item and Packaging Qualification for Robotic Picking

Treat the catalog entry and the robot handling qualification as separate records. Start with one item, its actual packaging revision, location, gripper and relevant calibration. Record where the robot may grip, how it can withdraw with the item, and which independent observation verifies the picked identity.

| Change | Reuse hypothesis | First discriminating check |
| --- | --- | --- |
| New catalog ID with familiar packaging | Existing grasp and motion may transfer | Pick the intended variant among look-alikes and verify it independently. |
| Same ID with a revised wrapper or label | Geometry may transfer while sensing changes | Test glare, grip slip and code visibility after pickup. Keep both revisions identifiable. |
| Same package in a different slot | Grasp geometry may transfer while access changes | Check approach, finger opening, extraction and exit with adjacent items in place. |
| Same item and package in a new lot | Handling may be reusable under the existing scope | Confirm the incoming lot maps to the approved revision and current conditions. |

Freeze the candidate configuration for a small trial. Include a positive case, a look-alike, an unreadable ID, and a difficult allowed slot. Define the denominator before testing. Score correct physical item, completion, intervention and unresolved identity separately. If the item cannot be verified, retain its physical location and use the specified handoff. This keeps an uncertain pick from becoming a confirmed inventory movement.

Compare against the current capability before tuning a model. A blocked extraction calls for a slot, tooling or approach change. If a shared model, gripper or calibration changes, rerun affected previously qualified items as well as the new item. Bind approval to the package, site or slot class, tool and capability revision actually tested.

**Worked decision.** Two boxes share a silhouette. The picker grasps one cleanly and its readable code resolves to the other variant. Record a successful physical grasp and a failed identity check. Hold the item at its known location, reconcile the order, and investigate the mapping or selection stage. During rollback preserve committed inventory movements and reconcile any item already in hand before allowing a retry.

**Deliverable.** Return the change classification, reusable capability, affected existing items, trial evidence, and permitted operating scope. Distinguish a proposed qualification plan from supervised trials already performed. For choosing among grasp candidates on an identified object, use [Grasp Selection](../robot-grasp-selection/SKILL.md).
