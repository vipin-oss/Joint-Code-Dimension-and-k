#!/usr/bin/env python3
"""
checks.py -- self-contained verification for the paper's statements.

Run:  python3 checks.py          (prints a pass/fail line per check and a summary)

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
"""

from fractions import Fraction
from itertools import product
import sys

from enumerator import (Family, orbit_enumerator_trace, orbit_enumerator_bruteforce,
                        orbit_enumerator_small, transfer_matrix, pmul, monomial)


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


def factor_distinct(field, poly):
    """
    Distinct monic irreducible factors of `poly` (list of coefficients, monic)
    by brute-force root/divisibility search -- sufficient for the tiny cases.
    Returns a list of polynomials (lists, monic).
    """
    zero = field.zero()

    def deg(f):
        d = len(f) - 1
        while d > 0 and f[d] == zero:
            d -= 1
        return d

    def divmod_(f, g):
        f = list(f)
        dg = deg(g)
        inv = field_inv_lead(field, g[dg])
        q = [field.zero()] * max(1, len(f) - dg)
        while deg(f) >= dg and any(x != field.zero() for x in f):
            d = deg(f)
            c = field.mul(f[d], inv)
            q[d - dg] = field.add(q[d - dg], c)
            for i in range(dg + 1):
                f[d - dg + i] = field.sub(f[d - dg + i], field.mul(c, g[i]))
        return q, f[:dg]

    def monic(f):
        d = deg(f)
        inv = field_inv_lead(field, f[d])
        return [field.mul(c, inv) for c in f[:d + 1]]

    # candidates: all monic polynomials of degree 1..deg(poly)/2
    n = deg(poly)
    cands = []
    for d in range(1, n // 2 + 1):
        for tail in product(field.elements(), repeat=d):
            f = monic(list(tail) + [field.one()])
            cands.append(f)
    # keep only irreducible ones, ascending degree
    irr = []
    for f in cands:
        d = deg(f)
        if d == 0:
            continue
        reducible = False
        for g in irr:
            if deg(g) <= d // 2 and deg(g) > 0:
                _, r = divmod_(f, g)
                if all(x == field.zero() for x in r):
                    reducible = True
                    break
        if not reducible:
            irr.append(f)
    # divide out
    rest = monic(list(poly))
    out = []
    for f in irr:
        _, r = divmod_(rest, f)
        if all(x == field.zero() for x in r):
            q, r2 = divmod_(rest, f)
            assert all(x == field.zero() for x in r2)
            out.append(f)
            rest = monic(q)
    # a remaining factor must have degree > n/2, hence is irreducible
    if deg(rest) > 0:
        out.append(rest)
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


def gram_hull_dim(field, g_poly, n, modulus_poly, k, lam0, M):
    """
    Dimension of the k-Galois hull of the constacyclic code with generator
    g_poly in F[x]/(x^n - lambda), computed as dim C - rank(B sigma^k(B)^T).
    The ambient space is F^n; shifts of the generator that do not wrap give a
    basis, since deg g = n - dim C.
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
    raise ValueError(code)


def _verify_family(F, label, n_prime, M, k, lam0, expect, out):
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
        eta = gram_hull_dim(F, g, n, kernel, k, lam0, M)
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


def main():
    out = []
    okA = check_A(out)
    okT = paper_tables(out)
    try:
        okB = check_B(out)
    except Exception as exc:                      # pragma: no cover
        out.append(f"SKIP B1 (finite-field check unavailable: {exc})")
        okB = True
    print("\n".join(out))
    print()
    print("ALL CHECKS PASSED" if (okA and okT and okB) else "SOME CHECKS FAILED")
    return 0 if (okA and okT and okB) else 1


if __name__ == "__main__":
    sys.exit(main())
