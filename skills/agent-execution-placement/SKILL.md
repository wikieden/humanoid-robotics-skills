---
name: agent-execution-placement
description: Design or review how a workbench binds an agent attempt to a local process, an external service or a managed runner. Use when the same backend can run in multiple places and workspace ownership, stopping or artifact retrieval is unclear.
metadata:
  title: Verifying Agent Execution Placement
---

# Verifying Agent Execution Placement

Start with one harmless job that reads a synthetic input and produces a small result. Draw its route from the UI to the component that owns the workspace, the running process and the resulting artifact. Keep the model provider, agent backend, transport and execution location as separate choices. A remotely hosted model can serve an agent whose tools and files are entirely local.

1. For each supported placement, specify who opens the workspace, starts the attempt, reports its state, accepts cancellation and retains outputs after disconnect. Distinguish the attempt ID from the UI connection and backend conversation IDs. Define the supported combinations explicitly and reject unsupported ones before allocating work.
2. Use different fixture markers in two same-named workspaces. Have the test job read its marker and write an artifact derived from it. Resolve the artifact through the interface the client will use and compare the expected digest. An echoed path, a successful connection or a process-exit notification cannot establish which workspace supplied the data.
3. Drop only the viewer connection while the job runs, then reconnect with the same attempt ID. Check the authoritative state and recover outputs without opening another job. Cancel a separate long-running fixture and verify what the executor observed. When the backend can acknowledge a cancellation request but cannot confirm process termination, preserve that distinction.
4. Exercise a binding that the adapter cannot support, a missing artifact and a retry after a lost acknowledgment. If an attempt is deliberately moved to a new runner, assign a new attempt identity and record what workspace revision or state was transferred. The client needs to know which attempt produced the result.

**Worked case.** A read-only worker on the remote service sees the same logical workspace name as the desktop but a different marker. Both answer a status query. Only a result containing the expected marker digest and bound to the remote attempt demonstrates that the remote read path ran. A schema test that accepts this binding exercises the design only.

**Deliverable.** Provide a backend-by-placement matrix with workspace, lifecycle and artifact owners. Mark each combination as specified, schema-checked or exercised end to end, and give the fixture evidence for the highest level reached.
