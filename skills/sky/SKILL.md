---
name: sky
description: Answer a question about Sky governance using the local knowledge base
argument-hint: <question> | sync | add repo <url> | remove repo <name>
allowed-tools: Grep(*), Read(*), Edit(*), Write(*), Bash(git *), Bash(python3 *), Bash(test *), Bash(rm -rf *), Bash(mkdir *), Bash(ls *), WebFetch(domain:sky-forum-proxy.skynav.workers.dev)
---

# Sky Knowledge Base

## Registry

<!-- Updated by /sky setup — do not edit manually -->
(Not configured yet. Ask a question or run `/sky sync` to set up.)

## Routing

Parse the user's input to determine the subcommand:

- `sync` → **Sync** flow
- `add repo <url>` → **Add Repo** flow
- `remove repo <name>` → **Remove Repo** flow
- Anything else → **Search** flow (default)

**Do not announce which flow you are running. Just execute it.**

---

## Setup flow

Triggered automatically when the Registry section above says "Not configured yet" and the user runs any command.

1. **Ask where to store the KB** using AskUserQuestion — suggest `~/sky-kb` as the default (with the user's actual home directory expanded). Let the user pick or type a custom path.

2. **Clone the repo** if the path doesn't exist:
   ```bash
   git clone https://github.com/arcniko/sky-kb.git <path>
   ```

3. **Ask which bundle** to install using AskUserQuestion with these options:
   - **All (Recommended)** — all categories + Atlas (~41 repos). "Full picture: governance, technical, everything."
   - **Core** — Atlas + protocol docs + core contracts (~18 repos). "Essential protocol documentation."
   - **Technical** — Core + Spark, Grove, keepers, migration, endgame (~29 repos). "Developer-focused: all code repos, skip governance/community."

4. **Map the bundle to category IDs**:
   - All → `["laniakea", "core-protocol", "spark", "grove", "migration", "endgame", "keepers", "governance"]`
   - Core → `["laniakea", "core-protocol"]`
   - Technical → `["laniakea", "core-protocol", "spark", "grove", "migration", "endgame", "keepers"]`

5. **Write `<path>/.kb_config.json`**:
   ```json
   {"preset": "sky", "categories": [...selected IDs...], "custom_repos": [], "atlas": true}
   ```

6. **Update the Registry section** in this SKILL.md — replace the placeholder text with `<path>` using the Edit tool.

7. **Run sync**:
   ```bash
   python3 <path>/scripts/sync.py --kb-path <path>
   ```

8. If the user had a question, continue to the **Search** flow to answer it.

---

## Search flow

1. **Resolve KB path** from the Registry section above. If it says "Not configured yet" → trigger **Setup** flow automatically.

2. **Read `<kb-path>/DIRECTORY.md`** to understand what content exists and where.

3. **Target your search** — based on DIRECTORY.md, identify the most relevant subdirectories for the question. Grep within those specific directories rather than all of `content/`.

4. **Read matching files** to find the answer.

5. For Atlas results: also read the parent scope file for broader context.

6. For protocol questions: check whether the question is about the **live system** or the **planned one** — see [Deployed vs. planned](#deployed-vs-planned) below. `laniakea-docs` describes a future architecture and must not be presented as current behaviour. For "how does X work today", ground the answer in the chainlog, the contract repos, and what governance has actually executed (`spells-mainnet`, `spark-spells`, `executive-votes`). Use `mcd-docs-content` for legacy background.

7. For smart contract address lookups: read `<kb-path>/content/chainlog-ui/api/mainnet/active.json` — this is the live chainlog with all current contract addresses.

8. **Search the forum** — if local KB results are incomplete, or the question is about governance discussions/proposals/community sentiment, also search the Sky forum:
   - Use WebFetch to call `https://sky-forum-proxy.skynav.workers.dev/search?q=<query>&max=5` with prompt "Return the raw JSON"
   - If a topic looks highly relevant, fetch full content: `https://sky-forum-proxy.skynav.workers.dev/topic/<id>` with prompt "Return the raw JSON"
   - For "latest", "recent", or "what's new" questions: call `https://sky-forum-proxy.skynav.workers.dev/latest?max=5` first, then fetch full content for the most relevant topics via `/topic/<id>`
   - **Always prefer the newest thread on a subject** — see [Forum recency](#forum-recency) below
   - Skip if local KB already provides a complete, authoritative answer

### Forum recency

Sky's forum has years of threads on the same recurring subjects — debt ceilings, rate changes, allocator parameters, risk assessments — each superseding the last. **The oldest match is usually the wrong answer.** A thread can also be from the MakerDAO era and use retired terminology (MIPs, DAI, Maker branding) for a mechanism that still exists under a different name.

`/search` ranks by relevance, **not** recency, and returns no dates. Recover recency like this:

- **Topic ID is monotonic — higher id means newer.** This is the main signal available on search results. For calibration: id ~22,000 is Maker-era (2023), ~26,100 is early 2025, ~27,600 is January 2026, ~28,160 is August 2026.
- **Many titles carry an explicit date**, e.g. `[Jan 15, 2026] Parameter Changes - Grove Allocator Vault`. Use it when present.
- **Only `/latest` returns real timestamps** (`created_at`, `last_posted_at`, `posts_count`). `/topic/<id>` returns just `title`, `url`, and `posts` with `username` + `content` — no dates. So a single topic fetch cannot tell you how old it is; judge from the id and the title.

Rules:

- Sort candidate topics by id descending and read the newest relevant one **first**. Only reach for older threads for history, or when the newest doesn't cover the question.
- If old and new threads conflict, the newer wins — and say the parameter or policy changed rather than presenting the stale value.
- **Never quote a number** (rate, ceiling, cap, fee) from an old thread as current. Confirm it against the newest thread, the chainlog, or `executive-votes`, which record what was actually enacted.
- Date what you cite: give the thread's date or note it is older discussion, so the reader can judge staleness.

### Deployed vs. planned

**`content/laniakea-docs/` is a forward-looking design corpus, not a description of the live system.** Its own README calls Laniakea "a comprehensive infrastructure overhaul rolling out through 2026" and states "These documents are drafts under active development."

The vocabulary it defines is largely **unbuilt**: Generator, PAU, Prime PAU, Halo, Folio, Sentinel Network, beacons, teleonomes, synomes, LCTS, NFATs, TEJRC / TISRC / srUSDS, the daily settlement cycle. The mainnet chainlog contains **no** `GENERATOR`, `PRIME`, or `HALO` entries. Reading these docs as current behaviour produces confidently wrong answers.

What is actually live for the same functions:

| Laniakea term | Live mechanism today |
|---|---|
| Generator creating USDS | The **Allocation System** — per-agent allocator ilks (`ALLOCATOR-SPARK-A`, `ALLOCATOR-GROVE-A`, …) in the vat |
| Prime PAU | `ALLOCATOR_<NAME>_A_VAULT` + `_BUFFER`, wired by `dss-allocator`'s `AllocatorInit.initIlk` |
| Prime credit line | The ilk debt ceiling (`line`), managed by DC-IAM / `MCD_IAM_AUTO_LINE` |
| Rate-limited capital flow | ALM controller rate limits in the Spark / Grove liquidity layers, separate from the vat ceiling |
| Daily settlement cycle | The **Monthly** Settlement Cycle, executed by executive spell |

Rules:

- **Never state Laniakea mechanics as how the protocol works now.** If asked how something works today, answer from live sources first; mention Laniakea only as the direction of travel, explicitly labelled as planned.
- **Label which is which.** When both exist, give the live mechanism and name the Laniakea successor separately.
- **Verify a contract exists before asserting it does** — `content/chainlog-ui/api/mainnet/active.json` is ground truth for what is deployed.
- **`content/laniakea-docs/inactive/`** is superseded even within the Laniakea corpus. Treat it as historical drafts, not as a fallback.
- **Atlas** (`content/atlas/`) is ratified governance policy and mostly binds today, but it contains forward-looking articles too. Check whether an article describes an active process before relying on it. Atlas uses "Prime Agent" for what Laniakea calls a "Prime".

### How to answer

- Be specific and cite your sources (Atlas formal ID like `A.1.2.3`, or file path for repo docs)
- Quote relevant passages when helpful
- When citing forum results, include the topic title and link to the discussion
- Forum posts are community discussion, not official protocol policy — note this distinction when relevant
- Prefer the newest forum thread on a subject and date what you cite, per [Forum recency](#forum-recency) above
- Distinguish deployed behaviour from planned architecture, per [Deployed vs. planned](#deployed-vs-planned) above. If an answer rests on `laniakea-docs`, say so and say it is not live yet
- If the content doesn't contain an answer, say so clearly

---

## Sync flow

1. **Resolve KB path** from the Registry section above. If it says "Not configured yet" → trigger **Setup** flow.
2. Run:
   ```bash
   python3 <kb-path>/scripts/sync.py --kb-path <kb-path>
   ```
3. Summarize concisely — only mention what changed:
   - Atlas: "updated" or "already up to date"
   - Repos: if ≤5 updated, list their names; if >5, just show the count (e.g. "12 repos updated")
   - If nothing changed: "Everything up to date."
4. If errors occurred, show them and suggest fixes.

---

## Add Repo flow

1. **Parse arguments** — extract repo URL (required), name (optional, derive from URL), description (optional, ask user).
2. **Resolve KB path** from the Registry section above. If it says "Not configured yet" → trigger **Setup** flow first.
3. **Validate** — run `git ls-remote <url> HEAD` to confirm accessibility.
4. **Read `<kb-path>/.kb_config.json`** — check `custom_repos` for duplicates.
5. **Add to config** — append to the `custom_repos` array in `.kb_config.json`.
6. **Run sync** to clone the new repo.
7. **Report** what was added.

---

## Remove Repo flow

1. **Parse the repo name** from arguments.
2. **Resolve KB path** from the Registry section above.
3. **Read `<kb-path>/.kb_config.json`** — find the repo in `custom_repos`.
   - If not found there, check if it's a preset repo. If so, tell the user to remove the category instead.
4. **Remove from config** — edit `.kb_config.json` to remove the entry.
5. **Delete content**: `rm -rf <kb-path>/content/<name>`
6. **Run sync** to regenerate DIRECTORY.md.
7. **Report** what was removed.
