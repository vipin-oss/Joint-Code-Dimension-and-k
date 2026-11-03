# Supplementary material

Manuscript: *Joint Code-Dimension and k-Galois-Hull Enumerators for Repeated-Root
Constacyclic Codes over Square-Free Affine Algebras*

This folder contains the program and all generated data referred to in the
paper. Every shipped `.py` file uses only the Python 3 standard library — no
Magma, no Sage, no SymPy, no installation and no external packages.

```
code/
  enumerator.py              transfer-matrix enumerator, restricted
                             self-orthogonal / dual-containing / self-dual counts,
                             moment formulas, cached global enumerator
  checks.py                  the complete verification (Levels A, B and C)
  generate_tables.py         regenerates every file in tables/
  checks_output.txt          saved live output of the exact root-level command
                             python3 -I 04_supplementary/code/checks.py
  symbolic_verification.txt  report of the external SymPy re-derivation of the
                             moment, covariance and complexity formulas
tables/
  summary_families.csv       Table I data (11 families)
  joint_<family>.csv         the 11 joint distributions N_{kappa,eta}
```

## Reproduce everything

From the repository root (not from `code/`):

```bash
python3 -I 04_supplementary/code/checks.py       # prints PASS/FAIL per claim
python3 04_supplementary/code/generate_tables.py # rewrites tables/*.csv
```

`checks.py` inserts its own directory on `sys.path`, so the exact isolated-mode
command works from the repository root. Regenerating the tables reproduces the
committed CSVs byte-for-byte.

`checks.py` verifies, in the order of the paper:

* **Level A:** the transfer-matrix trace against brute-force enumeration of all
  exponent words (60 triples `(orbit length, multiplicity, weight)`); the closed
  forms for orbit lengths 1 and 2; complement–reversal symmetry; the checksum
  `E(1,1) = (M+1)^(number of factors)`; the LCD count; the one-orbit trapezoid
  support; the mean / variance / zero-covariance formulas; the `M=1` transfer
  matrix; **every row of Table I**, the joint table of Example 7.1, the
  conditional mean `E[eta | kappa = 7] = 533/131`, `max_kappa E[eta | kappa]`
  at `kappa = 31`, and every other number printed in an example or caption.
* **Level B:** for seven small families over `F_4`, `F_8`, `F_3` and `F_9` it
  factors the square-free kernel, computes the reciprocal from its definition,
  reads off the orbit skeleton, builds every generator matrix, computes the hull
  dimension as `dim C − rank(B sigma^k(B)^T)`, and matches the full joint
  histogram with the trace product (27, 27, 27, 2187, 64, 16 and 256 words).
* **Level C (added for this submission):** brute-force verification over real
  finite-field codes for 20 independent families: `F_2` and `F_4` with
  `n = 4, 6, 12`, `F_3` with `n = 6, 9`, `F_5` with `n = 10`, `k = 0, 1`,
  `lambda_0 != 1` including incompatible twists, and product algebras
  `F_4 x F_16` and `F_4 x F_4`. For every family it checks the compatibility
  condition, the reciprocal permutation, the Gram-rank hull dimension, the
  min-edge formula, the whole joint histogram, `W`, `E[kappa]`, `Var(kappa)`,
  `Cov`, the LCD / self-orthogonal / self-dual counts, all conditional means and
  the maximal conditional mean against the `Family` output. A genuine
  irreducibility test replaces the previous assumption that a large residual
  cofactor is irreducible.

The last line of `checks_output.txt` must read `ALL CHECKS PASSED`.

## Symbolic re-derivation

The moment, covariance and complexity formulas were additionally re-derived
symbolically with SymPy 1.14.0 in a scratch script outside the repository
(`python3 /tmp/symbolic_check.py`); the full output is recorded in
`symbolic_verification.txt`. SymPy is an external verification tool only and is
**not** imported by any shipped file.

## Correspondence with the paper

| paper | file |
|---|---|
| the main theorem (joint enumerator) | `enumerator.py`: `Family.enumerator`, `orbit_enumerator_trace` |
| the trapezoid theorem (Appendix A) | `checks.py`: check A6 |
| the short-orbit proposition | `enumerator.py`: `orbit_enumerator_small`; check A2 |
| the moment proposition | `enumerator.py`: `mean_var_hull`, `mean_var_dim`, `covariance`; checks A7, C |
| the simple-root (M = 1) proposition | `checks.py`: check A10 |
| LCD / SO / DC / SD counts | `enumerator.py`: `lcd_count`, `self_orthogonal_count`, `self_dual_count` |
| Table I | `generate_tables.py` → `tables/summary_families.csv` |
| Figures 2–3 | the data in `tables/joint_F8.csv`, `tables/joint_F32-M2.csv` |
| Table II (verification) | `checks.py`: `check_B` and Level C |
