# Skill Platform Reference

Last verified: 2026-07-20

This file tracks what is actually documented for the deployment targets in this repo, plus how this repository currently packages skills for them.

It separates three things:

1. Official product support documented by the vendor
2. This repo's current build/deploy convention
3. Gaps, limits, and risks

## Working parameters

Use these as the repo's current planning values unless superseded by better vendor documentation or empirical deployment tests.

### Source skill size limit

- **Published cross-tool source-skill limit:** none verified
- **Repo working source-skill limit:** **20,000 bytes for the authored markdown body**, excluding frontmatter
- **Why 20,000 bytes:** current large skills are already near this size, several targets have undocumented real limits, and non-skill-native targets are the likely bottleneck
- **Action threshold:** if a skill body exceeds 18,000 bytes, treat it as approaching split/refactor territory
- **Hard repo recommendation:** if a skill body exceeds 20,000 bytes, split or trim it unless we have verified deploy tests proving safety
- **Enforcement:** validate size limits from the `skill-tooling` deployment workflow before deployment; this repo should not carry local validator or deploy-wrapper scripts

This is an engineering budget, not a vendor-documented cap.

### Current measured transform profile

Measured on [source/field-hockey-strength-conditioning-coach.md](../source/field-hockey-strength-conditioning-coach.md) as of 2026-07-20:

- source total bytes: `21,569`
- source body bytes after frontmatter removal: `20,654`
- generated `codex` prompt bytes: `17,948`
- generated `openai-skills-api` prompt bytes: `17,960`
- generated `claude-code` skill bytes: `17,954`
- generated `grok` prompt bytes: `17,947`
- generated `grok-build` prompt bytes: `17,953`
- generated `chatgpt-work` zip bytes: `7,196`
- generated `claude-ai` zip bytes: `7,201`

Observed transform effect on prompt-like targets:

- current target generation **shrinks** the final text by about `2,700 bytes` relative to the markdown body
- this is because generation removes frontmatter and some source-only formatting rather than simply wrapping the source verbatim

Important caution:

- This shrinkage is a property of the **current** pipeline and sample skill.
- Do **not** treat it as guaranteed headroom without re-measuring after tooling changes.

### Tool-specific max deployable size

| Target | Max deployable size | Confidence | Notes |
|---|---|---|---|
| `chatgpt-work` | **Unknown for Skill bundle** | low | Related file upload limits are documented, but not a Skill bundle cap |
| `codex` | **Unknown for Skill bundle** | low | Official skill support exists, but no published per-skill size cap found |
| `openai-skills-api` | **Unknown** | low | Skills in API are mentioned, but no public upload cap found |
| `claude-code` | **Unknown for full skill body** | medium | First-class skill support exists; metadata discovery text truncates at 1,536 chars |
| `claude-ai` | **Unknown for zip skill target** | low | Public docs validate Projects/Knowledge, not this repo's zip-skill workflow |
| `grok` | **Unknown for skill bundle** | low | Public docs validate file uploads, not skill bundles |
| `grok-build` | **Unknown for skill bundle** | low | Public docs validate API file uploads, not skill bundles |

Because the true max deployable size is undocumented for most targets, the repo must operate off a conservative working budget rather than a verified universal cap.

### Smallest documented related limits

These are not all true "skill size" caps, but they are the tightest documented constraints adjacent to the skill surfaces:

- Claude Code skill-listing discovery text (`description + when_to_use`): `1,536 characters`
- Claude.ai file/project-knowledge upload: `30 MB/file`
- xAI Files API: `48-50 MB/file` depending on doc page
- OpenAI GPT/chat upload: `512 MB/file`

### Tool-specific formatting requirements and size effect

| Target | Primary artifact | Formatting requirements | Measured size effect |
|---|---|---|---|
| `codex` | `.prompt` | heading, family/skill/target lines, description line, `## Instructions`, body text | about `-2,706 bytes` vs current source body |
| `openai-skills-api` | `.prompt` | same general wrapper as `codex` | about `-2,694 bytes` vs current source body |
| `claude-code` | `.skill` | heading, family/skill/target lines, description line, `## Instructions`, body text | about `-2,700 bytes` vs current source body |
| `grok` | `.grok` | heading plus target metadata and body text | about `-2,707 bytes` vs current source body |
| `grok-build` | `.grokbuild` | heading plus target metadata and body text | about `-2,701 bytes` vs current source body |
| `chatgpt-work` | `.zip` upload bundle | generated zip packaging for manual upload | compressed artifact was `7,196 bytes` for Coach PJ |
| `claude-ai` | `.zip` upload bundle | generated zip packaging for manual upload | compressed artifact was `7,201 bytes` for Coach PJ |

