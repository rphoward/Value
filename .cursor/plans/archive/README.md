# Archived plans

Completed or superseded Cursor plans. **Living state:** `handoff/STATE.md`. Gate records: `handoff/*-PASSED.md`.

Last indexed: 2026-07-17.

**Stub pattern:** flat `*_fdb7afb8.plan.md` / `scorer-v2_final_phases_*.plan.md` files are Cursor stubs pointing at sibling folders with session-sized splits.

## Reverse-engineering benchmark (phases 1–17)

| Path | Gate record |
|------|-------------|
| [reverse-engineering-quality-master_da289ff7.plan.md](reverse-engineering/reverse-engineering-quality-master_da289ff7.plan.md) | Master plan |
| [phase-01](reverse-engineering/reverse-engineering-phase-01.plan.md) · [02](reverse-engineering/reverse-engineering-phase-02.plan.md) · [03](reverse-engineering/reverse-engineering-phase-03.plan.md) · [04](reverse-engineering/reverse-engineering-phase-04.plan.md) · [05](reverse-engineering/reverse-engineering-phase-05.plan.md) · [06](reverse-engineering/reverse-engineering-phase-06.plan.md) · [07](reverse-engineering/reverse-engineering-phase-07.plan.md) · [08](reverse-engineering/reverse-engineering-phase-08.plan.md) · [09](reverse-engineering/reverse-engineering-phase-09.plan.md) · [10](reverse-engineering/reverse-engineering-phase-10.plan.md) · [11](reverse-engineering/reverse-engineering-phase-11.plan.md) · [12](reverse-engineering/reverse-engineering-phase-12.plan.md) · [13](reverse-engineering/reverse-engineering-phase-13.plan.md) · [14](reverse-engineering/reverse-engineering-phase-14.plan.md) · [15](reverse-engineering/reverse-engineering-phase-15.plan.md) · [16](reverse-engineering/reverse-engineering-phase-16.plan.md) · [17](reverse-engineering/reverse-engineering-phase-17.plan.md) | `handoff/REVERSE-ENGINEERING-PHASE-*-PASSED.md` (17 skipped) |

## Reference preference + metric repair

| Path | Gate record |
|------|-------------|
| [repair-fidelity-ruler-corrected_36174a7b.plan.md](repair-fidelity-ruler-corrected_36174a7b.plan.md) | `handoff/REFERENCE-PREFERENCE-SHIPPED.md`, `handoff/PREFERENCE-ORCHESTRATION-PASSED.md`, `handoff/PREFERENCE-ORCHESTRATION-TOLSTOY-PASSED.md` |

Orchestration/Tolstoy gates shipped without separate plan files (`finish-preference-orchestration`, `tolstoy_gate_friction_fixes` were ephemeral Cursor session names).

## Scorer v2

| Path | Gate record |
|------|-------------|
| [scorer-v2_final_phases_589276ee.plan.md](scorer-v2_final_phases_589276ee.plan.md) | Cursor stub → folder below |
| [scorer-v2-final-phases/overview.md](scorer-v2-final-phases/overview.md) | `handoff/SCORER-V2-PASSED.md` |
| [phase-1-corpus](scorer-v2-final-phases/phase-1-corpus.md) · [phase-2-authorprint](scorer-v2-final-phases/phase-2-authorprint.md) · [phase-3-discrimination](scorer-v2-final-phases/phase-3-discrimination.md) · [phase-4-gate](scorer-v2-final-phases/phase-4-gate.md) · [phase-5-smoke](scorer-v2-final-phases/phase-5-smoke.md) | Session splits |
| [shared.md](scorer-v2-final-phases/shared.md) | Dispatch prompts |

## Web UI v2

| Path | Gate record |
|------|-------------|
| [web_ui_pipeline_wizard_be50658c.plan.md](web_ui_pipeline_wizard_be50658c.plan.md) | Phase 1 |
| [web_ui_pipeline_wizard_phase2_be50658c.plan.md](web_ui_pipeline_wizard_phase2_be50658c.plan.md) | Phase 2 |
| [web_ui_wizard_phase_3_db503675.plan.md](web_ui_wizard_phase_3_db503675.plan.md) | Phase 3 |
| [web_ui_wizard_4-5_bbb1e9d8.plan.md](web_ui_wizard_4-5_bbb1e9d8.plan.md) | Phases 4–5 |
| [web_ui_wizard_phase_6_0461cab1.plan.md](web_ui_wizard_phase_6_0461cab1.plan.md) | `handoff/WEB-UI-V2-PHASE6-PASSED.md` |

## Hillclimb + workflow

