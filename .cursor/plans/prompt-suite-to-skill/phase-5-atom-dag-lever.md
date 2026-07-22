# Phase 5. Atom DAG lever

Back-link: [overview.md](./overview.md)

## Goal

Encode the value-era lesson that unlocks ≠ requires and that standard mode must visit every non-soft-skip atom. Give poteto a rerunnable DAG auditor and a synthesis checklist so agents do not hand-wave the tree.

## Changes

- Add `tools/prompt-suite-compile/audit_dag.py` (the simulator used in the lean-mvp audit). Modes. `standard` must cover all atoms; `express` must cover spine only; report soft-but-blocking mislabels.
- Extend FOR_AGENTS curriculum step. synthesize atoms from IR modules → write `atoms.json` + `section-map.json` → run `audit_dag.py` → fix until green.
- Optional. emit soft/hard defaults from structural keywords (gate, rubric, optional) as suggestions only; agent still owns labels.

## Data structures

- Atom record unchanged from value (`id`, `module`, `asks`, `accepts_summary`, `requires`, `unlocks`, `gate`, `soft`, `section`).
- Audit report JSON. `missing_hard`, `missed_soft`, `soft_but_required_by`, `unlock_require_mismatches`.

## Verification

**Static.** `audit_dag.py` on `skills/value` and `skills/lean-mvp` matches known expectations (value standard complete; express skips documented).

**Runtime.** Broken toy atoms fixture fails the audit with a clear missing-hard list.
