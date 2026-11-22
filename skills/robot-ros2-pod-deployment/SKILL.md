---
name: robot-ros2-pod-deployment
description: Deploy or review isolated ROS 2 environments for humanoid robots using Pods. Use to map hardware ownership, reproduce build and runtime environments, verify DDS across boundaries, and test startup, replacement, and rollback without issuing motion commands.
metadata:
  title: ROS 2 Pod Deployment and Isolation
---

# ROS 2 Pod Deployment and Isolation

Identify the runtime from the artifact that actually starts the workload. A Kubernetes workload specifies a Pod template or Pod manifest. A Podman deployment may use a pod unit, pod creation command, or Kubernetes-style YAML consumed by Podman. A Compose file supplies useful migration evidence. A container image alone establishes only the packaged environment. If the launcher is unavailable, document the Pod-level contract and leave runtime-specific commands and restart semantics open. [Kubernetes Pods](https://kubernetes.io/docs/concepts/workloads/pods/) · [Podman pod creation](https://docs.podman.io/en/latest/markdown/podman-pod-create.1.html)

## Reconstruct the environment

Record the target board architecture, host kernel and device drivers, accelerator runtime, ROS distribution, RMW implementation, workspace revisions, dependency sources, and selected image digest for the target architecture. Build from the declared underlay and pinned overlays in a clean environment. Inspect the resolved package prefix and generated interfaces in the runtime image. A successful workstation build leaves board drivers and target ABI compatibility untested.

Make a row per Pod: environment and robot assignment, contained processes, restart owner, hardware devices, network and IPC namespaces, writable volumes, host dependencies, resource budgets, and motion authority. For development, simulation, and hardware, compare the effective settings as well as the manifest defaults.

| Boundary | What to check on the target |
| --- | --- |
| Devices and privileges | Assign the actuator bus to its intended writer. List camera, GPU, serial, and fieldbus access separately. Compare the actual device mappings, groups, capabilities, host mounts, and privileged flags to the manifest. Keep replay and simulation environments off physical actuator interfaces. |
| ROS and DDS traffic | Record namespaces, domain ID, RMW profile, participating interfaces, discovery configuration, and clock mode. Domain IDs help separate discovery; access to the network and devices needs its own controls. Test intended cross-Pod traffic and unintended cross-environment visibility using harmless synthetic topics. |
| Files and configuration | Identify the owners and versions of calibration, robot description, parameters, controller configuration, and recorded data. Record what is image content, injected configuration, temporary storage, or persistent state. Test which state survives a container restart versus Pod replacement. |
| Compute and failure containment | Verify CPU, memory, accelerator access, shared memory, and scheduling under expected sensor load. Identify whether restarting a sidecar, controller container, or entire Pod also interrupts balance or the only state estimator. Record the lower-level fallback and who can authorize recovery. |

## Bring up without motion

1. Start in the documented motion-inhibited mode. Confirm that homing, controller activation, retained commands, and hardware writers cannot start motion as a launch side effect. If that mode has no supporting evidence, use disconnected hardware interfaces or simulation for the first check.
2. Inspect the effective workload, selected image digest, host/device assignment, configuration mounts, restart counts, and logs. In each relevant container, check the ROS graph and resolved packages using the deployed environment. Useful read-only probes include `ros2 pkg prefix <package>`, `ros2 topic info --verbose <topic>`, and, where ros2_control is used, `ros2 control list_controllers`.
3. Verify the data path from both sides of an intended Pod boundary with a synthetic sample or passive observation. Record publisher, subscriber, QoS, message arrival, source timestamp and sample age. Check joint state, required transforms, camera timestamps, and the selected clock where applicable. Discovery alone does not establish sample delivery. Run the negative control from the simulation or development environment and record whether the synthetic sample is visible there.
4. Define what startup, readiness, and liveness mean for this robot. A process responding to a probe can still have stale joint feedback or a missing calibration. Keep service readiness separate from permission to move. In Kubernetes, a failing readiness probe normally removes the endpoint from matching Services; ROS peers can still communicate directly over DDS. Test the final command gate in simulation. [Kubernetes probe semantics](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)

## Replace and roll back

In an isolated environment, compare a single-container restart with a complete Pod replacement. Observe which processes stayed alive, whether discovery recovered, whether old goals were discarded, whether hardware ownership remained exclusive, and whether the newly started controller waited for fresh feedback. Include a delayed action from the old instance and verify rejection using a simulated actuator. For an actuator-owning workload, inspect whether the rollout strategy allows old and new instances to overlap on the same bus.

Pin the previous image digest, configuration, calibration, and state-schema compatibility as a rollback set. Rehearse restoration in the isolated environment, then rerun the no-motion checks. A release proposal should name the robot, operator, rollback trigger, and supporting evidence before any live change.

**Deliverable.** Return the manifest revision and image digests, Pod-to-device and Pod-to-node mapping, isolation exceptions, no-motion results, and restart and rollback records. Label build, simulated deployment, target-board read-only checks, and controlled physical trials separately. For questions about where ROS nodes and control authority belong, use [Humanoid ROS 2 Architecture Design and Review](../robot-ros2-architecture/SKILL.md).
