# Algorithm and method checks

Eight specialist decisions selected from the 53-workflow directory received a source and counterexample review on 2026-11-22. The table separates a failed executable example from improvements to previously underspecified instructions. Each row describes the setting in which the result holds.

| Specialist | Decision and reproducible observation | Basis |
| --- | --- | --- |
| Motion retargeting | The previous two-link solver rejected the fully extended 0.80 m leg. Its computed cosine was 1.0000000000000004. The corrected solver accepts both annulus boundaries, reconstructs the foot by forward kinematics, and rejects targets 1 μm beyond each boundary. The tolerance covers floating-point roundoff in this fixture. Joint limits and dynamics require separate checks. | [Two-link IK derivation](https://motion.cs.illinois.edu/RoboticSystems/InverseKinematics.html) |
| Trajectory retiming | In Jazzy spline mode the presence of acceleration fields changes the interpolant. A 1 rad move in 1 s has peak speed 1.5 rad/s with the cubic and 1.875 rad/s with the zero-end-acceleration quintic. Only the cubic satisfies a 1.6 rad/s limit. | [Jazzy interpolation contract](https://control.ros.org/jazzy/doc/ros2_controllers/joint_trajectory_controller/doc/trajectory.html) |
| Navigation planning | An admissible heuristic can violate edge consistency. On the four-node fixture, permanently closing A returns cost 6. Reopening it returns 5, the Dijkstra optimum on the same graph. This applies to optimal A* graph search with nonnegative edges. | [Original A* reopening analysis](https://ijcai.org/proceedings/2009/111) |
| RGB-D pose | Treating a radial range of 1.25 m as optical Z at the specified off-axis pixel adds 0.25 m of Z error. The wrong point reprojects to the same pixel. Identify the stream's distance convention and compare an independent off-axis measurement. | [REP 118](https://github.com/ros-infrastructure/rep/blob/master/rep-0118.rst) · [CameraInfo](https://github.com/ros2/common_interfaces/blob/jazzy/sensor_msgs/msg/CameraInfo.msg) |
| Sensor calibration | Relative rotations about z give translation-system rank 2. The fixture cannot see a 10 cm shift along z. Adding a rotation about x gives rank 3. This tests translational observability conditional on rotation. It gives no physical calibration tolerance. | [OpenCV hand-eye equations and frame directions](https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html) |
| Episode audit | Resolving aliases and dropping identical exports leaves three different windows from four exports. Splitting two sibling windows at random can share two raw frames across folds. Grouping by source before windowing retains the distinct clips with zero shared frames across the chosen splits. Group by the larger unit for a session- or layout-level claim. | [Grouped cross-validation contract](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html) |
| Policy training | Replacing future observations changes a centered feature from 6 to 10. Both actions clip to 1. Inspect the request built from raw data as well as the action. For a thresholded feature, include replacements on both sides of the threshold. Trace feature availability at decision time. The falsification procedure below is a local engineering control. | [LaWAM inference and supervision](https://arxiv.org/html/2606.15768v2) |
| Policy evaluation | Identical margins of 8/20 and 14/20 give the same +30 percentage points. Changing the paired ledger yields exact two-sided p-values 0.03125 or 0.109375. Replications within one layout do not establish between-layout uncertainty. | [Exact McNemar test](https://www.statsmodels.org/stable/generated/statsmodels.stats.contingency_tables.mcnemar.html) · [Resampling clusters](https://www.stata.com/manuals/rbootstrap.pdf) |

## Run the eight controls

From the checkout root, supply this Markdown file as the last argument. The checks use Python 3.9+ and NumPy. The reach test runs the retargeting example shipped with the checkout. The other tests independently reconstruct the small fixtures. The complete example suite also uses MuJoCo for its two physics examples.

```sh
python3 -c 'import pathlib,re,sys; text=pathlib.Path(sys.argv[1]).read_text(); code=re.search(r"^`{3}python\n(.*?)^`{3}",text,re.M|re.S)[1]; exec(code)' tests/robot-dev-skills/method-checks.md
```

```python
from contextlib import redirect_stdout
from fractions import Fraction
from heapq import heappop, heappush
from io import StringIO
from itertools import product
from pathlib import Path
import math
import re
import numpy as np


def check_reach():
    path = Path("skills/robot-motion-retargeting/references/stance-foot-check.md")
    code = re.search(r"^`{3}python\n(.*?)^`{3}", path.read_text(), re.M | re.S)[1]
    ns = {}
    with redirect_stdout(StringIO()):
        exec(code, ns)
    lengths = ns["TARGET"]
    inner, outer = abs(lengths[0] - lengths[1]), sum(lengths)
    result = []
    for radius in (inner, outer, inner - 1e-6, outer + 1e-6):
        root = (0, radius)
        angles = ns["solve_leg"](root, lengths, (0, 0))
        if angles is not None:
            assert math.dist(ns["foot_fk"](root, lengths, *angles), (0, 0)) < 1e-9
        result.append(angles is not None)
    assert result == [True, True, False, False]
    return result


def check_retiming():
    # Recover each polynomial from endpoint constraints, independently of the skill's formulas.
    from numpy.polynomial import Polynomial
    peaks = []
    for order in (3, 5):
        basis = [Polynomial.basis(i) for i in range(order + 1)]
        constraints = [(d, t) for d in range((order + 1) // 2) for t in (0, 1)]
        matrix = [[term.deriv(d)(t) for term in basis] for d, t in constraints]
        targets = [1 if (d, t) == (0, 1) else 0 for d, t in constraints]
        curve = Polynomial(np.linalg.solve(matrix, targets))
        critical = [r.real for r in curve.deriv(2).roots() if abs(r.imag) < 1e-8 and 0 < r.real < 1]
        peaks.append(max(abs(curve.deriv()(t)) for t in [0, 1, *critical]))
    assert np.allclose(peaks, [1.5, 1.875])
    return [round(float(x), 3) for x in peaks]


def search(heuristic, reopen):
    edges = {"S": [("A", 3), ("B", 1)], "A": [("G", 3)], "B": [("A", 1)], "G": []}
    best, closed = {"S": 0}, set()
    queue = [(heuristic["S"], 0, "S")]
    while queue:
        _, cost, node = heappop(queue)
        if cost != best[node]:
            continue
        if node == "G":
            return cost
        closed.add(node)
        for target, weight in edges[node]:
            candidate = cost + weight
            if target in closed and not reopen:
                continue
            if candidate < best.get(target, math.inf):
                best[target] = candidate
                heappush(queue, (candidate + heuristic[target], candidate, target))
    raise AssertionError("Goal unreachable in the fixture")


def check_search():
    h = dict.fromkeys("SABG", 0)
    oracle = search(h, False)
    h["B"] = 4
    costs = (search(h, False), search(h, True), oracle)
    assert costs == (6, 5, 5)
    return costs


def check_depth():
    ray = np.array([0.75, 0, 1.0])
    correct = ray * (1.25 / np.linalg.norm(ray))
    wrong = ray * 1.25
    assert np.allclose(correct / correct[2], wrong / wrong[2])
    assert np.isclose(np.linalg.norm(correct), 1.25)
    assert np.isclose(wrong[2] - correct[2], 0.25)
    return correct.tolist(), wrong.tolist()


def check_hand_eye():
    identity = np.eye(3)
    rz = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
    rx = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]])
    yaw = np.vstack([rz - identity, rz @ rz - identity])
    mixed = np.vstack([yaw, rx - identity])
    offset = np.array([0.0, 0.0, 0.1])
    ranks = [int(np.linalg.matrix_rank(a)) for a in (yaw, mixed)]
    assert ranks == [2, 3] and np.allclose(yaw @ offset, 0)
    assert np.linalg.norm(mixed @ offset) > 0.1
    return ranks


def check_windows():
    # A copied raw file has the same identity and labels in this fixture.
    source = {"take": "A", "copy": "A", "second": "B"}
    exports = [("take", 0, 4), ("copy", 0, 4), ("take", 2, 6), ("second", 0, 4)]
    unique = sorted({(source[name], start, stop) for name, start, stop in exports})
    def frames(rows):
        return {(group, idx) for group, start, stop in rows for idx in range(start, stop)}
    first, sibling, second = unique
    leaked = frames([first]) & frames([sibling])
    assert len(unique) == 3 and len(leaked) == 2
    assert frames([first, sibling]).isdisjoint(frames([second]))
    return len(unique), len(leaked), 0


def check_future():
    # A centered feature cached before truncation can carry the next observation.
    def replay(raw, centered):
        t = 1
        feature = np.mean(raw[t-1:t+2] if centered else raw[t-1:t+1])
        request = (raw[t], float(feature))
        action = float(np.clip(feature, -1., 1.))
        return request, action
    first, second = [4, 6, 8], [4, 6, 20]
    causal = replay(first, False), replay(second, False)
    leaky = replay(first, True), replay(second, True)
    assert causal[0] == causal[1] and leaky[0][0] != leaky[1][0]
    assert leaky[0][1] == leaky[1][1]  # Action clipping conceals leakage.
    flags = [int(value > 120) for value in (162, 170, 100)]
    assert flags == [1, 1, 0]  # Only the second replacement reveals the dependency.
    return [request[1] for request, _ in leaky], [a for _, a in leaky], flags


def check_pairs():
    results = []
    for both, gained, lost, neither in [(8, 6, 0, 6), (6, 8, 2, 4)]:
        n = both + gained + lost + neither
        assert n == 20 and (both + lost, both + gained) == (8, 14)
        # Enumerate all equally likely directions under the conditional null.
        flips = list(product((0, 1), repeat=gained + lost))
        extreme = sum(abs(2 * sum(f) - len(f)) >= abs(gained - lost) for f in flips)
        results.append((Fraction(gained - lost, n), Fraction(extreme, len(flips))))
    assert results == [(Fraction(3, 10), Fraction(1, 32)), (Fraction(3, 10), Fraction(7, 64))]
    return [(float(change), float(p)) for change, p in results]


for check in (check_reach, check_retiming, check_search, check_depth, check_hand_eye,
              check_windows, check_future, check_pairs):
    print(check.__name__, check())
```

## Observed output

Python 3.12.13 and NumPy 2.5.4 produced the following results. A separate run executed all 27 Python examples in the installable skills, including the two MuJoCo 3.17.0 physics examples. All 54 package headers and 49 relative Markdown links passed validation. The directory and the routing case matrix contained the same 53 specialists. These checks cover specified offline decisions and fixtures. Deployment measurements and physical robot performance require their own evidence.

```text
check_reach [True, True, False, False]
check_retiming [1.5, 1.875]
check_search (6, 5, 5)
check_depth ([0.75, 0.0, 1.0], [0.9375, 0.0, 1.25])
check_hand_eye [2, 3]
check_windows (3, 2, 0)
check_future ([6.0, 10.0], [1.0, 1.0], [1, 1, 0])
check_pairs [(0.3, 0.03125), (0.3, 0.109375)]
```

## Blind reader check

Two fresh Codex sessions received the same three questions, the same instructions to read the three corresponding guides and the same model and reasoning settings. One had the previous public specialist texts (`eb999e1`), the other had the revised texts. Neither prompt identified the version. Each session answered the three questions together. The checks scored the engineering decisions and numerical results.

| Previously unseen input | Required decision | Previous | Revised |
| --- | --- | --- | --- |
| A 0.72 rad move in 0.6 s, zero endpoint velocities, acceleration omitted versus supplied as zero, limit 2 rad/s | Accept the cubic at 1.80 rad/s and reject the quintic at 2.25 rad/s. | Pass | Pass |
| 16 independent pairs with ledgers (5,5,0,6) and (3,7,2,4), plus a single-layout alternative | Same +31.25 percentage points, exact two-sided p-values 0.0625 and 0.1796875. Sixteen repetitions of one layout support a within-layout statement. | Pass | Pass |
| A cached feature uses brightness at the next frame with threshold 120. Changing it from 162 to 170 leaves both inputs and clipped actions unchanged. | Reject the future-derived input. Cross the threshold, regenerate the cache and inspect the bit, raw action and clipped action. | Pass | Pass |

The observed reader score was 3/3 for each version. The confirmed before/after behavior change is the two-link solver's reach decision. This small reader comparison establishes no increase in overall model answer accuracy.
