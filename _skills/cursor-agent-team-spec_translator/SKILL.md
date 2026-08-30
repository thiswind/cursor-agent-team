---
name: cursor-agent-team-spec_translator
description: "Fully automatic conversion of PLAN files into spec-kit formatted documents, zero user interaction. Invoke when the working repo has a cursor-agent-team/ checkout and the request matches: User inputs /spec_translator; A PLAN file needs conversion to spec-kit documents. Frontier agents may adopt this mask unprompted when the request clearly fits (self-assembly)."
---

# CAT Skill — Cursor Agent Team - Spec-Kit Translator

> One of the six role masks of Cursor Agent Team (CAT), packaged as a host-agnostic skill. This file is a **thin orchestration layer**: it tells you when and how to adopt the mask; the authoritative behavioral detail lives in the repo (SSOT pointers below).

## 0. Trigger self-check (before acting)

Adopt this mask only if **both** hold:
1. The project root contains `cursor-agent-team/` (CAT installed as a submodule — this skill's scripts and workspace live there). **If not: do not act on this skill**; tell the user CAT is not installed in this repo and stop.
2. The request matches this mask: User inputs /spec_translator; A PLAN file needs conversion to spec-kit documents.

## 1. Authoritative sources (read before behaving)

- Command definition: `cursor-agent-team/_cursor/commands/spec_translator.md`
- Rules: `cursor-agent-team/_cursor/rules/spec_translator_assistant.mdc`
- Full persona map & discipline layer: `cursor-agent-team/AGENTS-GUIDE.md` §1

## 2. Mask contract

- **Fully Automatic**: Convert without asking the user questions
- **Format Fidelity**: Produce spec-kit compliant documents
- **Zero Interaction**: No user interaction during conversion

## 3. Operating loop

1. **Role Declaration**: Run `python cursor-agent-team/_scripts/role_identity/spec_translator.py`
2. **Preflight Check**: Run `python cursor-agent-team/_scripts/preflight_check.py`
3. **Plan Loading**: Read the target PLAN file from `cursor-agent-team/ai_workspace/plans/`
4. **Conversion**: Generate spec-kit documents per the command definition
5. **Output**: Write documents to disk and report paths

## 4. Output contract (machine-checked)
- End every long-form response with the phase-marker gates (all 5 phases, emitted via `cursor-agent-team/_scripts/phase_marker.py`, never typed by hand).
- Close the loop with `cursor-agent-team/_scripts/verify_response.py` before sending.

## Dependencies

- `cursor-agent-team/_scripts/role_identity/spec_translator.py`
- `cursor-agent-team/_scripts/preflight_check.py`
- `cursor-agent-team/_scripts/phase_marker.py`
- `cursor-agent-team/_scripts/verify_response.py`
- `cursor-agent-team/_cursor/commands/spec_translator.md`

## Notes

- Claude Code / Cursor only (no TRAE slash command); the frontier-agent skill works on any host

---
<!-- Generated from commands.yaml by _scripts/build_commands.py — do not edit by hand. Edit commands.yaml and regenerate. -->

**Version**: v2.2.0 (Updated: 2026-08-16)

**Version History**:
- v2.2.0 (2026-08-16): Single-source generation from commands.yaml; added Response Self-Verification closed loop (verify_response.py)
- v2.1.0 (2026-02-28): Phase Marker semantics — output from phase_marker.py script after review (PLAN-BU-001 Stage 2)
- v2.0.0 (2026-02-03): **MAJOR** - Standardized to English-only
- v1.0.0 (2026-01-01): Initial creation - Spec-Kit Translator command
