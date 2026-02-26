---
name: sky-sync
description: Fetch latest Sky Atlas docs and pull documentation repos
allowed-tools: Bash(python3 *), Bash(git *)
---

# Sync Sky Knowledge Base

1. If `~/sky-kb/` doesn't exist, clone it:
   `git clone https://github.com/arcniko/sky-kb.git ~/sky-kb`
2. Run: `python3 ~/sky-kb/scripts/sync.py`
3. Report what was downloaded (Atlas files, repo status)
4. If there were errors, show them and suggest fixes
