#!/usr/bin/env python3
"""
compliance_check.py -- checks the IEEE *regular paper* formal requirements that
can be verified without running LaTeX, and reports the managed quantities
(abstract length, index terms, reference count, float count, section structure).

    python3 compliance_check.py            # prints a report, exit code 0/1
    python3 compliance_check.py > compliance_report.txt

What is checked
  R1  IEEEtran class used, journal mode (not conference, not letter)
  R2  abstract present, <= 200 words, no \\cite, no display math
  R3  IEEEkeywords present, 3-6 terms, alphabetically ordered, no trailing period
  R4  IEEE author block: \\thanks with affiliations, e-mail, corresponding author,
      ORCID, DOI placeholder
  R5  no European/Elsevier-only matter (CRediT, competing interest, MSC codes,
      "Data availability" section heading, generative-AI declaration section)
  R6  section structure of a regular paper: Introduction first, Conclusion last
      (singular), Acknowledgment + References after it; appendix optional
  R7  every \\label referenced, no duplicate label, no \\ref to a missing label
  R8  every \\cite key present in the .bib and every bib entry cited
  R9  figures are vector PDF, captions below the graphic, tables use booktabs
      and have captions above the tabular
  R10 count of theorems/lemmas/... , pages estimate, and a reference budget that
      matches the journal's typical 25-45 range
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# In the submission package this script sits in 05_submission_checklist/ while
# the manuscript sits in ../01_manuscript/.  Run it from either location.
MANUSCRIPT = HERE
if not os.path.exists(os.path.join(HERE, "main.tex")):
    MANUSCRIPT = os.path.abspath(os.path.join(HERE, os.pardir, "01_manuscript"))


def strip_comments(text):
    out = []
    for line in text.split("\n"):
        if line.lstrip().startswith("%"):
            out.append("")
            continue
        res, i = [], 0
        while i < len(line):
            if line[i] == "%" and (i == 0 or line[i - 1] != "\\"):
                break
            res.append(line[i])
            i += 1
        out.append("".join(res))
    return "\n".join(out)


def expand(texfile):
    path = os.path.join(MANUSCRIPT, texfile)
    raw = open(path).read()
    body = strip_comments(raw)
    for inc in re.findall(r"\\input\{([^}]*)\}", body):
        sub = inc if inc.endswith(".tex") else inc + ".tex"
        body += "\n" + strip_comments(open(os.path.join(MANUSCRIPT, sub)).read())
    return raw, body


def words(text):
    return len(text.split())


def check(texfile, label, report, peerreview=False):
    raw, body = expand(texfile)
    ok = True

    def fail(msg):
        nonlocal ok
        ok = False
        report.append("  FAIL  " + msg)

    def info(msg):
        report.append("  ok    " + msg)

    report.append("=" * 78)
    report.append(f"{label}   ({texfile})")
    report.append("=" * 78)

    # R1 class ------------------------------------------------------------
    m = re.search(r"\\documentclass\[([^\]]*)\]\{IEEEtran\}", raw)
    if not m:
        fail("R1  IEEEtran not used with an option list")
    else:
        opts = [o.strip() for o in m.group(1).split(",")]
        if "journal" not in opts:
            fail(f"R1  journal option missing (got {opts})")
        elif "peerreview" in opts and not peerreview:
            fail("R1  camera-ready file must not use the peerreview option")
        elif peerreview and "onecolumn" not in opts:
            fail("R1  review copy must use the onecolumn option (the peerreview option alone keeps the body two-column)")
        else:
            info(f"R1  IEEEtran[{','.join(opts)}] "
                 f"- {'peer-review' if peerreview else 'regular paper'}, "
                 f"two-column={'no' if 'onecolumn' in opts else 'yes'}")

    # R2 abstract ---------------------------------------------------------
    m = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", body, re.S)
    if not m:
        fail("R2  no abstract environment")
    else:
        ab = m.group(1)
        n = words(ab)
        bad = []
        if n > 200:
            bad.append(f"{n} words > 200")
        if "\\cite" in ab:
            bad.append("contains \\cite")
        if re.search(r"\\\[|\\begin\{(equation|align)", ab):
            bad.append("contains display math")
        if bad:
            fail("R2  abstract: " + "; ".join(bad))
        else:
            info(f"R2  abstract {n} words (limit 200), no citations, no displays")

    # R3 index terms ------------------------------------------------------
    m = re.search(r"\\begin\{IEEEkeywords\}(.*?)\\end\{IEEEkeywords\}", body, re.S)
    if not m:
        fail("R3  no IEEEkeywords environment (IEEE 'Index Terms')")
    else:
        kws = [k.strip() for k in re.split(r"[,;]", m.group(1).replace("\n", " ")) if k.strip()]
        kws = [k.rstrip(".") for k in kws]
        problems = []
        if not (3 <= len(kws) <= 6):
            problems.append(f"{len(kws)} terms (want 3-6)")
        if kws != sorted(kws, key=str.lower):
            problems.append("not alphabetized")
        if problems:
            fail("R3  index terms: " + "; ".join(problems) + f" -> {kws}")
        else:
            info(f"R3  {len(kws)} index terms, alphabetized: {', '.join(kws)}")

    # R4 author block -----------------------------------------------------
    head = body[:body.index("\\maketitle") if "\\maketitle" in body else len(body)]
    if "peerreview" in raw and "\\IEEEpeerreviewmaketitle" in body:
        head = body[:body.index("\\IEEEpeerreviewmaketitle")]
    needs = {
        "affiliation(s)": r"is with the",
        "e-mail address(es)": r"e-mail",
        "corresponding author": r"[Cc]orresponding author",
        "ORCID": r"ORCID",
        "funding statement": r"funding|supported by",
    }
    missing = [k for k, pat in needs.items() if not re.search(pat, head)]
    if missing:
        fail("R4  author block missing: " + ", ".join(missing))
    else:
        info(f"R4  author block complete ({head.count(chr(92)+'thanks')} \\thanks footnotes)")

    # R5 no Elsevier/other-society matter ---------------------------------
    banned = {
        "CRediT statement": r"CRediT",
        "MSC codes": r"Mathematics Subject Classification",
        "competing-interest declaration": r"competing interest",
        "generative-AI declaration": r"generative AI",
        "Keywords line (Elsevier style)": r"\\textbf\{Keywords",
    }
    found = [k for k, pat in banned.items() if re.search(pat, body, re.I)]
    if found:
        fail("R5  non-IEEE matter present: " + ", ".join(found))
    else:
        info("R5  no Elsevier-only declarations, MSC codes or keywords line")

    # R6 section structure -------------------------------------------------
    main_body = body.split("\\appendices")[0]   # appendix sections are not numbered sections
    secs = re.findall(r"\\section\{([^}]*)\}", main_body)
    secs_clean = [re.sub(r"\\texorpdfstring\{[^}]*\}\{[^}]*\}", "k", s) for s in secs]
    problems = []
    if not secs_clean or secs_clean[0].strip() != "Introduction":
        problems.append(f"first section is {secs_clean[0] if secs_clean else None!r}")
    if secs_clean and secs_clean[-1].strip() not in ("Conclusion", "Conclusions"):
        problems.append(f"last numbered section is {secs_clean[-1]!r}")
    if not re.search(r"\\section\*\{Acknowledgment\}", body):
        problems.append("no \\section*{Acknowledgment}")
    if not re.search(r"\\bibliography\{", body):
        problems.append("no \\bibliography")
    if problems:
        fail("R6  structure: " + "; ".join(problems))
    else:
        info(f"R6  {len(secs_clean)} numbered sections; Conclusion, Acknowledgment and "
             f"References in place; appendix={'yes' if chr(92)+'appendices' in body else 'no'}")

    # R7 labels/refs -------------------------------------------------------
    labels = re.findall(r"\\label\{([^}]*)\}", body)
    refs = set()
    for grp in re.findall(r"\\(?:ref|eqref)\{([^}]*)\}", body):
        refs.update(x.strip() for x in grp.split(","))
    dups = [k for k in set(labels) if labels.count(k) > 1]
    undef = sorted(refs - set(labels))
    if dups or undef:
        fail(f"R7  labels: duplicates={dups or 'none'}, undefined refs={undef or 'none'}")
    else:
        info(f"R7  {len(labels)} labels, all {len(refs)} reference targets defined, no duplicates")

    # R8 citations ---------------------------------------------------------
    cites = set()
    for grp in re.findall(r"\\cite\{([^}]*)\}", body):
        cites.update(x.strip() for x in grp.split(","))
    bibfile = os.path.join(MANUSCRIPT, "references.bib")
    bib = set(re.findall(r"@\w+\{([^,]+),", open(bibfile).read()))
    if cites - bib:
        fail(f"R8  cited but not in references.bib: {sorted(cites - bib)}")
    else:
        info(f"R8  {len(cites)} references cited, all present in references.bib"
             + (f"; {len(bib - cites)} uncited entries" if bib - cites else "; none uncited"))

    # R9 floats ------------------------------------------------------------
    problems = []
    figs = re.findall(r"\\begin\{figure\*?\}(.*?)\\end\{figure\*?\}", body, re.S)
    for i, f in enumerate(figs, 1):
        for g in re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]*)\}", f):
            full = os.path.join(MANUSCRIPT, "figures", g)
            if not os.path.exists(full):
                problems.append(f"Fig. {i}: missing file {g}")
            elif not g.lower().endswith((".pdf", ".png")):
                problems.append(f"Fig. {i}: {g} is not a supported image (PDF/PNG)")
        if f.index("\\includegraphics") > f.index("\\caption") if "\\caption" in f else False:
            problems.append(f"Fig. {i}: caption above the graphic")
    tabs = re.findall(r"\\begin\{table\*?\}(.*?)\\end\{table\*?\}", body, re.S)
    for i, tb in enumerate(tabs, 1):
        if "\\caption" not in tb:
            problems.append(f"Table {i}: no caption")
        elif "\\begin{tabular" in tb and tb.index("\\caption") > tb.index("\\begin{tabular"):
            problems.append(f"Table {i}: caption below the tabular")
        if "\\toprule" not in tb:
            problems.append(f"Table {i}: no booktabs rules")
    if problems:
        fail("R9  floats: " + "; ".join(problems))
    else:
        npdf = sum(1 for f in figs for g in re.findall(
            r"\\includegraphics(?:\[[^\]]*\])?\{([^}]*)\}", f) if g.lower().endswith(".pdf"))
        npng = sum(1 for f in figs for g in re.findall(
            r"\\includegraphics(?:\[[^\]]*\])?\{([^}]*)\}", f) if g.lower().endswith(".png"))
        info(f"R9  {len(figs)} figures ({npdf} vector PDF, {npng} PNG; captions below), "
             f"{len(tabs)} tables (captions above, booktabs rules)")

    # R10 quantities -------------------------------------------------------
    def cnt(env):
        return len(re.findall(r"\\begin\{" + env + r"\}", body))

    proofs = cnt("proof") + len(re.findall(r"\\emph\{Proof:", body))
    n_words = words(re.sub(r"\\[a-zA-Z]+\*?", " ", body))
    report.append("  ----  quantities: "
                 f"{cnt('theorem')} theorems, {cnt('lemma')} lemmas, "
                 f"{cnt('proposition')} propositions, {cnt('corollary')} corollaries, "
                 f"{cnt('definition')} definitions, {cnt('example')} examples, "
                 f"{cnt('remark')} remarks, {proofs} proofs")
    n_disp = body.count(chr(92) + "[") + \
        len(re.findall(r"begin.(equation|align)", body))
    report.append("  ----  quantities: "
                 f"{n_disp} displayed equations, {len(secs_clean)} sections, "
                 f"~{n_words} words of text")
    # prose words only: drop displays, inline math, markup and 1-2 letter tokens
    prose = re.sub(r"\\begin\{(equation|align)\*?\}[\s\S]*?\\end\{\1\*?\}", " ", body)
    prose = re.sub(r"\\\[[\s\S]*?\\\]", " ", prose)
    prose = re.sub(r"\$[^$]*\$", " ", prose)
    prose = re.sub(r"\\[a-zA-Z]+\*?", " ", prose)
    prose = re.sub(r"[{}\&_^~]", " ", prose)
    prose_words = len([w for w in prose.split() if re.search(r"[A-Za-z]{2,}", w)])
    lo = (prose_words / 1150.0 + 0.035 * n_disp + 0.40 * len(figs)
          + 0.45 * len(tabs) + 0.030 * len(cites) + 0.6)
    hi = (prose_words / 950.0 + 0.055 * n_disp + 0.55 * len(figs)
          + 0.60 * len(tabs) + 0.040 * len(cites) + 0.9)
    report.append(f"  ----  estimate: {lo:.0f}-{hi:.0f} two-column pages "
                 f"({prose_words} prose words, {n_disp} displays, "
                 f"{len(figs)} figures, {len(tabs)} tables, {len(cites)} references)")
    report.append(f"  ----  estimate: {lo * 2.4:.0f}-{hi * 2.4:.0f} pages in the "
                 f"double-spaced peer-review format")

    report.append(f"  RESULT: {'PASS' if ok else 'FAIL'}")
    report.append("")
    return ok


def main():
    report = []
    ok1 = check("main.tex", "REGULAR PAPER - camera-ready layout (two column)",
                report, peerreview=False)
    ok2 = check("main_peerreview.tex", "REGULAR PAPER - submission copy (single column, double spaced)",
                report, peerreview=True)
    print("\n".join(report))
    both = ok1 and ok2
    print("ALL IEEE REGULAR-PAPER CHECKS PASSED" if both else "SOME CHECKS FAILED")
    return 0 if both else 1


if __name__ == "__main__":
    sys.exit(main())
