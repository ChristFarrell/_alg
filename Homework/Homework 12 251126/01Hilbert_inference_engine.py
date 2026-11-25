"""
05 - Hilbert's Dream: Mechanical Proof (Chapter 1)
==================================================
Hilbert asked: can theorem proving be automated, and can it prove EVERYTHING
that is true (completeness)?  Here is the simplest mechanical prover: forward
chaining with Modus Ponens
        P,  P => Q
        ----------
             Q
and a truth-table check showing what a logical "theorem" (tautology) is.

Run:  python 05_inference_engine.py
"""

from itertools import product


# --- 1. Forward-chaining inference engine -----------------------------------
def parse(text):
    """Lines containing '=>' are rules ('A & B => C'); other lines are facts."""
    facts, rules = set(), []
    for line in text.strip().splitlines():
        line = line.strip()
        if "=>" in line:
            left, right = line.split("=>")
            rules.append(([s.strip() for s in left.split("&")],
                          [s.strip() for s in right.split("&")]))
        elif line:
            facts.add(line)
    return facts, rules


def infer(facts, rules, verbose=True):
    facts = set(facts)
    round_no = 1
    while True:
        new_found = False
        if verbose:
            print(f"  --- round {round_no} ---")
        for premises, conclusions in rules:
            if all(p in facts for p in premises):          # Modus Ponens
                for c in conclusions:
                    if c not in facts:
                        facts.add(c)
                        new_found = True
                        if verbose:
                            print(f"  {' & '.join(premises)}  and  rule  =>  {c}")
        if not new_found:
            if verbose:
                print("  nothing new: done.")
            return facts
        round_no += 1


SIMPLE_KB = """
E & F => H
A => E
C => G
B => F
A
B
"""

ANIMAL_KB = """
has_hair => mammal
gives_milk => mammal
has_feathers => bird
flies & lays_eggs => bird
mammal & eats_meat => carnivore
mammal & has_hooves => ungulate
mammal & eats_meat & spots => cheetah
mammal & eats_meat & stripes => tiger
ungulate & long_legs & spots => giraffe
ungulate & stripes => zebra
bird & long_legs => ostrich
flies
lays_eggs
long_legs
"""


# --- 2. Theorems of propositional logic = tautologies ------------------------
IMPLIES = lambda p, q: (not p) or q


def is_tautology(formula, names):
    """True if the formula is true under EVERY assignment (a 'theorem')."""
    return all(formula(**dict(zip(names, vals)))
               for vals in product([False, True], repeat=len(names)))


if __name__ == "__main__":
    print(__doc__)

    print("Knowledge base 1: facts A, B")
    result = infer(*parse(SIMPLE_KB))
    print("  derived H?", "H" in result)

    print("\nKnowledge base 2: animals  (flies, lays_eggs, long_legs)")
    result = infer(*parse(ANIMAL_KB))
    print("  derived ostrich?", "ostrich" in result)

    print("\nThe Hilbert-style axioms of propositional logic are tautologies:")
    axioms = {
        "p -> (q -> p)":
            (lambda p, q: IMPLIES(p, IMPLIES(q, p)), "pq"),
        "(p -> (q -> r)) -> ((p -> q) -> (p -> r))":
            (lambda p, q, r: IMPLIES(IMPLIES(p, IMPLIES(q, r)), IMPLIES(IMPLIES(p, q), IMPLIES(p, r))), "pqr"),
        "(~p -> ~q) -> (q -> p)":
            (lambda p, q: IMPLIES(IMPLIES(not p, not q), IMPLIES(q, p)), "pq"),
    }
    for text, (f, names) in axioms.items():
        print(f"  {text:45} tautology: {is_tautology(f, names)}")

    print("\nA law such as De Morgan's is a theorem too:")
    de_morgan = lambda p, q: (not (p and q)) == ((not p) or (not q))
    print("  ~(p & q) == (~p | ~q)   tautology:", is_tautology(de_morgan, "pq"))

    print("""
Limits
------
The engine only derives single facts (like 'H'), not general LAWS such as
De Morgan's - that needs axioms plus richer rules.  And Goedel (next file)
showed that for arithmetic, NO fixed set of axioms and rules can derive
every true statement.  Hilbert's completeness hope fails.""")
