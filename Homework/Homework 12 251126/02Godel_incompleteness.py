"""
06 - Russell, Peano and Goedel (Chapter 2)
==========================================
Three ideas, each with a small demo:
  1. Russell's paradox  - naive set theory is inconsistent.
  2. Peano arithmetic   - numbers defined only from 0 and successor S.
  3. Goedel numbering + self-reference - the trick behind incompleteness.

Run:  python 06_godel_incompleteness.py
"""

import re
import sys

# --- 1. Russell's paradox ----------------------------------------------------
# Model a "set" as a membership predicate: A(x) means "x is in A".
# R = { x | x not in x }   ->   R(x) = not x(x).  Is R in R?   Evaluate R(R):
def russell():
    R = lambda x: not x(x)
    sys.setrecursionlimit(200)
    try:
        return R(R)
    except RecursionError:
        return "no answer: R(R) = not R(R) never settles"


# The barber: shaves exactly those who do not shave themselves.
def barber_shaves_self(assume):
    """The rule says: barber shaves himself  <=>  he does NOT shave himself."""
    return (not assume) == assume       # is the assumption consistent with the rule?


# --- 2. Peano arithmetic -----------------------------------------------------
# Only 0 and S(x) = x+1 exist.  Addition and multiplication come from axioms:
#   x + 0 = x            x + S(y) = S(x + y)
#   x * 0 = 0            x * S(y) = x*y + x
class Nat:
    def __init__(self, pred=None):
        self.pred = pred                      # None means zero
    def __repr__(self):
        return str(to_int(self))

ZERO = Nat()
S = lambda x: Nat(x)

def to_int(n):
    k = 0
    while n.pred is not None:
        n, k = n.pred, k + 1
    return k

def from_int(k):
    n = ZERO
    for _ in range(k):
        n = S(n)
    return n

def add(x, y):
    return x if y.pred is None else S(add(x, y.pred))       # axioms 3, 4

def mul(x, y):
    return ZERO if y.pred is None else add(mul(x, y.pred), x)  # axioms 5, 6


# --- 3. Goedel numbering and self-reference ----------------------------------
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
          73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151]

def godel_number(formula):
    """Encode a string as ONE integer: 2^c1 * 3^c2 * 5^c3 ... (c = char code)."""
    n = 1
    for p, ch in zip(PRIMES, formula):
        n *= p ** ord(ch)
    return n

def godel_decode(n):
    out = []
    for p in PRIMES:
        e = 0
        while n % p == 0:
            n //= p
            e += 1
        if e == 0:
            break
        out.append(chr(e))
    return "".join(out)


# For the self-reference construction we use a compact numbering (one byte per
# character, read as a big integer).  Any injective, computable encoding works.
def enc(text):  return int.from_bytes(text.encode(), "big")
def dec(n):     return n.to_bytes((n.bit_length() + 7) // 8, "big").decode()

def sub(n, m):
    """Goedel number of the formula obtained by putting the numeral m in place of
    the variable x inside the formula numbered n.  (A purely arithmetic function
    on numbers - exactly what the proof needs to express inside Peano arithmetic.)"""
    return enc(dec(n).replace("x", str(m)))


def build_goedel_sentence():
    template = "not Provable(sub(x,x))"       # T(x): "sub(x,x) is not provable"
    g = enc(template)                         # the REAL number of the template
    G = template.replace("x", str(g))         # G = T(g)
    return template, g, G


if __name__ == "__main__":
    print(__doc__)

    print("1. Russell's paradox")
    print("  R = {x | x not in x};  evaluating 'R in R' ->", russell())
    print("  barber consistent if he shaves himself?", barber_shaves_self(True))
    print("  barber consistent if he does not?      ", barber_shaves_self(False))
    print("  -> both assumptions fail: naive set theory needs repair (ZFC).")

    print("\n2. Peano arithmetic from 0 and S only")
    a, b = from_int(3), from_int(4)
    print("  3 + 4 =", add(a, b), "   3 * 4 =", mul(a, b))
    print("  axiom 1: 0 is never a successor ->", all(S(from_int(k)).pred is not None for k in range(5)))
    print("  axiom 3: x + 0 = x for x in 0..5 ->", all(to_int(add(from_int(k), ZERO)) == k for k in range(6)))
    print("  axiom 4: x + S(y) = S(x+y) for x,y in 0..5 ->",
          all(to_int(add(from_int(x), S(from_int(y)))) == to_int(S(add(from_int(x), from_int(y))))
              for x in range(6) for y in range(6)))

    print("\n3. Goedel numbering: statements about formulas become statements about numbers")
    for f in ["0=0", "Ax x=x"]:
        n = godel_number(f)
        digits = str(n)
        shown = digits if len(digits) <= 40 else digits[:20] + "..." + f" ({len(digits)} digits)"
        print(f"  {f!r:10} -> {shown}")
        assert godel_decode(n) == f
    print("  (decoding recovers the formula, so a number can 'talk about' a formula)")

    template, g, G = build_goedel_sentence()
    shown = lambda n: str(n) if len(str(n)) < 16 else str(n)[:6] + "..." + str(n)[-4:]
    print(f"\n  template T(x) = {template}")
    print(f"  g = godel number of T  = {shown(g)}  ({len(str(g))} digits)")
    print(f"  G = T(g)               = not Provable(sub({shown(g)},{shown(g)}))")

    # Verify the self-reference by actually computing it:
    inner = re.search(r"sub\((\d+),(\d+)\)", G)
    number_G_talks_about = sub(int(inner.group(1)), int(inner.group(2)))
    print(f"  the number inside G's claim, sub(g,g)  = {shown(number_G_talks_about)}")
    print(f"  the godel number of G itself            = {shown(enc(G))}")
    print("  equal? ->", number_G_talks_about == enc(G))
    assert number_G_talks_about == enc(G)
    print("  So G literally says: 'the formula with MY OWN number is not provable'.")

    print("""
Why that matters (Goedel 1931)
------------------------------
(The code above checks the self-reference. The next paragraph is the theorem
itself, which cannot be run - it is a statement about every consistent system.)

If the system proves G, then it proves something false (G says it is unprovable),
so the system would be inconsistent.  If it is consistent, G is true but
unprovable.  Hence any consistent system containing Peano arithmetic has true
statements it cannot prove.  Compare: Turing's halting proof uses the same
diagonal self-reference (see 04_turing_machine.py).

Note: Goedel's COMPLETENESS theorem (1929) is about first-order logic alone and
is not contradicted - adding Peano arithmetic is what makes proving
'Provable' expressible.""")