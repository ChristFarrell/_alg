"""
02 - Formal Grammars and the Chomsky Hierarchy
==============================================
A grammar generates a language by repeatedly rewriting symbols using rules.

  Type 3  Regular            A -> aB | a            machine: finite automaton   e.g. a^n b^m
  Type 2  Context-free       A -> gamma             machine: pushdown automaton e.g. a^n b^n
  Type 1  Context-sensitive  aAb -> a gamma b       machine: linear-bounded TM  e.g. a^n b^n c^n
  Type 0  Unrestricted       alpha -> beta          machine: Turing machine

Convention used here: UPPERCASE symbols are non-terminals (they must be rewritten),
lowercase symbols are terminals (the final output).

Run:  python 02_grammar.py
"""

import random


def generate(grammar, start="S", max_steps=200, rng=random):
    """Derive one sentence by applying randomly chosen rules.

    Returns the list of sentential forms (first = start symbol, last = final
    sentence), or None if the derivation got stuck or ran too long.

    grammar: dict mapping a left-hand side (tuple of symbols) to a list of
             right-hand sides (each a tuple of symbols).
    """
    form = [start]
    history = [list(form)]
    for _ in range(max_steps):
        # Every (position, lhs) where some rule could be applied right now.
        options = []
        for lhs in grammar:
            n = len(lhs)
            for i in range(len(form) - n + 1):
                if tuple(form[i:i + n]) == lhs:
                    options.append((i, lhs))
        if not options:                       # nothing left to rewrite
            done = not any(sym.isupper() for sym in form)
            return history if done else None  # stuck with non-terminals = failure
        i, lhs = rng.choice(options)
        rhs = rng.choice(grammar[lhs])
        form[i:i + len(lhs)] = list(rhs)
        history.append(list(form))
    return None


def sample(grammar, tries=1000, min_len=0, **kw):
    """Retry until a derivation succeeds (context-sensitive rules can dead-end)."""
    for _ in range(tries):
        h = generate(grammar, **kw)
        if h is not None and len(h[-1]) >= min_len:
            return h
    return None


def show(history):
    for form in history:
        print("   ", " ".join(form))


def G(rules):
    """Helper: write rules as {"A B": ["a A", "b"]} -> tuple form."""
    return {tuple(l.split()): [tuple(r.split()) for r in rs] for l, rs in rules.items()}


# ---------------------------------------------------------------------------
# Type 3 - regular:  a^n b^m   (n >= 0, m >= 1)
regular = G({
    "S": ["A"],
    "A": ["a A", "B"],
    "B": ["b B", "b"],
})

# Type 2 - context-free:  a^n b^n   (n >= 1)
context_free = G({"S": ["a S b", "a b"]})

# Type 1 - context-sensitive:  a^n b^n c^n   (n >= 1)
#   The key rule  C B -> B C  lets symbols swap places, which a CFG cannot do.
context_sensitive = G({
    "S":   ["a B C", "a S B C"],
    "C B": ["B C"],
    "a B": ["a b"],
    "b B": ["b b"],
    "b C": ["b c"],
    "c C": ["c c"],
})

# A natural-language flavoured context-free grammar
english = G({
    "S":  ["NP VP"],
    "NP": ["D N"],
    "VP": ["V NP"],
    "N":  ["dog", "cat"],
    "V":  ["eats", "chases"],
    "D":  ["a", "the"],
})


# ---------------------------------------------------------------------------
# Recognisers: the other direction (is a given string in the language?)
def is_anbm(s):                     # finite-state power is enough
    n = len(s) - len(s.lstrip("a"))
    rest = s[n:]
    return len(rest) >= 1 and set(rest) == {"b"}

def is_anbn(s):                     # needs a counter (a stack)
    n = len(s) // 2
    return len(s) % 2 == 0 and n >= 1 and s == "a" * n + "b" * n

def is_anbncn(s):                   # needs two comparisons at once
    n = len(s) // 3
    return len(s) % 3 == 0 and n >= 1 and s == "a" * n + "b" * n + "c" * n


if __name__ == "__main__":
    print(__doc__)
    random.seed(7)

    print("English sentences (context-free):")
    for _ in range(3):
        print("  ", " ".join(sample(english)[-1]))

    print("\nOne derivation, step by step (a^n b^n):")
    show(sample(context_free, min_len=6))

    print("\nOne derivation of a^n b^n c^n (watch the C B -> B C swaps):")
    show(sample(context_sensitive, min_len=6))

    print("\nChecking generated strings against recognisers:")
    for name, g, check in [("a^n b^m", regular, is_anbm),
                           ("a^n b^n", context_free, is_anbn),
                           ("a^n b^n c^n", context_sensitive, is_anbncn)]:
        words = ["".join(sample(g)[-1]) for _ in range(5)]
        print(f"  {name:12} {words}  all valid: {all(check(w) for w in words)}")
