"""
03 - Lambda Calculus (Alonzo Church)
====================================
The whole language has only two ingredients:
    (lambda x. M)     an anonymous function
    (M N)             applying M to N
and one computation rule, beta-reduction:   (lambda x. M) N  ->  M[x := N]

There are NO built-in booleans, numbers, or lists.  Everything is encoded
with functions.  Python lambdas are close enough to run these encodings.

Run:  python 03_lambda_calculus.py
"""

# --- Church booleans: a boolean is "a function that picks one of two options"
TRUE  = lambda t: lambda f: t
FALSE = lambda t: lambda f: f
IF    = lambda c: lambda t: lambda f: c(t)(f)
NOT   = lambda p: p(FALSE)(TRUE)
AND   = lambda p: lambda q: p(q)(p)
OR    = lambda p: lambda q: p(p)(q)

# --- Church numerals: the number n means "apply f, n times"
ZERO  = lambda f: lambda x: x
SUCC  = lambda n: lambda f: lambda x: f(n(f)(x))
ADD   = lambda m: lambda n: n(SUCC)(m)
MUL   = lambda m: lambda n: lambda f: m(n(f))
POW   = lambda b: lambda e: e(b)
PRED  = lambda n: lambda f: lambda x: n(lambda g: lambda h: h(g(f)))(lambda _: x)(lambda u: u)
SUB   = lambda m: lambda n: n(PRED)(m)
IS_ZERO = lambda n: n(lambda _: FALSE)(TRUE)
LEQ   = lambda m: lambda n: IS_ZERO(SUB(m)(n))

# --- Pairs and lists (like Lisp's cons/car/cdr)
PAIR  = lambda a: lambda b: lambda f: f(a)(b)
FIRST = lambda p: p(TRUE)
SECOND = lambda p: p(FALSE)
NIL   = lambda f: TRUE                      # the empty list
IS_NIL = lambda p: p(lambda a: lambda b: FALSE)

# --- Y combinator (the strict-evaluation "Z" form, which Python needs).
# It lets an anonymous function call ITSELF, giving us recursion without names.
Y = lambda f: (lambda x: f(lambda v: x(x)(v)))(lambda x: f(lambda v: x(x)(v)))

# Recursion on top of it
FACT = Y(lambda self: lambda n:
         IF(IS_ZERO(n))
           (lambda _: SUCC(ZERO))                       # 0! = 1
           (lambda _: MUL(n)(self(PRED(n))))            # n! = n * (n-1)!
           (NIL))

FIB = Y(lambda self: lambda n:
        IF(LEQ(n)(SUCC(ZERO)))
          (lambda _: n)                                 # fib(0)=0, fib(1)=1
          (lambda _: ADD(self(PRED(n)))(self(PRED(PRED(n)))))
          (NIL))


# --- Helpers to translate back to Python values (only for display!)
def to_int(n):  return n(lambda x: x + 1)(0)
def to_bool(b): return b(True)(False)
def from_int(k):
    n = ZERO
    for _ in range(k):
        n = SUCC(n)
    return n
def to_list(p):
    out = []
    while not to_bool(IS_NIL(p)):
        out.append(FIRST(p))
        p = SECOND(p)
    return out


if __name__ == "__main__":
    print(__doc__)

    print("Booleans")
    print("  IF TRUE  'yes' 'no' =", IF(TRUE)("yes")("no"))
    print("  IF FALSE 'yes' 'no' =", IF(FALSE)("yes")("no"))
    print("  AND(T,F) =", to_bool(AND(TRUE)(FALSE)), "  OR(T,F) =", to_bool(OR(TRUE)(FALSE)),
          "  NOT(T) =", to_bool(NOT(TRUE)))

    two, three = from_int(2), from_int(3)
    print("\nArithmetic on Church numerals")
    print("  2 + 3  =", to_int(ADD(two)(three)))
    print("  2 * 3  =", to_int(MUL(two)(three)))
    print("  2 ^ 3  =", to_int(POW(two)(three)))
    print("  3 - 2  =", to_int(SUB(three)(two)))
    print("  is 0 zero?", to_bool(IS_ZERO(ZERO)), "   is 3 zero?", to_bool(IS_ZERO(three)))

    print("\nPairs and lists")
    p = PAIR("left")("right")
    print("  FIRST(pair) =", FIRST(p), "  SECOND(pair) =", SECOND(p))
    lst = PAIR(from_int(1))(PAIR(from_int(2))(PAIR(from_int(3))(NIL)))
    print("  list [1,2,3] ->", [to_int(x) for x in to_list(lst)])

    print("\nRecursion via the Y combinator (no function has a name!)")
    print("  5!      =", to_int(FACT(from_int(5))))
    print("  fib(10) =", to_int(FIB(from_int(10))))

    print("""
Church's negative result (1936)
-------------------------------
There is no algorithm that decides whether two lambda terms are
beta-convertible (equal).  Deciding whether two functions behave the same
is impossible in general - a sibling of Turing's halting problem.""")
