# Universal YouTube Branding Skill: AI channel identity for YouTube

[Tiếng Việt](README.md) | **English**

![GRAINVEYRA sample channel identity made with the skill](docs/cover.jpg)

![CI](https://github.com/ducdg88/youtube-channel-branding-skill/actions/workflows/validate.yml/badge.svg) ![license](https://img.shields.io/badge/license-MIT-green) ![version](https://img.shields.io/badge/version-1.3-blue)

An Agent Skill (`SKILL.md`) that lets an AI agent build a complete identity for a **new YouTube channel** in any niche: channel name research, SEO, logo, avatar, banner (channel art) and wordmark, then check sizes, real transparency and the YouTube safe area. Works with Google Antigravity, Claude Code, Gemini CLI, Codex and any agent that reads `SKILL.md`. Built and used in production by [DUCPT](https://ducpt.com/?utm_source=github&utm_medium=readme&utm_campaign=youtube-channel-branding-skill).

## What it produces

By default (`ASSET_PROFILE=REFERENCE_6`) the skill creates **six standalone images** for one brand:

| ID | File | Size | Purpose |
|---|---|---|---|
| 01 | `01_BANNER_CINEMATIC_2048x682.png` | 2048×682 | Panoramic hero banner with logo and name |
| 02 | `02_BATTLE_SCENE_A_1672x941.png` | 1672×941 | Story scene A (16:9) |
| 03 | `03_LOGO_PLUS_NAME_TRANSPARENT_2048x682.png` | 2048×682 | Emblem plus name, real transparent PNG |
| 04 | `04_AVATAR_ROUND_1254x1254.png` | 1254×1254 | Round avatar, readable at 98 px |
| 05 | `05_WORDMARK_TRANSPARENT_2048x682.png` | 2048×682 | Text wordmark, real transparent PNG |
| 06 | `06_BATTLE_SCENE_B_ALTERNATE_2048x1152.png` | 2048×1152 | Story scene B, different layout from A |

Plus a YouTube upload banner **2560×1440 under 6 MB** with every word and logo inside the central safe area (x 508 to 2052, y 509 to 932), following [YouTube's guidance](https://support.google.com/youtube/answer/10456525). Use `ASSET_PROFILE=LEGACY_5` for the older five-image set.

Full mode also writes `name_research.md` (20 to 30 screened names), `brand.lock.json` (locked name, palette, fonts, motif), `brand_guide.md`, `seo_keywords.csv`, `content_ideas.md`, `prompts_final.md`, `manifest.json`, `qa_report.json` and `README_upload.md`.

## Install

Clone the repo and copy `skills/universal-youtube-branding` to where your agent loads skills:

| Agent | Copy to |
|---|---|
| Google Antigravity (one project) | `<project>/.agents/skills/universal-youtube-branding/` |
| Google Antigravity (all projects) | `~/.gemini/config/skills/universal-youtube-branding/` |
| Claude Code | `~/.claude/skills/universal-youtube-branding/` or `<project>/.claude/skills/...` |
| Other `SKILL.md` agents | that agent's skills folder |

```bash
git clone https://github.com/ducdg88/youtube-channel-branding-skill.git
cp -r youtube-channel-branding-skill/skills/universal-youtube-branding ~/.claude/skills/
pip install pillow   # for the QA scripts
```

Restart the agent if the skill does not show up.

## Usage

Type a command or ask in plain language ("build a channel identity for a space documentary channel"):

```
/universal-youtube-branding MODE=FULL NICHE="Luxury Woodworking" STYLE=AUTO MARKET=Global
/universal-youtube-branding MODE=NAME NICHE="Space Documentary" MARKET=Global
/universal-youtube-branding MODE=VISUAL BRAND_NAME="My Channel" NICHE="AI Tutorials" STYLE=AUTO
/universal-youtube-branding MODE=FULL NICHE="Nature Mysteries" STYLE=REFERENCE
```

- `MODE=NAME`: niche and keyword research, 20 to 30 names, name and @handle collision screening, SEO. No images.
- `MODE=VISUAL`: with a locked name, create the six images plus the YouTube banner, then QA. Never renames a locked brand.
- `MODE=FULL`: everything from A to Z (NAME, brand lock, VISUAL, QA, upload guide).
- `STYLE=AUTO` (default): the AI picks palette, motif and fonts for the niche. `STYLE=REFERENCE`: follow the layout of your reference images (layout only, never their logo or characters). `STYLE=HYBRID`: a mix.
- Long-form channels: say `long-form` and the skill locks `content_format=LONG_FORM`, no drift into Shorts or memes.
- Spanish or other languages: the original name keeps its accents and every tagline and SEO line stays in that language.

### An image engine is required

The skill is a workflow plus QA; **the images are drawn by your agent's image generator**. Antigravity ships one. Elsewhere, connect an image model. Note: Gemini image models over the API are **not in the free tier**, billing must be enabled. Without an engine the skill outputs prompts only and reports `IMAGE GENERATION NOT AVAILABLE` instead of pretending. When the AI misspells text, the skill keeps the scene and re-composites the exact lettering.

## How it works

1. **Niche research**: main niche, 3 to 5 sub-niches, viewer needs, 4 to 6 content pillars, 15 to 30 keyword phrases.
2. **Naming**: 20 to 30 names in four styles (coined, compound, evocative, brand plus descriptor), scored, checked with exact-phrase searches. @handles stay `UNVERIFIED, CHECK IN STUDIO` until confirmed in YouTube Studio.
3. **Brand lock**: `brand.lock.json` stores name, descriptor, tagline, a five-role palette, fonts and motif. Every later image reads the same lock, so names and colors never drift.
4. **Image generation**: one generation per file, never sliced from a collage. Logo and wordmark need real alpha, never a fake checkerboard.
5. **QA**: scripts check file count, size, alpha and file size; a human checks spelling, the avatar at 98 px and the safe area on phone and TV.

QA and helper scripts (need Pillow):

```bash
python skills/universal-youtube-branding/scripts/validate_assets.py <project> --profile reference6 --report qa_report.json
python skills/universal-youtube-branding/scripts/init_project.py --brief skills/universal-youtube-branding/templates/brief.json --out ./new-channel
python skills/universal-youtube-branding/scripts/build_prompts.py --brand ./new-channel/brand.lock.json --out ./new-channel/prompts.md
python skills/universal-youtube-branding/scripts/niche_router.py --niche "Space Documentary"
```

`PASS_TECHNICAL_VISUAL_PENDING` means technically valid; a visual review is still required.

## Upload to YouTube

YouTube Studio, Customization, Branding:
- **Picture**: `04_AVATAR_ROUND_1254x1254.png`
- **Banner image**: the 2560×1440 file in `02_YOUTUBE_READY/`
- **Video watermark**: the emblem from 04 resized to 150×150

The horizontal logo and wordmark (03, 05) are for intros, thumbnails, the channel website and social profiles.

## Example: GRAINVEYRA

`skills/universal-youtube-branding/examples/luxury_woodworking/` is a full sample for a luxury woodworking niche: 5 images, 2 YouTube banners, 25-name research, SEO, 10 video ideas, prompts, manifest and QA. GRAINVEYRA is a demo name; exclusivity and @handle are not verified.

## Build a similar skill

The layout of this skill works as a template:

```
universal-youtube-branding/
  SKILL.md       # frontmatter name + description (when to use), then the step-by-step workflow
  references/    # detail loaded only when needed: naming and SEO, niche adaptation, visuals, QA
  templates/     # hard JSON specs: image sizes, sample brief, a 15-niche style library
  scripts/       # what a machine does more reliably than an AI: QA, scaffolding, prompt packs
  examples/      # one real finished set so the agent and readers see what "done" looks like
```

Lessons from building it:
- The `description` says exactly when to use the skill, because agents choose skills from that line.
- Anything that must be exact (sizes, file count, safe area) lives in JSON and scripts, not in the AI's memory.
- One shared lock file (`brand.lock.json`) feeds every step so names and colors stay consistent.
- Machine QA is only a technical gate; always state what still needs human eyes.
- Write limits plainly ("never claim a free @handle", "no engine, say so") so the AI does not make things up.

## Limits

- Web search never proves a name or @handle is free; confirm in YouTube Studio. No trademark search is done.
- Technical QA cannot catch misspelled text or a weak logo; always review visually.
- No fonts or API keys are bundled. The skill refuses to imitate an official channel of another brand or publisher.
- Layout reference images (`assets/layout_refs/`) are not shipped because they belong to other channels; add your own.

## About DUCPT

[DUCPT](https://ducpt.com/?utm_source=github&utm_medium=readme&utm_campaign=youtube-channel-branding-skill) builds AI tools, automation workflows and training for creators, YouTube channels and small businesses in Vietnam:

- [DUCPT Skills](https://ducpt.com/skills/?utm_source=github&utm_medium=readme&utm_campaign=youtube-channel-branding-skill): free Agent Skills for solo founders working with AI
- [YouTube Title Lab](https://ducpt.com/skills/youtube-title-lab/?utm_source=github&utm_medium=readme&utm_campaign=youtube-channel-branding-skill): write and score YouTube titles
- [YouTube source finder](https://ducpt.com/dich-vu/tim-nguon-youtube?utm_source=github&utm_medium=readme&utm_campaign=youtube-channel-branding-skill): find video sources for a channel
- [Tab Cộng Đồng AI](https://ducpt.com/cong-cu-ai/tab-cong-dong-ai?utm_source=github&utm_medium=readme&utm_campaign=youtube-channel-branding-skill): AI posts for the YouTube Community tab
- [Courses](https://ducpt.com/khoa-hoc/?utm_source=github&utm_medium=readme&utm_campaign=youtube-channel-branding-skill): grow channels and run a business with AI

## License

[MIT](LICENSE). Use, modify and share freely; keep the copyright notice.
