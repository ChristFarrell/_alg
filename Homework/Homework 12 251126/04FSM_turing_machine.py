"""
04 - Finite State Machine  ->  Turing Machine  ->  Halting Problem
===================================================================
Part 1  A finite state machine (DFA) has states but no memory.  It recognises
        REGULAR languages only (Chomsky Type 3).
Part 2  Add an unbounded tape the machine can read AND write, and you get a
        Turing machine:  Turing machine = finite state machine + tape.
        Formally (Q, Sigma, Gamma, delta, q0, q_accept, q_reject) with
            delta : Q x Gamma -> Q x Gamma x {L, R, -}
        The tape is memory, so it can recognise a^n b^n c^n and, by the
        Church-Turing thesis, anything computable.
Part 3  Even so, some questions no Turing machine can answer: the halting problem.

Run:  python 04_fsm_and_turing_machine.py
"""

import re
from itertools import product as _product


class DFA:
    def __init__(self, start, finals, delta):
        self.start = start
        self.finals = set(finals)
        self.delta = delta  # dict: (state, symbol) -> state

    def accepts(self, text, trace=False):
        state = self.start
        for ch in text:
            nxt = self.delta.get((state, ch))
            if trace:
                print(f"    {state} --{ch}--> {nxt}")
            if nxt is None:          # no transition = implicit dead state
                return False
            state = nxt
        return state in self.finals


def demo(title, dfa, words, regex=None):
    print(f"\n{title}")
    for w in words:
        verdict = dfa.accepts(w)
        line = f"  {w!r:12} -> {verdict}"
        if regex is not None:        # cross-check against a regular expression
            assert verdict == bool(re.fullmatch(regex, w)), "DFA and regex disagree!"
            line += "   (matches regex too)"
        print(line)


# 1. Even number of 0s in a binary string --------------------------------------
even_zeros = DFA("even", ["even"], {
    ("even", "0"): "odd",  ("even", "1"): "even",
    ("odd",  "0"): "even", ("odd",  "1"): "odd",
})

# 2. a*  (any number of a's, including none) -----------------------------------
only_a = DFA("s", ["s"], {("s", "a"): "s"})

# 3. a+ b+  (one or more a's followed by one or more b's) ----------------------
a_then_b = DFA("A", ["B"], {
    ("A", "a"): "A2", ("A2", "a"): "A2", ("A2", "b"): "B",
    ("B", "b"): "B",
})

# --- Why some languages are NOT regular: count distinguishable prefixes --------
def in_anbn(w):
    n = len(w) // 2
    return len(w) % 2 == 0 and w == "a" * n + "b" * n

def in_even0(w):
    return w.count("0") % 2 == 0

def distinct_prefix_classes(in_lang, alphabet, N):
    """Lower bound on DFA states: the number of prefixes (length <= N) that behave
    differently on some suffix (length <= N+1).  Pure brute force."""
    words = lambda L: ["".join(t) for k in range(L + 1) for t in _product(alphabet, repeat=k)]
    prefixes, suffixes = words(N), words(N + 1)
    signatures = {tuple(in_lang(p + w) for w in suffixes) for p in prefixes}
    return len(signatures)




BLANK = "_"


class TuringMachine:
    def __init__(self, delta, start, accept, reject=()):
        self.delta = delta                  # (state, symbol) -> (state, write, move)
        self.start = start
        self.accept = set(accept)
        self.reject = set(reject)

    def run(self, text, max_steps=10_000, trace=False):
        """Return 'accept', 'reject', or 'timeout' (we gave up - it may loop forever)."""
        tape = {i: c for i, c in enumerate(text)}   # sparse tape: blank elsewhere
        state, head = self.start, 0
        for step in range(max_steps):
            if state in self.accept:
                return "accept"
            if state in self.reject:
                return "reject"
            symbol = tape.get(head, BLANK)
            if (state, symbol) not in self.delta:   # no rule = reject
                return "reject"
            new_state, write, move = self.delta[(state, symbol)]
            if trace:
                cells = "".join(tape.get(i, BLANK) for i in range(min(tape, default=0), max(tape, default=0) + 1))
                print(f"    step {step:3}  state={state:7} head={head:2}  tape={cells}")
            tape[head] = write
            head += {"L": -1, "R": 1, "-": 0}[move]
            if head < 0:
                head = 0                            # one-way infinite tape
            state = new_state
        return "timeout"


