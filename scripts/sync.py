"""Sync knowledge base content: Atlas markdown and documentation repos.

Reads .kb_config.json from the KB path to determine which preset and
categories to sync.  Tracks state in .sync_state.json to skip unchanged sources.

Usage:
    python3 sync.py --kb-path <path>          # sync configured sources
    python3 sync.py --kb-path <path> --force   # re-download everything
"""

import argparse
import io
import json
import os
import subprocess
import urllib.request
import zipfile


def resolve_paths(kb_path):
    """Derive all file paths from the KB root."""
    return {
        "kb": kb_path,
        "content": os.path.join(kb_path, "content"),
        "atlas": os.path.join(kb_path, "content", "atlas"),
        "state": os.path.join(kb_path, ".sync_state.json"),
        "config": os.path.join(kb_path, ".kb_config.json"),
        "directory": os.path.join(kb_path, "DIRECTORY.md"),
    }


def find_preset_path(kb_path, preset_name):
    """Locate the preset JSON file, checking the KB repo first."""
    # Check inside the KB repo (cloned from the framework repo)
    candidate = os.path.join(kb_path, "presets", f"{preset_name}.json")
    if os.path.exists(candidate):
        return candidate
    # Fallback: check relative to this script (source repo)
    script_dir = os.path.dirname(os.path.dirname(__file__))
    candidate = os.path.join(script_dir, "presets", f"{preset_name}.json")
    if os.path.exists(candidate):
        return candidate
    return None


def load_json(path):
    with open(path) as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def maybe_migrate(paths):
    """Migrate old sources.json format to .kb_config.json."""
    old_sources = os.path.join(paths["kb"], "sources.json")
    if not os.path.exists(old_sources) or os.path.exists(paths["config"]):
        return False

    print("Migrating from old sources.json format...")
    config = {
        "preset": "sky",
        "categories": ["laniakea", "core-protocol"],
        "custom_repos": [],
        "atlas": True,
    }

    # Preserve any custom repos that aren't in the default preset
    try:
        old = load_json(old_sources)
        preset_path = find_preset_path(paths["kb"], "sky")
        if preset_path:
            preset = load_json(preset_path)
            preset_urls = set()
            for cat in preset.get("categories", []):
                for repo in cat.get("repos", []):
                    preset_urls.add(repo["url"])

            for repo in old.get("repos", []):
                if repo["url"] not in preset_urls:
                    config["custom_repos"].append(repo)
    except Exception:
        pass

    save_json(paths["config"], config)
    print(f"  Created {paths['config']} with defaults: laniakea + core-protocol")
    return True


def resolve_sources(paths):
    """Read config + preset to build the list of sources to sync."""
    config = load_json(paths["config"])
    preset_name = config.get("preset")

    # Custom KB with no preset — only custom repos, no atlas
    if not preset_name:
        repos = list(config.get("custom_repos", []))
        return None, repos, None

    preset_path = find_preset_path(paths["kb"], preset_name)
    if not preset_path:
        print(f"Error: preset '{preset_name}' not found")
        return None, None, None

    preset = load_json(preset_path)

    # Atlas config
    atlas = preset.get("atlas") if config.get("atlas", True) else None

    # Collect repos from selected categories
    selected = set(config.get("categories", []))
    repos = []
    for cat in preset.get("categories", []):
        if cat["id"] in selected:
            repos.extend(cat["repos"])

    # Add custom repos
    repos.extend(config.get("custom_repos", []))

    return atlas, repos, preset


def generate_directory(paths, atlas, repos, preset):
    """Auto-generate DIRECTORY.md from the synced sources."""
    lines = ["# Content Directory\n"]

    if atlas:
        lines.append("## Atlas (`content/atlas/`)")
        lines.append(
            "Sky Atlas governance documentation — one markdown file per scope, "
            "synced from sky-atlas.io.\n"
        )
        lines.append(
            "Documents use dot-separated formal IDs (e.g. `A.1.2.3`) and type "
            "labels in brackets:"
        )
        lines.append(
            "`[Scope]`, `[Article]`, `[Section]`, `[Core]`, "
            "`[Type Specification]`, `[Subtype]`.\n"
        )

    # Group repos by category for nice output
    config = load_json(paths["config"])
    selected = set(config.get("categories", []))
    custom = config.get("custom_repos", [])

    if preset:
        for cat in preset.get("categories", []):
            if cat["id"] not in selected:
                continue
            lines.append(f"## {cat['name']}\n")
            for repo in cat["repos"]:
                lines.append(
                    f"- **{repo['name']}** (`content/{repo['name']}/`) — "
                    f"{repo.get('description', '')}"
                )
            lines.append("")

    if custom:
        lines.append("## Custom Repos\n")
        for repo in custom:
            lines.append(
                f"- **{repo['name']}** (`content/{repo['name']}/`) — "
                f"{repo.get('description', '')}"
            )
        lines.append("")

    with open(paths["directory"], "w") as f:
        f.write("\n".join(lines))

    print(f"  Generated {paths['directory']}")


