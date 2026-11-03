#!/usr/bin/env python3
"""Submission checks for Finite Fields and Their Applications (Elsevier).

Run after building the manuscript:  python3 -I compliance_check.py
It reads ../01_manuscript/{main.tex, body.tex, references.bib, highlights.txt,
main.log} and verifies the journal's stated requirements:
  abstract <= 250 words, 1-7 keywords (no multi-word "and"/"of" keywords),
  3-5 highlights of at most 85 characters, required declaration sections,
  corresponding author, no IEEE-class leftovers or XXXX placeholders,
  every bibliography entry cited and every citation defined,
  no LaTeX errors or undefined references in the build log.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MS = os.path.join(HERE, "..", "01_manuscript")


def read(name):
    with open(os.path.join(MS, name), encoding="utf-8") as fh:
        return fh.read()


fails = []


def check(ok, msg):
    print(("  PASS  " if ok else "  FAIL  ") + msg)
    if not ok:
        fails.append(msg)


main = read("main.tex")
body = read("body.tex")
bib = read("references.bib")
hl = [l.strip() for l in read("highlights.txt").splitlines() if l.strip()]
log = read("main.log") if os.path.exists(os.path.join(MS, "main.log")) else ""

# abstract ------------------------------------------------------------------
m = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", main, re.S)
words = len(re.sub(r"\\[A-Za-z]+|[$\\{}~]", " ", m.group(1)).split()) if m else 0
check(m is not None and 0 < words <= 250, f"abstract has {words} words (limit 250)")

# keywords ------------------------------------------------------------------
m = re.search(r"\\begin\{keyword\}(.*?)\\MSC", main, re.S)
kws = [k.strip() for k in re.split(r"\\sep", m.group(1))] if m else []
check(1 <= len(kws) <= 7, f"{len(kws)} keywords (allowed 1-7): {', '.join(kws)}")
bad = [k for k in kws if re.search(r"\b(and|of)\b", k)]
check(not bad, "no keyword contains 'and' / 'of'" + (f" (found {bad})" if bad else ""))

# highlights ----------------------------------------------------------------
check(3 <= len(hl) <= 5, f"{len(hl)} highlights (allowed 3-5)")
long = [h for h in hl if len(h) > 85]
check(not long, "every highlight is at most 85 characters" + (f" (too long: {long})" if long else ""))

# declarations and structure -------------------------------------------------
for needle in ("CRediT authorship contribution statement",
               "Declaration of competing interest",
               "Funding",
               "Declaration of generative AI",
               "Data availability"):
    check(needle in main, f"section present: {needle}")
check("\\cortext" in main and "\\corref" in main, "corresponding author marked")
check(len(re.findall(r"\\ead\{", main)) == 3, "three author e-mail addresses")
check(len(re.findall(r"\\address\[", main)) == 3, "three affiliations with postal addresses")
check("elsarticle-num" in main, "numbered reference style (elsarticle-num)")

# leftovers -------------------------------------------------------------------
tex = main + body
check("IEEE" not in tex, "no IEEE-template text in the manuscript sources")
check("XXXX" not in tex, "no XXXX placeholders in the manuscript sources")
check("Magma" not in tex and "Magma" not in bib, "no Magma mention")

# references --------------------------------------------------------------------
keys = set(re.findall(r"@\w+\{([^,\s]+),", bib))
cited = set()
for grp in re.findall(r"\\cite[a-z]*\{([^}]*)\}", tex):
    cited.update(k.strip() for k in grp.split(","))
check(not (cited - keys), "every citation has a bib entry" +
      (f" (missing {sorted(cited - keys)})" if cited - keys else ""))
check(not (keys - cited), f"every bib entry is cited ({len(keys)} entries)" +
      (f" (uncited {sorted(keys - cited)})" if keys - cited else ""))

# build log ------------------------------------------------------------------
if log:
    check(not re.search(r"^!", log, re.M), "no LaTeX errors in main.log")
    check(not re.search(r"undefined (references|citations)|\?\?", log, re.I),
          "no undefined references or citations in main.log")
    m = re.search(r"Output written on main\.pdf \((\d+) pages", log)
    print(f"  info  main.pdf has {m.group(1) if m else '?'} pages")
else:
    print("  info  main.log not found; build the manuscript first (./build.sh)")

print()
if fails:
    print(f"{len(fails)} CHECK(S) FAILED")
    sys.exit(1)
print("ALL FFA SUBMISSION CHECKS PASSED")
