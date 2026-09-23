import itertools

def solve_sat_truth_table(variables, formula_func):
    n = len(variables)
    
    col_w = 6
    
    headers = [f"{v:^{col_w}}" for v in variables] + [f"{'Result':^{col_w + 2}}"]
    header_str = "│ " + " │ ".join(headers) + " │"
    
    top_border = "┌─" + "─┬─".join(["─" * col_w] * n) + "─┬─" + "─" * (col_w + 2) + "─┐"
    divider    = "├─" + "─┼─".join(["─" * col_w] * n) + "─┼─" + "─" * (col_w + 2) + "─┤"
    bot_border = "└─" + "─┴─".join(["─" * col_w] * n) + "─┴─" + "─" * (col_w + 2) + "─┘"
    
    print(top_border)
    print(header_str)
    print(divider)
    
    satisfiable_assignments = []

    # Generasi sistematis 2^n kombinasi nilai (True/False)
    for values in itertools.product([True, False], repeat=n):
        env = dict(zip(variables, values))
        result = bool(formula_func(**env))
        
        #1 is True and 0 is false
        formatted_vals = [f"{int(v):^{col_w}}" for v in values]
        res_symbol = "1 (SAT)" if result else "0"
        res_str = f"{res_symbol:^{col_w + 2}}"
        
        print("│ " + " │ ".join(formatted_vals) + f" │ {res_str} │")
        
        if result:
            satisfiable_assignments.append(env)

    print(bot_border)
    
    if satisfiable_assignments:
        print(f"\nResult: SATISFIABLE ({len(satisfiable_assignments)} solution was found)")
        for assignment in satisfiable_assignments:
            formatted = ", ".join([f"{k}={int(v)}" for k, v in assignment.items()])
            print(f"  └─> {formatted}")
    else:
        print("\nResult: UNSATISFIABLE (No combination to create formrue)")


if __name__ == "__main__":
    vars_list = ['A', 'B', 'C']
    
    def formula(A, B, C):
        clause1 = A or B
        clause2 = (not A) or C
        clause3 = (not B) or (not C)
        return clause1 and clause2 and clause3

    print("Find solution of SAT for formula: (A v B) ^ (~A v C) ^ (~B v ~C)\n")
    solve_sat_truth_table(vars_list, formula)

if __name__ == "__main__":
    vars_list = ['A', 'B', 'C']
    
    def formula_3_solutions(A, B, C):
        c1 = A or B
        c2 = (not A) or C
        c3 = (not B) or C
        return c1 and c2 and c3

    print("\nFind solution of SAT for formula: (A v B) ^ (~A v C) ^ (~B v C)\n")
    solve_sat_truth_table(vars_list, formula_3_solutions)