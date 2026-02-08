# SCI Writing Pitfalls

> Agent-facing reference for `/writer`. Covers format, formula, and structure rules NOT already in `writer_assistant.mdc`.

---

## 1. Section Numbering (IEEE / CCF-A)

- **Correct hierarchy**: `# 3. Method` → `## 3.1 Overview` → `### 3.1.1 Problem`
- **NEVER use x.0**: IEEE disallows `3.0`; start from `3.1`
- **Continuity**: No skipping (e.g. 3.1 → 3.3); numbers must be consecutive
- **Cross-ref sync**: After renumbering, update all in-text "Section x.x" references

## 2. Heading Format (IEEE)

- **L1 (##)**: Title case, centered. AVOID colons and question marks.
- **L2 (###)**: Left-aligned, italic. AVOID colons.
- **L3/L4**: Run-in (inline with body text). Colons permitted.
- **Descriptive > directory-style**: AVOID `### 3.1.1 Problem Setup` → USE `### 3.1.1 Embedding Challenges in Time Series`

## 3. Format Prohibitions

- **AVOID `---` horizontal rules**: Not academic format. Use section headings to separate.
- **AVOID excessive bold in body**: Distracts readers. Let language convey importance.
- **AVOID `——` (Chinese em dash)**: Use comma or colon instead.
- **AVOID colons/question marks in headings**: IEEE prohibits them at L1/L2.
- **Bold is correct for**: First definition of a term (e.g., **mask-weighted distance**); step labels (**Step 1:**).

## 4. Formula and Symbol Conventions

### 4.1 Symbol Explanation Scope (CCF-A)

- **Paper-specific symbols**: MUST explain on first use (e.g., $\boldsymbol{G}(\boldsymbol{z})$, $\mathcal{L}_{\text{geo}}$)
- **Standard math**: No explanation needed ($\mathbb{R}$, $\sum$, $\arg\min$, $\|\cdot\|$)
- **Domain-standard**: No explanation needed ($\nabla$, $\mathbb{E}[\cdot]$)
- **Chinese draft vs. English final**: Chinese draft may over-explain; English final follows CCF-A convention (only new symbols)

### 4.2 No Chinese in Formulas

- AVOID `\text{需满足}` → USE `\text{s.t.}`
- AVOID `\text{其中}` → USE `where` in body text
- AVOID `\text{miss_rate}` → USE `$r_{\mathrm{miss}}$`

### 4.3 LaTeX Pitfalls (Markdown Environment)

- **`%` in `\text{}`**: Parsed as comment. Escape: `\text{10\%-15\%}`
- **Block formula line breaks**: Multi-line `\[...\]` may fail to render. Write on single line, or use `aligned`:

```latex
\[\begin{aligned}
d_{\mathcal{M}}^2 &\approx Q_i \\
&= \Delta \boldsymbol{z}^{\top} \boldsymbol{G} \Delta \boldsymbol{z}
\end{aligned}\]
```

## 5. Terminology and Citation Rules

- **New term format**: `Chinese name (English name) [citation]` — e.g., 度规网络 (metric network) [13]
- **Classic terms** (LLE, PCA, Transformer): No citation needed; reviewers are domain experts
- **Pre-submission citation verification** (MUST):
  1. Paper exists (verify via Google Scholar)
  2. Author names spelled correctly
  3. Venue name correct
  4. Year, volume, pages correct
- **GB/T 7714-2015 format**:
  - Journal `[J]`: Author. Title[J]. Journal, Year, Vol(Issue): Pages.
  - Conference `[C]`: Author. Title[C]//Conference. Year: Pages.
  - Preprint `[EB/OL]`: arXiv: xxxx.xxxxx, Year.

## 6. Structure Organization

- **AVOID dual frameworks**: Do not simultaneously use "three problems" AND "three stages" for the same method. Pick one organizational scheme.
  - Stage framework: clear flow, maps to section numbers
  - Problem framework: highlights problem-driven contributions
- **Complexity analysis**: AVOID a standalone subsection. Instead: one sentence at end of each subsection, or compare in experiments, or put in appendix.

## 7. Multi-Chapter Merge Rules

### 7.1 Reference Merge Workflow

1. Collect references from each chapter
2. De-duplicate (same author + title + year)
3. Renumber by first-appearance order: [1], [2], ...
4. Update all in-text citations to new numbers
5. Verify every [n] has a matching entry

**Order**: Merge body text → merge references → update citation numbers

### 7.2 Equation Numbering Strategy

- **Chapter-prefix** (1.1), (1.2), (3.1): Good for Chinese drafts; local edits don't cascade
- **Global sequential** (1), (2), (3): Good for English final; by appearance order

### 7.3 Section Number Continuity

- Verify no gaps (e.g. Section 1 → Section 3 without Section 2)
- Update cross-references ("as described in Section 3" → confirm number is correct)
- Add placeholder for incomplete sections: `> **[TODO]** This section is pending`

---

**Version**: v1.0.0 (2026-02-08)
