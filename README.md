# Sky Knowledge Base

Knowledge base skill for Claude Code — search Sky Protocol governance and technical documentation using `/sky`.

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) (or another AI coding agent that supports skills)
- Git
- Python 3

## Install

**macOS / Linux:**

```bash
git clone https://github.com/arcniko/sky-kb.git /tmp/sky-kb && mkdir -p ~/.claude/skills && cp -r /tmp/sky-kb/skills/* ~/.claude/skills/ && rm -rf /tmp/sky-kb
```

**Windows (PowerShell):**

```powershell
git clone https://github.com/arcniko/sky-kb.git $env:TEMP\sky-kb; New-Item -ItemType Directory -Force $HOME\.claude\skills | Out-Null; Copy-Item -Recurse $env:TEMP\sky-kb\skills\* $HOME\.claude\skills\; Remove-Item -Recurse -Force $env:TEMP\sky-kb
```

**Manual:**

1. Download [`skills/sky/SKILL.md`](skills/sky/SKILL.md) from this repo
2. Copy it into one of these locations:
   - `~/.claude/skills/sky/SKILL.md` — available in all projects
   - `<project>/.claude/skills/sky/SKILL.md` — available in one project

Content is downloaded automatically on first use.

## Usage

```
/sky <question>               Search the Sky knowledge base
/sky sync                     Sync/update content
/sky add repo <url>           Add a custom repo
/sky remove repo <name>       Remove a custom repo
```

### First run

The first time you run `/sky <question>`, the skill detects that it isn't set up yet and walks you through setup:

1. Asks where to store the KB (default: `~/sky-kb`)
2. Clones this repo
3. Shows available categories — you pick which to include
4. Syncs selected content
5. Answers your question

### Categories

| Category | Repos | Description |
|----------|-------|-------------|
| **Laniakea (Core)** | 5 | Current core work on the Sky Protocol |
| **Core Protocol** | 13 | Maker/Sky core smart contracts and modules |
| **Spark** | 5 | Spark Protocol lending and vaults (Sky Prime) |
| **Grove** | 2 | Grove Protocol (Sky Prime) |
| **Migration** | 1 | Migration tools and contracts |
| **Endgame / Staking** | 1 | Endgame toolkit and staking infrastructure |
| **Keepers** | 2 | Keeper bots and automation |
| **Governance** | 12 | Governance tools, spells, and community resources |

The **Atlas** (Sky governance documentation from sky-atlas.io) is always included.

## Architecture

```
~/.claude/skills/sky/SKILL.md    Skill file (registry + instructions)
~/sky-kb/                        KB instance (cloned from this repo)
  .kb_config.json                Config (selected categories, custom repos)
  presets/sky.json                Preset definition (all available sources)
  scripts/sync.py                Sync engine
  content/                       Downloaded documentation (gitignored)
    atlas/                       Sky Atlas markdown files
    laniakea-docs/               Cloned repos...
    mcd-docs-content/
    ...
  DIRECTORY.md                   Auto-generated content index
```
