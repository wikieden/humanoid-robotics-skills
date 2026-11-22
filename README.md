# Humanoid Robotics Skills

English · [简体中文](README.zh-CN.md)

This collection contains 54 English-language agent skills. One entry skill routes to 53 specialists. Of those specialists, 46 cover humanoid and mobile manipulation robotics. The other seven cover agent evaluation and execution, technical learning, interactive applications, offline archives, skill distribution and technical publishing. Each skill is a Markdown workflow for a specific engineering decision, from tracing a reversed gripper command to deciding whether a new robot policy should replace its baseline.

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

You can also copy just the `robot-dev-skills/` package, including `references/workflows.md`. It reads a locally installed specialist or a checkout you identify first. If neither is available, it can read the selected guide from a pinned public GitHub commit. With only the entry package and no network, it identifies the missing package.

## Use a skill

Clone the repository, open the skill that matches your question, and give your agent the relevant inputs. For example:

> Follow `skills/robot-episode-audit/SKILL.md` to review this recording. One operator took control twice. Show which two-step action windows are eligible for behavior cloning and identify the evidence for each boundary.

To install one skill, copy its entire folder into your agent’s skills directory. Keep its bundled `references/` and open the guide for the task at hand. Sibling packages are optional. Installing the collection side by side also makes those companion links available offline. [Single-package file guide](skills/README.md#install-one-skill)

## Choose a workflow

Browse the [skill index](skills/README.md) to choose a workflow by engineering question.

Seven workflows now cover motion retargeting, simulation environment construction, joint feedback recovery, multi-component updates, edge vision scheduling, manipulator workspace regression, and continuous bag recording. For existing installations, the index lists the four retired names and their replacement guides. [Migration table](skills/README.md#existing-installations)

| Category | Specialist skills |
| --- | ---: |
| [Systems, deployment, and safety](skills/README.md#systems-deployment-and-safety) | 9 |
| [Perception, calibration, and navigation](skills/README.md#perception-calibration-and-navigation) | 9 |
| [Grasping, planning, and motion control](skills/README.md#grasping-planning-and-motion-control) | 11 |
| [Teleoperation and demonstration data](skills/README.md#teleoperation-and-demonstration-data) | 6 |
| [Policy training and evaluation](skills/README.md#policy-training-and-evaluation) | 4 |
| [Robot platform and cloud services](skills/README.md#robot-platform-and-cloud-services) | 7 |
| [Engineering methods for agents and technical learning](skills/README.md#engineering-methods-for-agents-and-technical-learning) | 3 |
| [Interactive tools and offline archives](skills/README.md#interactive-tools-and-offline-archives) | 2 |
| [Skill distribution and technical publishing](skills/README.md#skill-distribution-and-technical-publishing) | 2 |

## Try an offline example

The [camera geometry example](skills/robot-sensor-calibration/references/geometry-check.md) runs with Python 3 and the standard library. It shows how two different depth values can map to the same pixel and how a held-out 3D landmark exposes the error. The [stop and restart cases](skills/robot-safety-policy/references/stop-restart-cases.md) give five synthetic event traces for reviewing evidence without connecting to hardware.

## License

The skill documents and original examples are available under the [MIT License](LICENSE). Linked papers, configurations, and manuals are published by their respective owners.
