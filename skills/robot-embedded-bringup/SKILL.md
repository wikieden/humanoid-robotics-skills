---
name: robot-embedded-bringup
description: Trace failures across Linux services, IPC, and the chassis MCU during board bring-up, service startup, command handling, or OTA update verification.
metadata:
  title: Embedded Linux and MCU Bring-Up
---

# Embedded Linux and MCU Bring-Up

Start with one failed request and find the last component that acknowledged it. Collect the robot model, board revision, BSP, application and MCU versions, boot logs, and failure window. If only source code is available, trace the interfaces and identify the logs needed to test that trace.

1. Use the board's build manifest to locate the Linux service and chassis firmware entry points. Compare submodule revisions and startup configuration to verify that the drivers, services, and protocols belong to the same build.
2. Use device handles and startup configuration to find the process that owns the camera, audio device, or chassis serial port. Check its readiness, restart history, IPC subscriptions, and protocol versions at both ends.
3. Align the timestamps for the request, request/reply acknowledgment, UART traffic, MCU state, and published completion event. If the MCU reached its terminal state but the caller timed out, check the event topic, payload fields, and when the subscriber connected. If MCU logs are missing, leave the fault localized to the interval between serial transmission and MCU processing.
4. For an update, identify the payload as a system package, MCU firmware, or model asset. Check download integrity, evidence of the write or load, the version active after restart, and recovery records for failed attempts. Flash a board or test physical motion only within the user's authorization and the appropriate board procedure.

**Deliverable.** Provide a version table and a failure timeline. For each hop, record the expected signal, observed value, and log location. Identify the next check that distinguishes the remaining causes. List the evidence for the build, on-board startup, and whole-robot design verification testing (DVT) separately.
