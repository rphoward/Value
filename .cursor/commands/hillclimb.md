---
description: One-command hillclimb from an external source, URL, pasted text, or resume/score an existing run.
---

Load `@.cursor/skills/workflow/SKILL.md` and execute **protocol-7-one-command-session**.

## Arguments (freeform after `/hillclimb`)

| Mode | Example | Notes |
|------|---------|-------|
| New run | `/hillclimb C:\Downloads\needham-rilke.txt` | External path |
| New run | `/hillclimb https://example.com/essay` | Agent fetches via Exa, saves temp file |
| New run | `/hillclimb` + pasted prose | Agent saves temp file |
| Resume | `/hillclimb resume rilke-hc-3iter` | Continue if `retry` true; else results card |
| Score only | `/hillclimb score rilke-hc-3iter` | Re-emit results card, no new iterations |

Optional flags in natural language: `slug`, `topic`, `iterations` (default 3, hard budget), `min-delta` (default 1.5, advisory unless `early-stop`), `early-stop` (opt-in regression/plateau halt before max iterations), `seeds` (default 3 for iter-1 emulate).

## Defaults

- Slug from source filename when omitted.
- Topic: neighboring scene in the same register — not a retell of the analyze passage; confirm in one line when the derived topic rewrites source beats.
- Register-matched held-out: after `style-block.md`, emit `held-out-brief.md` (DEIXIS/ENV/DNA), Exa-fetch 2–3 candidates, run `held_out_gate.py`, then `write_held_out` on first pass. Prefer no held-out over wrong-register. See `references/held-out-sibling.md`. Discrimination `--genuine` uses `held-out.txt` when present else `source.txt`; `--n 10`. Init may precede held-out; held-out must exist before first `job-open`.
- Seeds: 3 independent emulate-drafter candidates on iter 1; **eval-audit all**, then `seed-promote --record` (winner by **style fidelity** / qualitative mean — never raw total alone).
- Models: `composer-2.5` for emulate-drafter, revise-drafter, and eval-audit unless overridden.
- **Voice split:** SURFACE, PROSODY, CAST scored in Python (countable author voice). Nine qualitative sections scored by eval-audit (judgment voice / taste). Models are weak at counting; Python owns counts.
- **Climb metric (default):** `style_fidelity` — qualitative mean 0–100; early-stop on qualitative delta vs `min_delta` (default 1.5). Expect mid-60s → low-80s; ~80 plateau is normal under judge noise.
- **Diagnostics:** `EvaluatorScore.total` (50/50 blend) for history and weak-axis hints. Deterministic mean as floor/tie-break. Optional blind spot-the-real (`job-*`) for tells — not the default climb signal.
- **Alternates at init:** `--climb-metric indistinguishability` (legacy blind-test climb); `reference_preference_v1` with explicit `--preference-judge-model` (pairwise winner).

## Do not

- Reimplement scoring in chat; use `hillclimb_once.py` subcommands only.
- **Draft, eval, or discriminate in the parent context** — always spawn fresh subagents (see below).
- Blank-page regenerate on iters 2+ — use `revise-drafter` on `best_draft`.
- Skip eval-audit qualitative merge on `record`, or skip optional blind `job-record` when running legacy discrimination.
- Edit scorer, rubric, or calibration mid-run.
- Relax `min_delta` mid-run.
- Thematic/brainstorm material + find a suited author + a few drafts **without** scoring, preference, or discrimination — that is pipeline invent session, not this command.

## Subagents (required)

Each draft, qualitative eval, and discrimination trial **must** use the Task tool with a fresh subagent. The parent supervises only.

| Step | Task `subagent_type` | Agent file | Parent passes |
|------|---------------------|------------|---------------|
| Draft (iter 1) | `emulate-drafter` | `.cursor/agents/emulate-drafter.md` | style-block path, topic, retry brief, output path; `model: composer-2.5` |
| Draft (iters 2+) | `revise-drafter` | `.cursor/agents/revise-drafter.md` | style-block path, prior draft path (`best_draft`), retry brief, output path; `model: composer-2.5` |
| Qualitative eval | `eval-audit` | `.cursor/agents/eval-audit.md` | draft path, style-block path; `model: composer-2.5`; parent writes `qualitative-vN.json` |
| Spot-the-real | `discriminate` | `.cursor/agents/discriminate.md` | one blind trial (`passage_a`, `passage_b`, `trial_id`); parent records via `job-trial` then `job-score` / `job-record` (seed suffix: sidecar only) |
| Reference preference | `reference-preference` | `.cursor/agents/reference-preference.md` | one window packet; parent records via `pref-job-order` → `pref-job-score` → `pref-job-record` (seed pairs: sidecar only; iter 2+: attaches `preference-vN.json`) |

**Iter 1 seed round (reference preference):** for each seed pair (`a-vs-b`, …): `pref-job-open` → `reference-preference` per pending order → `pref-job-order` → `pref-job-score` → `pref-job-record`. Then `seed-status`; when `ready_to_promote`, `seed-promote --record`. Do not call `record` on `draft-v1.md` before `seed-promote`.

**Iter 1 seed round (style fidelity, default):** for each suffix `a|b|c`: emulate → eval-audit → `qualitative-v1{suffix}.json`. Then `seed-status`; when `ready_to_promote`, `seed-promote --record` (winner = highest qualitative mean). Do not call `record` on `draft-v1.md` before `seed-promote`.

**Iter 1 seed round (legacy indistinguishability):** for each suffix `a|b|c`: `job-open --seed-suffix` → discriminate all pending → `job-score` → `job-record`. Then `seed-status`; when `ready_to_promote`, `seed-promote --record`. Do not call `record` on `draft-v1.md` before `seed-promote`.

Subagents get clean context (no `scores.json`, `decision.tsv`, or score history). Revisers may read the prior draft path only. **Never** inline draft, rubric scoring, or spot verdicts in the parent. **Never** write verdicts by hand; use `job-*` on `hillclimb_once.py`.

## Resume checklist

1. `hillclimb_once.py inspect --run-dir tools/runs/<slug>` — follow exactly one `next_action`
2. `hillclimb_once.py status --run-dir tools/runs/<slug>`
3. Preference mode: `pref-job-status`; legacy: `job-status`
4. Finish any in-progress jobs before a new draft. Seed round: finish every pair/suffix, then `seed-promote --record`
5. `seed-status` — if `ready_to_promote` and iter 1 missing from scores.json → `seed-promote --record`
6. Style fidelity: if iter 1 seeds exist but not promoted → finish qualitative JSON per suffix, then `seed-promote --record`. Preference mode: `pref-job-open` batch. Legacy indist: `job-open` then full batch
7. Else if `retry` → `revise-drafter` from `best_draft`
7. Else results card.

Dense Style Block from source: parent uses ELIOT skill once for `style-block.md`, or spawn a one-shot agent with only `source.txt` + ELIOT skill if the block is not yet built.