| Path | Gate record |
|------|-------------|
| [one-command_hillclimb_automation_a555d79b.plan.md](one-command_hillclimb_automation_a555d79b.plan.md) | `.cursor/commands/hillclimb.md` |
| [writing-first_scoring_fixes_ad2e6923.plan.md](writing-first_scoring_fixes_ad2e6923.plan.md) | Shipped 2026-07-07 |
| [revise_in_place_loop_27882297.plan.md](revise_in_place_loop_27882297.plan.md) | `handoff/REVISE-IN-PLACE-SHIPPED.md` |
| [same-book_held-out_climb_64fc1cae.plan.md](same-book_held-out_climb_64fc1cae.plan.md) | Workflow v1.9 held-out sibling |
| [pre-ui_pipeline_workflow_0c93738a.plan.md](pre-ui_pipeline_workflow_0c93738a.plan.md) | Pipeline skill contracts |
| [resolve_passage_word_bounds_250c5ad0.plan.md](resolve_passage_word_bounds_250c5ad0.plan.md) | Merged into pre-ui plan |
| [paragraph_rhythm_contract_4534d90d.plan.md](paragraph_rhythm_contract_4534d90d.plan.md) | Shipped |

## Job board + SDK climb

| Path | Gate record |
|------|-------------|
| [job_board_sdk_climb_fdb7afb8.plan.md](job_board_sdk_climb_fdb7afb8.plan.md) | Cursor stub → folder below |
| [job_board_sdk_climb/overview.md](job_board_sdk_climb/overview.md) | Phases 1–4, 6 shipped |
| [phase-1](job_board_sdk_climb/phase-1-job-board-types.md) · [phase-2](job_board_sdk_climb/phase-2-job-cli.md) · [phase-3](job_board_sdk_climb/phase-3-resume-protocol.md) · [phase-4](job_board_sdk_climb/phase-4-sdk-spike.md) · [phase-5](job_board_sdk_climb/phase-5-sdk-driver.md) (cancelled) · [phase-6](job_board_sdk_climb/phase-6-pipeline-seam.md) | Session splits |
| [testing.md](job_board_sdk_climb/testing.md) | Manual gates |
| [job_board_doc_fix/plan.md](job_board_doc_fix/plan.md) | `handoff/JOB-BOARD-DOC-FIX.md` |
| [hooks_sdk_climb/hooks,_automation_&_sdk_climb_fb104dc2.plan.md](hooks_sdk_climb/hooks,_automation_&_sdk_climb_fb104dc2.plan.md) | `handoff/HOOKS-SDK-PASSED.md` — merged to `master` 2026-07-16 |

## Climb-signal redesign + intent repair

| Path | Gate record |
|------|-------------|
| [climb_signal_redesign.plan.md](climb_signal_redesign.plan.md) + [climb_signal_redesign/](climb_signal_redesign/overview.md) | `handoff/CLIMB-SIGNAL-REDESIGN-PASSED.md` — **PASS** on `master` 2026-07-17 |
| [climb_signal_final_36cba773.plan.md](climb_signal_final_36cba773.plan.md) | Fresh-session brief; same track |
| [climb_intent_repair_f2128c14.plan.md](climb_intent_repair_f2128c14.plan.md) + [climb_signal_intent_repair/](climb_signal_intent_repair/overview.md) | `handoff/CLIMB-SIGNAL-INTENT-REPAIR-PASSED.md` — consumer contracts lock |

## Full-workflow webapp

| Path | Gate record |
|------|-------------|
| [full_workflow_webapp_829fdc0a.plan.md](full_workflow_webapp_829fdc0a.plan.md) + [full_workflow_webapp/](full_workflow_webapp/overview.md) | `handoff/FULL-WORKFLOW-WEBAPP-PASSED.md` — PR #2 |

## Eliotapp layout

| Path | Gate record |
|------|-------------|
| [eliotapp_rules_gate_fca58b8f.plan.md](eliotapp_rules_gate_fca58b8f.plan.md) | Rules gate on `master` |
| [eliotwf_app_restructure_bcfc6cd4.plan.md](eliotwf_app_restructure_bcfc6cd4.plan.md) | `handoff/ELIOTAPP-RESTRUCTURE-EVACUATE-PASSED.md` — PR #1 |
| [eliotapp_synthesis_peel.plan.md](eliotapp_synthesis_peel.plan.md) + [eliotapp_synthesis_peel/](eliotapp_synthesis_peel/) | `handoff/ELIOTAPP-SYNTHESIS-PEEL-PASSED.md` |

## Invent seeds

| Path | Gate record |
|------|-------------|
| [invent_seeds_flow_7045190e.plan.md](invent_seeds_flow_7045190e.plan.md) | Skill-first invent v1; `PIPELINE-UI-CATALOG.md` |

## Workflow build + thermos `.cursor` fixes

| Path | Gate record |
|------|-------------|
| [eliot_workflow_build.plan.md](eliot_workflow_build.plan.md) | Phases 0–6 shipped; phase 7 superseded by `HOOKS-SDK-PASSED.md` |
| [thermos_.cursor_fixes_e323cca5.plan.md](thermos_.cursor_fixes_e323cca5.plan.md) | Todos completed in later landings; archived 2026-07-17 |

## Tooling / conventions

| Path | Notes |
|------|-------|
| [def_ref_conversion.plan.md](def_ref_conversion.plan.md) | Skill reference def-ref migration (no separate gate record) |
