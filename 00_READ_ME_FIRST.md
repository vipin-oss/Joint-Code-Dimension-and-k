# START HERE — IEEE submission package

**Paper:** *Joint Code-Dimension and k-Galois-Hull Enumerators for Repeated-Root
Constacyclic Codes over Square-Free Affine Algebras*
**Type:** regular journal paper (not a letter / correspondence)
**Target:** IEEE Transactions on Information Theory (regular paper track)
**Authors:** Arun Kumar Yadav, Vipin Gupta, Pooja Soni, Manju Pruthi

This archive contains **only** what is needed to submit the paper. Nothing else.

```
00_READ_ME_FIRST.md            this file
01_manuscript/                 LaTeX sources + figures (compile this)
02_cover_letter/               cover letter (markdown + plain-text version)
03_declarations/               originality / authorship / funding / COI / data / AI-use
04_supplementary/              Python code, generated tables, verification log
05_submission_checklist/       format compliance report + checklist
```

---

## Step 1 — build the two PDFs (5 minutes)

LaTeX could not be run when this package was assembled (no TeX installation in
the build environment), so **the PDFs are not included**. Build them yourself in
any of these three ways.

**a) Overleaf (easiest, nothing to install)**

1. Upload `01_manuscript/` as a new project (drag the whole folder, or the zip of
   it).
2. Set the main file to `main_peerreview.tex` and press *Recompile* →
   `main_peerreview.pdf`. This is the file you upload for review.
3. Switch the main file to `main.tex` and recompile → `main.pdf`. This is the
   journal-layout version (keep it for yourself / final version).

**b) Local TeX Live / MiKTeX**

```bash
cd 01_manuscript
./build.sh                      # builds main.pdf and main_peerreview.pdf
# or explicitly:
pdflatex main_peerreview && bibtex main_peerreview && pdflatex main_peerreview && pdflatex main_peerreview
```

`IEEEtran.cls` is required (Debian/Ubuntu: `texlive-publishers`; MiKTeX installs
it on demand).

**c) About the review copy:** `main_peerreview.tex` uses the standard IEEE review
options (`12pt, journal, draftclsnofoot, onecolumn`) with `\maketitle`
(single column, double spaced, about 40 pages). The class option `peerreview`
alone would only make a one-column cover page and keep the body two-column.

After compiling, check the console for `??` (undefined references) and
`There were undefined citations` — there must be none. Then note the page count
of `main_peerreview.pdf` and write it into the cover letter
(`02_cover_letter/COVER_LETTER.md`, paragraph 2).

## Step 2 — fill the placeholders (10 minutes)

Search for `XXXX` in the whole package. There are only a few:

| where | what |
|---|---|
| `01_manuscript/main.tex`, `main_peerreview.tex` (`\thanks`) | manuscript received/revised/accepted dates, DOI line, e-mail addresses of V. Gupta, P. Soni, M. Pruthi |
| `02_cover_letter/COVER_LETTER.md` and `.txt` | date, editor name, reviewer suggestions (3 names), page count |
| `03_declarations/AUTHOR_DECLARATIONS.md` | the same e-mail addresses, signature date |

## Step 3 — upload to the journal (exact list)

| upload slot | file |
|---|---|
| Manuscript (PDF) | `main_peerreview.pdf` — after you compile it |
| Source files (if requested) | `01_manuscript/` (the `.tex` files, `references.bib`, `figures/`) |
| Cover letter | `02_cover_letter/COVER_LETTER.txt` (or export the `.md` to PDF) |
| Declarations / author information | `03_declarations/AUTHOR_DECLARATIONS.md` (export to PDF if a file is required; otherwise paste the fields into the form) |
| Supplementary material | `04_supplementary/` as a single zip |

`05_submission_checklist/` is for **you**, not for the journal — keep it.

## What is in each folder

**01_manuscript/** — the complete, self-contained LaTeX source.
`main.tex` (two-column journal layout) and `main_peerreview.tex` (single-column,
double-spaced, what reviewers read) both `\input` the same `body.tex`, so the two
PDFs can never differ in content. `references.bib` holds exactly the 31 cited
references; `figures/` holds the three vector figures.

**02_cover_letter/** — one-page cover letter: what the paper does, the four
contributions, relation to the closest literature, suggested reviewers. `.md` for
editing, `.txt` for pasting into the web form.

**03_declarations/** — everything a journal asks about besides the paper:
originality and no concurrent submission, authorship and contributions,
funding, competing interests, data availability, AI-tool disclosure (IEEE
policy), ORCID, and the permissions/ethics statements.

**04_supplementary/** — the program and its output: the transfer-matrix
enumerator, the complete verification script, the script that regenerates the
tables, the saved verification log (`ALL CHECKS PASSED`), and the twelve CSV
files behind Table I and the figures. Running `python3 code/checks.py`
reproduces every number in the paper (≈30 s, no dependencies beyond the Python
standard library).

**05_submission_checklist/** — the automated compliance report (abstract length,
index terms, references, floats, structure, page estimate) and the
step-by-step checklist, including what to do if the Associate Editor asks for a
shorter paper.

## Honest status of the package

* Content, structure, abstract length (192 words, limit 200), index terms,
  references (31, all cited), float conventions and section order were verified
  by `05_submission_checklist/compliance_check.py` — all checks pass.
* The two PDFs must be produced by you (Step 1); they are the only missing
  artefacts, and they are required by every editorial system.
* All numbers in the paper are reproduced by the supplied code; the saved log is
  in `04_supplementary/code/checks_output.txt`.
