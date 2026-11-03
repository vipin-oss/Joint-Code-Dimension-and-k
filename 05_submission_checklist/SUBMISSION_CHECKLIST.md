# IEEE regular paper — format compliance and submission checklist

> **In this submission package** the manuscript is in `../01_manuscript/`
> (`main.tex`, `main_peerreview.tex`, `body.tex`, `references.bib`,
> `figures/`), the code and data are in `../04_supplementary/`, the cover letter
> in `../02_cover_letter/` and the declarations in `../03_declarations/`.
> To re-run the formal checks: `python3 compliance_check.py` (it finds the
> manuscript automatically), or `cd ../01_manuscript && python3 ../05_submission_checklist/compliance_check.py`.

**Paper type: regular paper** (a full journal article, *not* a letter and *not*
an IEEE "Correspondence"). IEEE Transactions on Information Theory, regular
paper track. There is no 5-page limit here; the paper is set for the normal
journal length and structure.

Everything in this folder belongs to that one regular paper:

| file | purpose |
|---|---|
| `main.tex` | **two-column IEEEtran journal layout** (regular-paper format, camera-ready style) |
| `main_peerreview.tex` | the *same* regular paper in **single-column, double-spaced** form, which is what the editorial system wants for review |
| `body.tex` | the manuscript body; both wrappers `\input` it, so the two PDFs can never diverge |
| `references.bib` | 31 entries — exactly the cited ones |
| `figures/` | 3 vector PDF figures |
| `supplementary/` | Python code + all generated data + verification log (zip for upload) |
| `compliance_check.py` | re-runs every formal check below and re-measures the budgets |
| `compliance_report.txt` | saved output of the last run — **all checks pass** |
| `COVER_LETTER.md` | submission cover letter (fill the placeholders) |
| `build.sh` | builds both PDFs |

```bash
cd paper/ieee
python3 compliance_check.py     # formal checks + budgets, no LaTeX needed
./build.sh                      # main.pdf and main_peerreview.pdf
```

---

## 1. Managed quantities (measured by `compliance_check.py`)

| item | IEEE regular-paper requirement | this paper | status |
|---|---|---|---|
| Abstract | ≤ **200 words**, no citations, no displayed math | **191 words** | ok |
| Index Terms | 3–6, alphabetized, no period | **5**: Constacyclic codes, Galois hulls, LCD codes, repeated-root codes, transfer matrices | ok |
| References | no cap; 25–45 typical for this journal | **31**, every one cited, no uncited bib entries | ok |
| Figures | vector, captions **below** | **2 vector PDF figures and 1 PNG workflow figure** | ok |
| Tables | captions **above**, booktabs rules | **2**, both full width (`table*`), `\scriptsize` | ok |
| Displayed equations | numbered sequentially (1), (2), … | **93** | ok |
| Numbered results | — | 3 theorems, 12 lemmas, 15 propositions, 6 corollaries, 2 definitions, 8 examples, 8 remarks; **34 proofs** | — |
| Section structure | Introduction first, **Conclusion** last, then Acknowledgment, References, Appendices | **7** numbered sections + **2** appendices + Acknowledgment + References | ok |
| Length | no hard cap for a regular paper | **≈15–19 two-column pages** (≈35–47 pages in the double-spaced review format), 8.8k words of prose | ok |

The page figure is an estimate produced by the checker from the prose length,
the number of displays, figures, tables and references; read the true count off
`main.pdf` after the first build and put it in the cover letter.

## 2. Regular-paper setting that is already applied

* `\documentclass[journal]{IEEEtran}` — two columns, Times, 10 pt, US Letter,
  IEEE section/equation numbering, IEEE-styled theorem headings, journal
  running head (`\markboth`) and the `\IEEEpubid` copyright line.
* Review target: `\documentclass[12pt,journal,draftclsnofoot,onecolumn]{IEEEtran}`
  with `\maketitle` (single column, double spaced; about 40 pages). *Note: the class
  option `peerreview` alone only produces a one-column cover page and leaves the
  body two-column, so it is not used.*
* IEEE `\author` block: six `\thanks` footnotes in the IEEE order — dates and
  funding and corresponding author, one affiliation per author, e-mail
  addresses, ORCID, DOI line, supplementary-material note.
