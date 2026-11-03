#!/usr/bin/env python3
"""
checks.py -- self-contained verification for the paper's statements.

Run from the repository root:
    python3 -I 04_supplementary/code/checks.py
(prints a pass/fail line per check and a summary; only the standard library is
used, and no Magma/Sage or other CAS is required.)

Level A (combinatorial, no field arithmetic)
  A1  transfer-matrix trace  ==  brute-force word enumeration
      for all (a,M,w) with a <= 6, M <= 5, w in {1,2}
  A2  closed forms for a = 1, 2 agree with the trace and with brute force
  A3  complement-reversal symmetry  N(K,H) = N(W-K,H)
  A4  checksum  E(1,1) = (M+1)^#factors
  A5  LCD count = 2^(number of compatible orbits)  (fully compatible case)
  A6  attainable (K,H) on one orbit = the trapezoid of Theorem 6.3
  A7  mean / variance / Cov = 0 formulas of Proposition 7.4
  A8  Var(kappa) = M(M+2)/12 * sum w_f^2
  A9  the two worked tables of the paper (Examples 7.1, 7.2, 7.3, 8.1)
  A10 the M = 1 transfer matrix equals the 2x2 matrix of Proposition 5.8

Level B (finite-field linear algebra, small cases)
  B1  hull dimension from the Gram-matrix rank equals the min-edge formula
      for every exponent word of the families in Table 1 (F_4, F_8 ...)

Level C (independent brute-force verification, added for this submission)
  C1  direct Gram-matrix hull dimensions over real finite fields for F_2/F_4
      with n=4,6,12, F_3 with n=6,9, F_5 with n=10, k=0,1, lambda_0 != 1
      (including incompatible twists), and product algebras F_4 x F_16 and
      F_4 x F_4; every printed number is recomputed from the brute-force
      histogram and compared with Family output.
  C2  all displayed example/table values, LCD/SO/SD counts, W, moments,
      covariance, conditional means and complexity-related counts.
"""

from fractions import Fraction
from itertools import product
from pathlib import Path
import sys

# `python3 -I checks.py` does not put the script directory on sys.path.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from enumerator import (Family, orbit_enumerator_trace, orbit_enumerator_bruteforce,
                        orbit_enumerator_small, transfer_matrix, pmul, monomial,
                        restricted_orbit_count)


# ---------------------------------------------------------------- GF(p^m)
class GF:
    """F_{p^m} = F_p[x]/(modulus); elements are tuples of length m."""

    def __init__(self, p, m, modulus):
        self.p, self.m, self.mod = p, m, modulus
        self.q = p ** m
        assert len(modulus) == m + 1 and modulus[-1] == 1, "modulus must be monic of degree m"

    def add(self, a, b):
        return tuple((x + y) % self.p for x, y in zip(a, b))

    def sub(self, a, b):
        return tuple((x - y) % self.p for x, y in zip(a, b))

    def neg(self, a):
        return tuple((-x) % self.p for x in a)

    def mul(self, a, b):
        p, m, mod = self.p, self.m, self.mod
        tmp = [0] * (2 * m - 1)
        for i, x in enumerate(a):
            if x:
                for j, y in enumerate(b):
                    tmp[i + j] = (tmp[i + j] + x * y) % p
        for d in range(2 * m - 2, m - 1, -1):
            c = tmp[d]
            if c:
                tmp[d] = 0
                # x^d = x^{d-m} * x^m = x^{d-m} * (-(mod - x^m))
                for j in range(m):
                    tmp[d - m + j] = (tmp[d - m + j] - c * mod[j]) % p
        return tuple(tmp[:m])

    def pow(self, a, e):
        r = self.one()
        base = a
        while e:
            if e & 1:
                r = self.mul(r, base)
            base = self.mul(base, base)
            e >>= 1
        return r

    def one(self):
        return tuple([1] + [0] * (self.m - 1))

    def zero(self):
        return tuple([0] * self.m)

    def from_int(self, i):
        return tuple([i % self.p] + [0] * (self.m - 1))

    def frob(self, a, k):
        """a -> a^(p^k)."""
        return self.pow(a, self.p ** k) if k else a

    def frob_inv(self, a, k):
        return self.pow(a, self.p ** (self.m - k)) if k % self.m else a

    def elements(self):
        return [tuple(t) for t in product(range(self.p), repeat=self.m)]


def poly_deg(F, f):
    """Degree of a polynomial (list of field elements), -1 for the zero poly."""
    d = len(f) - 1
    while d >= 0 and f[d] == F.zero():
        d -= 1
    return d


def _poly_inv(F, a):
    return F.pow(a, F.q - 2)


def poly_monic(F, f):
    d = poly_deg(F, f)
    if d < 0:
        return []
    inv = _poly_inv(F, f[d])
    return [F.mul(c, inv) for c in f[:d + 1]]


def poly_equal(F, f, g):
    df, dg = poly_deg(F, f), poly_deg(F, g)
    if df != dg:
        return False
    return all(f[i] == g[i] for i in range(df + 1))


def poly_divmod(F, f, g):
    """Quotient and trimmed remainder of f / g; g must be monic and nonzero."""
    f = list(f)
    dg = poly_deg(F, g)
    if dg < 0:
        raise ValueError("division by the zero polynomial")
    inv = _poly_inv(F, g[dg])
    df = poly_deg(F, f)
    if df < dg:
        return [F.zero()], f[:max(0, df + 1)]
    q = [F.zero()] * (df - dg + 1)
    while True:
        df = poly_deg(F, f)
        if df < dg or df < 0:
            break
        c = F.mul(f[df], inv)
        q[df - dg] = F.add(q[df - dg], c)
        for i in range(dg + 1):
            f[df - dg + i] = F.sub(f[df - dg + i], F.mul(c, g[i]))
    dr = poly_deg(F, f)
    return q, (f[:dr + 1] if dr >= 0 else [])


