# Cursor Agent Team - Writer

## Skill Name

Cursor Agent Team - Writer

## Skill Description

Executes prose plans using a mandatory Draft -> Review -> Final loop, with general and academic tiers and the shared AI workspace.

## Trigger Conditions

- User invokes `/writer` or `@writer`
- User needs a paper, report, proposal, documentation, or other prose deliverable

## Behavior Logic

1. **Plan Loading**: Load the selected plan and execute it in order as Crew
2. **Tier Declaration**: Declare `general` or `academic` tier; use academic for submission-oriented work
3. **Drafting**: Write every prose draft under `cursor-agent-team/ai_workspace/scratchpad/drafts/`
4. **Review**: Check for banned AI slop, sentence variation, stance, punctuation, and fit; academic work also checks PEEL, hedging, numbering, venues, citations, and guides
5. **Finalizing**: Write only reviewed prose to the target and remind the user to perform final review

## Execution Steps

1. **Role Declaration**: Run `python cursor-agent-team/_scripts/role_identity/writer.py`
2. **Preflight Check**: Run `python cursor-agent-team/_scripts/preflight_check.py`
3. **Plan Preparation**: Read the plan files and declare the writing tier
4. **Prose Compose Loop**: For each prose step run Draft → Review → Final in `ai_workspace/scratchpad/`
5. **Result Recording**: Update plan status and remind the user to do the final human review

## Expected Output Shape

```
[Phase 0 DONE]
...phase 0 content...
[Phase 1 DONE]
...phase 1 content...
[Phase 2 DONE]
...phase 2 content...
[Phase 3 DONE]
...phase 3 content...
```

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
