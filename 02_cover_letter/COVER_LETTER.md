# Cover letter — regular paper submission

*(Fill the bracketed fields, export to PDF, and upload with
`main_peerreview.pdf`. Keep it to one page.)*

---

3 November 2026

Prof. [Name], Editor-in-Chief
*IEEE Transactions on Information Theory*

Dear Prof. [Name],

We submit the enclosed **regular paper**, "Joint Code-Dimension and
$k$-Galois-Hull Enumerators for Repeated-Root Constacyclic Codes over
Square-Free Affine Algebras", by Arun Kumar Yadav, Mohd Vasiulla and
Vipin Gupta, for consideration for publication in the *IEEE Transactions on
Information Theory*. It has not been published elsewhere and is not under
consideration by any other journal; all authors have approved the submission.
This is a full regular paper (a **40-page** double-spaced review manuscript),
not a correspondence.

**What the paper does.** For all $\mathcal A$-linear $\lambda$-constacyclic
codes of a fixed repeated-root length over a square-free affine algebra over a
finite field, we determine the exact joint distribution of the code dimension
and the $k$-Galois hull dimension. The Frobenius identity writes every
component modulus as a $p^{t}$-th power of a square-free kernel, so a code is an
exponent selection on the distinct kernel factors; the $k$-Galois dual then acts
through a Frobenius-twisted reciprocal permutation, and on each of its orbits the
hull dimension is a cyclic sum of pairwise minima. The bivariate law of one
orbit is the trace of a power of an explicit weighted transfer matrix, and
multiplying over orbits — with a dimension-only factor for components whose
twist is incompatible — yields a bivariate enumerator whose coefficients are the
exact multiplicities.

**Main contributions.**
1. the exact joint enumerator, valid for every twist, including incompatible
   components, with the per-code hull formula recovered as a special case;
2. the exact support of attainable (code dimension, hull dimension) pairs on one
   orbit — a trapezoid, including a lower bound that is invisible from
   dimensions alone (Appendix A);
3. closed means, variances and conditional laws, with the two dimensions
   uncorrelated but strongly dependent, and the numbers of LCD,
   self-orthogonal, dual-containing and self-dual codes, the LCD count being
   independent of the multiplicity in the fully compatible case;
4. an algorithm polynomial in the length, the multiplicity and the number of
   kernel factors, verified exhaustively against finite-field linear algebra in
   characteristics 2 and 3, and evaluated for all $3^{31}$ codes of length 62
   over $\mathbb F_{32}$.

**Relation to the literature.** For a single code, Galois hull dimensions of
constacyclic codes over a field and over an affine algebra are known
([DPI2023], [DIMP2026]) and the average hull dimension has been computed
([DP2025]); the contribution here is the full joint law over a family together
with its enumerative consequences, and we state explicitly where the paper
agrees with, and where it goes beyond, that work.

The supplementary material contains the complete implementation, the
verification log, the symbolic moment/covariance/complexity report and the
regenerated CSV tables; every table and every worked example in the paper is
reproduced by the exact root-level command recorded in the submission
package.

We suggest the following reviewers, none of whom is at our institutions:
[Name, affiliation, e-mail], [Name, affiliation, e-mail],
[Name, affiliation, e-mail]. We request the exclusion of [name(s)], if any.

Yours sincerely,

Vipin Gupta (corresponding author)
Department of Mathematics, Gurugram University, Gurugram, India
vipin@gurugramuniversity.ac.in

*on behalf of* Arun Kumar Yadav and Mohd Vasiulla

---

### Notes before sending

* Replace the editor name and the three reviewer suggestions with real names;
  IEEE requires that suggested reviewers have no conflict of interest with any
  author. The date and the 40-page count are already filled in.
* The real page count of the compiled `main_peerreview.pdf` is **40** and is
  already quoted in the cover letter; do not change it unless the PDF is
  rebuilt with a different length.
* In the relation-to-literature paragraph the bracketed keys refer to the
  numbered references of the paper; the journal's cover-letter field accepts
  plain text, so you may spell them out as "Debnath–Prakash–Islam (2023)",
  "Debnath–Islam–Martínez-Moro–Prakash (2026)", "Debnath–Prakash (2025)".
