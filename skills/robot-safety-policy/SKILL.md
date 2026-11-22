---
name: robot-safety-policy
description: Design or review physical safety measures for a robot application. Use for motion authorization, human access, operating limits, loss of feedback or control, protective and emergency stops, restart behavior, and evidence needed for hardware acceptance.
metadata:
  title: Robot Safety Policy and Safeguard Verification
---

# Robot Safety Policy and Safeguard Verification

Start with one operation, such as a mobile manipulator carrying a load past a shared aisle. Identify who can enter the area, what moves or stores energy, who controls motion, and what could still move or fall after a stop. Record the operating mode, tool, payload, configuration, and intended use. Review setup, teaching, fault recovery, and servicing alongside routine operation.

## Select safeguards for the hazard

| Situation | Design or review decision | Evidence to request |
| --- | --- | --- |
| A person can reach a pinch point, moving tool, or the swept volume of the arm and load | First consider eliminating the exposure through layout, tooling, or task changes. Identify guards, interlocks, or protective sensing appropriate to the remaining exposure and operating mode. Include the base, arm, tool, and payload in the envelope. | Layout and access paths, blind spots, stopping envelope, and the applicable safeguarding validation record. |
| Multiple sources can command motion, including a learned policy, teleoperator, or recovery routine | At the last controllable point before actuation, enforce a single command owner, current mode, valid command generation, fresh required feedback, and the configured envelope. Check a queued action again at dispatch. At takeover, invalidate outstanding commands from the previous owner. | A trace joining proposal, authorization, dispatch, and drive feedback. Include a late reply from the previous owner and an action already buffered downstream. |
| Perception goes stale, the host disconnects, or a controller restarts | Identify the component still able to act when the failed component is unavailable. Specify how it detects the fault, inhibits new motion, handles motion already in progress, and establishes the hazard-specific safe state. Treat unavailable required feedback as unknown. | A recorded or simulated fault timeline covering the last fresh sample, detection, local response, and independently observed outcome. |
| A vertical axis or gripper carries a load, or the base is moving on a slope | Determine how the load is supported during deceleration, loss of power, and recovery. An immediate torque cut or gripper release can introduce a drop or rollaway hazard. Use the machine-specific braking and load-retention design. | Brake or restraint specifications and test evidence for the actual payload, orientation, tooling, and surface. |

Trace each safety function from its sensor or initiating device through the logic to the final element, such as a drive or brake. Identify shared failure points, including shared power, controller, or communications. Record which functions have documented safety ratings and what the integrated installation has actually validated. Application checks provide additional protection within that boundary. For industrial robot applications, task-specific hazard assessment and safeguarding guidance is available in the [OSHA Technical Manual](https://www.osha.gov/otm/section-4-safety-hazards/chapter-4).

## Define stop and restart behavior

1. **Motion admission.** Write down which observations and protective functions must be healthy for this mode. Identify the source of each speed, force, workspace, separation, and freshness limit that applies. Use the machine documentation and application risk assessment for thresholds. On initialization or ambiguous ownership, keep motion inhibited until those conditions can be established.
2. **Stop response.** Distinguish a routine task cancel, a protective stop triggered by a safeguard, and an operator-initiated emergency stop. For each, specify the trigger, affected axes and peripherals, controller response, load behavior, and expected final state. Keep the emergency-stop function available independently of the task application. For servicing or entry that requires hazardous-energy isolation, use the site's energy-control procedure. A stopped axis may still store energy.
3. **Recovery.** Record how the initiating condition is cleared, who may reset the function, and how a new command owner is established. Releasing or resetting an emergency stop must not initiate motion. For protective stops, verify the configured restart behavior against the application risk assessment, including possible occupancy outside sensor coverage. On reconnect, discard pre-stop commands and in-flight policy responses. Verify the effect at the drive as well as in the host queue.
4. **Stop measurement.** Put hazard onset, detection, stop request, drive response, observed standstill, and any subsequent motion on a common timebase. Report detection delay and total stopping time separately. Measure distance along the hazardous motion, including the tool or load where relevant. Record initial speed, payload, pose, surface, sampling uncertainty, and the observation interval at standstill. A command acknowledgment establishes receipt only. Missing independent feedback leaves the physical outcome unverified.

## Verify the policy and report its scope

Exercise stale feedback, interrupted communications, a queued command arriving after a stop, reset without a new start, and a valid new command after re-arming. Start with software-only fault injection or recorded traces. Use the [offline stop and restart cases](references/stop-restart-cases.md) to check how the evidence is interpreted. For a physical test, use the authorized procedure for the actual installation, the designated test personnel, a controlled exclusion area, and the agreed abort conditions. Keep people out of hazardous motion paths.

**Deliverable.** For each hazard give the exposed person or asset, trigger, safeguard, enforcing component, safe state, reset and restart conditions, acceptance criterion and its source, and observed evidence. Identify residual risks and the owner of each open item. Distinguish design review, software tests, simulation, and measured hardware behavior. Mark a missing limit or physical measurement as an open acceptance item.
