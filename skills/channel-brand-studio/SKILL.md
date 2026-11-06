---
name: channel-brand-studio
version: 3.0.1
description: >-
  White-label YouTube channel branding workflow, approval first. Creates 10 (1 to 20) distinct brand
  concept previews (logo or symbol, name treatment, palette, typography), waits for the user to pick,
  then delivers only the final assets the user asked for, with technical QA. Use when the user says
  "brand concepts", "10 logo directions", "channel branding", "brand studio", "bộ nhận diện kênh",
  "10 phương án logo", "làm thương hiệu kênh YouTube", "chọn concept rồi mới xuất ảnh".
---
# CHANNEL BRAND STUDIO v3.0: MULTI-CONCEPT / APPROVAL-FIRST

## Purpose
A reusable, niche-neutral, commercial-friendly workflow for crafting identities for creator channels. This is not affiliated with YouTube. **The initial 10 images are ten independent BRAND CONCEPT PREVIEWS, NOT ten images of one finished kit.** After approval, produce the desired deliverables; **never assume the user wants six final images**.

## NON-NEGOTIABLE STAGE GATE
1. `INTAKE` (script: `init`; state `PREVIEWS_PENDING`, or `AWAITING_NAME_SELECTION` when no name yet): user enters a name OR requests name generation OR provides existing logo/reference; collect niche, audience, language, mood (optional), output goals. If not given, choose editable creative defaults. Preserve the user's exact spelling and diacritics.
2. `NAME_REVIEW` (if name requested; script: `set-name`, state `AWAITING_NAME_SELECTION` until then): produce distinct candidate names, label name/handle clearance as **unverified** without a live check. Do not promise exclusivity. User approves one before previews; if the user supplied a name, skip name approval.
3. `PREVIEW_BATCH` (script: `check-previews`; state `AWAITING_USER_SELECTION`, or `PREVIEWS_INCOMPLETE`): default **10 independent concept preview images**, user can choose 1-20 (and more only if implementation supports). Each preview MUST show a credible identity direction: symbol/logo concept, readable channel-name treatment if available, color system and visual language. Each should meaningfully differ (composition, iconography, palette, type, mood); not just color swaps. Preview assets must be individually inspectable, with a numbered gallery/contact sheet as a secondary index. An illustration or stock scene with no branding IS NOT a brand concept.
4. `SELECT` (script: `select`; state `AWAITING_OUTPUT_SPEC`): show variants #01 to #10 (or requested N), invite choice(s), modifications, and mixing approved features. **DO NOT AUTO-SELECT**, DO NOT start production based on your own preference. Save selected concept ID, modifications, and precise locked brand decisions. If selection not received, status=`AWAITING_USER_SELECTION`, remain paused awaiting response; no fake background execution.
5. `OUTPUT_SPEC` (script: `lock-spec`; state `PRODUCTION`): ask or infer requested final products from explicit user instructions. Profiles: `CUSTOM` (default; freely configurable asset types/dimensions/formats/count), `REFERENCE_MATCH` (match user-supplied images and size; only with rights), `REFERENCE_6` (optional legacy six-asset layout), `YOUTUBE_BASIC` (optional avatar+banner+logo). Never force any profile or count. User can choose any subset and custom dimensions. Make preview safe zone when banner for YouTube is included.
6. `PRODUCE` (state stays `PRODUCTION` while files are made): create separate final files for approved concepts. Respect selected concept design lock, language, spelling and logo; no hallucinated asset or export. Prefer layered typography/compositing to keep text correct. Design has to look like a brand identity, not just a wildlife/picture thumbnail. Produce outputs only with available image engine; prompt-only mode must be clearly identified.
7. `QA` (script: `check-final`, then `approve-final`; state `REVIEW_REQUIRED`, `PRODUCTION_INCOMPLETE`, then `COMPLETE`): validate counts, dimensions, MIME, file integrity and transparency where requested. Semantic QA needs human check for name spelling, consistency, logo legibility, rights; `technical_pass` is NOT `visual_approved`. For bad outputs regenerate only affected assets and revalidate.
8. `DELIVER` (script: `bundle`): `deliverables.zip` holds the approved asset files under `assets/`, `brand.lock.json`, `output_spec.lock.json`, `reports/final_qa.json` and a `manifest.json` (size and sha256 of every asset). `bundle` re-checks every file against the QA record and refuses if anything changed. A job is `COMPLETE` only after `approve-final`; otherwise it stays in `REVIEW_REQUIRED` or an earlier state. Do not claim automatic background work if runtime lacks it.

## Multi-variant plan
- 10 default, up to 20 per batch; stage previews first to control rendering cost. User may opt into full production for all 10/20; require clear confirmation of additional cost and expected output count.
- Preview IDs immutable and sorted; no duplicate or overly similar styles; preserve separate filenames. Provide gallery with labels (e.g. #01 forest cinematic, #02 geometric editorial) plus each individual image.
- If engine cannot render N at once, create *sequential or queued jobs* with progress; only deliver completed items; retry failed jobs with limits. No mockup placeholders presented as finished AI assets.

## Brand consistency
Single source of truth `brand.lock.json`. `select` writes the exact channel name, locale, niche, selected concept IDs and the approved notes (`--notes`, put the agreed palette, icon, typography and exclusions there). Every later file follows it. A new `check-previews` marks it `SUPERSEDED`; a new `select` rewrites it, and the job audit log in `job.json` keeps the history. Never leak reference project names or images into public examples.

## Neutrality / rights / privacy
White-label. All shipped demo data is fake or generic; no identifiable user channels, private content, secret keys or proprietary references. For public paid use verify licensing, user upload rights, privacy/storage/retention policies; disclose AI generation and cost. Never guarantee a trademark, YouTube handle, content copyright or quality outcome. Do not assume privileged access to any website, account or deployment target.

## When installed in Claude or Antigravity
1. Read `docs/WORKFLOW.md` and `configs/defaults.json` (paths are relative to this skill folder; run the commands below from it).
2. For a user project: `python scripts/studio.py init --dir ./jobs/my-project --niche "Your niche" --name "Your name" --count 10`. Without `--name` the job waits in `AWAITING_NAME_SELECTION`; after the user approves a name run `python scripts/studio.py set-name --dir ./jobs/my-project --name "Exact Name"`.
3. Generate REAL previews via an approved image provider; save them in `jobs/my-project/previews/` as `01.png`, `02.png` and so on (one file per concept), and tell the user which provider made them.
4. Validate previews with `python scripts/studio.py check-previews --dir ./jobs/my-project`, show them, and wait.
5. Only after the user selects a concept: `python scripts/studio.py select --dir ./jobs/my-project --ids 03`.
6. Write the exact final asset list as a spec JSON (same shape as `configs/sample_custom_assets.json`), get the user to approve it, then `python scripts/studio.py lock-spec --dir ./jobs/my-project --spec path/to/desired_assets.json`.
7. Produce real assets into `jobs/my-project/final/`, run `python scripts/studio.py check-final --dir ./jobs/my-project`, show the files, and only after the user says yes run `approve-final --confirmed`, then `bundle`.
8. Changing the selection, the spec, the previews or any final file clears the approval: run `check-final` and get a new `approve-final` before `bundle`.

## Honest capability boundaries
These scripts manage state, produce generation briefs and check files. They do NOT independently call a paid image model or deploy a website. Agent must connect a licensed image service in the target environment. When user asks for a demo without an image provider, show labeled *concept proposals only*, not fictional generated image files.
