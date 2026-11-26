---
name: robot-sim-asset-validation
description: Validate a converted robot asset before simulated experiments. Use for URDF, SDF or MJCF import, CAD-to-simulation handoff, invalid inertial properties, missing collision or actuator bindings, and changed kinematics or dynamics after conversion.
metadata:
  title: Robot Asset Import and Physics Validation
---

# Robot Asset Import and Physics Validation

Start with the source robot description, dependent meshes, importer version and options, and the target simulator. Expand macros and resolve resources with the intended loader. Preserve the source and emit a separate converted artifact.

1. Check what loads. Record missing, substituted or rescaled meshes. Inspect joint parent and child links, root or floating-base convention, joint axes, limits, mimic relationships and the intended tool frame. Record simulator-specific omissions such as transmissions or plugin configuration. Compare values by link and joint identity, with an explicit mapping when the importer merges fixed bodies.
2. Check physical quantities before and after import. Compare mass and centre of mass in a common frame at agreed configurations. Compare inertias about the same point and expressed in the same basis. Rotate tensors when changing axes and apply the parallel-axis theorem when changing the reference point. For a nondegenerate rigid body, the principal moments should be positive and each should be at most the sum of the other two, within a tolerance justified by the units and source precision. Inspect effective compiler settings that infer inertia from geometry, clamp mass, or balance moments. [MuJoCo compiler and inertial settings](https://mujoco.readthedocs.io/en/stable/XMLreference.html#compiler)
3. Validate behaviour after native loading. Compare FK at neutral and with each relevant joint moved individually, using known tool positions and expected axis directions. Command one actuator at a time at bounded effort in simulation and check the measured direction, affected degree of freedom and limit response. Exercise a known blocking contact and a known clear pose with the collision geometry. Visual similarity is supporting evidence for the render. Use the physics probes for dynamics and collision acceptance.
4. Preserve a positive and a negative control for the tested contract, such as a correct link and a tenfold mesh scale error, or a correct actuator and an intentionally reversed gear sign. Record which import warnings were observed and which differences were intentional.

**Offline example.** Both diagonal tensors below are positive definite, but only one has principal moments consistent with a rigid-body mass distribution. The values use kg·m² and the same inertial frame.

```python
def valid_principal_moments(values, tolerance=1e-12):
    first, second, third = sorted(values)
    return first > 0 and third <= first + second + tolerance


assert valid_principal_moments([0.002, 0.003, 0.004])
assert not valid_principal_moments([0.002, 0.003, 0.006])
```

With MuJoCo 3.17.0, a one-body MJCF with these explicit inertias loads the first tensor unchanged. The compiler rejects the second tensor with `balanceinertia="false"` and changes all three moments to approximately `0.003667 kg·m²` with `balanceinertia="true"`. Inspect the compiled inertia when this setting is enabled.

**Deliverable.** Return source and converted revisions, effective importer settings, mapping and expected differences, a simulator load receipt and the kinematic, actuator and collision probe results. Note the reference data supporting each physical check. For end-to-end environment setup, use [Simulation Environment Construction (optional)](../robot-sim-environment-build/SKILL.md).
