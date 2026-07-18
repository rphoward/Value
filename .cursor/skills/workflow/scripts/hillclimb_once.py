#!/usr/bin/env python3
"""Backward-compatible entry for hillclimb run-folder CLI.

Orchestration lives in /hillclimb + workflow SKILL.md. This script only
persists run state under tools/runs/<slug>/ via hillclimb_cli submodules.
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCRIPT_ROOT = Path(__file__).resolve().parent
if str(_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_ROOT))

from hillclimb_cli.common import agent_prompt_hash as _agent_prompt_hash
from hillclimb_cli.discrimination import (
    cmd_job_open as _cmd_job_open,
    cmd_job_record as _cmd_job_record,
    cmd_job_score as _cmd_job_score,
    cmd_job_status as _cmd_job_status,
    cmd_job_trial as _cmd_job_trial,
)
from hillclimb_cli.entry import main
from hillclimb_cli.preference import (
    cmd_pref_job_open as _cmd_pref_job_open,
    cmd_pref_job_order as _cmd_pref_job_order,
    cmd_pref_job_record as _cmd_pref_job_record,
    cmd_pref_job_score as _cmd_pref_job_score,
    cmd_pref_job_status as _cmd_pref_job_status,
)
from hillclimb_cli.run import (
    cmd_decision as _cmd_decision,
    cmd_freeze as _cmd_freeze,
    cmd_init as _cmd_init,
    cmd_inspect as _cmd_inspect,
    cmd_prepare as _cmd_prepare,
    cmd_prompt_hash as _cmd_prompt_hash,
    cmd_record as _cmd_record,
    cmd_record_discrimination as _cmd_record_discrimination,
    cmd_record_preference as _cmd_record_preference,
    cmd_seed_promote as _cmd_seed_promote,
    cmd_seed_status as _cmd_seed_status,
    cmd_status as _cmd_status,
    cmd_validation_open as _cmd_validation_open,
)

__all__ = ["main"]

if __name__ == "__main__":
    raise SystemExit(main())