* `abstract` + `IEEEkeywords` ("Index Terms") exactly as IEEE sets them.
* Structure of a regular paper: I. Introduction (with an explicit
  "The paper is organized as follows") … VII. **Conclusion** (singular, IEEE
  style), then **Acknowledgment**, **References**, then **Appendix A**
  (proof of the support theorem) and **Appendix B** (computing the orbit data).
  Moving the longest proof and the preprocessing routine to appendices is
  standard for a regular paper and keeps the main text readable.
* Only IEEE matter: the Elsevier-specific blocks (CRediT, competing interests,
  data-availability statement, generative-AI declaration, MSC codes, keyword
  line) are **removed**; a single IEEE Acknowledgment points to the code.
* Every float is called out in the text (`Fig. 1`–`Fig. 3`, `Table I`,
  `Table II`); the two huge decimal expansions of Table I were replaced by
  `3^{31}` and `5^{31}` (expansions are in the `F_{32}` example) so that the
  table cannot overflow; the widest 7 of the 93 displays are set in `\small`.
* Unnumbered appendix proof closes with `■`, IEEE style.

## 3. Fill these in before uploading (search for `XXXX`)

1. `\thanks` #1 — manuscript received / revised / accepted / publication dates.
2. `\thanks` #2–#4 — e-mail addresses of V. Gupta and M. Pruthi, and
   confirm that A. K. Yadav is the corresponding author.
3. `\thanks` #6 — DOI line (leave as `XXXXXXX` until the editorial office
   assigns it; delete the line for the first submission if you prefer).
4. `\thanks` #1 — if you have a grant, add "This work was supported by …" with
   the grant number (IEEE requires it when applicable).
5. Final accepted version only: IEEE author biographies
   (`\begin{IEEEbiography}`) and, if the journal asks, photographs.

## 4. Upload list

```
main_peerreview.pdf        manuscript for review (double spaced)
figures/*.pdf              Fig. 1–3 (3 files)
references.bib             optional
supplementary.zip          enumerator.py, checks.py, generate_tables.py,
                           checks_output.txt, summary_families.csv, joint_*.csv
COVER_LETTER.md            paste into the cover-letter field / export as PDF
```

## 5. If the Associate Editor asks for a shorter paper (nothing is lost)

Apply in this order; each item moves to `supplementary/` and leaves one sentence
behind in the main text.

1. The examples on `F_4 × F_16`, `F_25`, `F_32` (labels `ex:mixed`, `ex:char35`,
   `ex:F32`) together with **Table I** → saves ≈2 pages.
2. **Verification coverage table (Table II)** and its two paragraphs → saves
   ≈1 page; the sentence "every table and example is reproduced by
   `checks_output.txt`" stays.
3. Subsection *Short orbits* (`prop:short-orbits`, `ex:a2M2`) → saves ≈1 page.
4. Compress Appendix B into three lines inside Section VII (the algorithm and
   `prop:complexity` are in the main text and stay) → saves ≈0.7 page.

Even after step 1 the paper still states and proves everything: only worked
data moves.

## 6. Other venues (only if you change your mind)

| venue | what changes |
|---|---|
| **IEEE Trans. Inf. Theory** (this package) | nothing; regular paper |
| **IEEE Trans. Inf. Theory, Correspondence** | *not used* — a 5-page correspondence cannot hold this paper |
| **IEEE Access** | keep the regular-paper structure; re-add the section headings `AUTHOR CONTRIBUTIONS`, `FUNDING`, `CONFLICTS OF INTEREST`, `DATA AVAILABILITY` (text is in `../main.tex`), abstract 150–250 words (current 191 is fine), APC applies |
| **Designs, Codes and Cryptography / Finite Fields Appl. / LAA** | use the non-IEEE version in `../main.tex` (Elsevier-style front and back matter) |

## 7. Final self-check

- [ ] `python3 compliance_check.py` prints **ALL IEEE REGULAR-PAPER CHECKS PASSED**.
- [ ] `./build.sh` compiles both PDFs with no `??` citations and no undefined references.
- [ ] `main.pdf` page count recorded (estimate: 15–19 pages) and quoted in the cover letter.
- [ ] All `XXXX` placeholders replaced.
- [ ] Every figure/table cited in the text; captions in the IEEE position.
- [ ] `python3 supplementary/checks.py` prints `ALL CHECKS PASSED`.
- [ ] ORCID of the corresponding author linked in the submission system.
- [ ] No concurrent submission of the two earlier drafts — they are superseded
      by this single paper (see `../PAPER_COMPARISON_REPORT.md`).
