#!/usr/bin/env python3
"""
enumerator.py -- reference implementation of the joint enumerator of the paper

    "Joint code-dimension and k-Galois-hull enumerators for repeated-root
     constacyclic codes over square-free affine algebras"

Everything here is exact integer arithmetic.  The bivariate enumerator is a
dict {(K,H): count} standing for sum count * U^K Z^H.

Input for a family is its *orbit skeleton*: the list of pairs (a_O, w_O)
(orbit length, orbit weight) for the compatible components, together with the
list of factor weights w_f for the incompatible components.  By Theorem 6.3
the global enumerator is

    prod over compatible orbits   tr( T_w(U,Z)^a )
    prod over incompatible factors (1 + U^{w_f} + ... + U^{M w_f}),

with T_w(U,Z)[alpha][beta] = U^{w(M-beta)} Z^{w min{alpha, M-beta}}, rows and
columns indexed by alpha, beta in {0,...,M}.
"""

from itertools import product
from fractions import Fraction


# --------------------------------------------------------------------------
# polynomials in U, Z with integer coefficients
# --------------------------------------------------------------------------
def pmul(p, q):
    out = {}
    for (k1, h1), c1 in p.items():
        for (k2, h2), c2 in q.items():
            key = (k1 + k2, h1 + h2)
            out[key] = out.get(key, 0) + c1 * c2
    return {k: v for k, v in out.items() if v}


def padd(p, q):
    out = dict(p)
    for k, v in q.items():
        out[k] = out.get(k, 0) + v
    return {k: v for k, v in out.items() if v}


def monomial(k, h, c=1):
    return {(k, h): c} if c else {}


# --------------------------------------------------------------------------
# one orbit
# --------------------------------------------------------------------------
def transfer_matrix(M, w):
    """T^{(M)}_w as a list of lists of polynomials."""
    return [[monomial(w * (M - b), w * min(a, M - b)) for b in range(M + 1)]
            for a in range(M + 1)]


def matrix_power(T, n):
    """n-th power of a square matrix of polynomials."""
    d = len(T)
    # identity
    R = [[monomial(0, 0) if i == j else {} for j in range(d)] for i in range(d)]
    B = T
    while n:
        if n & 1:
            R = [[_dot(R[i], [B[k][j] for k in range(d)]) for j in range(d)]
                 for i in range(d)]
        B = [[_dot(B[i], [B[k][j] for k in range(d)]) for j in range(d)]
             for i in range(d)]
        n >>= 1
    return R


def _dot(row, cols):
    acc = {}
    for c, entry in zip(row, cols):
        if c and entry:
            acc = padd(acc, pmul(c, entry))
    return acc


def orbit_enumerator_trace(a, M, w):
    """tr(T_w^a): the joint law of one orbit, computed by the transfer matrix."""
    T = transfer_matrix(M, w)
    P = matrix_power(T, a)
    out = {}
    for i in range(len(T)):
        out = padd(out, P[i][i])
    return out


def orbit_enumerator_bruteforce(a, M, w):
    """Direct enumeration of all (M+1)^a exponent words of one orbit."""
    out = {}
    for e in product(range(M + 1), repeat=a):
        K = w * sum(M - e[i] for i in range(a))
        H = w * sum(min(e[i], M - e[(i + 1) % a]) for i in range(a))
        out[(K, H)] = out.get((K, H), 0) + 1
    return out


def orbit_enumerator_small(a, M, w):
    """Closed forms for a = 1, 2 (Proposition 5.6 of the paper)."""
    out = {}
    if a == 1:
        for r in range(M + 1):
            key = (w * r, w * min(r, M - r))
            out[key] = out.get(key, 0) + 1
        return out
    if a == 2:
        for R in range(2 * M + 1):
            key = (w * R, w * min(R, 2 * M - R))
            out[key] = out.get(key, 0) + M + 1 - abs(R - M)
        return out
    raise ValueError("closed form only for a = 1, 2")


# --------------------------------------------------------------------------
# restricted counts (self-orthogonal, dual-containing, self-dual words)
# --------------------------------------------------------------------------
def restricted_orbit_count(a, M, relation):
    """
    Number of words on one orbit of length a whose every edge e_{i-1}+e_i
    satisfies `relation`, where relation is 'so' (>= M), 'dc' (<= M) or
    'sd' (== M).  Implemented as tr(J^a) with J the corresponding 0/1 matrix.
    """
    def ok(prev, cur):
        s = prev + cur
        return s >= M if relation == "so" else (s <= M if relation == "dc" else s == M)

    J = [[1 if ok(prev, cur) else 0 for cur in range(M + 1)]
         for prev in range(M + 1)]
    # integer matrix power
    def mul(A, B):
        d = len(A)
        return [[sum(A[i][k] * B[k][j] for k in range(d)) for j in range(d)]
                for i in range(d)]
    R = [[1 if i == j else 0 for j in range(M + 1)] for i in range(M + 1)]
    B = J
    n = a
    while n:
        if n & 1:
            R = mul(R, B)
        B = mul(B, B)
        n >>= 1
    return sum(R[i][i] for i in range(M + 1))


