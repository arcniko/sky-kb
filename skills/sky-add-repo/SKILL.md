---
name: sky-add-repo
description: Add a git repo to the Sky knowledge base
argument-hint: <repo-url> [name] [description]
allowed-tools: Read(*), Edit(*), Bash(git *), Bash(python3 *)
---

# Add Repo to Sky Knowledge Base

Add a git repository to `~/sky-kb/sources.json` and sync it.

## Before starting

1. Check if `~/sky-kb/` exists
2. If not: `git clone https://github.com/arcniko/sky-kb.git ~/sky-kb`

## Steps

1. **Parse arguments** — extract from the user's input:
   - **repo URL** (required) — the git clone URL
   - **name** (optional) — short identifier for the repo. If not provided, derive from the URL (e.g. `https://github.com/org/my-repo.git` → `my-repo`)
   - **description** (optional) — what this repo contains. If not provided, ask the user

2. **Validate the repo URL** — run `git ls-remote <url> HEAD` to confirm it's accessible. If it fails, report the error and stop.

3. **Check for duplicates** — read `~/sky-kb/sources.json` and check the `repos` array. If an entry with the same `url` or `name` already exists, tell the user and stop.

4. **Add to sources.json** — append a new object to the `repos` array:
   ```json
   {"name": "<name>", "url": "<url>", "description": "<description>"}
   ```
   Use the Edit tool to modify `~/sky-kb/sources.json`. Add the new entry as the last element in the `repos` array, maintaining valid JSON formatting consistent with the existing file.

5. **Run sync** — `python3 ~/sky-kb/scripts/sync.py` to clone the new repo into `~/sky-kb/content/`.

6. **Update DIRECTORY.md** — append a new section to `~/sky-kb/DIRECTORY.md`:
   ```markdown
   ## <Name> (`content/<name>/`)
   <description>
   ```

7. **Report results** — confirm what was added: repo name, URL, and the content path (`~/sky-kb/content/<name>/`).