Interpretation:

- For prompt-like targets, the deployable text is currently smaller than the source markdown body.
- For zip-upload targets, compressed bundle size is not a safe proxy for prompt/context load; use it only as a packaging number.

## Bottom line

- OpenAI ChatGPT Skills and Codex have clear first-class skill support.
- Claude Code has clear first-class skill support.
- Claude.ai projects/styles are documented, but I did **not** find public Anthropic docs for a separate "upload a zip skill bundle" Claude web skill surface.
- xAI Grok has documented file uploads and API file/rate limits, but I did **not** find public docs for a first-class Grok "skill bundle" product comparable to OpenAI Skills or Claude Code skills.
- For targets without documented first-class skill bundles, assume essential behavior must be embedded in the main deployable artifact unless and until we verify a supported packaging mechanism.

## Repo targets

Current targets from [family.json](../family.json):

- `grok`
- `grok-build`
- `claude-ai`
- `claude-code`
- `openai-skills-api`
- `chatgpt-work`
- `codex`

## Target matrix

| Target | Official primitive I could verify | Repo deployment method | First-class support for separate reference files? | Hard limits I could verify | Throttling / usage I could verify | Status |
|---|---|---|---|---|---|---|
| `chatgpt-work` | OpenAI Skills in ChatGPT | Manual upload of generated `.zip` bundles from `dist/chatgpt-work/uploads/` | OpenAI says skills can include supporting resources, but I did not find a published skill-bundle size limit | No published ChatGPT Skill bundle size limit found. Related ChatGPT file limits exist for GPT/chat uploads. | ChatGPT file upload caps exist; Work uses the same usage structure as Codex | Supported surface, but skill size limits are not clearly documented |
| `codex` | OpenAI Skills / Agent Skills in Codex | Local/generated per-skill `.prompt` bundles | Yes in principle: official skill format supports bundled `references/`, `scripts/`, `assets/` | No published per-skill file size limit found. Codex listing truncation exists for some metadata. | Codex usage follows ChatGPT plan / Codex pricing and credits | Strong support |
| `openai-skills-api` | OpenAI says skills are supported in the API | Repo emits hosted prompt bundles in `dist/openai-skills-api/` | Unclear from public docs reviewed | No public upload/registration size limit found | No public skill-specific rate limit found in the reviewed docs | Partially documented; packaging is ahead of the public docs I found |
| `claude-code` | Claude Code Skills | Local skill folders / `SKILL.md` | Yes: official docs explicitly support supporting files and delayed loading | No hard per-skill file size limit found; docs recommend concise skill bodies and target under 200 lines for `CLAUDE.md` files | General model/account limits apply; no separate skill throttling doc found | Strong support |
| `claude-ai` | Claude Projects, Project Knowledge, Styles | Repo emits manual `.zip` uploads in `dist/claude-ai/uploads/` | Not verified as a first-class Claude web skill product in public docs | Project knowledge: 30 MB/file; chat uploads: 20 files/chat; project knowledge unlimited files but bounded by context/RAG behavior | Plan-based Claude usage limits apply; no skill-specific throttling doc found | Public docs do not clearly validate this target model |
| `grok` | Grok chats with file uploads | Repo emits Grok text artifacts | No verified first-class skill bundle support found | Grok web/app uploads: up to ~150 MB/file; web up to ~100 files/message | Weekly usage pool on consumer Grok plans | Public docs support files, not skill bundles |
| `grok-build` | xAI API / build model (`grok-build-0.1`) | Repo emits build-target prompt bundles | No verified first-class skill bundle support found | Files API: 48-50 MB/file depending on page; no batch with document search | API rate limits documented by tier, including `grok-build-0.1` | API/model support documented; skill-bundle concept not clearly documented |

## OpenAI

### ChatGPT Skills / ChatGPT Work

Official docs:

- OpenAI Help: Skills in ChatGPT
  - https://help.openai.com/en/articles/20001066-skills-in-chatgpt
- OpenAI Help: ChatGPT Work and Codex
  - https://help.openai.com/en/articles/20001275/
- OpenAI Help: File Uploads FAQ
  - https://help.openai.com/en/articles/8555545-chatgpt-citations
- OpenAI Help: Creating and editing GPTs
  - https://help.openai.com/en/articles/8554397-creating-a-gpt

