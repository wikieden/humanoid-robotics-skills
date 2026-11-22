"""Replay the robot-dev-skills routing matrix using isolated, read-only Codex CLI sessions."""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import json
import os
import re
import signal
import subprocess
import tempfile
import time


def read_cases(path):
    cases = {}
    for line in path.read_text().splitlines():
        if not re.match(r"^\| \d{2} \|", line):
            continue
        ident, package, explicit, implicit, extra = [s.strip() for s in line.strip("|").split("|")]
        package = package.strip("`")
        refs = {}
        match = re.search(r"`(references/[^\s`]+)\x60", extra)
        if match:
            modes = ["implicit"] if extra.startswith("自然") else ["explicit"] if extra.startswith("显式") else ["implicit", "explicit"]
            refs = dict.fromkeys(modes, match[1])
        if ident in cases or package in explicit or package in implicit:
            raise ValueError("Duplicate case ID or target name in prompt: " + ident)
        cases[ident] = dict(id=ident, pkg=package, explicit=explicit, implicit=implicit, refs=refs)
    return cases


def make_markers(root):
    docs = {}
    for entry in root.glob("*/SKILL.md"):
        for path in entry.parent.rglob("*.md"):
            docs[str(path.relative_to(root))] = path.read_text().split("\n---\n", 1)[-1]
    normalized = {key: " ".join(body.split()) for key, body in docs.items()}
    result = {}
    for key, body in docs.items():
        candidates = []
        for line in body.splitlines():
            if line.startswith("| ") and line.endswith(" |"):
                candidates.append(line)
            words = line.split()
            for start in range(0, len(words) - 7, 12):
                candidates.append(" ".join(words[start:start + 10]))
        result[key] = [s for s in candidates if len(s) >= 52 and
                       all(s not in other for k, other in normalized.items() if k != key)]
        if not result[key]:
            raise ValueError("Missing distinctive body text: " + key)
    return result


DIRECTORY = "robot-dev-skills/references/workflows.md"


def grade(events, markers, case, mode, rc):
    reads, messages = [], []
    partial_directory = False
    for event in events:
        item = event.get("item", {})
        if event.get("type") != "item.completed":
            continue
        if item.get("type") == "agent_message":
            messages.append(item.get("text", ""))
        if item.get("type") != "command_execution":
            continue
        output = " ".join(item.get("aggregated_output", "").split())
        if item.get("exit_code") != 0:
            # A multi-path rg can return usable rows from one file and fail on a second path.
            if "workflows.md" in item.get("command", "") and any(
                row in output for row in markers[DIRECTORY] if row.startswith("|") and row.endswith("|")
            ):
                reads.append([DIRECTORY])
                partial_directory = True
            continue
        hits = []
        for key, snippets in markers.items():
            positions = [output.find(s) for s in snippets if s in output]
            if positions:
                hits.append((min(positions), key))
        if hits:
            reads.append([key for _, key in sorted(hits)])
    flat = [k for group in reads for k in group]
    primary = []
    for group in reads:
        primary = [k.split("/")[0] for k in group if k.endswith("/SKILL.md") and not k.startswith("robot-dev-skills/")]
        if primary:
            break
    router = any(k.startswith("robot-dev-skills/") for k in flat)
    reference = case["refs"].get("implicit" if mode == "guided" else mode)
    has_ref = reference is None or case["pkg"] + "/" + reference in flat
    finished = rc == 0 and any(e.get("type") == "turn.completed" for e in events) and bool(messages)
    passed = finished and router and primary == [case["pkg"]] and has_ref
    status = "pass" if passed else ("routing" if finished else "runtime")
    return dict(id=case["id"], mode=mode, expected=case["pkg"], status=status, router=router,
                first=primary, required=reference, required_read=has_ref, reads=reads,
                partial_directory=partial_directory, answer=messages[-1] if messages else "",
                thread=next((e.get("thread_id") for e in events if e.get("type") == "thread.started"), None))