# --- A machine for { a^n b^n c^n : n >= 0 } --------------------------------
# Strategy: repeatedly cross out one a (X), one b (Y), one c (Z), then return
# to the left.  If everything gets crossed out together, accept.
ANBNCN = TuringMachine(
    delta={
        # q0: look for the next 'a' to cross out
        ("q0", "a"): ("q1", "X", "R"),
        ("q0", "Y"): ("q4", "Y", "R"),     # no a's left: verify the rest
        ("q0", BLANK): ("qacc", BLANK, "-"),   # empty input is in the language
        # q1: move right to the first 'b'
        ("q1", "a"): ("q1", "a", "R"),
        ("q1", "Y"): ("q1", "Y", "R"),
        ("q1", "b"): ("q2", "Y", "R"),
        # q2: move right to the first 'c'
        ("q2", "b"): ("q2", "b", "R"),
        ("q2", "Z"): ("q2", "Z", "R"),
        ("q2", "c"): ("q3", "Z", "L"),
        # q3: walk back left to the last X, then start the next round
        ("q3", "a"): ("q3", "a", "L"),
        ("q3", "b"): ("q3", "b", "L"),
        ("q3", "Y"): ("q3", "Y", "L"),
        ("q3", "Z"): ("q3", "Z", "L"),
        ("q3", "X"): ("q0", "X", "R"),
        # q4: only Y's and Z's may remain
        ("q4", "Y"): ("q4", "Y", "R"),
        ("q4", "Z"): ("q4", "Z", "R"),
        ("q4", BLANK): ("qacc", BLANK, "-"),
    },
    start="q0",
    accept=["qacc"],
)


# --- The halting problem ---------------------------------------------------
# A machine that loops forever on input 'a':
LOOPER = TuringMachine(
    delta={("s", "a"): ("s", "a", "-"),        # stay put forever
           ("s", BLANK): ("done", BLANK, "-")},
    start="s", accept=["done"],
)


# Programs are generator functions: each `yield` is one computation step, so we
# can run them for a limited number of steps.
def run_steps(program, arg, limit):
    """Return 'halted' if program(arg) finishes within `limit` steps, else 'running'."""
    gen = program(arg)
    for _ in range(limit):
        try:
            next(gen)
        except StopIteration:
            return "halted"
    return "running"


def slow(_):                      # finishes, but only after 3,000,000 steps
    for _ in range(3_000_000):
        yield

def forever(_):                   # never finishes
    while True:
        yield


def make_paradox(halts):
    """Given ANY candidate halts(program, data), build the program that defeats it."""
    def paradox(program):
        if halts(program, program):
            while True:           # predicted to halt  -> loop forever
                yield
        else:
            return                # predicted to loop  -> halt at once
            yield                 # (makes this a generator)
    return paradox


def refute(name, halts):
    paradox = make_paradox(halts)
    try:
        prediction = halts(paradox, paradox)
    except RecursionError:
        print(f"  {name:28} -> crashed (RecursionError): it cannot even answer for paradox")
        return
    # If the prediction is True, paradox sits in `while True` and never halts.
    # If False, paradox returns immediately.  Run it to see what really happens:
    actual = run_steps(paradox, paradox, 1000)
    truth = "halts" if actual == "halted" else "loops forever"
    wrong = (prediction and actual != "halted") or ((not prediction) and actual == "halted")
    print(f"  {name:28} predicts {'halts' if prediction else 'loops':5} | paradox(paradox) really {truth:13} | wrong: {wrong}")