What the docs clearly say:

- ChatGPT Skills are reusable workflows and can include instructions, examples, and code.
- Skills can include supporting resources.
- Skills can be created in chat, in the editor, or uploaded from your computer.
- Skills are supported in ChatGPT and are also supported in Codex and the API.
- ChatGPT Work uses the same usage structure as Codex.

What I could not verify:

- A published hard size cap for a ChatGPT Skill bundle itself
- A published token cap for skill instructions
- A published cap on number of supporting files inside a skill bundle

Related documented limits that may matter but are not explicitly labeled as Skill limits:

- ChatGPT/GPT file uploads:
  - 512 MB per file
  - 2M tokens per text/document file
  - 20 MB per image
  - 25 GB/user and 100 GB/org storage caps
  - up to 80 files every 3 hours
- GPT knowledge:
  - up to 20 files per GPT

Important caution:

- These file-upload limits are clearly documented for GPTs and ChatGPT conversations.
- I cannot prove from the public docs that they are exactly the same limits for uploaded Skill bundles.

Repo deployment method:

- Manual upload of `.zip` bundles described in [dist/chatgpt-work/INSTALL.md](../dist/chatgpt-work/INSTALL.md)

### Codex

Official docs:

- OpenAI Help: Using Codex with your ChatGPT plan
  - https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan
- OpenAI Help: Skills in ChatGPT
  - https://help.openai.com/en/articles/20001066-skills-in-chatgpt
- OpenAI official GitHub: `openai/skills`
  - https://github.com/openai/skills
- OpenAI Codex repository example/docs
  - https://github.com/openai/codex

What the docs clearly say:

- Skills are supported in Codex.
- OpenAI Skills follow the Agent Skills open standard.
- Codex uses skills as folders with `SKILL.md` plus optional bundled resources.
- Bundled resources can include `references/`, `scripts/`, and `assets/`.

What I could verify about limits:

- I did **not** find a published hard cap on `SKILL.md` size.
- In Claude Code there is an explicit 1,536-character listing cap for `description` + `when_to_use`; Codex has no equivalent published cap in the OpenAI docs I reviewed.

Repo deployment method:

- Generated local bundles in [dist/codex](../dist/codex)

### OpenAI Skills API

Official docs reviewed:

- OpenAI Help: Skills in ChatGPT
  - https://help.openai.com/en/articles/20001066-skills-in-chatgpt

What the docs clearly say:

- OpenAI says Skills are supported in the API.

What I could **not** verify from public docs reviewed:

- The public API endpoint or workflow for uploading/registering a Skill bundle
- Any hard size limits for uploaded API Skills
- Any API-side throttling specific to Skills

Repo deployment method:

- Generated hosted-style prompt bundles in [dist/openai-skills-api](../dist/openai-skills-api)

Assessment:

- This target may be valid internally or via tooling not surfaced in the public docs I found.
- Treat it as partially documented.

## Anthropic

### Claude Code

Official docs:

- Claude Code Skills
  - https://code.claude.com/docs/en/slash-commands
- Claude Code memory / CLAUDE.md
  - https://code.claude.com/docs/en/memory
- Claude Code settings
  - https://code.claude.com/docs/en/settings
- Claude Code CLI reference
  - https://docs.anthropic.com/en/docs/claude-code/cli-usage

What the docs clearly say:

- Claude Code has first-class Skills.
- A skill is a directory with `SKILL.md`; Claude can invoke it automatically or via `/skill-name`.
- Supporting files are explicitly supported.
- Skill bodies load only when used, which makes long reference material cheaper than always-loaded `CLAUDE.md`.
- `.claude/skills/` is an official location.
- Cloud/Cowork sessions can sync skills differently from local sessions.

Documented limits / constraints:

- No hard skill-file size cap found.
- Claude Code docs explicitly say to keep the skill body concise because once loaded it persists in context across turns.
- `description` + `when_to_use` text is truncated at 1,536 characters in the skill listing Claude sees each turn.
- `CLAUDE.md` guidance says target under 200 lines per file, but that is for memory/instructions, not a formal skill limit.

Repo deployment method:

- Per-skill generated `.skill` files in `dist/claude-code/`

Assessment:

- This is a real first-class skill surface.
- Separate reference files are a supported pattern here.

### Claude.ai

Official docs:

- Claude Projects
  - https://support.claude.com/en/articles/9517075-what-are-projects
- Manage projects
  - https://support.claude.com/en/articles/9519177-how-can-i-create-and-manage-projects
