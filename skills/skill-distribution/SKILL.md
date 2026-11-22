---
name: skill-distribution
description: Package or maintain a skill collection for several agent hosts. Use when installation must be repeatable, existing user skills must survive updates and removal, or a host lists a package but cannot resolve its references.
metadata:
  title: Distributing a Skill Collection Across Agent Hosts
---

# Distributing a Skill Collection Across Agent Hosts

Maintain one canonical directory per skill with its entrypoint and bundled resources. For each supported host, establish its effective discovery root, naming rules, directory-link support and refresh behavior from its installed configuration or documentation. Keep host-specific adapters thin. Test project-local and user-scoped installations only for the modes offered by the installer.

| Destination observed | Install decision | Removal decision |
| --- | --- | --- |
| Absent | Expose the canonical package and record ownership | Nothing to remove |
| Managed link to this exact source | Already installed | Remove the link after checking ownership again |
| Existing directory, foreign link, or ambiguous dangling link | Report a conflict and preserve it | Preserve it |
| Managed copy with a recorded digest | Update a matching, unmodified copy | Preserve local edits and report the conflict |

Distinguish a dangling link from an absent path using link metadata. For a copy-based adapter, track the destination and installed digest or file manifest. Preserve references, assets and relative links between sibling skills. During upgrades, detect renamed or retired packages from the previous manifest. If a run stops partway, report what was installed so rerunning converges without taking ownership of unrelated files.

**Exercise the installer in disposable roots.** Preview the changes and check that the preview creates nothing. Install, repeat installation, verify every expected entrypoint and one nested reference, then uninstall. Repeat with a same-name user directory containing a marker, a link to another checkout and a configured nondefault discovery root. The marker and foreign target must survive both install and uninstall. Finally, open a clean session in each supported host and check whether it discovers the skill and can read its resource. If only filesystem checks were run, report discovery as untested.

**Deliverable.** Give one row per host and scope with install, repeat, conflict, reference resolution, uninstall and host discovery results. Include the paths or package names the operator needs to resolve a conflict in their own environment.
