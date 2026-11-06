# Channel Brand Studio v3.0: 10 AI brand concepts for a YouTube channel

[Tiếng Việt](README.md) | **English**

![Ten brand directions for one channel: you pick, then the AI exports](docs/cover.png)

![CI](https://github.com/ducdg88/youtube-channel-branding-skill/actions/workflows/validate.yml/badge.svg) ![license](https://img.shields.io/badge/license-MIT-green) ![version](https://img.shields.io/badge/version-3.0-blue)

An Agent Skill (`SKILL.md`) for **approval-first** YouTube channel branding. The agent proposes **10 genuinely different brand concepts** (symbol, name treatment, palette, typography), **you choose**, and only then does it export **exactly the files you ask for**, checking each one. Works with Claude Code, Google Antigravity, Gemini CLI, Codex and any agent that reads `SKILL.md`. Built and used in production by [DUCPT](https://ducpt.com/?utm_source=github&utm_medium=readme&utm_campaign=youtube-channel-branding-skill).

## What is new in v3.0

- **10 concept previews, not 10 finished images.** Default 10, any count from 1 to 20. Each concept is a full brand direction, not a colour swap.
- **The agent never picks for you.** Without your choice the job sits at `AWAITING_USER_SELECTION`.
- **No forced six-image kit.** You define the outputs: just avatar and banner (2 files), or add wordmark, horizontal logo, watermark, any size and format. The old six-image set is the optional `REFERENCE_6` profile.
- **One lock file**, `brand.lock.json`, written at approval so every later file keeps the same name, spelling and palette.
- **Any change needs a new approval.** A new selection, spec, preview check or edited file voids the earlier approval; `bundle` re-checks every file's sha256 before zipping.
- **Honest QA.** Scripts check count, size, format and real transparency; `technical_pass` is not visual approval, a human still reviews.

![Eight-stage workflow and an example: pick concept 04, export only 3 files](docs/demo/workflow.png)

## Workflow

| Step | `studio.py` command | State after | What happens |
|---|---|---|---|
| 1 | `init` | `PREVIEWS_PENDING` (no name yet: `AWAITING_NAME_SELECTION`) | Create the job: channel name, niche, concept count |
| 2 | `set-name` | `PREVIEWS_PENDING` | Approve a name when the AI suggested names; until then previews and selection are blocked |
| 3 | `check-previews` | `AWAITING_USER_SELECTION` (errors: `PREVIEWS_INCOMPLETE`) | Check the 10 concept images (1 to 20), one file each |
| 4 | `select` | `AWAITING_OUTPUT_SPEC` | You pick, edit or mix; writes `brand.lock.json` |
| 5 | `lock-spec` | `PRODUCTION` | Lock the file list, pixel sizes, formats, transparency |
| 6 | `check-final` | `REVIEW_REQUIRED` (errors: `PRODUCTION_INCOMPLETE`) | Check every file, record size and sha256 |
| 7 | `approve-final --confirmed` | `COMPLETE` | You review visually and approve |
| 8 | `bundle` | `COMPLETE` | ZIP with files, `brand.lock.json`, spec, QA report, `manifest.json` |

## Install

Copy `skills/channel-brand-studio` to where your agent loads skills:

| Agent | Copy to |
|---|---|
| Claude Code (all projects) | `~/.claude/skills/channel-brand-studio/` |
| Claude Code (one project) | `<project>/.claude/skills/channel-brand-studio/` |
| Google Antigravity | `<project>/.agents/skills/channel-brand-studio/` |
| Other agents | attach `SKILL.md`, `docs/WORKFLOW.md`, `docs/CLAUDE_BUILD_PROMPT.md` |

```bash
git clone https://github.com/ducdg88/youtube-channel-branding-skill.git
cp -r youtube-channel-branding-skill/skills/channel-brand-studio ~/.claude/skills/
pip install pillow   # for image QA
```

## Try the workflow (Python 3.9+)

Run inside `skills/channel-brand-studio`:

```bash
python scripts/studio.py init --dir ./test_job --niche "Example topic" --name "EXAMPLE BRAND" --count 10
python scripts/studio.py status --dir ./test_job
# job created without --name? approve one first: python scripts/studio.py set-name --dir ./test_job --name "Channel Name"
# connect an image provider, save 10 real previews as test_job/previews/01.png ... 10.png
python scripts/studio.py check-previews --dir ./test_job
python scripts/studio.py select --dir ./test_job --ids 03
# lock outputs only after the user approves them:
python scripts/studio.py lock-spec --dir ./test_job --spec configs/sample_custom_assets.json
# produce the files into test_job/final/, then:
python scripts/studio.py check-final --dir ./test_job
# after the client reviews the files and agrees:
python scripts/studio.py approve-final --dir ./test_job --confirmed
python scripts/studio.py bundle --dir ./test_job
python tests/test_studio.py   # stage gate tests
```

The scripts manage state, write briefs and check files. They **do not call a paid image model** or deploy a website. Without an image provider the skill shows labelled concept proposals only.

## Inside the skill

```
skills/channel-brand-studio/
  SKILL.md                    # 8-stage workflow, approval gates, limits
  docs/WORKFLOW.md            # state table, wizard for a commercial site, QA
  docs/CLAUDE_BUILD_PROMPT.md # prompt for an AI to build a white-label site
  docs/USER_GUIDE_PUBLIC.md   # 5-step guide for end users
  configs/                    # defaults, 3-file CUSTOM sample, optional REFERENCE_6
  scripts/studio.py           # init, set-name, status, check-previews, select, lock-spec, check-final, approve-final, bundle
  scripts/demo_gallery.py     # builds an illustrative HTML selection gallery
  examples/                   # 10 neutral concept briefs, gallery page labelled as mockup
  tests/test_studio.py        # gates: no name, no selection, no approval, files changed after QA are all blocked
```

## About the README images

Both images are built with HTML and SVG from `docs/demo/` (`cover.html`, `workflow.html`, `concepts.js`, `demo.css`). AURIVAN is a fictional channel name; these are not AI renders. Rebuild with headless Chrome:

```bash
chrome --headless=new --hide-scrollbars --window-size=1600,900 --force-device-scale-factor=2 --virtual-time-budget=15000 --screenshot=docs/cover.png docs/demo/cover.html
```

## Legacy v1.3: universal-youtube-branding

`skills/universal-youtube-branding/` stays as it was: one brand, six images by default (`REFERENCE_6`), `MODE=NAME` (20 to 30 screened names and SEO), `MODE=VISUAL`, `MODE=FULL`, the `validate_assets.py`, `init_project.py`, `build_prompts.py` and `niche_router.py` scripts, and the GRAINVEYRA example in `examples/luxury_woodworking/`.

```
/universal-youtube-branding MODE=FULL NICHE="Luxury Woodworking" STYLE=AUTO MARKET=Global
python skills/universal-youtube-branding/scripts/validate_assets.py <project folder> --profile reference6 --report qa_report.json
```

Use v3.0 when you want several directions to choose from before any export.

## Limits

- Name search helps screening only; it never proves a name or @handle is free. Check in YouTube Studio. No trademark search.
- Technical QA cannot catch misspelled text inside an image or an ugly logo; always review visually.
- Reference uploads need usage rights. Do not imitate another channel or brand.
- No fonts, API keys or customer channel data are included. Image quality depends on the provider you connect.

## About DUCPT

[DUCPT](https://ducpt.com/?utm_source=github&utm_medium=readme&utm_campaign=youtube-channel-branding-skill) builds AI tools, automation workflows and training for creators, YouTube channels and small businesses in Vietnam. More free skills: [DUCPT Skills](https://ducpt.com/skills/?utm_source=github&utm_medium=readme&utm_campaign=youtube-channel-branding-skill), [YouTube Title Lab](https://ducpt.com/skills/youtube-title-lab/?utm_source=github&utm_medium=readme&utm_campaign=youtube-channel-branding-skill).

## License

[MIT](LICENSE). Use, modify and share freely; keep the copyright line.
