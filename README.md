# Humanoid Robotics Skills

English · [简体中文](README.zh-CN.md)

This collection contains 60 English-language agent skills. One entry skill routes to 59 specialists. Of those specialists, 52 cover humanoid and mobile manipulation robotics. The other seven cover agent evaluation and execution, technical learning, interactive applications, offline archives, skill distribution and technical publishing. Each skill is a Markdown workflow for a specific engineering decision, from tracing a reversed gripper command to deciding whether a new robot policy should replace its baseline.

## Use the collection through one entry skill

From the repository root, link the entry skill to the Codex and Claude Code user skill directories. Keep the checkout at a stable path. Both hosts can then read individual specialists and their resources from the same local copy, including offline.

```sh
(
  set -e
  entry="$PWD/skills/robot-dev-skills"
  test -f "$entry/SKILL.md"
  for skills_dir in "$HOME/.agents/skills" "$HOME/.claude/skills"; do
    mkdir -p "$skills_dir"
    target="$skills_dir/robot-dev-skills"
    if [ -e "$target" ] || [ -L "$target" ]; then
      printf 'Already present: %s\n' "$target"
    else
      ln -s "$entry" "$target"
    fi
  done
)
```

Start a new chat. In Codex, enter `$robot-dev-skills My mocap clip skates on a shorter robot. What should I check?` In Claude Code, enter `/robot-dev-skills My mocap clip skates on a shorter robot. What should I check?` The entry skill opens the motion retargeting guide and applies it to the evidence you supply.

The [routing regression cases](tests/robot-dev-skills/cases.md) include a direct request and a natural-language example for every specialist. In a broad or cross-domain question, invoking the entry explicitly makes your intent to use this collection clear.

Eight [algorithm checks](tests/robot-dev-skills/method-checks.md) include primary sources, executable counterexamples and observed results for motion, navigation, perception and policy development.

For simulation, [asset import validation](skills/robot-sim-asset-validation/SKILL.md) checks the converted robot's kinematics and physics. [Fault injection and attribution](skills/robot-sim-fault-injection/SKILL.md) checks whether a fault fired before scoring recovery.

You can also copy just the `robot-dev-skills/` package, including `references/workflows.md`. It reads a locally installed specialist or a checkout you identify first. If neither is available, it can read the selected guide from a pinned public GitHub commit. With only the entry package and no network, it identifies the missing package. For a specialist added after that pin, use a matching checkout or supply its published full commit ID.

## Use a skill

Clone the repository, open the skill that matches your question, and give your agent the relevant inputs. For example:

> Follow `skills/robot-episode-audit/SKILL.md` to review this recording. One operator took control twice. Show which two-step action windows are eligible for behavior cloning and identify the evidence for each boundary.

To install one skill, copy its entire folder into your agent’s skills directory. Keep its bundled `references/` and open the guide for the task at hand. Sibling packages are optional. Installing the collection side by side also makes those companion links available offline. [Single-package file guide](skills/README.md#install-one-skill)

## Choose a workflow

Browse the [skill index](skills/README.md) to choose a workflow by engineering question.

Seven workflows now cover motion retargeting, simulation environment construction, joint feedback recovery, multi-component updates, edge vision scheduling, manipulator workspace regression, and continuous bag recording. For existing installations, the index lists the four retired names and their replacement guides. [Migration table](skills/README.md#existing-installations)

| Category | Specialist skills |
| --- | ---: |
| [Systems, deployment, and safety](skills/README.md#systems-deployment-and-safety) | 11 |
| [Perception, calibration, and navigation](skills/README.md#perception-calibration-and-navigation) | 9 |
| [Grasping, planning, and motion control](skills/README.md#grasping-planning-and-motion-control) | 12 |
| [Teleoperation and demonstration data](skills/README.md#teleoperation-and-demonstration-data) | 6 |
| [Policy training and evaluation](skills/README.md#policy-training-and-evaluation) | 7 |
| [Robot platform and cloud services](skills/README.md#robot-platform-and-cloud-services) | 7 |
| [Engineering methods for agents and technical learning](skills/README.md#engineering-methods-for-agents-and-technical-learning) | 3 |
| [Interactive tools and offline archives](skills/README.md#interactive-tools-and-offline-archives) | 2 |
| [Skill distribution and technical publishing](skills/README.md#skill-distribution-and-technical-publishing) | 2 |

## Robot recursive self-improvement (RSI)

Repeat R1–R3 on external development tasks. A candidate that passes independent validation becomes the parent for the next round. If it regresses on a required task, keep the parent. If the evidence is inconclusive, collect the observation or correction that can distinguish the competing explanations.

| Stage | What to do | Evidence for the next decision |
| --- | --- | --- |
| R0 · Audit sources | Identify the parent system and the origin of its data, weights, prompts and recovery logic. Assign whole recordings or layouts to development, independent validation and sealed acceptance before selecting examples. | A record of permitted uses, prior exposure and unresolved provenance. |
| R1 · Attribute failures | Run the parent on external tasks. Trace observations, subgoals, proposed actions, executed commands, physical outcomes and scores. Compare how many trials reached each stage with how many passed it. | The earliest divergence and a matched-state experiment that could disprove its proposed cause. [Failure attribution](skills/robot-rsi-failure-attribution/SKILL.md) |
| R2 · Build one candidate | Collect expert labels for the learner states that need them. Tie observed outcomes to the actions actually executed. Change the implicated component, such as the planner, action policy or executor, and record the update budget. | A reproducible candidate, its parent and the evidence for the change. [Correction data design](skills/robot-rsi-correction-design/SKILL.md) · [Policy training](skills/robot-policy-training/SKILL.md) |
| R3 · Decide inheritance | Compare parent and candidate on matched independent trials under the same budget. Count new successes and losses on previously solved tasks. Apply the gain and retention criteria set before the run. Periodically compare against a fixed baseline across rounds. | Promote the candidate, retain the parent or collect more evidence. Record rejected candidates too. [Paired policy evaluation](skills/robot-policy-eval/SKILL.md) · [Candidate promotion](skills/robot-rsi-candidate-promotion/SKILL.md) |
| R4 · Verify transfer and freeze | Check the target robot’s camera frames, action units, control rate and episode reset. Freeze the baseline and candidate bundles, including weights, prompts, tools, recovery logic, controller and runtime. | Version manifests and a cold-load check for the exact systems entering acceptance. |
| R5 · Run sealed acceptance | Fix the metrics and failure handling before the first acceptance rollout. Preserve successes, failures and interventions. Report simulation, hardware and official results separately. | A transfer result for the frozen systems. RoboDojo prohibits iterative tuning with feedback from rollouts on its layouts. [Official evaluation protocol](https://robodojo-benchmark.com/leaderboard/protocol?lang=en) |

## Try an offline example

The [camera geometry example](skills/robot-sensor-calibration/references/geometry-check.md) runs with Python 3 and the standard library. It shows how two different depth values can map to the same pixel and how a held-out 3D landmark exposes the error. The [stop and restart cases](skills/robot-safety-policy/references/stop-restart-cases.md) give five synthetic event traces for reviewing evidence without connecting to hardware.

## License

The skill documents and original examples are available under the [MIT License](LICENSE). Linked papers, configurations, and manuals are published by their respective owners.