# --------------------------------------------------------------------------
# a family = orbit skeleton + incompatible factors
# --------------------------------------------------------------------------
class Family:
    def __init__(self, name, n, M, orbits, incompatible_weights=(), N_F=None):
        self.name = name
        self.n = n
        self.M = M
        self.orbits = list(orbits)                  # [(a_O, w_O), ...]
        self.incompatible_weights = list(incompatible_weights)
        # number of distinct kernel factors: orbits contribute a_O each
        n_orb = sum(a for a, _ in self.orbits)
        self.N_F = n_orb + len(self.incompatible_weights) if N_F is None else N_F

    # ---- global enumerator ------------------------------------------------
    def enumerator(self):
        E = monomial(0, 0)
        for a, w in self.orbits:
            E = pmul(E, orbit_enumerator_trace(a, self.M, w))
        for w in self.incompatible_weights:
            E = pmul(E, {(w * r, 0): 1 for r in range(self.M + 1)})
        return E

    # ---- the statistics quoted in the tables ------------------------------
    def total_codes(self):
        return (self.M + 1) ** self.N_F

    def joint_terms(self):
        return len(self.enumerator())

    def lcd_count(self):
        """Number of selections with eta_k = 0."""
        return sum(c for (K, H), c in self.enumerator().items() if H == 0)

    def self_orthogonal_count(self):
        c = (self.M + 1) ** len(self.incompatible_weights)
        for a, _w in self.orbits:
            c *= restricted_orbit_count(a, self.M, "so")
        return c

    def self_dual_count(self):
        c = 1 if not self.incompatible_weights else 0
        for a, _w in self.orbits:
            c *= restricted_orbit_count(a, self.M, "sd")
        return c

    def mean_var_hull(self):
        E = self.enumerator()
        tot = sum(E.values())
        # A(Z) = E(1, Z)
        A = {}
        for (K, H), c in E.items():
            A[H] = A.get(H, 0) + c
        m1 = Fraction(sum(h * c for h, c in A.items()), tot)
        m2 = Fraction(sum(h * h * c for h, c in A.items()), tot)
        return m1, m2 - m1 * m1

    def mean_var_dim(self):
        E = self.enumerator()
        tot = sum(E.values())
        A = {}
        for (K, H), c in E.items():
            A[K] = A.get(K, 0) + c
        m1 = Fraction(sum(k * c for k, c in A.items()), tot)
        m2 = Fraction(sum(k * k * c for k, c in A.items()), tot)
        return m1, m2 - m1 * m1

    def covariance(self):
        E = self.enumerator()
        tot = sum(E.values())
        mK = Fraction(sum(K * c for (K, H), c in E.items()), tot)
        mH = Fraction(sum(H * c for (K, H), c in E.items()), tot)
        mKH = Fraction(sum(K * H * c for (K, H), c in E.items()), tot)
        return mKH - mK * mH

    def W(self):
        return self.n * 1  # single field component of degree 1 over F_q

    def conditional_mean(self, K):
        """E[eta_k | kappa = K]."""
        E = self.enumerator()
        num = sum(h * c for (k, h), c in E.items() if k == K)
        den = sum(c for (k, h), c in E.items() if k == K)
        return Fraction(num, den) if den else None

    def max_conditional_mean(self):
        E = self.enumerator()
        ks = sorted({k for (k, _h) in E})
        return max((self.conditional_mean(k), k) for k in ks)

    def summary(self):
        mH, vH = self.mean_var_hull()
        mK, vK = self.mean_var_dim()
        return {
            "family": self.name,
            "n'": self.n,
            "M": self.M,
            "codes": self.total_codes(),
            "terms": self.joint_terms(),
            "LCD": self.lcd_count(),
            "SO": self.self_orthogonal_count(),
            "SD": self.self_dual_count(),
            "E_eta": mH,
            "Var_eta": vH,
            "E_kappa": mK,
            "Var_kappa": vK,
            "Cov": self.covariance(),
        }
