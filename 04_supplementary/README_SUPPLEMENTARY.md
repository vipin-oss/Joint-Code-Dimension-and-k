# Supplementary material

Manuscript: *Joint Code-Dimension and k-Galois-Hull Enumerators for Repeated-Root
Constacyclic Codes over Square-Free Affine Algebras*

This folder contains the program and all generated data referred to in the
paper. It uses only the Python 3 standard library — no installation, no external
packages.

```
code/
  enumerator.py        transfer-matrix enumerator, restricted
                       self-orthogonal / dual-containing / self-dual counts,
                       moment formulas, CSV writer helpers
  checks.py            the complete verification (Level 1 and Level 2)
  generate_tables.py   regenerates every file in tables/
  checks_output.txt    saved output of checks.py  --  ALL CHECKS PASSED
tables/
  summary_families.csv Table I data (11 families)
  joint_<family>.csv   the 11 joint distributions N_{kappa,eta}
```

## Reproduce everything

```bash
cd code
python3 checks.py            # ~30 s; prints PASS/FAIL per claim
python3 generate_tables.py   # rewrites ../tables/*.csv
```

`checks.py` verifies, in the order of the paper:

* the transfer-matrix trace against brute-force enumeration of all exponent
  words, for 60 triples `(orbit length, multiplicity, weight)`;
* the closed forms for orbit lengths 1 and 2 (the short-orbit proposition);
* the complement–reversal symmetry, the checksum `E(1,1) = (M+1)^(number of
  factors)`, the LCD count `2^(number of orbits)`, and the one-orbit trapezoid
  support (the trapezoid theorem, proved in Appendix A);
* the mean / variance / zero-covariance formulas (the moment proposition);
* **every row of Table I**, the joint table of the first worked example, the
  conditional mean `E[eta | kappa = 7] = 533/131`, and
  `max_kappa E[eta | kappa] = 17.392` at `kappa = 31`;
* **Level 2, from the definitions:** for seven small families over `F_4`, `F_8`,
  `F_3` and `F_9`, it factors the square-free kernel, computes the reciprocal from
  its definition, reads off the orbit skeleton (recovering independently the
  skeletons quoted in the worked examples), builds every generator matrix,
  computes the hull dimension as `dim C − rank(B sigma^k(B)^T)`, and matches the
  full joint histogram with the trace product — 27, 27, 27, 2187, 64, 16 and 256
  words.

The last line of `checks_output.txt` must read `ALL CHECKS PASSED`.

## Correspondence with the paper

| paper | file |
|---|---|
| the main theorem (joint enumerator) | `enumerator.py`: `Family.enumerator`, `orbit_enumerator_trace` |
| the trapezoid theorem (Appendix A) | `checks.py`: check A6 |
| the short-orbit proposition | `enumerator.py`: `orbit_enumerator_small`; check A2 |
| the moment proposition | `enumerator.py`: `mean_var_hull`, `mean_var_dim`, `covariance`; check A7 |
| the simple-root (M = 1) proposition | `checks.py`: check A10 |
| LCD / SO / DC / SD counts | `enumerator.py`: `lcd_count`, `self_orthogonal_count`, `self_dual_count` |
| Table I | `generate_tables.py` → `tables/summary_families.csv` |
| Figures 2–3 | the data in `tables/joint_F8.csv`, `tables/joint_F32-M2.csv` |
| Table II (verification) | `checks.py`: `check_B` |
