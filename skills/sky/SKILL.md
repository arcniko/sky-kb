---
name: sky
description: Answer a question about Sky governance using the local knowledge base
argument-hint: <question>
allowed-tools: Grep(*), Read(*), Bash(git clone *), Bash(python3 *)
---

# Sky Governance Search

Answer the user's question using the Sky knowledge base at `~/sky-kb/content/`.

## Before searching

1. Check if `~/sky-kb/content/` exists
2. If not:
   - `git clone https://github.com/arcniko/sky-kb.git ~/sky-kb`
   - `python3 ~/sky-kb/scripts/sync.py`

## How to search

1. Grep across `~/sky-kb/content/` for keywords from the question
2. Read the matching files to find the answer
3. For Atlas results: also read the parent scope file for broader context
4. For protocol questions: prioritize `~/sky-kb/content/laniakea-docs/` (current), then `~/sky-kb/content/mcd-docs-content/` (legacy)

## How to answer

- Be specific and cite your sources (Atlas formal ID like `A.1.2.3`, or file path for repo docs)
- Quote relevant passages when helpful
- If the content doesn't contain an answer, say so clearly
