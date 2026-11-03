# Reference, attribution and policy verification

## 1. Bibliography metadata

`01_manuscript/references.bib` contains **31 entries**. Every DOI was queried
against Crossref in four batched `/works?filter=doi:...` requests (8 + 8 + 8 +
7 filters); all 31 DOIs returned a Crossref record. Authors, titles, venues,
volumes, issues, pages, years and publishers were compared with the `.bib`
entries and with the publisher/arXiv pages where a field was missing or garbled.

Verified caveats, none of which is a missing DOI:

* Crossref online dates often precede the volume year.
* `wildeBrun2008`: Crossref has no page field; the DOI/title give `064302`.
* `eldinLeroy2026`: Crossref has no volume or page field.
* `bouyuklieva2026`: Crossref has no page field; Springer/arXiv give article 39.
* `jitmanZ4`, `dinh2012`, `dinhai2010`: Crossref titles are MathML-garbled, but
  the remaining metadata corroborates the entries.
* `debnathAffine2026`: Crossref confirms *Discrete Mathematics* 349(2), 114750,
  2026, DOI `10.1016/j.disc.2025.114750`, authors Debnath, Islam,
  Martínez-Moro and Prakash.

Secondary publisher/search corroboration used:
<https://www.sciencedirect.com/science/article/abs/pii/S0012365X25003589>,
<https://api.crossref.org/works/10.1016/j.disc.2025.114750>,
<https://arxiv.org/abs/2412.08512>,
<https://arxiv.org/html/2412.08512v1>,
<https://www.aimsciences.org//article/doi/10.3934/amc.2025054>.

## 2. Introduction attributions

The following introductory attributions were corroborated by publisher pages,
arXiv abstracts/introductions or search-result abstracts:

* Fan and Zhang — introduction of the Galois inner product.
* Liu and Pan — hull dimension from generator matrices.
* Debnath et al. — finite-field / affine-algebra per-code hull formulas and
  counts.
* Guenda et al. — EAQECC entanglement related to hull dimension.
* Taki Eldin / Solé — generator/parity-check matrix methods for Galois hulls of
  MT codes.
* Debnath and Prakash — average hull dimensions over fields and a finite
  non-chain ring.
* Debnath et al. — small hull dimensions 1 and 2.
* Bouyuklieva et al. — hull-count sequence.

Corroborating pages include:
<https://link.springer.com/article/10.1007/s10623-019-00681-2>,
<https://arxiv.org/abs/1606.00134>,
<https://arxiv.org/abs/2305.15237>,
<https://www.aimsciences.org//article/doi/10.3934/amc.2025010>,
<https://www.aimsciences.org//article/doi/10.3934/amc.2025054>,
<https://arxiv.org/abs/2402.01255>,
<https://www.sciencedirect.com/science/article/abs/pii/S0012365X22003739>.

**Status:** these are DOI-metadata, abstract, introduction and search-snippet
checks, *not* full-text line-by-line verification of every attribution claim.
That remains an unresolved item.

## 3. Debnath notation and component fields

The arXiv v1 preprint of `debnathAffine2026` decomposes the affine algebra into
finite fields, defines the `k`-Galois inner product with exponent `p^k` on
`F_q` (`q=p^e`), and states Lemma 1 / Theorem 8 hypotheses
`r | 1+p^{e-k}` and `gcd(ord(lambda),n')=1`. The publisher introduction
confirms `q=p^e` and factorization over `F_q` projected into the simple
components, but the accessible ScienceDirect snippets do not display every
technical hypothesis of the published article.

The manuscript's Introduction (line 45) keeps the cited work's reported
`1+p^{e-k}` condition. The repeated-root component theory uses
`1+p^{d_s-k}` with `d_s=e m_s`, the absolute degree of the component field
`K_s` over `F_p`; the Debnath-agreement remark was revised to say only that
the cited condition is stated over the base field, not that every component
field is `F_q`. A new `F_64`/`F_8` Level-C family exercises the extension-field
criterion.

**Unresolved:** the published full text was not fetched (publisher access is
required), so an exact line-by-line comparison of `e-k` versus `d_s-k` across
the published theorem and the present component theory is not complete. The
introductory claim and the revised remark are disclosed as reported rather
than silently harmonised.

## 4. IEEE AI-use policy recheck

The official IEEE Author Center page was fetched:
<https://journals.ieeeauthorcenter.ieee.org/become-an-ieee-journal-author/publishing-ethics/guidelines-and-policies/submission-and-peer-review-policies/>.
It requires AI-generated content (text, figures, images, code) to be disclosed
in the Acknowledgments, the AI system to be identified, the specific sections
to be identified, and the level of AI involvement to be explained; grammar-only
editing is generally outside the intent but disclosure is recommended. AI
systems cannot be authors and human authors remain fully responsible.
Secondary summaries are consistent: [1](https://libguides.iou.edu.gm/c.php?g=1482669&p=11059806),
[2](https://www.enago.com/responsible-ai-movement/publisher-ai-guidelines/ieee-ai-guidelines/),
[3](https://www.monperrus.net/martin/generative-ai-scientific-writing).

Accordingly, the identical AI-use disclosure in both wrappers and the
declarations now identifies Arena.ai Agent Mode, names Section I, Section VII
and Appendices A–B, describes the assistive level, states that no results,
proofs, data, figures or tables were generated independently, and states that
the tool is not an author. Journal-specific form fields beyond the official
policy were not checked.

## 5. Explicitly unresolved / unverified items

* Full-text line-by-line accuracy of every Introduction attribution.
* Published full text of `debnathAffine2026` and the exact relation between
  `1+p^{e-k}` in that article and `1+p^{d_s-k}` in the present component
  theory.
* Whether any journal-specific submission form requires additional AI
  disclosure beyond the Acknowledgments.
* Author-only `XXXX` values listed in `FINAL_REPORT.md`.
