---
name: sky
description: Answer a question about Sky governance using the local knowledge base
argument-hint: <question> | sync | add repo <url> | remove repo <name>
allowed-tools: Grep(*), Read(*), Edit(*), Bash(git *), Bash(python3 *), Bash(test *), Bash(rm -rf ~/sky-kb/content/*)
---

# Sky Knowledge Base

## Routing

Parse the user's input to determine the subcommand:

- Starts with `sync` → run the **Sync** flow
- Starts with `add repo` → run the **Add Repo** flow
- Starts with `remove repo` → run the **Remove Repo** flow
- Anything else → run the **Search** flow (default)

**Do not announce which flow you are running. Just execute it.**

---

## Search flow

Answer the user's question using the Sky knowledge base at `~/sky-kb/content/`.

### How to search

1. Grep across `~/sky-kb/content/` for keywords from the question
2. Read the matching files to find the answer
3. For Atlas results: also read the parent scope file for broader context

If `~/sky-kb/content/` doesn't exist or Grep returns no results, suggest running `/sky sync` and stop.

### How to answer

- Be specific and cite your sources (Atlas formal ID like `A.1.2.3`, or file path for repo docs)
- Quote relevant passages when helpful
- If the content doesn't contain an answer, say so clearly

---

## Sync flow

1. Run: `python3 ~/sky-kb/scripts/sync.py`
2. If the command fails because `~/sky-kb/` doesn't exist, clone first: `git clone https://github.com/arcniko/sky-kb.git ~/sky-kb` — then retry the sync
3. Report what was downloaded (Atlas files, repo status)
4. If there were errors, show them and suggest fixes

---

## Add Repo flow

Add a git repository to `~/sky-kb/sources.json` and sync it.

1. **Parse arguments** — extract from the user's input:
   - **repo URL** (required) — the git clone URL. If the user provides a short form like `org/repo`, expand it to `https://github.com/org/repo.git`
   - **name** (optional) — short identifier for the repo. If not provided, derive from the URL (e.g. `https://github.com/org/my-repo.git` → `my-repo`)
   - **description** (optional) — what this repo contains. If not provided, ask the user

2. **Validate the repo URL** — run `git ls-remote <url> HEAD` to confirm it's accessible. If it fails, report the error and stop.

3. **Check for duplicates** — read `~/sky-kb/sources.json` and check the `repos` array. If the file doesn't exist, clone first: `git clone https://github.com/arcniko/sky-kb.git ~/sky-kb`. If an entry with the same `url` or `name` already exists, tell the user and stop.

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

---

## Remove Repo flow

Remove a git repository from the Sky knowledge base.

1. **Parse the repo name** from arguments (the text after `remove repo`).

2. **Read `~/sky-kb/sources.json`** — find the matching entry in the `repos` array by name.

3. If not found, list available repos and stop.

4. **Remove the entry from `sources.json`** using the Edit tool.

5. **Delete the cloned content**: `rm -rf ~/sky-kb/content/<name>`

6. **Remove the repo's section from `~/sky-kb/DIRECTORY.md`** using the Edit tool.

7. **Report** what was removed: repo name, URL, and that its content was deleted.