def run_case(job, work, output, markers):
    mode, case = job
    label = mode + "-" + case["id"]
    prefixes = {"explicit": "$robot-dev-skills ", "implicit": "",
                "guided": "请按本机的机器人开发指南处理以下问题，只打开当前交付物需要的专项。"}
    prompt = prefixes[mode] + case["implicit" if mode == "guided" else mode]
    (output / (label + ".prompt")).write_text(prompt + "\n")
    args = ["codex", "-a", "never", "-c", f'projects."{work}".trust_level="trusted"', "exec",
            "--ephemeral", "--sandbox", "read-only", "--ignore-rules", "--ignore-user-config",
            "--disable", "multi_agent", "--json", "-"]
    raw = output / (label + ".events")
    start = time.monotonic()
    with raw.open("wb") as stream, (output / (label + ".err")).open("wb") as errors:
        proc = subprocess.Popen(args, cwd=work, stdin=subprocess.PIPE, stdout=stream,
                                stderr=errors, start_new_session=True)
        try:
            proc.communicate(input=prompt.encode(), timeout=135)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGTERM)
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(proc.pid, signal.SIGKILL)
                proc.wait()
    events = [json.loads(line) for line in raw.read_text().splitlines() if line.strip()]
    result = grade(events, markers, case, mode, proc.returncode)
    result["elapsed_seconds"] = round(time.monotonic() - start, 1)
    (output / (label + ".result.json")).write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(label, result["status"], ",".join(result["first"]) or "-", flush=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--matrix", type=Path, default=Path(__file__).with_name("cases.md"))
    parser.add_argument("--entry", type=Path, default=Path.home() / ".agents/skills/robot-dev-skills")
    parser.add_argument("--mode", choices=["check", "explicit", "implicit", "both", "guided"], default="check")
    parser.add_argument("--case", action="append", default=[], help="Two-digit case ID; repeat to select more.")
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--output", type=Path, help="A new directory for evidence. Defaults to a temporary directory.")
    opts = parser.parse_args()
    entry = opts.entry.expanduser().resolve(strict=True)
    cases = read_cases(opts.matrix)
    names = {p.parent.name for p in entry.parent.glob("*/SKILL.md")} - {"robot-dev-skills"}
    routes = re.findall(r"^\| .*? \| `([\w-]+)` \|$", (entry / "references/workflows.md").read_text(), re.M)
    if len(cases) != len(names) or len(routes) != len(names) or {r["pkg"] for r in cases.values()} != set(routes) or set(routes) != names:
        parser.error("The case matrix, router and installed specialist set disagree.")
    if not 1 <= opts.workers <= 6 or set(opts.case) - set(cases):
        parser.error("Invalid worker count or case ID.")
    markers = make_markers(entry.parent)
    print(f"{len(names)} routes covered.", flush=True)
    if opts.mode == "check":
        return 0
    installed = Path.home() / ".agents/skills/robot-dev-skills"
    if not installed.is_dir() or installed.resolve() != entry:
        parser.error("The live suite uses the active Codex user entry. Point --entry at the same installation.")
    if opts.output:
        output = opts.output.resolve()
        output.mkdir(parents=True, exist_ok=False)
    else:
        output = Path(tempfile.mkdtemp(prefix="robot-router-eval-"))
    work = output / "project"
    work.mkdir()
    subprocess.run(["git", "init", "-q", str(work)], check=True)
    (work / "AGENTS.md").write_text("Treat each request as a synthetic offline question. Use only the given facts and relevant local documentation. You may inspect local instructions read-only. No network, edits, or hardware operations. Answer in at most two short sentences.\n")
    modes = ["explicit", "implicit"] if opts.mode == "both" else [opts.mode]
    jobs = [(mode, cases[ident]) for mode in modes for ident in dict.fromkeys(opts.case or cases)]
    print(f"Running {len(jobs)} fresh CLI sessions. Evidence: {output}", flush=True)
    with ThreadPoolExecutor(max_workers=opts.workers) as pool:
        results = list(pool.map(lambda job: run_case(job, work, output, markers), jobs))
    totals = Counter(r["status"] for r in results)
    print(dict(totals))
    return int(totals["pass"] != len(jobs))


if __name__ == "__main__":
    raise SystemExit(main())
