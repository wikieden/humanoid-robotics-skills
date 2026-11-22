---
name: robot-dev-skills
description: Entry point for the robotics development skill collection. Use when the user invokes robot-dev-skills, asks which workflow fits a robotics problem, or needs to connect several engineering stages. Select and read the relevant specialist guide before applying it.
metadata:
  title: Robotics Development Workflow Router
---

# Robot Development Skills

Use the [workflow directory](references/workflows.md) to match the user's intended result and available evidence to a specialist. If the user asks for a recommendation only, return the specialist name and why it fits. When they ask for engineering work, open the selected guide and apply it to their inputs. If invoked without a task, offer a few examples and ask what they want to build or diagnose.

## Read the selected guide

1. Take the exact package name from the directory. Resolve any symlink to this entry package's real directory. Read `../<package>/SKILL.md` relative to that directory. A full checkout or a side-by-side installation provides these paths. If the host has already discovered that exact specialist elsewhere, use the path reported by the host. If the user supplied another checkout, its `skills/<package>/SKILL.md` also works. Confirm the file's frontmatter name matches the selected package.
2. For a copied entry package without a local specialist, the public source for this directory is `https://raw.githubusercontent.com/wikieden/humanoid-robotics-skills/331c4fac2c7ddcec17c270f5748531aa6a2c3fa0/skills/`. When online access is available, read the file at that base URL plus `<package>/SKILL.md`. The lookup needs only the public file path. Keep user logs, prompts and project data local.
3. Follow a reference only when the selected guide calls for it on this task. Resolve it relative to the file that contains the link, using the same checkout or pinned revision. If the guide or a required reference is unavailable, give its exact package and relative path, identify what is missing, and point to the full-checkout or selected-package installation. Only claim to have used files actually read.

## Route by the decision

- A motion clip skates when transferred to a shorter robot. Start with `robot-motion-retargeting` to check the mapping and stance constraints. If the exported clip passes FK checks but feedback diverges during execution, continue with `robot-motion-validation` using the accepted reference and measured trace.
- For a failed waypoint, route a recorded incident to `robot-navigation-replay`, a change to scan matching to `robot-slam-development`, and a saved map that locks onto the wrong floor to `robot-map-relocalization`.
- If the user asks to build a simulated environment and compare policies in it, start with `robot-sim-environment-build`. Use the validated scene, reset contract and scoring predicate as inputs to `robot-policy-eval` when the comparison is in scope.

Keep one primary workflow for a focused question. Add a second when a distinct requested result or a finding from the first warrants it. For an ambiguous request, use the supplied evidence to select the first actionable stage, or ask the one question that would change the selection. Report the engineering result, the specialist used, and any evidence still needed.