def halting_paradox():
    print("Candidate halting-deciders, each attacked by its own paradox program:")
    refute("always answers True",  lambda p, d: True)
    refute("always answers False", lambda p, d: False)
    refute("simulate 1000 steps",  lambda p, d: run_steps(p, d, 1000) == "halted")

    print("\nWhy a step budget cannot work: 'slow' halts, 'forever' does not.")
    for budget in [1_000, 100_000, 10_000_000]:
        print(f"  budget {budget:>10,}:  slow -> {run_steps(slow, None, budget):8}  forever -> {run_steps(forever, None, budget)}")
    print("  At small budgets the two look identical; no fixed budget works for all programs.")


# --- Bridge: every DFA is a (very limited) Turing machine ---------------------
def dfa_to_tm(dfa):
    """A DFA is a Turing machine that never writes and only moves right.
    On reaching the first blank it accepts iff the DFA state is final."""
    delta = {}
    states = {s for s, _ in dfa.delta} | set(dfa.delta.values()) | {dfa.start}
    for (state, symbol), nxt in dfa.delta.items():
        delta[(state, symbol)] = (nxt, symbol, "R")
    for state in states:
        delta[(state, BLANK)] = ("ACCEPT" if state in dfa.finals else "REJECT", BLANK, "-")
    return TuringMachine(delta, dfa.start, ["ACCEPT"], ["REJECT"])


if __name__ == "__main__":
    print(__doc__)

    print("=" * 70 + "\nPART 1 - Finite state machines\n" + "=" * 70)
    demo("Even number of 0s", even_zeros, ["", "1", "0", "010", "1001", "10100"],
         r"1*(01*01*)*")
    demo("a*", only_a, ["", "a", "aaaa", "ab"], r"a*")
    demo("a+ b+", a_then_b, ["ab", "aabbb", "a", "ba", "abab"], r"a+b+")

    print("\nTrace of even_zeros on '1001':")
    even_zeros.accepts("1001", trace=True)

    print("\nWhy a DFA cannot recognise a^n b^n  (computed, Myhill-Nerode)")
    print("  Two prefixes are 'different' if some suffix accepts one but not the other.")
    print("  A DFA needs at least one state per mutually-different prefix.")
    for N in [1, 2, 3, 4, 5, 6]:
        print(f"    N={N}  a^n b^n needs >= {distinct_prefix_classes(in_anbn, 'ab', N):2} states"
              f"   |   even-0s needs >= {distinct_prefix_classes(in_even0, '01', N)}")
    print("  The a^n b^n bound grows without limit; even-0s stays at 2 (our 2-state DFA).")

    print("\n" + "=" * 70 + "\nPART 2 - From FSM to Turing machine\n" + "=" * 70)
    tm_even = dfa_to_tm(even_zeros)
    words = ["".join(t) for n in range(9) for t in _product("01", repeat=n)]
    same = all((tm_even.run(w) == "accept") == even_zeros.accepts(w) for w in words)
    print(f"  even_zeros rebuilt as a Turing machine, compared on {len(words)} strings: identical = {same}")
    assert same
    print("  (An FSM is a Turing machine that never writes and only moves right.)")

    print("\n  With writing and moving left, we can do what no FSM can: a^n b^n c^n")
    for w in ["", "abc", "aabbcc", "aaabbbccc", "ab", "aabbc", "abcabc", "abcc", "cba"]:
        print(f"    {w!r:14} -> {ANBNCN.run(w)}")

    print("\n  Trace on 'abc':")
    ANBNCN.run("abc", trace=True)

    print("\n" + "=" * 70 + "\nPART 3 - What no Turing machine can do\n" + "=" * 70)
    print("A Turing machine that never halts on 'a':")
    print("  running with a 1000-step limit ->", LOOPER.run("a", max_steps=1000))
    print()
    halting_paradox()