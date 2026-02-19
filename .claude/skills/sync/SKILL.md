---
name: sync
description: Fetch latest Sky Atlas docs and pull documentation repos
allowed-tools: Bash(python3 *), Bash(git *)
---

# Sync Sky Knowledge Base

Fetch the latest Sky Atlas governance documentation and pull documentation repos.

## Steps

1. Run the sync script:
   ```bash
   python3 scripts/sync.py
   ```
2. Report what was downloaded (Atlas files, repo status)
3. If there were errors, show them and suggest fixes