# --- Atlas sync ---

def get_remote_head(repo_url):
    result = subprocess.run(
        ["git", "ls-remote", repo_url, "HEAD"],
        capture_output=True, text=True,
    )
    if result.returncode == 0 and result.stdout.strip():
        return result.stdout.split()[0]
    return None


def sync_atlas(state, atlas, atlas_dir, force=False):
    if not atlas:
        print("  Atlas not configured — skipping")
        return False

    atlas_url = atlas.get("url")
    atlas_repo = atlas.get("repo")

    if not atlas_url:
        print("  No atlas URL configured — skipping")
        return False

    if atlas_repo:
        remote_head = get_remote_head(atlas_repo)
        old_head = state.get("atlas_repo_head")

        if not force and remote_head and old_head and remote_head == old_head:
            print(f"  source repo unchanged ({remote_head[:8]}) — skipping download")
            return False

        print(
            f"  source repo updated "
            f"({old_head[:8] if old_head else 'first sync'} → "
            f"{remote_head[:8] if remote_head else '?'})"
        )

    print(f"  Fetching from {atlas_url} ...")
    req = urllib.request.Request(atlas_url)
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = resp.read()

    print(f"  Downloaded {len(data) / 1024:.0f} KB — extracting ...")

    if os.path.exists(atlas_dir):
        for f in os.listdir(atlas_dir):
            if f.endswith(".md"):
                os.remove(os.path.join(atlas_dir, f))
    else:
        os.makedirs(atlas_dir)

    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        md_files = [n for n in zf.namelist() if n.endswith(".md")]
        for name in md_files:
            basename = os.path.basename(name)
            target = os.path.join(atlas_dir, basename)
            with zf.open(name) as src, open(target, "wb") as dst:
                dst.write(src.read())

    extracted = [f for f in os.listdir(atlas_dir) if f.endswith(".md")]
    total_size = sum(os.path.getsize(os.path.join(atlas_dir, f)) for f in extracted)

    print(f"  Extracted {len(extracted)} files ({total_size / 1024:.0f} KB total)")
    for f in sorted(extracted):
        size = os.path.getsize(os.path.join(atlas_dir, f))
        print(f"    {f} ({size / 1024:.0f} KB)")

    if atlas_repo:
        state["atlas_repo_head"] = remote_head
    return True


# --- Repo sync ---

def get_local_head(repo_path):
    result = subprocess.run(
        ["git", "-C", repo_path, "rev-parse", "HEAD"],
        capture_output=True, text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def sync_repos(state, repos, content_dir, force=False):
    os.makedirs(content_dir, exist_ok=True)
    repo_state = state.setdefault("repos", {})

    for repo in repos:
        name = repo["name"]
        repo_path = os.path.join(content_dir, name)

        if os.path.exists(repo_path):
            local_head = get_local_head(repo_path)
            remote_head = get_remote_head(repo["url"])

            if not force and local_head and remote_head and local_head == remote_head:
                print(f"  {name}: already up to date ({local_head[:8]})")
                repo_state[name] = local_head
                continue

            print(
                f"  {name}: pulling "
                f"({local_head[:8] if local_head else '?'} → "
                f"{remote_head[:8] if remote_head else '?'}) ..."
            )
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


# --- Main ---

def main():
    parser = argparse.ArgumentParser(description="Sync knowledge base content")
    parser.add_argument("--kb-path", required=True, help="Path to the KB root")
    parser.add_argument("--force", action="store_true", help="Force re-download")
    args = parser.parse_args()

    kb_path = os.path.expanduser(args.kb_path)
    paths = resolve_paths(kb_path)

    if not os.path.exists(paths["config"]):
        maybe_migrate(paths)

    if not os.path.exists(paths["config"]):
        print(f"Error: no .kb_config.json found at {kb_path}")
        print("Run /sky sync or create the config manually.")
        return 1

    atlas, repos, preset = resolve_sources(paths)
    if atlas is None and repos is None and preset is None:
        return 1

    state_file = paths["state"]
    state = load_json(state_file) if os.path.exists(state_file) else {}

    if args.force:
        print("Force sync enabled\n")

    if atlas is not None:
        print("=== Atlas ===")
        sync_atlas(state, atlas, paths["atlas"], args.force)
        print()

    print(f"=== Repos ({len(repos)}) ===")
    sync_repos(state, repos, paths["content"], args.force)
    print()

    save_json(state_file, state)
    generate_directory(paths, atlas, repos, preset)

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
