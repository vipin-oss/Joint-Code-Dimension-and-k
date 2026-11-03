# IEEE regular paper — format compliance and submission checklist

> **Paths in this package:** manuscript in `../01_manuscript/`, code and data in
> `../04_supplementary/`, cover letter in `../02_cover_letter/`, declarations in
> `../03_declarations/`. Run the checker from the repository root with
> `python3 05_submission_checklist/compliance_check.py`.

**Paper type: regular paper** (a full journal article, *not* a letter and *not*
an IEEE "Correspondence"). IEEE Transactions on Information Theory, regular
paper track. There is no 5-page limit.

| file | purpose |
|---|---|
| `../01_manuscript/main.tex` | two-column IEEEtran journal layout (18-page PDF) |
| `../01_manuscript/main_peerreview.tex` | single-column review copy (40-page PDF) |
| `../01_manuscript/body.tex` | shared manuscript body; both wrappers `\input` it |
| `../01_manuscript/references.bib` | 31 entries — exactly the cited ones |
| `../01_manuscript/figures/` | 2 vector PDF figures and 1 PNG workflow figure |
| `../04_supplementary/` | Python code, generated data, verification logs (zip for upload) |
| `compliance_check.py` | re-runs every formal check below |
| `compliance_report.txt` | saved output of the final live run — all checks pass |
| `../02_cover_letter/COVER_LETTER.md` | submission cover letter |
| `../01_manuscript/build.sh` | rebuilds both PDFs |

```bash
cd ..
python3 05_submission_checklist/compliance_check.py
python3 -I 04_supplementary/code/checks.py
python3 04_supplementary/code/generate_tables.py
cd 01_manuscript && ./build.sh
```

---

## 1. Managed quantities (measured by `compliance_check.py` and the final build)

| item | IEEE regular-paper requirement | this paper | status |
|---|---|---|---|
| Abstract | ≤ 200 words, no citations, no displayed math | **191 words** | ok |
| Index Terms | 3–6, alphabetized, no period | **5**: Constacyclic codes, Galois hulls, LCD codes, repeated-root codes, transfer matrices | ok |
| References | no cap; 25–45 typical | **31**, every one cited, no uncited bib entries | ok |
| Figures | vector, captions below | **2 vector PDF figures and 1 PNG workflow figure** | ok |
| Tables | captions above, booktabs rules | **2**, both full width (`table*`), `\scriptsize` | ok |
| Displayed equations | numbered sequentially | **114** | ok |
| Numbered results | — | 3 theorems, 12 lemmas, 15 propositions, 6 corollaries, 2 definitions, 8 examples, 8 remarks; 34 proofs | — |
| Section structure | Introduction first, Conclusion last, then Acknowledgment, References, Appendices | 7 numbered sections + 2 appendices + Acknowledgment + References | ok |
| Length | no hard cap | **18** two-column pages; **40** single-column review pages | ok |

The compliance checker still prints a prose-based *estimate* (16–21 / 37–50
pages); the true counts above come from the final rebuilt PDFs. The 40-page
review count is already quoted in the cover letter.

## 2. Regular-paper setting already applied

* `\documentclass[journal]{IEEEtran}` for the camera-ready style; review target
  `\documentclass[12pt,journal,draftclsnofoot,onecolumn]{IEEEtran}` with
  `\baselinestretch=1.4` and `\maketitle` (single column, 40 pages). The class
  option `peerreview` alone only produces a one-column cover page and is not
  used.
* IEEE `\author` block: six `\thanks` footnotes in IEEE order — dates/funding,
  one affiliation per author, e-mail addresses, ORCID, DOI line and
  supplementary-material note.
* `abstract` + `IEEEkeywords` ("Index Terms") exactly as IEEE sets them.
* Structure: I. Introduction … VII. Conclusion, then Acknowledgment,
  References, Appendix A (support theorem) and Appendix B (orbit data).
* Elsevier-specific blocks (CRediT, competing interests, data-availability,
  generative-AI declaration, MSC codes, keyword line) are removed; a single
  IEEE Acknowledgment carries the AI-use disclosure and points to the code.
* Every float is called out in the text. The two huge decimal expansions of
  Table I are written as `3^{31}` and `5^{31}`; the widest displays are set in
  `\small`.

## 3. Fill these in before uploading (author-only)

1. Cover letter — Editor-in-Chief name, three suggested reviewers and requested
   exclusions (a prompt for finding verified reviewers is provided separately).
2. Declarations — signature date; ORCID iDs can be added in the submission form.
3. Add a grant sentence to `\thanks` #1 only if a grant applies.
4. Final accepted version only — IEEE author biographies and photographs if
   requested.

## 4. Upload list

```
01_manuscript/main_peerreview.pdf   manuscript for review
01_manuscript/                     .tex, references.bib, figures/ (source files)
04_supplementary/                  zip: code, tables, checks_output.txt,
                                   symbolic_verification.txt
02_cover_letter/COVER_LETTER.txt   paste into cover-letter field / export PDF
03_declarations/AUTHOR_DECLARATIONS.md
```

## 5. If the Associate Editor asks for a shorter paper

Apply in this order; each item moves to `../04_supplementary/` and leaves one
sentence behind in the main text.

1. The examples on `F_4 × F_16`, `F_25`, `F_32` together with Table I (≈2 pages).
2. Verification coverage Table II and its Level-2 prose (≈1 page).
3. Subsection *Short orbits* (≈1 page).
4. Compress Appendix B into three lines inside Section VII (≈0.7 page).

Even after step 1 the paper still states and proves everything: only worked
data moves.

## 6. Final self-check

- [x] `python3 05_submission_checklist/compliance_check.py` prints
      **ALL IEEE REGULAR-PAPER CHECKS PASSED**.
- [x] `./build.sh` compiles both PDFs with no undefined references/citations,
      no `??`, no errors and zero overfull/underfull boxes.
- [x] True page counts recorded: `main.pdf` 18, `main_peerreview.pdf` 40.
- [x] Cover letter quotes the real 40-page count.
- [x] Every figure/table cited; captions in the IEEE position.
- [x] Exact `python3 -I 04_supplementary/code/checks.py` prints
      `ALL CHECKS PASSED`.
- [x] `generate_tables.py` rewrites all CSVs byte-for-byte.
- [x] `MANIFEST_SHA256.txt` regenerated after all final files.
- [ ] Author-only `XXXX` placeholders replaced before upload.
- [ ] ORCID iDs of the co-authors linked in the submission system.
- [ ] No concurrent submission: the earlier internal drafts are superseded by
      this single paper.
