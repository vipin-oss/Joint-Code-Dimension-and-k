# Skeptical mathematics review

**Scope.** A line-by-line skeptical review of `01_manuscript/body.tex` was
carried out for duality and compatibility, the reciprocal and root action, the
min-edge hull generator, the transfer matrix and orbit product, moment,
covariance, support and extremal-count statements, complexity, all worked
examples, Table I and Table II, and the two appendices. The goal was to find
gaps, wrong signs, unjustified endpoint claims, notation mismatches and
verification claims that the shipped code does not actually perform.

**Overall conclusion.** No fatal gap was found in the reviewed passages. The
main theorem's transfer-product reduction, the complementary-reversal symmetry,
the min-edge formula and the extremal counts are consistent with the independent
brute-force checks. Twelve presentation or logical gaps were found and fixed.
This is a human/assisted skeptical review plus executable checks; it is not a
formal proof-assistant certificate. The authors remain responsible for every
proof.

## Gap list and fixes applied

1. **Inverse Frobenius exponent.** `\lambda_{s,0}=\Frob^{-t}(\lambda_s)` was
   ambiguous about the exponent on a component field of degree `d_s`. Fixed in
   Eq. (1) and Appendix B to
   `\lambda_{s,0}=\lambda_s^{p^{d_s-t mod d_s}}`.
2. **Componentwise maps.** The global `sigma_{A,k}` / `rho_{A,k}` were introduced
   without saying what they do on a component. Fixed by defining
   `sigma_{A,k}|_{K_s}=sigma_{s,k}` and
   `rho_{A,k}|_{K_s}=rho_{s,k}`.
3. **Absolute degree.** Added `d_s=em_s` and noted that `m_s=1` reduces the
   compatibility criterion to the base-field condition
   `lambda_{s,0}^{1+p^{e-k}}=1`.
4. **Debnath agreement / extension components.** The remark now distinguishes
   the base-field condition `ord lambda | 1+p^{e-k}` quoted in the introduction
   from the component-field criterion `1+p^{d_s-k}`. A new test family
   `F_64` over `F_8`, `k=1`, `n'=3`, `M=2`, order-3 `lambda_{s,0}`, is
   compatible by `d_s-k=5` (`3 | 33`) but not by `e-k=2` (`3 ∤ 5`), with
   `gcd(ord lambda_{s,0},n')=3`. It is included in Level C of `checks.py`.
5. **Telescoping sign.** The symmetry proof used
   `\sum_i(e_i-e_{i+1})=0`; the correct telescoping sum from the displayed
   re-indexing is `\sum_i(e_{i+1}-e_i)=0`. Fixed.
6. **Incompatible extremal factors.** The self-orthogonal / dual-containing
   count now explicitly says that incompatible components contribute a factor
   `1` by the incompatible-component corollary.
7. **Complexity proof.** Added the final-hull bound
   `\eta <= min{kappa,W-kappa} <= floor(W/2)` for intermediate dictionaries,
   and defined `N_F^{comp} = sum_{s in comp} |F_s|` instead of using an
   undefined symbol.
8. **Support theorem, Appendix A.** The vertex argument now allows zero-contribution
   `M -> M` edges before the `M -> c -> 0` passage, and says explicitly that a
   point of the polytope is a convex combination of vertices before applying
   concavity.
9. **Even-`M` endpoint contradictions.** The attainability argument now spells
   out the contradictions that force `M` odd in both the `S <= R` and
   `S >= R` cases, instead of leaving even `M` implicit.
10. **Appendix B factorization.** Replaced the incorrect description that a
    remaining cofactor of degree `> n'/2` is automatically irreducible with the
    genuine recursive trial-division irreducibility test actually used by
    `checks.py`.
11. **Verification levels.** Rewrote Section VII's verification subsection from
    two levels with a "larger families not brute-forced" limitation to three
    levels (A/B/C), 21 independent finite-field families, every printed
    number, and the external symbolic report.
12. **Code/manuscript consistency.** Added the `F64-over-F8` family to
    `INDEPENDENT_FAMILIES`, regenerated `checks_output.txt`, and reconciled the
    manuscript, `README_SUPPLEMENTARY.md` and `checks.py` on the 21-family
    count and the A/B/C labels.

## Executable corroboration

* `python3 -I 04_supplementary/code/checks.py` exits 0 with
  `ALL CHECKS PASSED`: Levels A1–A10, all 11 Table-I rows, the joint table of
  Example 7.1, `533/131`, `17.392`, the `M=1` example, 7 Level-B Gram-rank
  families, 21 Level-C independent brute-force families and 10 printed-number
  checks. Level C recomputes compatibility, the reciprocal permutation,
  Gram-rank hull dimensions, the min-edge formula, whole histograms, `W`,
  moments, `Cov`, LCD/SO/SD counts and all conditional means.
* `python3 04_supplementary/code/generate_tables.py` rewrites all 12 CSVs
  byte-identically.
* `04_supplementary/code/symbolic_verification.txt` records the external SymPy
  1.14.0 re-derivation of `E[Y]`, `E[Y^2]`, `Var(Y)`, adjacent-edge moments and
  covariance, `nu_M`, `v(2,M)`, `Var(M-e_f)=M(M+2)/12`, `Cov(kappa,eta)=0` and
  the complexity / coefficient-bit formulas.
* No shipped `.py` file imports SymPy.

## Remaining mathematical items disclosed, not silently "fixed"

* The published full text of Debnath et al., *Discrete Math.* 349(2) (2026),
  114750, was not retrieved. The arXiv v1 preprint uses `1+p^{e-k}` and
  `gcd(ord lambda,n')=1`; the publisher introduction confirms the base field
  `q=p^e` but the accessible snippets do not show every technical hypothesis.
  The manuscript's Introduction keeps the reported `e-k` condition for that
  cited work, while the component theory uses `d_s-k`. See
  `REFERENCES_VERIFICATION.md`.
* The root-exponent shortcut for the `F_32` family is checked through the
  printed orbit skeleton and the regenerated tables; an entirely separate
  re-derivation of that shortcut outside the shipped code was not recorded.
* The skeptical review is not a formal verification of every proof step in a
  proof assistant. All proofs remain subject to author and peer review.
