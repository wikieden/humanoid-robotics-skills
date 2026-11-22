---
name: robot-teleop-session
description: Review how a robot platform pairs an operator with a device, preserves exclusive control through reconnects, processes stop receipts, and transfers authority between teleoperation sessions.
metadata:
  title: Teleoperation Session Ownership and Handoff
---

# Teleoperation Session Ownership and Handoff

Model operator presence, session reservation, and authority to actuate separately. Identify the coordinator, the endpoint that accepts commands, and the transport carrying control and video. A coordinator outage can leave a direct operator-to-robot data path alive.

1. Trace admission for both endpoints. Check that competing reservations for the same robot cannot both succeed, including during teardown. Identify the evidence for ownership at the robot. A reservation or a live video stream establishes only its own layer.
2. For reconnects, reconcile device and operator identity, session generation, and the last acknowledged state. Duplicate pairing requests should reuse the intended session. Re-registration during an active session must preserve the reservation and must not start a second execution stack.
3. Follow disconnect from the requested stop to the robot response and session closure. If the platform frees a reservation after a timeout, record the physical stop as unconfirmed until independently observed. Before a new operator can command the robot, verify that the old authority has been invalidated at the final command consumer. Check what local supervision does during a network partition.
4. Use a simulated actuator to deliver an old-generation command after the handoff and a fresh command from the new holder. Record which command the final consumer accepted, rather than inferring authority from the operator UI. For reversed controls after a valid handoff, continue with [Dual-Arm Teleoperation](../robot-teleop-bringup/SKILL.md).

**Offline case.** Operator A loses the coordinator while the robot's control channel remains open. Operator B requests the robot during teardown. A delayed command from A arrives after B has legitimately acquired it. Pass if B cannot acquire a conflicting active reservation, and after handoff the actuator rejects A's old command. If a stop acknowledgment was lost, report the stop outcome separately.

**Deliverable.** Draw the reservation and actuation timelines for both operators. Record the handoff condition, the rejection evidence for stale commands, and any interval of unknown motion authority.
