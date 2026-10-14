from typing import Dict, Any, Tuple, Set

# =====================================================================
# 1. AST Constructors (JSON / Dictionary-based)
# =====================================================================

def Var(name: str) -> Dict[str, Any]:
    return {"type": "var", "name": name}

def Abs(param: str, body: Dict[str, Any]) -> Dict[str, Any]:
    return {"type": "abs", "param": param, "body": body}

def App(func: Dict[str, Any], arg: Dict[str, Any]) -> Dict[str, Any]:
    return {"type": "app", "func": func, "arg": arg}


# =====================================================================
# 2. Format AST to Lambda Notation
# =====================================================================

def to_string(term: Dict[str, Any]) -> str:
    """Converts a dictionary-based AST into readable lambda string notation."""
    term_type = term["type"]
    if term_type == "var":
        return term["name"]
    elif term_type == "abs":
        return f"(λ{term['param']}. {to_string(term['body'])})"
    elif term_type == "app":
        return f"({to_string(term['func'])} {to_string(term['arg'])})"
    return ""


# =====================================================================
# 3. Free Variables & Capture-Avoiding Substitution
# =====================================================================

def free_vars(term: Dict[str, Any]) -> Set[str]:
    """Returns the set of all free variables in a term."""
    term_type = term["type"]
    if term_type == "var":
        return {term["name"]}
    elif term_type == "abs":
        return free_vars(term["body"]) - {term["param"]}
    elif term_type == "app":
        return free_vars(term["func"]) | free_vars(term["arg"])
    return set()


def substitute(term: Dict[str, Any], var_name: str, replacement: Dict[str, Any]) -> Dict[str, Any]:
    """Substitutes `var_name` with `replacement` term inside `term`."""
    term_type = term["type"]
    if term_type == "var":
        return replacement if term["name"] == var_name else term

    elif term_type == "abs":
        param = term["param"]
        body = term["body"]
        if param == var_name:
            return term
        
        # Alpha-conversion to handle variable capture
        if param in free_vars(replacement):
            new_param = param + "'"
            renamed_body = substitute(body, param, Var(new_param))
            return Abs(new_param, substitute(renamed_body, var_name, replacement))

        return Abs(param, substitute(body, var_name, replacement))

    elif term_type == "app":
        return App(
            substitute(term["func"], var_name, replacement),
            substitute(term["arg"], var_name, replacement)
        )


# =====================================================================
# 4. Evaluator (Normal Order Beta-Reduction)
# =====================================================================

def step_eval(term: Dict[str, Any]) -> Tuple[Dict[str, Any], bool]:
    """Performs a single step of Normal Order beta reduction (Leftmost Outer)."""
    term_type = term["type"]

    if term_type == "app":
        func = term["func"]
        arg = term["arg"]

        # Core Rule: (λx. E) A ==> E [x := A]
        if func["type"] == "abs":
            reduced = substitute(func["body"], func["param"], arg)
            return reduced, True

        # Try reducing the function (left side) first
        new_func, changed = step_eval(func)
        if changed:
            return App(new_func, arg), True

        # Try reducing the argument (right side) next
        new_arg, changed = step_eval(arg)
        if changed:
            return App(func, new_arg), True

    elif term_type == "abs":
        new_body, changed = step_eval(term["body"])
        if changed:
            return Abs(term["param"], new_body), True

    return term, False


def run_interpreter(expr: Dict[str, Any], label: str = "", max_steps: int = 20):
    """Evaluates the term step-by-step and displays the execution log."""
    print(f"=== {label} ===")
    print(f"Input : {to_string(expr)}")
    current = expr
    step = 0

    while step < max_steps:
        next_expr, changed = step_eval(current)
        if not changed:
            print("Status: Normal Form (Evaluation Complete)\n")
            break
        step += 1
        print(f"Step {step}: {to_string(next_expr)}")
        current = next_expr


# =====================================================================
# 5. Program Inputs & Demonstrations
# =====================================================================

if __name__ == "__main__":
    # Program 1: Identity Function
    # (λx. x) a
    prog1 = App(Abs("x", Var("x")), Var("a"))
    run_interpreter(prog1, "Identity Function")

    # Church Booleans Definitions
    TRUE  = Abs("x", Abs("y", Var("x")))                 # λx. λy. x
    FALSE = Abs("x", Abs("y", Var("y")))                 # λx. λy. y
    AND   = Abs("p", Abs("q", App(App(Var("p"), Var("q")), Var("p")))) # λp. λq. p q p

    # Program 2: Boolean Logic (AND TRUE FALSE)
    prog2 = App(App(AND, TRUE), FALSE)
    run_interpreter(prog2, "Church Logic: AND TRUE FALSE")

    # Church Numerals Definitions
    ONE  = Abs("f", Abs("x", App(Var("f"), Var("x"))))   # λf. λx. f x
    SUCC = Abs("n", Abs("f", Abs("x", App(Var("f"), App(App(Var("n"), Var("f")), Var("x")))))) # λn. λf. λx. f (n f x)

    # Program 3: Church Arithmetic (SUCC ONE) -> Yields Church Numeral 2
    prog3 = App(SUCC, ONE)
    run_interpreter(prog3, "Church Arithmetic: SUCC ONE")