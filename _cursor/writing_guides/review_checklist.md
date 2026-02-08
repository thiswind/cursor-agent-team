# Pre-Submission Review Checklist

> Agent-facing checklist for `/writer`. Covers submission-specific checks NOT already in `writer_assistant.mdc`.

---

## 1. Structure Completeness

1. **Title**: Accurate, ≤15 words, keywords front-loaded
2. **Abstract**: Self-contained; covers purpose, method, results, conclusion; within word limit
3. **Keywords**: 3–5, covering core concepts
4. **Introduction**: Problem statement, motivation, contributions, paper structure
5. **Method**: Detailed enough to reproduce
6. **Experiments**: Datasets, metrics, baselines, ablation
7. **Discussion**: Result analysis, limitations, future work
8. **Conclusion**: Concise summary of findings and contributions
9. **References**: Consistent format, sequential numbering, no dangling citations

## 2. Format Compliance

1. **Page limit**: 9 pages for main conferences (NeurIPS/ICML); appendix excluded
2. **Template**: Official LaTeX template; NEVER modify margins or font size
3. **Equation numbering**: Sequential (1), (2), (3)...; all referenced in text
4. **Figures/tables**: Sequential numbering, complete captions, all cited in text
5. **References**: Uniform style (IEEE/APA); no orphan entries

## 3. Language and Expression

1. **Tense**: Present for method description; past for experimental results
2. **Passive voice**: Use sparingly; active voice preferred
3. **Terminology consistency**: Same concept = same term throughout
4. **Abbreviations**: Spell out on first use; abbreviate thereafter
5. **Comparison phrasing**: USE "outperforms / comparable to"; AVOID "better / worse"

## 4. CCF-A Conference-Specific (NeurIPS/ICML/ICLR)

- **Claim ⊆ Evidence**: Abstract/intro claims must not exceed experimental scope
- **Limitations section**: MUST explicitly discuss method limitations
- **Assumptions**: All assumptions for theoretical results listed explicitly
- **Proofs**: All theorems/propositions have complete proofs (main text or appendix)
- **Reproducibility**: Code, data, hyperparameters, training details, random seeds
- **Error bars**: Mean ± std over multiple runs
- **Compute resources**: GPU type, training time, memory usage
- **Ethics statement**: Potential negative impact (privacy, fairness, bias)
- **Data license**: Dataset license and access method

## 5. Anonymization (Double-Blind)

- **Author info**: No names in text, appendix, or code
- **Self-citation**: AVOID "In [X], we showed..." → USE "Smith et al. [X] showed..."
- **Code links**: Anonymous URL or anonymous zip
- **Acknowledgments**: Remove for initial submission

## 6. Common Reviewer Red Flags

### Technical

- **Claim > Evidence**: Claims "significant improvement" without statistical test
- **Missing baselines**: No comparison with SOTA methods
- **Insufficient ablation**: Multiple innovations but no individual ablation
- **Hidden assumptions**: Using undeclared assumptions
- **Proof gaps**: Key derivation steps missing

### Writing

- **Dangling citation**: [X] in text but absent from reference list
- **Orphan figure/table**: Figure or table not cited in text
- **Numbering errors**: Equation/figure/table numbers skip or repeat
- **Symbol inconsistency**: Same variable denoted by different symbols

## 7. Pre-Submission 5-Minute Check

1. Pages ≤ limit?
2. Author info removed?
3. All figures/tables/equations cited in text?
4. Reference format uniform?
5. Conference checklist completed?

---

**Version**: v1.0.0 (2026-02-08)