def monic_polys(F, d):
    for coeffs in product(F.elements(), repeat=d):
        yield list(coeffs) + [F.one()]


def is_irreducible(F, f):
    """Trial division by every monic polynomial of degree <= deg(f)/2."""
    d = poly_deg(F, f)
    if d <= 0:
        return False
    if d == 1:
        return True
    for e in range(1, d // 2 + 1):
        for g in monic_polys(F, e):
            _, r = poly_divmod(F, f, g)
            if poly_deg(F, r) < 0:
                return False
    return True


def factor_distinct(F, poly):
    """
    Distinct monic irreducible factors of the square-free polynomial `poly`.
    Linear factors are found by root evaluation; the remaining part is split
    by trial division by all monic polynomials of degree at most half its
    degree, recursively.  This is a genuine irreducibility test and uses only
    the Python standard library.
    """
    rest = poly_monic(F, poly)
    out = []
    for x in F.elements():
        lin = [F.neg(x), F.one()]
        while True:
            q, r = poly_divmod(F, rest, lin)
            if poly_deg(F, r) < 0:
                out.append(lin)
                rest = poly_monic(F, q)
            else:
                break
    while True:
        r = poly_deg(F, rest)
        if r <= 0:
            break
        found = None
        q_found = None
        for d in range(1, r // 2 + 1):
            for f in monic_polys(F, d):
                q, r2 = poly_divmod(F, rest, f)
                if poly_deg(F, r2) < 0:
                    found, q_found = f, q
                    break
            if found is not None:
                break
        if found is None:
            out.append(rest)
            break
        out.extend(factor_distinct(F, found))
        rest = poly_monic(F, q_found)
    return out


def field_inv_lead(field, a):
    """inverse of the nonzero element a (by Fermat)."""
    return field.pow(a, field.q - 2)


def poly_eval(field, f, x):
    acc = field.zero()
    for c in reversed(f):
        acc = field.add(field.mul(acc, x), c)
    return acc


def poly_roots(field, f):
    return [x for x in field.elements() if poly_eval(field, f, x) == field.zero()]


# ------------------------------------------------------- Level A checks
def check_A(out):
    ok = True

    # A1 trace vs brute force
    cases = 0
    for M in range(1, 6):
        for w in (1, 2):
            for a in range(1, 7):
                if (M + 1) ** a > 200000:
                    continue
                t = orbit_enumerator_trace(a, M, w)
                b = orbit_enumerator_bruteforce(a, M, w)
                cases += 1
                if t != b:
                    ok = False
                    out.append(f"FAIL A1 (a,M,w)=({a},{M},{w})")
    out.append(f"{'PASS' if ok else 'FAIL'} A1  transfer trace == brute force ({cases} cases)")

    # A2 closed forms
    ok2 = True
    for M in range(1, 7):
        for w in (1, 2, 3):
            for a in (1, 2):
                if orbit_enumerator_small(a, M, w) != orbit_enumerator_trace(a, M, w):
                    ok2 = False
                    out.append(f"FAIL A2 (a,M,w)=({a},{M},{w})")
    out.append(f"{'PASS' if ok2 else 'FAIL'} A2  closed forms a=1,2 (Proposition 5.6)")

    # A3 symmetry, A4 checksum, A5 LCD count
    ok3 = True
    for M in range(1, 5):
        for orb in [[(1, 1)], [(2, 1)], [(3, 1)], [(1, 2), (2, 1)], [(4, 2)], [(2, 2), (3, 1)]]:
            fam = Family("tmp", n=None or 1, M=M, orbits=orb)
            E = fam.enumerator()
            W = sum(M * w * a for a, w in orb)
            for (K, H), c in E.items():
                if E.get((W - K, H), 0) != c:
                    ok3 = False
                    out.append(f"FAIL A3 M={M} orb={orb} at {(K, H)}")
            if sum(E.values()) != (M + 1) ** sum(a for a, _ in orb):
                ok3 = False
                out.append(f"FAIL A4 M={M} orb={orb}")
            if fam.lcd_count() != 2 ** len(orb):
                ok3 = False
                out.append(f"FAIL A5 M={M} orb={orb}: LCD={fam.lcd_count()}")
    out.append(f"{'PASS' if ok3 else 'FAIL'} A3-A5  symmetry, checksum, LCD count = 2^#orbits")

    # A6 trapezoid support
    ok4 = True
    for M in range(1, 6):
        for a in range(1, 7):
            E = orbit_enumerator_trace(a, M, 1)
            support = {k for k in E}
            expect = {(R, H) for R in range(a * M + 1) for H in range(a * M + 1)
                      if min(R, M, a * M - R) <= H <= min(R, a * M - R)}
            if support != expect:
                ok4 = False
                out.append(f"FAIL A6 (a,M)=({a},{M}) missing={sorted(expect - support)[:5]} "
                           f"extra={sorted(support - expect)[:5]}")
    out.append(f"{'PASS' if ok4 else 'FAIL'} A6  one-orbit support = trapezoid (Theorem 6.3)")

    # A7 / A8 moment formulas
    ok5 = True
    for M in range(1, 8):
        for orb in [[(1, 1)], [(1, 2)], [(2, 1)], [(3, 1)], [(4, 1)], [(2, 2), (3, 1)],
                    [(1, 1), (1, 2)], [(5, 1)], [(2, 1), (2, 1)]]:
            fam = Family("tmp", n=1, M=M, orbits=orb)
            mH, vH = fam.mean_var_hull()
            pred_m = Fraction(0)
            pred_v = Fraction(0)
            for a, w in orb:
                # a length-one orbit has mean nu(M); longer orbits a*mu(M)
                pred_m += w * (nu(M) if a == 1 else a * mu(M))
                pred_v += w * w * v(a, M)
            if mH != pred_m or vH != pred_v:
                ok5 = False
                out.append(f"FAIL A7 M={M} orb={orb}: {mH},{vH} vs {pred_m},{pred_v}")
            mK, vK = fam.mean_var_dim()
            wf = [w for a, w in orb for _ in range(a)]
            if vK != Fraction(M * (M + 2), 12) * sum(x * x for x in wf):
                ok5 = False
                out.append(f"FAIL A8 M={M} orb={orb}")
            if fam.covariance() != 0:
                ok5 = False
                out.append(f"FAIL A7 Cov M={M} orb={orb}")
    out.append(f"{'PASS' if ok5 else 'FAIL'} A7-A8  means, variances, Cov = 0 (Proposition 7.4)")

    # A10 the M = 1 matrix
    T = transfer_matrix(1, 1)
    expect = [[{(1, 0): 1}, {(0, 0): 1}], [{(1, 1): 1}, {(0, 0): 1}]]
    ok6 = T == expect
    out.append(f"{'PASS' if ok6 else 'FAIL'} A10 M=1 transfer matrix == Proposition 5.8")

    return all([ok, ok2, ok3, ok4, ok5, ok6])


def mu(M):
    return Fraction(M * (2 * M + 1), 6 * (M + 1))


def nu(M):
    """mean of min{X, M-X} for a length-1 orbit."""
    s = 0
    for r in range(M + 1):
        s += min(r, M - r)
    return Fraction(s, M + 1)


def v(a, M):
    if a == 1:
        # variance of min{X, M-X}
        vals = [min(r, M - r) for r in range(M + 1)]
        m = Fraction(sum(vals), M + 1)
        return Fraction(sum(x * x for x in vals), M + 1) - m * m
    if a == 2:
        return Fraction(M * (M + 2) * (M * M + 2 * M + 3), 18 * (M + 1) ** 2)
    return Fraction(a * M * (M + 2) * (M * M + 2 * M + 2), 60 * (M + 1) ** 2)


# ------------------------------------------------------- Level B checks
def hull_dim_formula(e, M, w):
    return w * sum(min(e[i], M - e[(i + 1) % len(e)]) for i in range(len(e)))


def gram_hull_dim(field, g_poly, n, k):
    """
    Dimension of the k-Galois hull of the constacyclic code with generator
    g_poly, computed as dim C - rank(B sigma^k(B)^T).  The ambient space is
    F^n; shifts of the generator that do not wrap give a basis, since
    deg g = n - dim C.  The twist lambda, the modulus and M are therefore not
    needed here (only the generator and sigma^k are).
    """
    d = len(g_poly) - 1               # degree of the generator
    dimC = n - d
    rows = []
    for i in range(dimC):
        # x^i * g mod (x^n - lambda): no wrap because i + d <= n-1
        vec = [field.zero()] * n
        for j, c in enumerate(g_poly):
            vec[i + j] = c
        rows.append(vec)
    # Gram matrix G = B * sigma^k(B)^T ; rank over F
    sig = [[field.frob(c, k) for c in row] for row in rows]
    Gm = [[_inner(field, rows[i], sig[j]) for j in range(len(rows))]
          for i in range(len(rows))]
    return dimC - rank(field, Gm)


def _inner(field, u, v):
    acc = field.zero()
    for a, b in zip(u, v):
        acc = field.add(acc, field.mul(a, b))
    return acc


def rank(field, mat):
    A = [row[:] for row in mat]
    r = 0
    ncols = len(A[0]) if A else 0
    for c in range(ncols):
        piv = None
        for i in range(r, len(A)):
            if A[i][c] != field.zero():
                piv = i
                break
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        inv = field_inv_lead(field, A[r][c])
        A[r] = [field.mul(x, inv) for x in A[r]]
        for i in range(len(A)):
            if i != r and A[i][c] != field.zero():
                f = A[i][c]
                A[i] = [field.sub(A[i][j], field.mul(f, A[r][j])) for j in range(ncols)]
        r += 1
        if r == len(A):
            break
    return r



def reciprocal(F, f, k, d):
    """The normalized inverse-Frobenius reciprocal f^{#} of the paper."""
    r = len(f) - 1
    rho = lambda a: F.pow(a, F.p ** (d - k))
    inv = field_inv_lead(F, rho(f[0]))
    return [F.mul(rho(f[r - i]), inv) for i in range(r + 1)]


FAMILIES = [
    # (label, p, m, field modulus, n', M, k, lambda_0, expected skeleton or None)
    ("F_4, n'=3, M=2, k=1", 2, 2, [1, 1, 1], 3, 2, 1, None, None),
    ("F_4, n'=5, M=2, k=1", 2, 2, [1, 1, 1], 5, 2, 1, None, [(1, 1), (2, 2)]),
    ("F_4, n'=5, M=2, k=1, lam0=omega", 2, 2, [1, 1, 1], 5, 2, 1, "omega",
     [(1, 1), (2, 2)]),
    ("F_8, n'=7, M=2, k=1", 2, 3, [1, 1, 0, 1], 7, 2, 1, None, [(1, 1), (6, 1)]),
    ("F_3, n'=4, M=3, k=0", 3, 1, [0, 1], 4, 3, 0, None,
     [(1, 1), (1, 1), (1, 2)]),
    ("F_9, n'=4, M=3, k=1, lam0=i", 3, 2, [1, 0, 1], 4, 3, 1, "i", [(2, 2)]),
    ("F_9, n'=4, M=3, k=1, lam0=-1", 3, 2, [1, 0, 1], 4, 3, 1, "minus1",
     [(2, 1), (2, 1)]),
]


def check_B(out):
    """Level B: from the definitions (factorization of the kernel, explicit
    generator matrices, Gram-matrix ranks) recompute the hull dimension of
    every code of a small family, build the joint histogram, and compare it
    with the transfer-matrix product of Theorem 6.3."""
    ok = True
    for label, p, m, mod, n_prime, M, k, lam0_code, expect in FAMILIES:
        F = GF(p, m, mod)
        lam0 = _element(F, lam0_code)
        ok &= _verify_family(F, label, n_prime, M, k, lam0, expect, out)
    return ok


def _element(F, code):
    """Named elements used in the examples."""
    if code is None:
        return F.one()
    if code == "omega":                      # generator of F_4^* = F_2(omega)
        return tuple([0, 1] + [0] * (F.m - 2))
    if code == "i":                          # generator of F_9^* with x^2 = -1
        return tuple([0, 1] + [0] * (F.m - 2))
    if code == "minus1":
        return F.from_int(F.p - 1)
    if code == "omega2":
        w = _element(F, "omega")
        return F.mul(w, w)
    if code == "gen":
        for a in F.elements():
            if a == F.zero():
                continue
            if all(F.pow(a, r) != F.one() for r in range(1, F.q - 1)):
                return a
        raise ValueError("no generator found")
    if isinstance(code, str) and code.startswith("int:"):
        return F.from_int(int(code[4:]))
    raise ValueError(code)


def _verify_family(F, label, n_prime, M, k, lam0, expect, out):
    # The compatibility criterion of the paper is stated for the *absolute*
    # degree d_s = F.m of the component field, not for the base-field exponent e.
    lam = F.pow(lam0, M)
    compat0 = (F.pow(lam0, 1 + F.p ** (F.m - k)) == F.one())
    compat = (F.pow(lam, 1 + F.p ** (F.m - k)) == F.one())
    mu_twist = F.pow(F.pow(lam, F.q - 2), F.p ** (F.m - k))
    if not (compat0 and compat and mu_twist == lam):
        out.append(f"FAIL B  {label}: compatibility condition "
                   f"lambda_0^{{1+p^(d_s-k)}} = lambda^{{1+p^(d_s-k)}} = 1 "
                   f"and mu = lambda fails")
        return False
    kernel = [F.neg(lam0)] + [F.zero()] * (n_prime - 1) + [F.one()]
    factors = factor_distinct(F, kernel)
    degs = [len(f) - 1 for f in factors]
    d = F.m
    perm = {}
    for i, f in enumerate(factors):
        fh = reciprocal(F, f, k, d)
        perm[i] = next(t for t, g in enumerate(factors) if g == fh)
    used = [False] * len(factors)
    cycles = []
    for i in range(len(factors)):
        if used[i]:
            continue
        cyc, j = [], i
        while not used[j]:
            used[j] = True
            cyc.append(j)
            j = perm[j]
        cycles.append(cyc)
    skeleton = sorted((len(c), degs[c[0]]) for c in cycles)
    msg = f"{label}: {len(factors)} factors, orbit skeleton {skeleton}"
    if expect is not None and skeleton != sorted(expect):
        out.append(f"FAIL B  {msg}; expected {sorted(expect)}")
        return False

    n = n_prime * M
    hist = {}
    for e in product(range(M + 1), repeat=len(factors)):
        g = [F.one()]
        for f, ex in zip(factors, e):
            for _ in range(ex):
                g = _polymul(F, g, f)
        kappa = n - (len(g) - 1)
        eta = gram_hull_dim(F, g, n, k)
        want = 0
        for cyc in cycles:
            w = degs[cyc[0]]
            want += w * sum(min(e[cyc[t]], M - e[cyc[(t + 1) % len(cyc)]])
                            for t in range(len(cyc)))
        if eta != want:
            out.append(f"FAIL B  {msg}: e={e} Gram={eta} formula={want}")
            return False
        hist[(kappa, eta)] = hist.get((kappa, eta), 0) + 1
    fam = Family(label, n=n, M=M, orbits=[(len(c), degs[c[0]]) for c in cycles])
    ok = fam.enumerator() == hist
    out.append(f"{'PASS' if ok else 'FAIL'} B  {msg}; "
               f"Gram-rank histogram == trace product on all "
               f"{(M + 1) ** len(factors)} words")
    return ok


def _polymul(F, f, g):
    out = [F.zero()] * (len(f) + len(g) - 1)
    for i, x in enumerate(f):
        if x != F.zero():
            for j, y in enumerate(g):
                out[i + j] = F.add(out[i + j], F.mul(x, y))
    return out


# ------------------------------------------------------- the paper's tables
def paper_tables(out):
    """Reproduce the numbers of Table 1 / Examples 7.1-7.3, 8.1."""
    rows = []

    def row(name, n_prime, M, orbits, expect):
        fam = Family(name, n=n_prime * M, M=M, orbits=orbits)
        s = fam.summary()
        rows.append((name, s))
        bad = []
        for key, val in expect.items():
            if s[key] != val:
                bad.append(f"{key}: got {s[key]}, expected {val}")
        out.append(f"{'PASS' if not bad else 'FAIL'} table row {name}"
                   + ("" if not bad else "  " + "; ".join(bad)))
        return not bad

    ok = True
    # F_4, n=10
    ok &= row("F4", 5, 2, [(1, 1), (2, 2)],
              dict(codes=27, terms=15, LCD=4, SD=3, E_eta=Fraction(23, 9),
                   Var_eta=Fraction(194, 81)))
    # F_8, n=14
    ok &= row("F8", 7, 2, [(1, 1), (6, 1)],
              dict(codes=2187, terms=44, LCD=4, SD=3, E_eta=Fraction(11, 3),
                   Var_eta=Fraction(10, 9)))
    # F_3, n=12
    ok &= row("F3", 4, 3, [(1, 1), (1, 1), (1, 2)],
              dict(codes=64, terms=33, LCD=8, SD=0, E_eta=Fraction(2),
                   Var_eta=Fraction(3, 2)))
    # F_9, lambda_0 = i, n=12
    ok &= row("F9-i", 4, 3, [(2, 2)],
              dict(codes=16, terms=7, LCD=2, SD=4, E_eta=Fraction(7, 2),
                   Var_eta=Fraction(15, 4)))
    # F_9, lambda_0 = -1, n=12
    ok &= row("F9-m1", 4, 3, [(2, 1), (2, 1)],
              dict(codes=256, terms=22, LCD=4, SD=16, E_eta=Fraction(7, 2),
                   Var_eta=Fraction(15, 8)))
    # F_9, n=24
    ok &= row("F9-n24", 8, 3, [(1, 1)] * 4 + [(2, 1), (2, 1)],
              dict(codes=65536, terms=142, LCD=64, SD=0, E_eta=Fraction(11, 2),
                   Var_eta=Fraction(23, 8)))
    # F_25, n=30
    ok &= row("F25", 6, 5, [(1, 1)] * 6,
              dict(codes=46656, terms=191, LCD=64, SD=0, E_eta=Fraction(6),
                   Var_eta=Fraction(4)))
    # F_4 x F_16, n=10
    ok &= row("F4xF16", 5, 2, [(1, 1), (2, 2), (1, 2), (4, 2)],
              dict(codes=6561, terms=123, LCD=16, SD=9, E_eta=Fraction(23, 3),
                   Var_eta=Fraction(458, 81)))
    # F_32, n=62
    ok &= row("F32-M2", 31, 2, [(1, 1), (10, 1), (10, 1), (10, 1)],
              dict(codes=3 ** 31, terms=916, LCD=16, SD=27, E_eta=Fraction(17),
                   Var_eta=Fraction(14, 3)))
    # F_32, n=124
    ok &= row("F32-M4", 31, 4, [(1, 1), (10, 1), (10, 1), (10, 1)],
              dict(codes=5 ** 31, terms=3531, LCD=16, SD=125,
                   E_eta=Fraction(184, 5), Var_eta=Fraction(326, 25)))

    # the joint table of Example 7.1 (F_4, n = 10) and Example 7.2 (F_8)
    fam = Family("F4", n=10, M=2, orbits=[(1, 1), (2, 2)])
    E = fam.enumerator()
    f4 = {(k, h): c for (k, h), c in E.items()}
    want_f4 = {}
    table = {
        0: {0: 1}, 1: {1: 1}, 2: {0: 1, 2: 2}, 3: {3: 2}, 4: {2: 2, 4: 3},
        5: {5: 3}, 6: {2: 2, 4: 3}, 7: {3: 2}, 8: {0: 1, 2: 2}, 9: {1: 1},
        10: {0: 1},
    }
    for k, d in table.items():
        for h, c in d.items():
            want_f4[(k, h)] = c
    ok_t = f4 == want_f4
    out.append(f"{'PASS' if ok_t else 'FAIL'} Example 7.1 joint table (F_4, n=10)")

    fam8 = Family("F8", n=14, M=2, orbits=[(1, 1), (6, 1)])
    cond = fam8.conditional_mean(7)
    ok8 = (cond == Fraction(533, 131))
    out.append(f"{'PASS' if ok8 else 'FAIL'} Example 7.2 E[eta_1|kappa=7] = 533/131 "
               f"(got {cond})")

    fam32 = Family("F32", n=62, M=2, orbits=[(1, 1)] + [(10, 1)] * 3)
    mx, kx = fam32.max_conditional_mean()
    ok32 = (kx == 31 and abs(float(mx) - 17.392) < 5e-4)
    out.append(f"{'PASS' if ok32 else 'FAIL'} Example 8.1 max_k E[eta_1|kappa] "
               f"= 17.392 at kappa=31 (got {float(mx):.3f} at {kx})")

    # F_4, n = 5, M = 1 (Example 5.9)
    fam1 = Family("M1", n=5, M=1, orbits=[(1, 1), (2, 2)])
    E1 = fam1.enumerator()
    m1, v1 = fam1.mean_var_hull()
    ok1 = (E1 == {(0, 0): 1, (1, 0): 1, (2, 2): 2, (3, 2): 2, (4, 0): 1, (5, 0): 1}
           and m1 == 1 and v1 == 1 and fam1.lcd_count() == 4)
    out.append(f"{'PASS' if ok1 else 'FAIL'} Example 5.9 (M=1, F_4, n=5): "
               f"E={(len(E1))} terms, E[eta]={m1}, Var={v1}, LCD={fam1.lcd_count()}")
    ok &= ok1
    return ok



# ---------------------------------------------------------------------------
# Level C: independent brute-force finite-field verification
# ---------------------------------------------------------------------------
def C(p, m, mod, e, k, n_prime, M, lam0):
    return dict(p=p, m=m, mod=mod, e=e, k=k,
                n_prime=n_prime, M=M, lam0=lam0)


INDEPENDENT_FAMILIES = [
    ("F2-n4",        [C(2, 1, [0, 1], 1, 0, 1, 4, "int:1")]),
    ("F2-n6",        [C(2, 1, [0, 1], 1, 0, 3, 2, "int:1")]),
    ("F2-n12",       [C(2, 1, [0, 1], 1, 0, 3, 4, "int:1")]),
    ("F4-n4",        [C(2, 2, [1, 1, 1], 2, 0, 1, 4, "int:1")]),
    ("F4-n6-k1-l1",  [C(2, 2, [1, 1, 1], 2, 1, 3, 2, "int:1")]),
    ("F4-n6-k0-w",   [C(2, 2, [1, 1, 1], 2, 0, 3, 2, "omega")]),
    ("F4-n6-k1-w",   [C(2, 2, [1, 1, 1], 2, 1, 3, 2, "omega")]),
    ("F4-n12-k1-l1", [C(2, 2, [1, 1, 1], 2, 1, 3, 4, "int:1")]),
    ("F4-n12-k0-w",  [C(2, 2, [1, 1, 1], 2, 0, 3, 4, "omega")]),
    ("F3-n6-l1",     [C(3, 1, [0, 1], 1, 0, 2, 3, "int:1")]),
    ("F3-n6-l2",     [C(3, 1, [0, 1], 1, 0, 2, 3, "int:2")]),
    ("F3-n9",        [C(3, 1, [0, 1], 1, 0, 1, 9, "int:1")]),
    ("F5-n10-l2",    [C(5, 1, [0, 1], 1, 0, 2, 5, "int:2")]),
    ("F5-n10-l4",    [C(5, 1, [0, 1], 1, 0, 2, 5, "int:4")]),
    ("F9-n6-k0-i",   [C(3, 2, [1, 0, 1], 2, 0, 2, 3, "i")]),
    ("F9-n6-k1-i",   [C(3, 2, [1, 0, 1], 2, 1, 2, 3, "i")]),
    ("F9-n6-k0-gen", [C(3, 2, [1, 0, 1], 2, 0, 2, 3, "gen")]),
    ("F9-n9-k1-l1",  [C(3, 2, [1, 0, 1], 2, 1, 1, 9, "int:1")]),
    ("F4xF16",       [C(2, 2, [1, 1, 1], 2, 1, 5, 2, "int:1"),
                      C(2, 4, [1, 1, 0, 0, 1], 2, 1, 5, 2, "int:1")]),
    ("F4xF4-inc",    [C(2, 2, [1, 1, 1], 2, 0, 3, 2, "int:1"),
                      C(2, 2, [1, 1, 1], 2, 0, 3, 2, "omega")]),
]


def _check_independent_family(label, comps, out):
    """Brute-force all codes of one (possibly multi-component) family from the
    definitions and compare every printed quantity with Family."""
    p = comps[0]["p"]
    e = comps[0]["e"]
    k = comps[0]["k"]
    n_prime = comps[0]["n_prime"]
    M = comps[0]["M"]
    for c in comps:
        assert (c["p"], c["e"], c["k"], c["n_prime"], c["M"]) == (p, e, k, n_prime, M)
    assert 0 <= k < e
    assert n_prime % p != 0
    t, mm = 0, 1
    while mm < M:
        mm *= p
        t += 1
    assert mm == M and t >= 1
    n = n_prime * M

    comp_infos = []
    w_f_list = []
    orbits = []
    inc_weights = []
    start = 0
    sum_ms = 0
    for c in comps:
        F = GF(p, c["m"], c["mod"])
        assert c["m"] % e == 0
        m_s = c["m"] // e
        sum_ms += m_s
        lam0 = _element(F, c["lam0"])
        assert lam0 != F.zero()
        kernel = [F.neg(lam0)] + [F.zero()] * (n_prime - 1) + [F.one()]
        assert poly_deg(F, kernel) == n_prime
        factors = factor_distinct(F, kernel)
        degs = [poly_deg(F, f) for f in factors]
        assert sum(degs) == n_prime
        assert len(set(tuple(f) for f in factors)) == len(factors)
        assert all(f[-1] == F.one() for f in factors)
        lam = F.pow(lam0, M)
        mu_twist = F.pow(F.pow(lam, F.q - 2), F.p ** (F.m - k))
        compat = (F.pow(lam0, 1 + F.p ** (F.m - k)) == F.one())
        assert (F.pow(lam, 1 + F.p ** (F.m - k)) == F.one()) == compat
        if compat:
            assert mu_twist == lam
            perm = {}
            for i, f in enumerate(factors):
                fh = reciprocal(F, f, k, F.m)
                assert poly_deg(F, fh) == degs[i]
                matches = [j for j, g in enumerate(factors) if poly_equal(F, g, fh)]
                assert len(matches) == 1
                perm[i] = matches[0]
            assert sorted(perm.values()) == list(range(len(factors)))
            used = [False] * len(factors)
            cycles = []
            for i in range(len(factors)):
                if used[i]:
                    continue
                cyc, j = [], i
                while not used[j]:
                    used[j] = True
                    cyc.append(j)
                    j = perm[j]
                cycles.append(cyc)
            for cyc in cycles:
                assert len(set(degs[j] for j in cyc)) == 1
            comp_orbits = [(len(cyc), m_s * degs[cyc[0]]) for cyc in cycles]
            orbits.extend(comp_orbits)
            comp_cycles = cycles
        else:
            assert mu_twist != lam
            comp_orbits = []
            comp_cycles = []
            inc_weights.extend(m_s * d for d in degs)
        comp_infos.append(dict(F=F, m_s=m_s, lam0=lam0, lam=lam, mu=mu_twist,
                               compatible=compat, factors=factors, degs=degs,
                               cycles=comp_cycles, start=start,
                               n=n, M=M, k=k))
        w_f_list.extend(m_s * d for d in degs)
        start += len(factors)

    N_F = len(w_f_list)
    assert sum(a for a, _ in orbits) + len(inc_weights) == N_F
    W = M * sum(w_f_list)
    assert W == n * sum_ms
    assert sum(w_f_list) == n_prime * sum_ms
    fam = Family(label, n=n, M=M, orbits=orbits,
                 incompatible_weights=inc_weights, N_F=N_F)
    assert fam.W() == W

    hist = {}
    for ev in product(range(M + 1), repeat=N_F):
        kappa = 0
        eta = 0
        expected_kappa = sum(w * (M - ex) for w, ex in zip(w_f_list, ev))
        want_eta = 0
        for ci in comp_infos:
            F = ci["F"]
            m_s = ci["m_s"]
            degs = ci["degs"]
            factors = ci["factors"]
            st = ci["start"]
            exps = ev[st:st + len(factors)]
            g = [F.one()]
            for f, ex in zip(factors, exps):
                for _ in range(ex):
                    g = _polymul(F, g, f)
            assert g[-1] == F.one()
            deg_g = poly_deg(F, g)
            assert deg_g == sum(d * ex for d, ex in zip(degs, exps))
            dim_K = n - deg_g
            kappa += m_s * dim_K
            hull_K = gram_hull_dim(F, g, n, k)
            comp_eta = m_s * hull_K
            if ci["compatible"]:
                comp_want = 0
                for cyc in ci["cycles"]:
                    w = m_s * degs[cyc[0]]
                    comp_want += w * sum(
                        min(exps[cyc[j]], M - exps[cyc[(j + 1) % len(cyc)]])
                        for j in range(len(cyc)))
            else:
                comp_want = 0
            assert comp_eta == comp_want, (label, ev, comp_eta, comp_want)
            eta += comp_eta
            want_eta += comp_want
        assert kappa == expected_kappa, (label, ev, kappa, expected_kappa)
        assert eta == want_eta
        hist[(kappa, eta)] = hist.get((kappa, eta), 0) + 1

    tot = sum(hist.values())
    codes = (M + 1) ** N_F
    terms = len(hist)
    LCD = sum(c for (K, H), c in hist.items() if H == 0)
    SO = sum(c for (K, H), c in hist.items() if H == K)
    SD = sum(c for (K, H), c in hist.items() if H == K and 2 * K == W)
    E_eta = Fraction(sum(H * c for (K, H), c in hist.items()), tot)
    Var_eta = Fraction(sum(H * H * c for (K, H), c in hist.items()), tot) - E_eta * E_eta
    E_kappa = Fraction(sum(K * c for (K, H), c in hist.items()), tot)
    Var_kappa = Fraction(sum(K * K * c for (K, H), c in hist.items()), tot) - E_kappa * E_kappa
    Cov = Fraction(sum(K * H * c for (K, H), c in hist.items()), tot) - E_kappa * E_eta

    E_eta_f = sum(w * (nu(M) if a == 1 else a * mu(M)) for a, w in orbits)
    Var_eta_f = sum(w * w * v(a, M) for a, w in orbits)
    Var_kappa_f = Fraction(M * (M + 2), 12) * sum(w * w for w in w_f_list)
    LCD_f = (M + 1) ** len(inc_weights) * 2 ** len(orbits)
    SO_f = 1
    for a, _w in orbits:
        SO_f *= restricted_orbit_count(a, M, "so")
    SD_f = 0 if inc_weights else 1
    for a, _w in orbits:
        SD_f *= restricted_orbit_count(a, M, "sd")

    ks = sorted({K for (K, _H) in hist})
    def cond(K):
        num = sum(H * c for (k, H), c in hist.items() if k == K)
        den = sum(c for (k, _H), c in hist.items() if k == K)
        return Fraction(num, den) if den else None
    max_cond_f = max((cond(K), K) for K in ks)

    expected_summary = dict(codes=codes, terms=terms, LCD=LCD, SO=SO, SD=SD,
                            E_eta=E_eta, Var_eta=Var_eta,
                            E_kappa=E_kappa, Var_kappa=Var_kappa, Cov=Cov)
    checks = [
        ("codes", tot == codes == fam.total_codes()),
        ("terms", terms == fam.joint_terms()),
        ("enumerator", fam.enumerator() == hist),
        ("W", fam.W() == W),
        ("symmetry", all(hist[(K, H)] == hist.get((W - K, H), 0)
                         for (K, H) in hist)),
        ("LCD", fam.lcd_count() == LCD == LCD_f),
        ("SO", fam.self_orthogonal_count() == SO == SO_f),
        ("SD", fam.self_dual_count() == SD == SD_f),
        ("mean_var_hull", fam.mean_var_hull() == (E_eta, Var_eta)
                          == (E_eta_f, Var_eta_f)),
        ("mean_var_dim", fam.mean_var_dim() == (E_kappa, Var_kappa)),
        ("Var_kappa formula", Var_kappa == Var_kappa_f),
        ("E_kappa", E_kappa == Fraction(W, 2)),
        ("Cov", fam.covariance() == Cov == 0),
        ("conditional means", all(fam.conditional_mean(K) == cond(K) for K in ks)),
        ("max conditional", fam.max_conditional_mean() == max_cond_f),
        ("summary", all(fam.summary()[key] == val
                        for key, val in expected_summary.items())),
    ]
    bad = [name for name, ok in checks if not ok]
    if bad:
        out.append(f"FAIL C  {label}: {', '.join(bad)} "
                   f"(N_F={N_F}, W={W}, orbits={orbits}, inc={inc_weights})")
        return False
    out.append(f"PASS C  {label}: {(M+1)**N_F} brute-force codes, "
               f"N_F={N_F}, W={W}, orbits={orbits}, "
               f"incompatible_weights={inc_weights}")
    return True


def check_C(out):
    ok = True
    for label, comps in INDEPENDENT_FAMILIES:
        ok &= _check_independent_family(label, comps, out)
    out.append(f"{'PASS' if ok else 'FAIL'} C  independent brute-force finite-field checks "
               f"({len(INDEPENDENT_FAMILIES)} families)")
    return ok


# ---------------------------------------------------------------------------
# Every printed number in the examples / captions
# ---------------------------------------------------------------------------
def paper_extras(out):
    ok = True
    # Example 8.1 self-orthogonal count and conditional-mean peaks
    f2 = Family("F32", n=62, M=2, orbits=[(1, 1)] + [(10, 1)] * 3)
    f4 = Family("F32", n=124, M=4, orbits=[(1, 1)] + [(10, 1)] * 3)
    so2 = f2.self_orthogonal_count()
    ok_so = (so2 == 70639674082)
    out.append(f"{'PASS' if ok_so else 'FAIL'} Example 8.1 self-orthogonal count "
               f"= 70639674082 (got {so2})")
    ok &= ok_so
    W2, W4 = f2.W(), f4.W()
    okW = (W2 == 62 and W4 == 124)
    out.append(f"{'PASS' if okW else 'FAIL'} Example 8.1 W = 62, 124 (got {W2}, {W4})")
    ok &= okW
    mx2, kx2 = f2.max_conditional_mean()
    mx4, kx4 = f4.max_conditional_mean()
    r2, r4 = float(mx2) / W2, float(mx4) / W4
    okpeak = (kx2 == 31 and abs(r2 - 0.281) < 0.001
              and abs(r4 - 0.302) < 0.001)
    out.append(f"{'PASS' if okpeak else 'FAIL'} Example 8.1 conditional peaks "
               f"~0.281W, 0.302W (got {r2:.4f} at k={kx2}, {r4:.4f} at k={kx4})")
    ok &= okpeak
    skel = float((Fraction(1, 4) + Fraction(30, 3)) / 31)
    oks = abs(skel - 0.331) < 0.001
    out.append(f"{'PASS' if oks else 'FAIL'} Example 8.1 skeleton limit "
               f"(1/4+30/3)/31 ~ 0.331 (got {skel:.4f})")
    ok &= oks

    # Figure 2 caption: only kappa in {1,3,11,13} occur at eta = 1
    f8 = Family("F8", n=14, M=2, orbits=[(1, 1), (6, 1)])
    at1 = sorted(K for (K, H), c in f8.enumerator().items() if H == 1 and c)
    okf8 = (at1 == [1, 3, 11, 13])
    out.append(f"{'PASS' if okf8 else 'FAIL'} Figure 2 caption: eta=1 only at "
               f"kappa in {{1,3,11,13}} (got {at1})")
    ok &= okf8

    # Example 7.3(b): eta = min(kappa, 12-kappa) is forced
    f9i = Family("F9-i", n=12, M=3, orbits=[(2, 2)])
    okforced = all(2 * H == 2 * min(K, 12 - K)
                   for (K, H), c in f9i.enumerator().items() if c)
    out.append(f"{'PASS' if okforced else 'FAIL'} Example 7.3(b) forced "
               f"eta = min(kappa,12-kappa)")
    ok &= okforced

    # Example 7.3(c): loop mean nu_5 = 1
    oknu = (nu(5) == 1)
    out.append(f"{'PASS' if oknu else 'FAIL'} Example 7.3(c) nu_5 = 1 (got {nu(5)})")
    ok &= oknu

    # Example 4.5 (incompatible twist): six codes (kappa,eta)=(10-2e,0)
    f5 = Family("F5-inc", n=10, M=5, orbits=[], incompatible_weights=[2])
    want5 = {(10 - 2 * e, 0): 1 for e in range(6)}
    ok5 = (f5.enumerator() == want5 and f5.lcd_count() == 6
           and f5.self_orthogonal_count() == 1 and f5.self_dual_count() == 0
           and f5.W() == 10)
    out.append(f"{'PASS' if ok5 else 'FAIL'} Example 4.5 incompatible F_5 twist: "
               f"six codes (10-2e,0), LCD=6, SO=1, SD=0, W=10")
    ok &= ok5

    # Example 7.4 (mixed product algebra): W = 30
    fmix = Family("F4xF16", n=10, M=2,
                  orbits=[(1, 1), (2, 2), (1, 2), (4, 2)])
    okmix = (fmix.W() == 30)
    out.append(f"{'PASS' if okmix else 'FAIL'} Example 7.4 W = 30 (got {fmix.W()})")
    ok &= okmix

    # Example 5.9 (M=1) and Table I counts already covered in paper_tables;
    # check the explicit LCD subset-sums of Example 7.1.
    f4ex = Family("F4", n=10, M=2, orbits=[(1, 1), (2, 2)])
    lcdk = sorted(K for (K, H), c in f4ex.enumerator().items() if H == 0 and c)
    oklcd = (lcdk == [0, 2, 8, 10])
    out.append(f"{'PASS' if oklcd else 'FAIL'} Example 7.1 LCD kappa subset-sums "
               f"{{0,2,8,10}} (got {lcdk})")
    ok &= oklcd

    out.append(f"{'PASS' if ok else 'FAIL'} all printed example/caption numbers")
    return ok


def main():
    out = []
    okA = check_A(out)
    okT = paper_tables(out)
    okB = check_B(out)          # no silent skip: a failure must fail the run
    okC = check_C(out)
    okE = paper_extras(out)
    print("\n".join(out))
    print()
    print("ALL CHECKS PASSED" if (okA and okT and okB and okC and okE)
          else "SOME CHECKS FAILED")
    return 0 if (okA and okT and okB and okC and okE) else 1


if __name__ == "__main__":
    sys.exit(main())
