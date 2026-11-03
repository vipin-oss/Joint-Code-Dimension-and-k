# Final report — corrected, fully verified submission package

**Pull request:** [https://github.com/vipin-oss/Joint-Code-Dimension-and-k/pull/1](https://github.com/vipin-oss/Joint-Code-Dimension-and-k/pull/1) — `submission-ready` → `main` (PR #1, open).
**Working branch:** `arena/96131abd-joint-code-dimension-and-k`, pushed to `origin`; the remote `submission-ready` ref is advanced to the same final commit that contains this report and the regenerated manifest.
**Required base:** `fix-theorem-brace-and-magma` / `2eb31db`. No history was amended, reset, force-pushed or rewritten.

---

## 1. Change log

Commit graph after the final report/manifest commit:

```
4cc8f52  main (base of the original repository snapshot)
   |
329b511  fix-branch prerequisite
   |
2eb31db  fix-theorem-brace-and-magma (required submission-ready base)
   |
9ff5f5b  Remove fourth author from the submission package
   |
7af447c  Fix LaTeX compilation and serious box warnings
   |
80f949c  Add independent finite-field verification and fix isolated-mode checks
   |
dfb071d  Finalize verified submission package, math review and materials
   |
(final)  Add FINAL_REPORT.md and regenerate MANIFEST_SHA256.txt
```

The later required commits were already linear descendants of `2eb31db`; no cherry-pick or history rewrite was needed. Final PDFs were committed in `dfb071d`.

### What changed

- **Authors / material cleanup (`9ff5f5b`, carried forward):** exactly three authors in both wrappers, both PDFs, cover letters, declarations and README; removed old fourth-author name, affiliation, contact text and "all four" wording. Yadav remains corresponding author. Whole-word source and full-repository/PDF byte scans show zero hits for the removed strings.
- **LaTeX / build (`7af447c`, `dfb071d`):** compile fixes, `\emergencystretch=2em`, `-halt-on-error` build script with no suppression, final `cor:global-support` wording, zero overfull/underfull boxes, no undefined references/citations or `??`, no `.aux/.log/.out/.bbl/.blg/__pycache__` committed.
- **Independent verification (`80f949c`, `dfb071d`):** `enumerator.py` and `checks.py` fixed for `python3 -I`, robust factorization, real Gram-rank hull dimensions, compatibility using `F.m-k`, cached enumerator, corrected `W()` and incompatible self-orthogonal count. Added the 21st Level-C family `F64-over-F8` (order-3 twist, `3 | 1+2^5=33`, `3 ∤ 1+2^2=5`, `gcd(3,3)=3`). Saved `checks_output.txt`, `symbolic_verification.txt`, 12 CSVs, and `README_SUPPLEMENTARY.md` are current. Shipped code is Python standard-library only.
- **Skeptical math review (`MATH_REVIEW.md`, `dfb071d`):** 12-item gap list and fixes inverse-Frobenius exponent, componentwise maps, `d_s=em_s`, Debnath agreement, telescoping sign, incompatible extremal factors, complexity bound and `N_F^{comp}`, Appendix-A convexity/vertex wording, even-`M` endpoint contradictions, Appendix-B irreducibility description, three-level verification rewrite, and code/manuscript count consistency.
- **Reference / attribution / policy (`REFERENCES_VERIFICATION.md`, `dfb071d`):** 31 Crossref DOI metadata checks, introduction-attribution corroboration, published-Debnath notation caveat, IEEE AI-use policy recheck. Both wrappers now carry the same IEEE-compliant AI-use disclosure identifying Arena.ai Agent Mode, the sections and the level of assistance; `03_declarations/AUTHOR_DECLARATIONS.md` mirrors it.
- **Submission materials (`dfb071d`):** final PDFs `main.pdf` (18 pages) and `main_peerreview.pdf` (42 pages); cover-letter date **3 November 2026** and real **42-page** count filled in; declarations, checklist, top-level README, saved compliance report and supplementary README updated; visual inspection of all three figures and both table pages performed.
- **This commit:** `FINAL_REPORT.md` with the PR link, tests, author-only `XXXX` items and every unverified claim/reference; regenerated `MANIFEST_SHA256.txt`.

---

## 2. Test results

| check | command / method | result |
|---|---|---|
| Exact isolated-mode verification | `python3 -I 04_supplementary/code/checks.py` | exit 0; final line `ALL CHECKS PASSED`; Levels A1–A10, 11 Table-I rows, Examples 7.1/7.2/8.1/5.9, 7 Level-B Gram-rank families, **21** Level-C independent brute-force families, 10 printed-number checks; saved to `04_supplementary/code/checks_output.txt` |
| Table regeneration | `python3 04_supplementary/code/generate_tables.py` | 11 summary rows + 11 joint files; `git diff -- 04_supplementary/tables` empty (byte-identical) |
| External symbolic checks | `04_supplementary/code/symbolic_verification.txt` | SymPy 1.14.0 re-derived `E[Y]`, `E[Y^2]`, `Var(Y)`, adjacent-edge moments/covariance, `nu_M`, `v(2,M)`, `Var(M-e_f)=M(M+2)/12`, `Cov(kappa,eta)=0`, complexity and coefficient-bit formulas; `grep -rni 'import sympy' --include='*.py' .` returns none |
| Final PDF rebuild | `pdflatex` → `bibtex` → `pdflatex` → `pdflatex` for both wrappers | `main.pdf` 18 pages, `main_peerreview.pdf` 42 pages; zero `Overfull|Underfull`; zero undefined references/citations; zero `??`; zero errors |
| PDF text zero-hit | PyMuPDF text extraction + word-boundary regex | both PDFs: zero hits for removed author strings, old affiliation, proprietary-CAS names and "four authors" |
| Full repository byte scan | all files except `.git`, word-boundary regex | zero hits for the same target strings |
| IEEE compliance | `python3 05_submission_checklist/compliance_check.py` | `ALL IEEE REGULAR-PAPER CHECKS PASSED`; 191-word abstract, 5 alphabetized index terms, 6 `\thanks`, 7 sections, 31 cited/31 present references, 2 vector PDF + 1 PNG figure, 2 tables; saved to `05_submission_checklist/compliance_report.txt` |
| Visual inspection | rendered pages 14–16 and all three figure assets | workflow figure, two joint-distribution plots, Table I and Table II are clean; no LaTeX junk, clipping or stale author text |
| Bibliography metadata | four batched Crossref DOI queries (8+8+8+7) | all **31** DOIs returned Crossref records; caveats listed in §4 |
| Manifest | `MANIFEST_SHA256.txt` regenerated after all final files | every shipped file hashed; manifest itself excluded |

Build junk was removed before the final commit. The peer-review wrapper uses `\baselinestretch=1.4` (IEEEtran `draftclsnofoot` defaults to 1.5) so the enlarged verification section still yields the real **42-page** review copy quoted in the cover letter.

---

## 3. Author-only `XXXX` items (not invented)

These remain for the authors; the final report deliberately does not fabricate them:

1. Manuscript received, revised, accepted, publication and current-version dates in both `\thanks` #1 footnotes.
2. DOI line `10.1109/TIT.2026.XXXXXXX` in both wrappers.
3. E-mail addresses of V. Gupta and M. Pruthi in `\thanks` #3–#4 and in `AUTHOR_DECLARATIONS.md`.
4. ORCID iDs of V. Gupta and M. Pruthi.
5. Editor-in-Chief name in `COVER_LETTER.md` / `.txt`.
6. Three suggested reviewers (name, affiliation, e-mail) and any requested exclusions.
7. Signature date in `AUTHOR_DECLARATIONS.md`.
8. Grant number / funding sentence if a grant actually applies (currently declared "no external funding").
9. Journal-specific ORCID links, biographies and photographs for the final accepted version, if requested.

Already filled from verifiable facts: cover-letter date **3 November 2026** and the **42-page** review count. The corresponding author's e-mail and ORCID `0009-0009-1169-3264` are retained from the source, but the ORCID value itself was not independently verified (see §4).

---

## 4. Every unverified / unresolved claim and reference

1. **Introduction attributions are not full-text verified.** All 31 DOIs returned Crossref records and the listed introduction claims were corroborated by publisher pages, arXiv abstracts/introductions or search-result abstracts, but no line-by-line full-text comparison of every attributed result was performed. Corroborating pages are listed in `REFERENCES_VERIFICATION.md`.
2. **Published full text of Debnath et al. (2026) not retrieved.** ScienceDirect provides the abstract, introduction and section snippets behind access control; the exact technical hypotheses of the published article were not read line by line. The publisher introduction confirms `q=p^e` and factorization over `F_q` projected into components, while arXiv v1 uses `r | 1+p^{e-k}` and `gcd(ord(lambda),n')=1`. The manuscript's Introduction retains the reported `1+p^{e-k}` condition; the component theory uses `1+p^{d_s-k}` with `d_s=e m_s`. The exact `e-k` versus `d_s-k` relation across the published theorem and the present component theory remains unresolved and is disclosed rather than silently harmonised.
3. **Crossref metadata caveats.** `wildeBrun2008` has no page field in Crossref (DOI/title give `064302`); `eldinLeroy2026` lacks volume/page; `bouyuklieva2026` lacks a page (Springer/arXiv say article 39); titles for `jitmanZ4`, `dinh2012`, `dinhai2010` are MathML-garbled in Crossref but corroborated by other fields; Crossref online dates often precede volume years. These are metadata gaps, not missing DOIs.
4. **IEEE AI-use policy.** The official IEEE Author Center page was fetched and requires Acknowledgments disclosure, identification of the AI system, the specific sections, the level of involvement, no AI authorship and human accountability. Secondary summaries are consistent: [1](https://libguides.iou.edu.gm/c.php?g=1482669&p=11059806), [2](https://www.enago.com/responsible-ai-movement/publisher-ai-guidelines/ieee-ai-guidelines/), [3](https://www.monperrus.net/martin/generative-ai-scientific-writing). Journal-specific submission-form fields beyond the official policy were **not** checked.
5. **Author declarations not independently audited.** Originality, no concurrent submission, no prior publication, no funding, no competing interests, no external datasets, permissions/ethics, author approval and willingness to pay charges are author statements, not independently verified facts. Until the suggested reviewers are named, their lack of conflicts of interest cannot be checked.
6. **Corresponding-author ORCID.** `0009-0009-1169-3264` is carried from the source but was not queried against ORCID.
7. **F32 root-exponent shortcut.** The printed orbit skeleton and regenerated tables are checked by the shipped code; an entirely separate re-derivation of that shortcut outside the shipped code was not recorded.
8. **Mathematics review scope.** `MATH_REVIEW.md` is a skeptical line-by-line review plus executable checks, not a formal proof-assistant certificate. All proofs remain subject to author and peer review.
9. **"Every printed number is verified."** This is verified for the manuscript examples, captions, Table I/II and supplementary tables by `checks.py`; it does not extend to dates, ORCID values, page counts or author-supplied metadata placeholders.
10. **No old fourth-author names/affiliation** is verified by full-repository and PDF text scans; **no proprietary-CAS reliance** is verified by the same scans plus the standard-library-only import check. These are positive verified results, not unresolved claims.

---

## 5. Deliverables

- `01_manuscript/main.pdf` — 18-page two-column journal layout.
- `01_manuscript/main_peerreview.pdf` — 42-page review copy.
- `01_manuscript/{main.tex,main_peerreview.tex,body.tex,references.bib,build.sh,figures/}` — current sources.
- `02_cover_letter/COVER_LETTER.{md,txt}` — date and 42-page count filled; editor/reviewers still author-only.
- `03_declarations/AUTHOR_DECLARATIONS.md` — three authors, IEEE AI-use disclosure.
- `04_supplementary/` — stdlib code, 21-family checks, saved `ALL CHECKS PASSED` output, symbolic report, 12 byte-identical CSVs.
- `05_submission_checklist/` — live compliance report and corrected checklist.
- `MATH_REVIEW.md`, `REFERENCES_VERIFICATION.md`, `FINAL_REPORT.md`, `MANIFEST_SHA256.txt`.

**PR:** [https://github.com/vipin-oss/Joint-Code-Dimension-and-k/pull/1](https://github.com/vipin-oss/Joint-Code-Dimension-and-k/pull/1)
