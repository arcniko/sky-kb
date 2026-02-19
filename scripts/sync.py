"""Sync Sky Atlas markdown and documentation repos.

Tracks state in .sync_state.json to skip sources that haven't changed:
- Atlas: checks next-gen-atlas repo HEAD before downloading
- Repos: compares local HEAD with remote HEAD via git ls-remote
"""

import io
import json
import os
import subprocess
import urllib.request
import zipfile

ROOT = os.path.dirname(os.path.dirname(__file__))
CONTENT_DIR = os.path.join(ROOT, "content")
ATLAS_DIR = os.path.join(CONTENT_DIR, "atlas")
STATE_FILE = os.path.join(ROOT, ".sync_state.json")
SOURCES_FILE = os.path.join(ROOT, "sources.json")


def load_sources():
    with open(SOURCES_FILE) as f:
        return json.load(f)


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def sync_atlas(state, sources, force=False):
    atlas_config = sources.get("atlas", {})
    atlas_url = atlas_config.get("url")
    atlas_repo = atlas_config.get("repo")

    if not atlas_url:
        print("  No atlas URL configured in sources.json — skipping")
        return False

    # Check if the source repo has new commits before downloading
    if atlas_repo:
        remote_head = get_remote_head(atlas_repo)
        old_head = state.get("atlas_repo_head")

        if not force and remote_head and old_head and remote_head == old_head:
            print(f"  source repo unchanged ({remote_head[:8]}) — skipping download")
            return False

        print(f"  source repo updated ({old_head[:8] if old_head else 'first sync'} → {remote_head[:8] if remote_head else '?'})")

    print(f"  Fetching from {atlas_url} ...")
    req = urllib.request.Request(atlas_url)
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = resp.read()

    print(f"  Downloaded {len(data) / 1024:.0f} KB — extracting ...")

    # Clear old files
    if os.path.exists(ATLAS_DIR):
        old_files = [f for f in os.listdir(ATLAS_DIR) if f.endswith(".md")]
        for f in old_files:
            os.remove(os.path.join(ATLAS_DIR, f))
    else:
        os.makedirs(ATLAS_DIR)

    # Extract
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        md_files = [n for n in zf.namelist() if n.endswith(".md")]
        for name in md_files:
            basename = os.path.basename(name)
            target = os.path.join(ATLAS_DIR, basename)
            with zf.open(name) as src, open(target, "wb") as dst:
                dst.write(src.read())

    extracted = [f for f in os.listdir(ATLAS_DIR) if f.endswith(".md")]
    total_size = sum(os.path.getsize(os.path.join(ATLAS_DIR, f)) for f in extracted)

    print(f"  Extracted {len(extracted)} files ({total_size / 1024:.0f} KB total)")
    for f in sorted(extracted):
        size = os.path.getsize(os.path.join(ATLAS_DIR, f))
        print(f"    {f} ({size / 1024:.0f} KB)")

    if atlas_repo:
        state["atlas_repo_head"] = remote_head
    return True


def get_local_head(repo_path):
    result = subprocess.run(
        ["git", "-C", repo_path, "rev-parse", "HEAD"],
        capture_output=True, text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def get_remote_head(repo_url):
    result = subprocess.run(
        ["git", "ls-remote", repo_url, "HEAD"],
        capture_output=True, text=True,
    )
    if result.returncode == 0 and result.stdout.strip():
        return result.stdout.split()[0]
    return None


def sync_repos(state, sources, force=False):
    os.makedirs(CONTENT_DIR, exist_ok=True)
    repo_state = state.setdefault("repos", {})

    for repo in sources.get("repos", []):
        name = repo["name"]
        repo_path = os.path.join(CONTENT_DIR, name)

        if os.path.exists(repo_path):
            # Check if remote has new commits
            local_head = get_local_head(repo_path)
            remote_head = get_remote_head(repo["url"])

            if not force and local_head and remote_head and local_head == remote_head:
                print(f"  {name}: already up to date ({local_head[:8]})")
                repo_state[name] = local_head
                continue

            print(f"  {name}: pulling ({local_head[:8] if local_head else '?'} → {remote_head[:8] if remote_head else '?'}) ...")
            subprocess.run(
                ["git", "-C", repo_path, "pull", "--ff-only"],
                check=True,
            )
            repo_state[name] = get_local_head(repo_path)
        else:
            print(f"  {name}: cloning ...")
            subprocess.run(
                ["git", "clone", "--depth", "1", repo["url"], repo_path],
                check=True,
            )
            repo_state[name] = get_local_head(repo_path)

        print(f"  {name}: OK")


def main():
    state = load_state()
    force = "--force" in __import__("sys").argv

    if force:
        print("Force sync enabled\n")

    sources = load_sources()

    print("=== Atlas ===")
    sync_atlas(state, sources, force)
    print()
    print("=== Repos ===")
    sync_repos(state, sources, force)
    print()

    save_state(state)
    print("Done.")


if __name__ == "__main__":
    main()
