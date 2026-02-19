# Sky Knowledge Base

Local knowledge base for Sky governance documentation. Works with both Claude Code and the Claude desktop app.

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

## Quick Start

```bash
python3 scripts/sync.py
```

This downloads the Atlas markdown and clones/pulls the documentation repos into `content/`.

## Usage

### Claude Code

Open this folder in Claude Code:

```bash
cd sky-knowledge
claude
```

Ask governance questions directly — Claude will search across all content to find answers. Use `/sync` to fetch the latest content.

### Claude Desktop App

One-click installers download the content and configure Claude Desktop automatically.

**Mac**: Double-click `install.command`

**Windows**: Double-click `install.bat`

The installer will:
1. Clone this repo to `~/sky-kb` (or `%USERPROFILE%\sky-kb` on Windows)
2. Download all Sky Atlas content
3. Configure Claude Desktop's MCP filesystem server

After it finishes, restart Claude Desktop. You should see "sky-knowledge" listed under the MCP tools icon (hammer).

**Updating**: Double-click the installer again to pull the latest content.
