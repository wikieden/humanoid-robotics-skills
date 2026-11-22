---
name: robot-sim-state-restore
description: Verify that two robot simulation trials can branch from the same in-progress state. Use when a recovery policy, planner or controller is compared after contact, partial execution or an interruption.
metadata:
  title: Verifying a Simulation Snapshot Before Branching
---

# Verifying a Simulation Snapshot Before Branching

Choose the exact branch boundary. “After grasp” is ambiguous if one trial sampled the sensors before the final physics step and another sampled after it. Record the physics step and substep, observation phase, controller update and next action index. Preserve an uninterrupted reference continuation starting at that boundary.

1. Inventory state by owner. In addition to body poses and velocities, check actuator state, solver history where exposed, constraints, random generators, task timers, planner state, policy history and any partly consumed action chunk. Identify cached contact or sensor readings from the previous step. Record what the engine serializes, what the application restores, and what can only be reconstructed by replaying the prefix.
2. Restore into the intended execution mode and inspect it before applying a new action. Compare named physical variables, controller and policy slots, and the observation the policy actually receives. Hash serialized bytes for identity. Check regenerated values separately with tolerances and units. Calling an update or observation routine can advance a sensor or alter a cache, so match its call sequence to the reference.
3. Run a no-change branch first. Feed the same recorded inputs, advance the same substeps, and identify the first difference in command, contact pair, planner decision or body state. Repeat restoration to expose dependence on branch order. If the active policy will replan, also compare a closed-loop no-change branch with the reference. Recorded-action replay alone exercises only the downstream path.
4. Once reference continuations agree over the comparison interval, change one recovery decision. If hidden state prevents agreement, shorten the claim to the verified interval or reconstruct the branch by replaying from reset. Document the residual and competing explanation.

**Counterexample.** Two states share a pose and the same cached commands. Restoring the wrong cursor changes the very next transition.

```python
commands = (2, -1)

def step(state):
    position, cursor = state
    return position + commands[cursor], cursor + 1

anchor = step((6, 0))
reference = step(anchor)
pose_only_restore = (anchor[0], 0)
assert pose_only_restore[0] == anchor[0]
assert step(pose_only_restore) != reference
assert step((anchor[0], anchor[1])) == reference == (7, 2)
```

**Deliverable.** Return the branch boundary, state coverage, no-change comparison, first divergent step and the candidate outcome that comparison supports. For engine-owned integration state, consult the [MuJoCo simulation guide](https://mujoco.readthedocs.io/en/stable/programming/simulation.html) when applicable.
