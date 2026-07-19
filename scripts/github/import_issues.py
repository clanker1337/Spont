#!/usr/bin/env python3
"""
Import the Spont GitHub backlog from docs/planning/issue-backlog.json.

Creates labels, milestones, and issues (with body sections, labels, milestone,
and resolved dependency links). Emits docs/planning/issue-number-map.json mapping
the planned issue numbers (1..32) to the GitHub-assigned issue numbers, so branches
and PRs can reference the real numbers.

Auth (in order of preference):
  1. `gh` CLI if authenticated (run `gh auth login` first for write access)
  2. GITHUB_TOKEN environment variable (needs issues / milestones scope)

This script is idempotent: existing labels/milestones are reused, and an open issue
with the same title is skipped.
"""
import json
import os
import subprocess
import sys
import urllib.request
import urllib.error

REPO_ROOT = subprocess.check_output(["git", "rev-parse", "--show-toplevel"]).decode().strip()
BACKLOG = os.path.join(REPO_ROOT, "docs", "planning", "issue-backlog.json")
NUMBER_MAP = os.path.join(REPO_ROOT, "docs", "planning", "issue-number-map.json")

# Module-level globals (assigned in main before use; declared here for clarity).
OR = ""
EXISTING_LABELS: dict = {}
EXISTING_MILESTONES: dict = {}


def owner_repo():
    url = subprocess.check_output(["git", "remote", "get-url", "origin"]).decode().strip()
    url = url.replace("git@github.com:", "https://github.com/").replace(".git", "")
    if url.endswith("/"):
        url = url[:-1]
    return "/".join(url.split("/")[-2:])


def have_gh():
    try:
        return subprocess.run(["gh", "auth", "status"], capture_output=True).returncode == 0
    except FileNotFoundError:
        return False


USE_GH = have_gh()


def api(method, path, params=None, body=None):
    """Call GitHub REST. params -> query string; body -> JSON payload."""
    if USE_GH:
        cmd = ["gh", "api", "-X", method, f"/repos/{OR}/{path}"]
        if params:
            for k, v in params.items():
                cmd += ["-f", f"{k}={v}"]
        if body:
            cmd += ["-f", f"body={json.dumps(body)}"]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"gh api failed: {res.stderr.strip()}")
        return json.loads(res.stdout) if res.stdout.strip() else {}
    else:
        import urllib.request
        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            raise RuntimeError("No auth: set GITHUB_TOKEN or run `gh auth login`.")
        url = f"https://api.github.com/repos/{OR}/{path}"
        if params:
            from urllib.parse import urlencode
            url += "?" + urlencode(params)
        data = json.dumps(body).encode() if body else None
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Authorization", f"Bearer {token}")
        req.add_header("Accept", "application/vnd.github+json")
        req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req) as r:
                return json.loads(r.read().decode() or "{}")
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"API {method} {path} failed: {e.read().decode()}")


def get_existing_labels():
    out = {}
    page = 1
    while True:
        data = api("GET", "labels", params={"per_page": "100", "page": str(page)})
        if not data:
            break
        for l in data:
            out[l["name"]] = l
        page += 1
    return out


def ensure_label(name):
    if name in EXISTING_LABELS:
        return
    api("POST", "labels", body={"name": name, "color": "c2c2cf"})
    EXISTING_LABELS[name] = True
    print(f"  + label {name}")


def get_existing_milestones():
    out = {}
    for m in api("GET", "milestones", params={"state": "all", "per_page": "100"}):
        out[m["title"]] = m["number"]
    return out


def ensure_milestone(title, desc):
    if title in EXISTING_MILESTONES:
        return EXISTING_MILESTONES[title]
    m = api("POST", "milestones", body={"title": title, "description": desc, "state": "open"})
    EXISTING_MILESTONES[title] = m["number"]
    print(f"  + milestone {title} -> {m['number']}")
    return m["number"]


def existing_open_issue_titles():
    out = set()
    page = 1
    while True:
        data = api("GET", "issues", params={"state": "open", "per_page": "100", "page": str(page)})
        if not data:
            break
        for i in data:
            out.add(i["title"])
        page += 1
    return out


def build_body(iss, num_map):
    lines = []
    lines.append(f"**Milestone:** {iss['milestone']}  |  **Size:** {iss['size']}  |  "
                 f"**Area:** {iss['area']}  |  **Release:** {iss['release']}")
    lines.append("")
    lines.append(f"## Outcome\n{iss['outcome']}")
    lines.append("")
    lines.append(f"## Scope\n{iss['scope']}")
    lines.append("")
    lines.append(f"## Non-goals\n{iss['non_goals']}")
    lines.append("")
    lines.append("## Acceptance criteria")
    for a in iss["acceptance"]:
        lines.append(f"- {a}")
    lines.append("")
    lines.append("## Test requirements")
    for t in iss["tests"]:
        lines.append(f"- {t}")
    lines.append("")
    if iss["dependencies"]:
        deps = []
        for d in iss["dependencies"]:
            deps.append(f"#{num_map.get(d, d)}" if isinstance(d, int) else str(d))
        lines.append("## Dependencies\n" + ", ".join(deps))
        lines.append("")
    if iss["docs"]:
        lines.append("## Expected documentation changes")
        for d in iss["docs"]:
            lines.append(f"- {d}")
        lines.append("")
    if iss.get("sub_issues"):
        lines.append("## Sub-issues")
        for s in iss["sub_issues"]:
            lines.append(f"- {s['title']} ({s['size']})")
        lines.append("")
        lines.append("> Note: GitHub sub-issue links require Projects V2; create the parent/child "
                     "relationship manually if desired.")
    return "\n".join(lines)


def main():
    global OR, EXISTING_LABELS, EXISTING_MILESTONES
    OR = owner_repo()
    print(f"Target repo: {OR}  (auth: {'gh' if USE_GH else 'token'})")

    with open(BACKLOG) as f:
        data = json.load(f)

    for l in data["labels"]:
        ensure_label(l)
    # add release labels for repo-level filtering (Project may be unavailable)
    ensure_label("release:mvp")
    ensure_label("release:post-mvp")

    EXISTING_MILESTONES = get_existing_milestones()
    mtitle_to_num = {}
    for m in data["milestones"]:
        mtitle_to_num[m["title"]] = ensure_milestone(m["title"], m["description"])

    existing_titles = existing_open_issue_titles()

    num_map = {}
    for iss in sorted(data["issues"], key=lambda x: x["number"]):
        if iss["title"] in existing_titles:
            print(f"  = skip existing issue #{iss['number']} {iss['title']}")
            continue
        labels = list(iss["labels"]) + [f"release:{iss['release'].lower()}"]
        milestone_num = mtitle_to_num.get(iss["milestone"])
        body = build_body(iss, num_map)
        created = api("POST", "issues",
                      body={"title": iss["title"], "body": body,
                            "labels": labels, "milestone": milestone_num})
        num_map[iss["number"]] = created["number"]
        print(f"  + issue {iss['number']} -> #{created['number']} {iss['title']}")

    with open(NUMBER_MAP, "w") as f:
        json.dump(num_map, f, indent=2)
    print(f"Wrote {NUMBER_MAP}")
    print("Done. Branches/PRs should use the mapped GitHub issue numbers.")


if __name__ == "__main__":
    main()
