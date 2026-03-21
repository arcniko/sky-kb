# Sky Knowledge Base

Search Sky Protocol governance and technical documentation from your AI coding agent.

## Install

```bash
npx skills add arcniko/sky-kb
```

Or copy [`skills/sky/SKILL.md`](skills/sky/SKILL.md) into your agent's skills directory (e.g. `~/.claude/skills/sky/SKILL.md` for Claude Code).

Content is downloaded automatically on first use. Forum discussions from [forum.sky.money](https://forum.sky.money) are searched live when relevant.

## Usage

```
/sky <question>               Search the Sky knowledge base
/sky sync                     Sync/update content
/sky add repo <url>           Add a custom repo
/sky remove repo <name>       Remove a custom repo
```

### First run

The first time you use `/sky`, it clones this repo to `~/sky-kb` and asks you to pick a bundle:

| Bundle | Categories | Repos | Description |
|--------|-----------|-------|-------------|
| **All** (recommended) | Everything + Atlas | ~41 | Full picture: governance, technical, everything |
| **Core** | Laniakea + Core Protocol + Atlas | ~18 | Essential protocol documentation |
| **Technical** | Core + Spark + Grove + Keepers + Migration + Endgame | ~29 | Developer-focused, skip governance/community |

The **Atlas** (Sky governance documentation from sky-atlas.io) is always included.

## Architecture

```
~/.claude/skills/sky/SKILL.md    Skill file (registry + instructions)
~/sky-kb/                        KB instance (cloned on first use)
  .kb_config.json                Config (selected bundle, custom repos)
  presets/sky.json                Source definitions (all categories + repos)
  scripts/sync.py                Sync engine
  content/                       Downloaded documentation (gitignored)
    atlas/                       Sky Atlas markdown files
    laniakea-docs/               Cloned repos...
    mcd-docs-content/
    ...
  DIRECTORY.md                   Auto-generated content index
```
