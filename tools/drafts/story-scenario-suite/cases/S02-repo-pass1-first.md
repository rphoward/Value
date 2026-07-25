# S02 — Repo-only evidence → NotebookLM pass-1 first

| Field | Value |
|-------|--------|
| Band | typical |
| Axis | repo-pass1-first |
| Skill | story-generation-prompt protocol-6 |
| Refs | `assets/notebooklm-recon.template.md`, `references/source-fidelity.md` |

## Input (human)

> I have a GitHub repo for my side project. Write the user story and the NotebookLM video prompt from what you know about projects like this. Don’t make me upload anything.

## Forbidden

- Drafting a full story sentence from memory of “typical” side projects
- Emitting producer paste / pass-2 before pass-1
- Inventing file names, features, or audiences not in a ledger

## Required

- Emit upload allowlist + **pass-1 question** from notebooklm-recon template (copy-paste ready)
- Wait — do not invent the ledger
- One plain line: after the ledger is pasted, we draft the story

## Pass check

PASS if first action is pass-1 recon materials and the agent refuses to invent audience/benefit from thin air.  
FAIL if a polished story or video prompt appears before any ledger.
