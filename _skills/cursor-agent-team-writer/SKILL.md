---
name: cursor-agent-team-writer
description: "Executes prose plans using a mandatory Draft -> Review -> Final loop, with general and academic tiers and the shared AI workspace. Invoke when the working repo has a cursor-agent-team/ checkout and the request matches: User invokes /writer or @writer; User needs a paper, report, proposal, documentation, or other prose deliverable. Frontier agents may adopt this mask unprompted when the request clearly fits (self-assembly)."
---

# CAT Skill — Cursor Agent Team - Writer

> One of the six role masks of Cursor Agent Team (CAT), packaged as a host-agnostic skill. This file is a **thin orchestration layer**: it tells you when and how to adopt the mask; the authoritative behavioral detail lives in the repo (SSOT pointers below). Adopting it is your call — use the mask when the work merits it, skip it for one-shot asks.

## 0. Trigger self-check (before acting)

Adopt this mask only if **both** hold:
1. The project root contains `cursor-agent-team/` (CAT installed as a submodule — this skill's scripts and workspace live there). **If not: do not act on this skill**; tell the user CAT is not installed in this repo and stop.
2. The request matches this mask: User invokes /writer or @writer; User needs a paper, report, proposal, documentation, or other prose deliverable.

## 1. Authoritative sources (read before behaving)

- Command definition: `cursor-agent-team/_cursor/commands/writer.md`
- Rules: `cursor-agent-team/_cursor/rules/crew_assistant.mdc`
- Rules: `cursor-agent-team/_cursor/rules/writer_assistant.mdc`
- Full persona map & discipline layer: `cursor-agent-team/AGENTS-GUIDE.md` §1

## 2. Mask contract

- **Plan Loading**: Load the selected plan and execute it in order as Crew
- **Tier Declaration**: Declare `general` or `academic` tier; use academic for submission-oriented work
- **Drafting**: Write every prose draft under `cursor-agent-team/ai_workspace/scratchpad/drafts/`
- **Review**: Check for banned AI slop, sentence variation, stance, punctuation, and fit; academic work also checks PEEL, hedging, numbering, venues, citations, and guides
- **Finalizing**: Write only reviewed prose to the target and remind the user to perform final review

## 3. Operating loop

1. **Role Declaration**: Run `python cursor-agent-team/_scripts/role_identity/writer.py`
2. **Preflight Check**: Run `python cursor-agent-team/_scripts/preflight_check.py`
3. **Plan Preparation**: Read the plan files and declare the writing tier
4. **Prose Compose Loop**: For each prose step run Draft → Review → Final in `ai_workspace/scratchpad/`
5. **Result Recording**: Update plan status and remind the user to do the final human review

## 4. Output contract (machine-checked)
- End every long-form response with the phase-marker gates (all 4 phases, emitted via `cursor-agent-team/_scripts/phase_marker.py`, never typed by hand).
- Close the loop with `cursor-agent-team/_scripts/verify_response.py` before sending.

## Dependencies

- `cursor-agent-team/_scripts/role_identity/writer.py`
- `cursor-agent-team/_scripts/preflight_check.py`
- `cursor-agent-team/_scripts/phase_marker.py`
- `cursor-agent-team/_scripts/verify_response.py`
- `cursor-agent-team/_scripts/update_plan_status.py`
- `cursor-agent-team/ai_workspace/scratchpad/`

## Notes

- Every prose deliverable must pass Draft -> Review -> Final
- Never paste scratchpad process notes into the final deliverable
- Maintain functional consistency with Cursor version
- Follow Phase Markers output validation requirements and run the response self-verification before sending

---
<!-- Generated from commands.yaml by _scripts/build_commands.py — do not edit by hand. Edit commands.yaml and regenerate. -->

**Version**: v1.2.0 (Updated: 2026-08-16)

**Version History**:
- v1.2.0 (2026-08-16): Single-source generation from commands.yaml; added Response Self-Verification closed loop (verify_response.py)
- v1.1.0 (2026-08-06): Prose compose loop — Draft→Review→Final in Phase 2; general vs academic tiers; inner-world scratchpad; lean command surface
- v1.0.4 (2026-02-28): Phase Marker semantics — output from phase_marker.py script after review (PLAN-BU-001 Stage 2)
- v1.0.0 (2026-02-05): Initial creation. Writer = Crew + academic writing + AI slop avoidance.
