# Sky Knowledge Base

Local knowledge base for Sky governance documentation. Works with Claude Code and other AI coding agents.

## Install

```bash
npx skills add arcniko/sky-kb
```

Content is downloaded automatically on first use.

## Content

All content lives in `content/` and is fetched by the sync script:

| Source | Path | Description |
|--------|------|-------------|
| **Sky Atlas** | `content/atlas/` | Full governance documentation — one markdown file per scope |
| **Laniakea Docs** | `content/laniakea-docs/` | Current core work on the Sky Protocol |
| **MCD Docs** | `content/mcd-docs-content/` | Maker Protocol technical documentation (older but foundational) |

### Atlas Structure

The Atlas files use a hierarchical heading structure with formal IDs (e.g. `A.1.2.3`) and document types in brackets (`[Scope]`, `[Article]`, `[Section]`, `[Core]`, etc.):

| File | Description |
|------|-------------|
| `A.0 - Atlas Preamble.md` | Foundational definitions and general provisions |
| `A.1 - The Governance Scope.md` | Core governance rules |
| `A.2 - The Support Scope.md` | Support functions and services |
| `A.3 - The Stability Scope.md` | Financial stability and risk |
| `A.4 - The Protocol Scope.md` | Technical protocol governance |
| `A.5 - The Accessibility Scope.md` | Accessibility standards |
| `A.6 - The Agent Scope.md` | AI agent governance |

## Usage

Use `/sky <question>` from any project in Claude Code:

```
/sky What is the Stability Scope?
```

Use `/sky-sync` to fetch the latest content.
