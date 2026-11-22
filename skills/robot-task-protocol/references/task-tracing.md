# Cloud-to-Robot Task Tracing

Select one task and define its user-visible outcome, such as arriving at a waypoint and finishing the narration. Collect the device identifier, time window, map and waypoint versions, session ID, service version, and available task IDs. Start with existing records because replay can create a new device task.

1. Check the target device and task parameters in the task service. For a voice or text request, use the session ID to locate the service version, authorization decision, and tool calls. For a directly dispatched task, start at the acceptance record.
2. Map the request ID to the task ID and ROS 2 action goal ID. In the device logs, trace receipt, goal resolution, action feedback and result, and safety supervision events. Identify any missing ID mapping. Treat records linked only by timestamp proximity as tentative matches.
3. Align acceptance, start, navigation result, device acknowledgment, audio acknowledgment, and the state shown to the user. Identify the publisher, subscriber, and clock source for each event. If the cloud accepted a task and the device never acknowledged it, check delivery and device assignment. If navigation succeeded but narration never played, inspect the narration trigger and playback feedback.
4. Record whether the evidence comes from replay with a synthetic identity, a real device session, or the observed physical outcome. To confirm the running version, link the service and device artifacts to deployment records for that environment. Verify arrival from goal feedback and narration completion from the end-of-playback event.

**Deliverable.** Produce a timeline showing the last confirmed state, the first missing or contradictory acknowledgment, the associated log records, and what the user observed. For retries or duplicate messages, identify the associated task and terminal state for each attempt.
