---
name: channel-brand-studio
version: 3.0.0
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
1. `INTAKE`: user enters a name OR requests name generation OR provides existing logo/reference; collect niche, audience, language, mood (optional), output goals. If not given, choose editable creative defaults. Preserve the user's exact spelling and diacritics.
2. `NAME_REVIEW` (if name requested): produce distinct candidate names, label name/handle clearance as **unverified** without a live check. Do not promise exclusivity. User approves one before previews; if the user supplied a name, skip name approval.
3. `PREVIEW_BATCH`: default **10 independent concept preview images**, user can choose 1-20 (and more only if implementation supports). Each preview MUST show a credible identity direction: symbol/logo concept, readable channel-name treatment if available, color system and visual language. Each should meaningfully differ (composition, iconography, palette, type, mood); not just color swaps. Preview assets must be individually inspectable, with a numbered gallery/contact sheet as a secondary index. An illustration or stock scene with no branding IS NOT a brand concept.
4. `SELECT`: show variants #01 to #10 (or requested N), invite choice(s), modifications, and mixing approved features. **DO NOT AUTO-SELECT**, DO NOT start production based on your own preference. Save selected concept ID, modifications, and precise locked brand decisions. If selection not received, status=`AWAITING_USER_SELECTION`, remain paused awaiting response; no fake background execution.
5. `OUTPUT_SPEC`: ask or infer requested final products from explicit user instructions. Profiles: `CUSTOM` (default; freely configurable asset types/dimensions/formats/count), `REFERENCE_MATCH` (match user-supplied images and size; only with rights), `REFERENCE_6` (optional legacy six-asset layout), `YOUTUBE_BASIC` (optional avatar+banner+logo). Never force any profile or count. User can choose any subset and custom dimensions. Make preview safe zone when banner for YouTube is included.
6. `PRODUCE`: create separate final files for approved concepts. Respect selected concept design lock, language, spelling and logo; no hallucinated asset or export. Prefer layered typography/compositing to keep text correct. Design has to look like a brand identity, not just a wildlife/picture thumbnail. Produce outputs only with available image engine; prompt-only mode must be clearly identified.
7. `QA`: validate counts, dimensions, MIME, file integrity and transparency where requested. Semantic QA needs human check for name spelling, consistency, logo legibility, rights; `technical_pass` is NOT `visual_approved`. For bad outputs regenerate only affected assets and revalidate.
8. `DELIVER`: ZIP assets and manifest, approval notes, thumbnails, QA report. Mark `COMPLETE` only once all requested deliverables exist, QA passes, and relevant approvals are satisfied; otherwise leave as `BLOCKED` or `AWAITING_USER_*`. Do not claim automatic background work if runtime lacks it.

## Multi-variant plan
- 10 default, up to 20 per batch; stage previews first to control rendering cost. User may opt into full production for all 10/20; require clear confirmation of additional cost and expected output count.
- Preview IDs immutable and sorted; no duplicate or overly similar styles; preserve separate filenames. Provide gallery with labels (e.g. #01 forest cinematic, #02 geometric editorial) plus each individual image.
- If engine cannot render N at once, create *sequential or queued jobs* with progress; only deliver completed items; retry failed jobs with limits. No mockup placeholders presented as finished AI assets.

## Brand consistency
Single source of truth `brand.lock.json`: exact channel name, locale, tagline, selected concept ID, palette, primary icon, typography, appearance, exclusions. Lock at approval. On revision keep version history. Never leak reference project names or images into public examples.

## Neutrality / rights / privacy
White-label. All shipped demo data is fake or generic; no identifiable user channels, private content, secret keys or proprietary references. For public paid use verify licensing, user upload rights, privacy/storage/retention policies; disclose AI generation and cost. Never guarantee a trademark, YouTube handle, content copyright or quality outcome. Do not assume privileged access to any website, account or deployment target.

## When installed in Claude or Antigravity
1. Read `docs/WORKFLOW.md` and `configs/defaults.json` (paths are relative to this skill folder; run the commands below from it).
2. For a user project: `python scripts/studio.py init --dir ./jobs/my-project --niche "Your niche" --name "Your name" --count 10`.
3. Generate REAL previews via approved image provider; save images in `jobs/my-project/previews/` named `01.png` etc; update `manifest.json` to identify provider outputs.
4. Validate previews with `python scripts/studio.py check-previews --dir ./jobs/my-project`.
5. Only after user selects a concept: `python scripts/studio.py select --dir ./jobs/my-project --ids 03`.
6. Lock exact final asset specifications in `request.json`; approve them and call `python scripts/studio.py lock-spec --dir ... --spec path/to/desired_assets.json`.
7. Produce real assets via available provider, then `python scripts/studio.py check-final --dir ...`; bundle files only when valid.

## Honest capability boundaries
These scripts manage state, produce generation briefs and check files. They do NOT independently call a paid image model or deploy a website. Agent must connect a licensed image service in the target environment. When user asks for a demo without an image provider, show labeled *concept proposals only*, not fictional generated image files.
