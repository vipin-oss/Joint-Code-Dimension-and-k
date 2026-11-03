#!/usr/bin/env python3
"""
generate_tables.py -- regenerates the data behind Table 1 (summary of computed
families) and the joint distributions quoted in the examples.

Run from the paper directory:

    python3 code/generate_tables.py

Outputs (written into ./tables):
    summary_families.csv   one row per family of Table 1
    joint_<slug>.csv       the full joint multiplicities N_{kappa,eta}
"""

import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from enumerator import Family  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tables")

# name, slug, n', M, orbit skeleton [(a_O, w_O), ...], k
FAMILIES = [
    ("F4-lam1", "F_4, lambda_0 = 1", 5, 2, [(1, 1), (2, 2)], 1),
    ("F4-lamw", "F_4, lambda_0 = omega", 5, 2, [(1, 1), (2, 2)], 1),
    ("F8", "F_8", 7, 2, [(1, 1), (6, 1)], 1),
    ("F3", "F_3", 4, 3, [(1, 1), (1, 1), (1, 2)], 0),
    ("F9-i", "F_9, lambda_0 = i", 4, 3, [(2, 2)], 1),
    ("F9-m1", "F_9, lambda_0 = -1", 4, 3, [(2, 1), (2, 1)], 1),
    ("F9-n24", "F_9", 8, 3, [(1, 1)] * 4 + [(2, 1), (2, 1)], 1),
    ("F25", "F_25", 6, 5, [(1, 1)] * 6, 1),
    ("F4xF16", "F_4 x F_16", 5, 2, [(1, 1), (2, 2), (1, 2), (4, 2)], 1),
    ("F32-M2", "F_32", 31, 2, [(1, 1)] + [(10, 1)] * 3, 1),
    ("F32-M4", "F_32", 31, 4, [(1, 1)] + [(10, 1)] * 3, 1),
]


def frac(f):
    return f"{f.numerator}/{f.denominator}" if f.denominator != 1 else str(f.numerator)


def main():
    os.makedirs(OUT, exist_ok=True)
    rows = []
    for slug, label, n_prime, M, orbits, k in FAMILIES:
        fam = Family(label, n=n_prime * M, M=M, orbits=orbits)
        s = fam.summary()
        E = fam.enumerator()
        # joint distribution file
        path = os.path.join(OUT, f"joint_{slug}.csv")
        with open(path, "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["kappa", "eta", "count"])
            for (K, H), c in sorted(E.items()):
                w.writerow([K, H, c])
        rows.append({
            "family": label,
            "n_prime": n_prime,
            "M": M,
            "n": n_prime * M,
            "k": k,
            "orbits": " ".join(f"({a},{w})" for a, w in orbits),
            "codes": s["codes"],
            "joint_terms": s["terms"],
            "LCD": s["LCD"],
            "self_dual": s["SD"],
            "E_eta": frac(s["E_eta"]),
            "Var_eta": frac(s["Var_eta"]),
            "E_kappa": frac(s["E_kappa"]),
            "Var_kappa": frac(s["Var_kappa"]),
            "Cov": frac(s["Cov"]),
        })
        print(f"{slug:9s} codes={s['codes']:<24} terms={s['terms']:<6} "
              f"LCD={s['LCD']:<4} SD={s['SD']:<5} E={frac(s['E_eta']):<8} "
              f"Var={frac(s['Var_eta'])}")

    with open(os.path.join(OUT, "summary_families.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"\nwrote {len(rows)} summary rows and {len(rows)} joint files to tables/")


if __name__ == "__main__":
    main()
