# REFERENCE_6: SIX INDEPENDENT ASSETS (v1.2 default)

The six original reference images are different deliverables; never stop at five because the second wide scene and final scene look similar. Niche design may be completely unrelated to the reference. Follow geometry and item type only.

01 Cinematic horizontal banner: 2048×682 (3:1) / title in compositional safe zone.
02 Illustrated scene A: 1672×941 / 16:9.
03 Transparent horizontal logo + name: 2048×682 / real PNG alpha.
04 Circular avatar/badge: 1254×1254 / identifiable at ~98px.
05 Transparent horizontal text wordmark: 2048×682 / real PNG alpha.
06 Alternate illustrated scene B: 2048×1152 / 16:9, different arrangement from 02.

All six assets share exact brand name, motif, palette, typography and editorial tone. If niche changes, theme and characters change; do not reuse the original animal imagery or any other niche's motifs. Make scenes separately, not crops of one moodboard. For scenes 02 and 06, maintain coherent style while using genuinely distinct character placements or compositions.

YouTube upload-ready art (bonus): 2560×1440, main text/logo inside center safe region 1544×423 (x508:2052, y509:932), file <=6MB. Exclude it from six core assets.

Use `scripts/build_prompts.py --profile reference6` to create six prompts. Use `scripts/validate_assets.py <project-root> --profile reference6` for technical QA. Visual QA requires manual review for typography, alignment, and legibility.

# LEGACY_5

The old GrainVeyra demo uses five assets. Invoke `--profile legacy5` explicitly to validate it. Do not reuse old five-asset list for a six-reference user task.