- Supported document types and file limits
  - https://support.anthropic.com/en/articles/8241126-what-kinds-of-documents-can-i-upload-to-claude-ai
- Styles
  - https://support.anthropic.com/en/articles/10181068-configuring-and-using-styles

What the docs clearly say:

- Claude Projects have project knowledge and project instructions.
- Project knowledge can scale via RAG on paid plans.
- Claude supports custom Styles.

Documented limits:

- 30 MB per file for Claude chat uploads
- up to 20 files per chat
- project knowledge: 30 MB per file
- project knowledge file count described as unlimited, but bounded by context/RAG behavior

What I could **not** verify:

- A public Anthropic doc for a separate Claude web "Skills" product that accepts zip bundle uploads
- A public doc that validates this repo's `dist/claude-ai/uploads/*.zip` workflow as a supported Claude.ai product surface

Repo deployment method:

- Manual zip upload flow described in [dist/claude-ai/INSTALL.md](../dist/claude-ai/INSTALL.md)

Assessment:

- Public Anthropic docs validate Projects, Knowledge, and Styles.
- They do not clearly validate this repo's Claude AI zip-skill target.

## xAI

### Grok consumer app/web

Official docs:

- Grok FAQ
  - https://docs.x.ai/grok/faq
- Grok overview
  - https://docs.x.ai/grok/overview

What the docs clearly say:

- Grok web/apps support file uploads in chat.
- Web supports up to about 100 files in one message.
- Most files can be up to 150 MB each.
- Paid consumer plans use a weekly usage pool across products.

What I could **not** verify:

- A first-class Grok "skill bundle" product comparable to OpenAI Skills or Claude Code Skills
- A documented zip-upload skill deployment path

Repo deployment method:

- Generated Grok-target prompt artifacts in `dist/grok/`

Assessment:

- File-based context is documented.
- First-class skill bundles are not documented in the sources I reviewed.

### xAI API / `grok-build`

Official docs:

- Files overview
  - https://docs.x.ai/developers/files
- Files upload API
  - https://docs.x.ai/developers/rest-api-reference/files/upload
- Rate limits
  - https://docs.x.ai/developers/rate-limits

What the docs clearly say:

- Files API supports uploaded files for document search/chat workflows.
- One doc says file size max is 48 MB per file for document-search style use.
- The upload endpoint says maximum file size is 50 MB.
- Document-search file attachments do not support batch mode.
- xAI API rate limits are tiered by spend and model.
- `grok-build-0.1` has published RPS/TPM limits by tier.

Verified rate-limit examples:

- `grok-build-0.1`
  - Tier 0: 37 RPS / 10M TPM
  - Tier 1: 50 RPS / 15M TPM
  - Tier 2: 75 RPS / 25M TPM
  - Tier 3: 125 RPS / 45M TPM
  - Tier 4: 208 RPS / 85M TPM

What I could **not** verify:

- A first-class "skill bundle" deployment product in the xAI API

Assessment:

- The API has strong docs for files and rate limits.
- It does not clearly document a Skill product analogous to OpenAI Skills or Claude Code Skills.

## Implications for this repo

### What is safe today

- Treat `codex` and `claude-code` as true skill-native targets.
- Treat `chatgpt-work` as a documented skill surface, but without a published hard bundle-size cap in the docs reviewed.
- Treat `claude-ai`, `grok`, and `grok-build` as targets where this repo's packaging may be ahead of the public product docs.

### What this means for reference files

- For Codex and Claude Code, separate reference files are a documented and natural fit.
- For the other targets, separate reference files are only safe if the build pipeline inlines them into the final deployable prompt or if the target has a clearly documented knowledge/file mechanism you are intentionally using instead of a skill bundle.

### Current recommendation

- If behavior depends on the content, embed it in the deployable persona for all targets unless the target has verified first-class bundled-resource support.
- If we want shared references as an authoring convenience, update `skill-tooling` to inline them into non-skill-native targets during generation.

## Follow-up tasks worth doing

1. Fix target assumptions in this repo docs so `claude-ai`, `grok`, and `grok-build` are clearly labeled as "verified" or "unverified" against public docs.
2. Decide whether `openai-skills-api` is backed by an internal/private workflow or whether the target name should be treated as provisional.
3. Update `skill-tooling` so non-skill-native targets inline referenced material instead of silently dropping it.
4. Add a build-time check that fails if a source prompt references external files that are not preserved in the generated target.
