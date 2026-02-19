---
name: sky
description: Answer a question about Sky governance using the local knowledge base
argument-hint: <question>
---

# Sky Governance Search

Answer the user's question using the local knowledge base in `content/`.

## How to search

1. Grep across `content/` for keywords from the question
2. Read the matching files to find the answer
3. For Atlas results: also read the parent scope file for broader context
4. For protocol questions: prioritize `content/laniakea-docs/` (current), then `content/mcd-docs-content/` (legacy)

## How to answer

- Be specific and cite your sources (Atlas formal ID like `A.1.2.3`, or file path for repo docs)
- Quote relevant passages when helpful
- If the content doesn't contain an answer, say so clearly
