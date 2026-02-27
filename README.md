# Sky Knowledge Base

Local knowledge base for Sky governance documentation. Works with Claude Code and other AI coding agents.

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) (or another AI coding agent that supports skills)
- Git
- Python 3

## Install

**macOS / Linux:**

```bash
git clone https://github.com/arcniko/sky-kb.git /tmp/sky-kb && cp -r /tmp/sky-kb/skills/* ~/.claude/skills/ && rm -rf /tmp/sky-kb
```

**Windows (PowerShell):**

```powershell
git clone https://github.com/arcniko/sky-kb.git $env:TEMP\sky-kb; Copy-Item -Recurse $env:TEMP\sky-kb\skills\* $HOME\.claude\skills\; Remove-Item -Recurse -Force $env:TEMP\sky-kb
```

**Manual (no terminal):**

1. Download [`skills/sky/SKILL.md`](skills/sky/SKILL.md) from this repo
2. Copy it into one of these locations:
   - `~/.claude/skills/sky/SKILL.md` — available in all projects
   - `<project>/.claude/skills/sky/SKILL.md` — available in one project
   - `<project>/.agents/sky/SKILL.md` — for non-Claude agents

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

Use `/sky` from any project in Claude Code:

```
/sky What is the Stability Scope?
/sky sync
/sky add repo <url> [name] [description]
/sky remove repo <name>
```
