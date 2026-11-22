# Headless Support Check

Run this Python example with MuJoCo and NumPy. A free sphere starts above a horizontal plane. Trial A lets it fall. In trial B gravity is zero and the sphere stays suspended. Both trials finish nearly motionless. The floor contact and upward load distinguish them.

```python
import mujoco
import numpy as np


def run_trial(gravity_z):
    xml = f"""
    <mujoco>
      <option timestep="0.002" gravity="0 0 {gravity_z}"/>
      <worldbody>
        <geom name="floor" type="plane" size="1 1 0.1"/>
        <body pos="0 0 0.20">
          <freejoint/>
          <geom name="object" type="sphere" size="0.025" mass="0.10"/>
        </body>
      </worldbody>
    </mujoco>"""
    model = mujoco.MjModel.from_xml_string(xml)
    data = mujoco.MjData(model)
    pair = {model.geom("floor").id, model.geom("object").id}
    window = []
    for step in range(500):
        mujoco.mj_step(model, data)
        if step < 450:
            continue
        # Refresh kinematics and contacts for the integrated state.
        mujoco.mj_forward(model, data)
        load = 0.0
        for i in range(data.ncon):
            contact = data.contact[i]
            if {contact.geom1, contact.geom2} == pair:
                wrench = np.zeros(6)
                mujoco.mj_contactForce(model, data, i, wrench)
                load += wrench[0]  # Normal force on this horizontal support.
        window.append((abs(float(data.qvel[2])), load))
    peak_speed = max(speed for speed, _ in window)
    min_load = min(load for _, load in window)
    # Fixture-specific thresholds for a 0.10 kg sphere on a horizontal plane.
    supported = peak_speed < 0.001 and min_load > 0.5
    return data.qpos[2], peak_speed, min_load, supported


for gravity, expected in [(-9.81, True), (0.0, False)]:
    height, speed, load, verdict = run_trial(gravity)
    print(f"g={gravity:.2f} z={height:.4f} max_vz={speed:.4f} "
          f"min_normal_N={load:.3f} supported={verdict}")
    assert speed < 0.001 and verdict == expected
```

Output observed with MuJoCo 3.17.0:

```text
g=-9.81 z=0.0246 max_vz=0.0000 min_normal_N=0.981 supported=True
g=0.00 z=0.2000 max_vz=0.0000 min_normal_N=0.000 supported=False
```

Height is the sphere center in meters. The last 50 simulation steps cover 0.10 seconds. For a different support orientation, resolve the force against gravity and check the intended contact pairs. This example validates the support predicate for a single body. Gripper release and full placement require separate tests.
