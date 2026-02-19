# Sky Knowledge Base

Local knowledge base for Sky Atlas governance documentation. Claude Code can browse these files directly to answer governance questions.

## Content

### Atlas (`content/atlas/`)

Sky Atlas governance documentation, one markdown file per scope. Synced from `https://sky-atlas.io/api/atlas.md?split-by-scope`.

**Hierarchy system**: Documents use a dot-separated formal ID system:
- `A.0` = top-level scope
- `A.0.1` = article within that scope
- `A.0.1.1` = section within that article
- `A.0.1.1.1` = primary document (Core, Type Specification, etc.)

**Document types** (in brackets after the name):
- `[Scope]` — top-level governance areas
- `[Article]` — major divisions within a scope
- `[Section]` — groups of related documents
- `[Core]` — primary governance rules
- `[Type Specification]`, `[Subtype]` — detailed specifications

### Laniakea Docs (`content/laniakea-docs/`)

Documentation for Laniakea — the current core work on the Sky Protocol. This is essential context for understanding protocol-level questions.

### Maker Protocol Tech Docs (`content/mcd-docs-content/`)

Technical documentation for the Maker Protocol (MCD). Older but still important for understanding the protocol's foundations and technical architecture.

### How to find answers

1. Grep across all content (`content/atlas/`, `content/`) for keywords related to the question
2. Read the matching file(s)
3. For Atlas questions: check parent scope for broader context (e.g., if answer is in A.1.2.3, also read the A.1 file)
4. For protocol questions: check `content/laniakea-docs/` first (current), then `content/mcd-docs-content/` (legacy)
5. Cite sources: use the formal ID for Atlas docs, or the file path for repo docs

## Syncing

Run `/sync` to fetch the latest content. This downloads Atlas markdown and pulls the documentation repos.
