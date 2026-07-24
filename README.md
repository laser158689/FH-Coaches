# FH-Coaches

Field hockey coaching skill family managed under the `skill-tooling` family-repo contract, with shared media-handling conventions for clips, screenshots, drawings, and example-footage references.

## Family

- `field-hockey-coaching`
- 17 coordinated skills
- Recommended entry point: `field-hockey-coaching-staff`

## Repository Contract

- `family.json` holds family metadata and publish targets.
- `source/*.md` contains the canonical authored skills.
- `dist/<target>/` contains generated deployable artifacts.
- Local `.env` files are for secrets only and must remain untracked.
- Public community interactions must follow [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) and [SECURITY.md](SECURITY.md).

## Skills

- `field-hockey-coaching-staff`
- `field-hockey-head-coach`
- `field-hockey-offense-coach`
- `field-hockey-defense-coach`
- `field-hockey-special-teams-coach`
- `field-hockey-rules-coach`
- `field-hockey-skills-tactics-coach`
- `field-hockey-research-coach`
- `field-hockey-strength-conditioning-coach`
- `field-hockey-mental-skills-coach`
- `field-hockey-college-recruiting-coach`
- `field-hockey-national-development-coach`
- `field-hockey-forward-coach`
- `field-hockey-midfield-coach`
- `field-hockey-backfield-coach`
- `field-hockey-goalie-coach`
- `field-hockey-opposing-coach`

## Shared Media Capability

This family is still coach-first. AV/media handling is a common capability used by the coaches, not a separate assistant persona.

The shared media capability should support four things:

1. Give the user explicit, plain-language instructions for what to share so the coaches can analyze it well.
2. Produce coach-facing outputs such as diagrams, annotated stills, and structured clip notes when the user asks for something to save or share.
3. Analyze media carefully across replays, slow motion, camera-angle changes, and partial sequences.
4. Maintain a library of example-footage references for the coaches using public URLs, timestamp ranges, and short descriptions of what the clip demonstrates.

## Example Footage Rules

The coaching family may reference public footage, but it must not serve or mirror video itself.

- Always point to a public URL.
- Always include a time index or time range.
- Always include a short plain-language description of what the clip demonstrates.
- Prefer official or rights-holder sources when available.
- Mark clips by coach and topic so they can be reused across the family.
- Seed the library from Olympic and world-championship-level field hockey from the last eight years, including indoor where public footage exists.

## Common Commands

Generate deployable target folders:

```bash
skill-deploy --source .
```

Publish to all configured targets in `family.json`:

```bash
skill-deploy --source . --publish
```

## ChatGPT Work

For manual ChatGPT Work upload, use the generated files in `dist/chatgpt-work/`.
Start with `dist/chatgpt-work/INSTALL.md`, then copy the generated `.prompt` files into the ChatGPT Work Skills UI.

## Claude AI

For manual Claude Desktop / `claude.ai` skill creation, use the generated files in `dist/claude-ai/`.
Start with `dist/claude-ai/INSTALL.md`, then create or import one Claude skill per generated `.skill` file.

## Discussions Safety

If you enable GitHub Discussions for this repository:

- Treat every post as public and indexable.
- Do not allow posting of athlete medical details, private contact information, or non-public video links.
- Do not use Discussions for vulnerability disclosure; use [SECURITY.md](SECURITY.md).
- Use the pinned maintainer notice in [docs/discussion-safety-notice.md](docs/discussion-safety-notice.md).
