# Headless Scene Bring-Up and a Paired Range-Stop Test

A one-axis carriage must stop 0.15–0.25 m from a wall without touching it. The baseline uses odometry and a nominal wall location. The candidate uses a forward range sensor. Each trial starts from rest and lasts four simulated seconds. The scorer measures final clearance from the fixture dimensions and checks contacts throughout the trial. A stationary carriage at the start would fail the clearance test.

Save the Python block as `range_stop.py`. In a Python environment with the `mujoco` package installed, run `python range_stop.py`. The fixture embeds its scene and uses CPU physics without a display or external assets. The rangefinder points along its site's local positive Z axis, aligned here with world positive X. [MuJoCo sensor reference](https://mujoco.readthedocs.io/en/stable/XMLreference.html#sensor-rangefinder)

```python
import math
import mujoco


def build(wall_face, collisions=True):
    mask = int(collisions)
    return mujoco.MjModel.from_xml_string(f"""
    <mujoco>
      <option timestep="0.005" gravity="0 0 0"/>
      <worldbody>
        <geom name="wall" type="box" pos="{wall_face + 0.05} 0 0"
              size="0.05 0.5 0.5" contype="{mask}" conaffinity="{mask}"/>
        <body name="carriage">
          <joint name="slide" type="slide" axis="1 0 0"/>
          <geom name="nose" type="box" size="0.1 0.1 0.1" mass="1"/>
          <site name="front" pos="0.1 0 0" zaxis="1 0 0"/>
        </body>
      </worldbody>
      <actuator><velocity joint="slide" kv="20"/></actuator>
      <sensor><rangefinder site="front"/></sensor>
    </mujoco>""")


def run(wall_face, controller, collisions=True):
    model = build(wall_face, collisions)
    data = mujoco.MjData(model)
    mujoco.mj_forward(model, data)
    initial_range = data.sensordata[0]
    assert math.isclose(initial_range, wall_face - 0.1, abs_tol=1e-8)
    touched = False
    for _ in range(800):
        mujoco.mj_step1(model, data)
        touched |= data.ncon > 0  # The wall and carriage are the only two geoms.
        data.ctrl[0] = controller(data.qpos[0], data.sensordata[0])
        mujoco.mj_step2(model, data)
    mujoco.mj_forward(model, data)
    touched |= data.ncon > 0
    clearance = wall_face - (data.qpos[0] + 0.1)
    stopped = abs(data.qvel[0]) < 0.01
    passed = 0.15 <= clearance <= 0.25 and stopped and not touched
    return float(initial_range), float(clearance), touched, passed


def drive_through(position, distance):
    return 0.35


def nominal_map(position, distance):
    return 0.35 if 1.0 - (position + 0.1) > 0.20 else 0.0


def range_feedback(position, distance):
    return 0.35 if distance > 0.20 else 0.0


for collisions in (True, False):
    initial, gap, touched, _ = run(0.75, drive_through, collisions)
    print(f"probe collisions={collisions} range={initial:.3f} gap={gap:.3f} touched={touched}")
    assert touched == collisions
    if collisions:
        assert abs(gap) < 0.01
    else:
        assert gap < -0.1  # The carriage crossed the nominal front face.

for wall_face in (1.0, 0.75):
    for controller in (nominal_map, range_feedback):
        _, gap, touched, passed = run(wall_face, controller)
        print(f"wall={wall_face:.2f} {controller.__name__} gap={gap:.3f} "
              f"touched={touched} passed={passed}")
        assert passed == (wall_face == 1.0 or controller is range_feedback)
```

Observed headless output with MuJoCo 3.17.0:

```text
probe collisions=True range=0.650 gap=-0.000 touched=True
probe collisions=False range=0.650 gap=-0.734 touched=False
wall=1.00 nominal_map gap=0.184 touched=False passed=True
wall=1.00 range_feedback gap=0.184 touched=False passed=True
wall=0.75 nominal_map gap=-0.000 touched=True passed=False
wall=0.75 range_feedback gap=0.183 touched=False passed=True
```

The probe isolates a scene-authoring failure common with imported visuals. The range sensor can see the obstacle even when the solver lets the carriage pass through it. Use only the intact scene for comparing controllers. The two wall positions exercise one controlled layout change. This fixture validates the integration and scoring procedure for a one-axis model. A mobile robot adds braking dynamics, a footprint, surface contact and sensor uncertainty that require their own measurements.
