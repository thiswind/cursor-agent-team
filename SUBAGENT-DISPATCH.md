# SUBAGENT-DISPATCH.md — Orchestrator → Sub-agent Dispatch Best Practice

> **Who this is for**: frontier-model agents acting as **orchestrators** that spawn mid-tier sub-agents (DeepSeek-V4-Flash, Claude-Sonnet, GPT-lite class) inside Cursor / Claude Code / Codex / TRAE sessions.
>
> **Companion doc**: `AGENTS-GUIDE.md` — how a frontier agent itself uses CAT masks. This doc covers the other link: **advanced agent → sub-agents**.
>
> **Field-tested**: the dispatch template below was exercised on 2026-08-29 with 3 parallel masked sub-agents (3/3 first-return compliance); see "Evidence" at the end.

## 1. Core Principles (four)

1. **Mask explicit, harness bound to mask**: the orchestrator's task prompt states who the sub-agent is (persona file path), what constrains it (rules file path), and what it produces (output contract). A bare task description produces format drift, out-of-scope file edits, skipped verification.
2. **Minimal-complete input**: pass only the context the subtask needs (file paths + 2–5 sentence summary). Never forward the whole session history — sub-agents start cold by design; that is a feature (context isolation), not a bug.
3. **Structured return**: sub-agents return exactly the contracted fields — `summary / files_changed / verification / leftovers` — nothing else. Free-form returns are un-mergeable and unauditable.
4. **State lands in workspace**: subtask outputs and logs are persisted under `ai_workspace/` (notes / plans / topic tree / scratchpad) per CAT discipline. Anything that must survive the session lives on disk, not in orchestrator memory.

## 2. Dispatch Template (task-prompt skeleton)

```text
[Role] You are dispatched wearing the CAT mask "<mask>".
  Behavioral rules: <host>/cursor-agent-team/_cursor/rules/<mask>_assistant.mdc
  Additional hard constraints for THIS task: <1–3 items>

[Context] Host project root: <path>. 2–5 sentences of background.
  Read-only files: ... ; writable files: ...(often "none")

[Task] One-sentence goal + numbered steps + checkable acceptance criteria.

[Output Contract] Return exactly: summary / files_changed / verification / leftovers.
```

Notes from field use:

- The `[Role]` block names the persona **file paths** (command def + rules), not a prose description — the sub-agent reads the real spec, which beats any summary the orchestrator could write.
- "Read-only task: no file writes" in `[Context]` proved sufficient boundary language; all three sub-agents complied.
- Output-contract field names should be literal `files_changed: none` for read-only work — honest negatives are part of the contract.

## 3. Mask Selection Table

| Subtask profile | Mask | Why |
|-----------------|------|-----|
| Retrieval / survey / inventory across the repo | `crew` | Crew is the plan-faithful surveyor: exact steps, logged search, no improvisation |
| Deep exploration, trade-off analysis, "what should we do" | `discuss` | Breadth-and-depth analysis without execution risk |
| Prompt / role-mask authoring | `prompt_engineer` | LangGPT structure + strict naming conventions |
| PLAN → spec-kit documents conversion | `spec_translator` | Fully automatic, zero-interaction converter |
| Long prose deliverables (docs, papers) | `writer` | Draft→Review→Final loop + academic tiers |

Default to `crew` for scoped recon; reach for `discuss` only when the subtask involves judgment; never dispatch `spec_translator` interactively.

## 4. Acceptance & Rejection Discipline

- **Trust but verify**: `verification` field is a claim; the orchestrator re-runs the key check itself (e.g. re-list the directory, re-run `--check`, spot-read cited files). No sub-agent self-report releases the orchestrator from verification.
- **Rejection = reason + expected-vs-actual**: send back with the failure reason and the expected difference. Incremental repair, blind retry forbidden.
- **Two strikes rule**: two consecutive same-type failures → orchestrator takes the task back or escalates to the user. Never a third blind dispatch.

## 5. Parallel Sub-agents & Workspace Conflicts

- **Split by file boundary**: no two parallel sub-agents may own write access to the same file. (Read overlap is fine.)
- **Topic-tree write power stays with the orchestrator** during parallel runs; sub-agents get it read-only.
- **Scratchpad staging**: sub-agent intermediate artifacts go to `ai_workspace/scratchpad/<subtask>/`; the orchestrator promotes them after acceptance. Sub-agents never write directly to `plans/` or the topic tree.

## Evidence

2026-08-29, host project cursor-agent-team-workshop (PLAN-WF-001 Phase 1): orchestrator dispatched 3 parallel read-only sub-agents (crew mask) for persona-map / scripts / workspace recon. 3/3 first-return compliance with mask + output contract; 0 rejections. One sub-agent flagged a real defect family (protected-file list inconsistency) that the orchestrator verified and folded into `AGENTS-GUIDE.md`. Full log: `ai_workspace/scratchpad/analysis/dispatch_log_20260829.md` (workshop repo).

## v2 Ideas (not required by this practice)

- `role_identity/dispatch_header.py`: render mask + rules into a task-prompt prefix
- `_scripts/templates/dispatch_task.md.tmpl` for non-agent human reuse
