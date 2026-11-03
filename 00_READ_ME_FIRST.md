# START HERE — Finite Fields and Their Applications submission package

**Paper:** *Joint Code-Dimension and k-Galois-Hull Enumerators for
Repeated-Root Constacyclic Codes over Square-Free Affine Algebras*
**Type:** research article
**Target:** Finite Fields and Their Applications (Elsevier), submission system
`submit.elsevier.com/FFA`
**Authors:** Arun Kumar Yadav, Mohd Vasiulla, Vipin Gupta (corresponding)

```
00_READ_ME_FIRST.md            this file
01_manuscript/                 elsarticle sources, figures, highlights, main.pdf
02_cover_letter/               cover letter (plain text)
03_declarations/               originality, CRediT, funding, competing interest, data, AI use
04_supplementary/              Python code, generated tables, verification log
05_submission_checklist/       compliance_check.py and the checklist
```

## Build the PDF

```
cd 01_manuscript
./build.sh        # pdflatex + bibtex + pdflatex x2  ->  main.pdf
```

Requires TeX Live with `elsarticle` (Debian/Ubuntu: `texlive-publishers`).
`main.pdf` is already included. Then run
`python3 -I 05_submission_checklist/compliance_check.py` to re-check the
journal requirements.

## What the journal asks for (from its Guide for Authors)

* editable source files (`.tex`) plus a PDF; figures as separate files
  (`figures/`); single corresponding author with e-mail; affiliations with
  full postal addresses;
* abstract of at most 250 words, 1 to 7 keywords (this paper: 199 words, 6
  keywords); numbered references (`elsarticle-num`);
* highlights are optional (`01_manuscript/highlights.txt`, 4 lines, each at most
  85 characters);
* required declarations: competing interests (via Elsevier's declarations tool
  or a Word file), funding, use of generative AI (in a section before the
  references), data availability; CRediT statement is encouraged. All of them
  are already in the manuscript.

## What is still left for you

1. `02_cover_letter/COVER_LETTER.txt` — fill the three suggested reviewers (name,
   affiliation, e-mail) and any excluded reviewers, or delete that paragraph.
2. In the Elsevier system, complete the competing-interest declaration (text in
   `03_declarations/AUTHOR_DECLARATIONS.md`, section 4).

## Upload list

| upload slot | file |
|---|---|
| Manuscript (source) | `01_manuscript/main.tex`, `body.tex`, `references.bib` |
| Manuscript (PDF) | `01_manuscript/main.pdf` |
| Figures (separate files) | `01_manuscript/figures/` |
| Highlights (optional) | `01_manuscript/highlights.txt` |
| Cover letter | `02_cover_letter/COVER_LETTER.txt` |
| Supplementary material | `04_supplementary/` as one zip |

`05_submission_checklist/` is for you, not for the journal.

## Status

* `python3 -I 04_supplementary/code/checks.py` ends with `ALL CHECKS PASSED`
  and reproduces every number in the paper.
* The manuscript builds with no LaTeX errors and no undefined references or
  citations.
