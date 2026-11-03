# START HERE — IEEE submission package

**Paper:** *Joint Code-Dimension and k-Galois-Hull Enumerators for Repeated-Root
Constacyclic Codes over Square-Free Affine Algebras*
**Type:** regular journal paper (not a letter / correspondence)
**Target:** IEEE Transactions on Information Theory (regular paper track)
**Authors:** Arun Kumar Yadav, Vipin Gupta, Manju Pruthi

This archive is the corrected, fully verified submission package. It contains
the final PDFs, the LaTeX sources, the cover letter, the declarations, the
supplementary code and data, the compliance report, the skeptical mathematics
review, the reference/attribution verification report and the final report.

```
00_READ_ME_FIRST.md            this file
01_manuscript/                 LaTeX sources, figures and both final PDFs
02_cover_letter/               cover letter (markdown + plain-text version)
03_declarations/               originality / authorship / funding / COI / data / AI-use
04_supplementary/              Python code, generated tables, verification logs
05_submission_checklist/       format compliance report + checklist
MATH_REVIEW.md                 skeptical mathematics review, gap list and fixes
REFERENCES_VERIFICATION.md     bibliography, attribution and IEEE-policy checks
FINAL_REPORT.md                change log, PR link, tests and unresolved items
MANIFEST_SHA256.txt            SHA-256 manifest of every shipped file
```

---

## Step 1 — the two final PDFs (already included)

`01_manuscript/main.pdf` is the two-column journal-layout version (**18
pages**). `01_manuscript/main_peerreview.pdf` is the single-column review copy
(**42 pages**, `\baselinestretch=1.4`). Both were rebuilt from the current
sources with `pdflatex` / `bibtex` (three `pdflatex` passes), with no undefined
references or citations, no `??`, and zero overfull/underfull boxes. No
`.aux`, `.log`, `.out`, `.bbl`, `.blg` or `__pycache__` files are shipped.

To rebuild if you change a source file:

```bash
cd 01_manuscript
./build.sh                      # builds main.pdf and main_peerreview.pdf
```

`IEEEtran.cls`, `mathtools`, `booktabs`, `microtype`, `mathrsfs` and the IEEE
bibliography style are required (a full TeX Live installation supplies them).
Overleaf also works: set the main file to `main_peerreview.tex` for the review
copy, or `main.tex` for the two-column version. Both wrappers `\input` the same
`body.tex`, so the PDFs cannot differ in content. After any rebuild, re-run the
compliance checker and re-read the true page count before quoting it in the
cover letter.

## Step 2 — fill the remaining author-only placeholders

Search for `XXXX`. The cover-letter date (**3 November 2026**) and the real
**42-page** review count are already filled in. The following still require
author input and were deliberately not invented:

| where | what |
|---|---|
| `01_manuscript/main.tex`, `main_peerreview.tex` (`\thanks`) | manuscript received/revised/accepted/publication dates, DOI line, e-mail addresses of V. Gupta and M. Pruthi |
| `02_cover_letter/COVER_LETTER.md` and `.txt` | Editor-in-Chief name, three suggested reviewers (name, affiliation, e-mail), requested exclusions |
| `03_declarations/AUTHOR_DECLARATIONS.md` | the same co-author e-mail addresses, ORCID iDs of V. Gupta and M. Pruthi, signature date |

## Step 3 — upload to the journal (exact list)

| upload slot | file |
|---|---|
| Manuscript (PDF) | `01_manuscript/main_peerreview.pdf` |
| Source files (if requested) | `01_manuscript/` (the `.tex` files, `references.bib`, `figures/`) |
| Cover letter | `02_cover_letter/COVER_LETTER.txt` (or export the `.md` to PDF) |
| Declarations / author information | `03_declarations/AUTHOR_DECLARATIONS.md` (export to PDF if a file is required) |
| Supplementary material | `04_supplementary/` as a single zip |

`05_submission_checklist/`, `MATH_REVIEW.md`, `REFERENCES_VERIFICATION.md`,
`FINAL_REPORT.md` and `MANIFEST_SHA256.txt` are for the authors and the record,
not for the journal upload.

## What is in each folder

**01_manuscript/** — complete, self-contained LaTeX source. `references.bib`
holds exactly the 31 cited references; `figures/` holds two vector PDF figures
and one PNG workflow figure. The final PDFs are built from these sources.

**02_cover_letter/** — one-page cover letter: what the paper does, the main
contributions, relation to the closest literature, suggested reviewers. `.md`
for editing, `.txt` for pasting into the web form.

**03_declarations/** — originality and no concurrent submission, authorship
and contributions, funding, competing interests, data availability, the IEEE
AI-use disclosure, ORCID, and the permissions/ethics statements.

**04_supplementary/** — the transfer-matrix enumerator, the complete
verification script, the table generator, the saved `ALL CHECKS PASSED` output,
the external symbolic moment/covariance/complexity report and the twelve CSV
files behind Table I and the figures. From the repository root, the exact
isolated-mode command is:

```bash
python3 -I 04_supplementary/code/checks.py
python3 04_supplementary/code/generate_tables.py
```

The first command checks Levels A/B/C, 21 independent finite-field families and
every printed number; the second regenerates all CSVs byte-for-byte. Shipped
code is Python standard library only; SymPy is used only in the external
verification report.

**05_submission_checklist/** — the live IEEE compliance report, the
step-by-step checklist and the compliance checker.

## Honest status of the package

* Content, structure, abstract length (**191 words**, limit 200), index terms,
  references (31, all cited), float conventions and section order were
  re-checked by `05_submission_checklist/compliance_check.py` —
  `ALL IEEE REGULAR-PAPER CHECKS PASSED`.
* Both final PDFs are included and were rebuilt from the current sources.
* The exact `python3 -I 04_supplementary/code/checks.py` ends in
  `ALL CHECKS PASSED`; all tables regenerate byte-identically.
* A full repository byte scan and PDF text extraction show no old fourth-author
  name, affiliation or proprietary-computer-algebra-system reliance.
* Bibliography DOI metadata, introduction attributions, the mathematics review,
  the IEEE AI-use policy recheck and the remaining unresolved items are
  disclosed in `REFERENCES_VERIFICATION.md`, `MATH_REVIEW.md` and
  `FINAL_REPORT.md`.
