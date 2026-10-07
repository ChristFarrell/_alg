import math

def sym_diff(expr, var='x'):
    if isinstance(expr, (int, float)):
        return 0

    if isinstance(expr, str):
        return 1 if expr == var else 0

    op = expr[0]

    # (OPERATION BINER)
    
    # Aturan Penjumlahan & Pengurangan: (f ± g)' = f' ± g'
    if op in ('+', '-'):
        u_prime = sym_diff(expr[1], var)
        v_prime = sym_diff(expr[2], var)
        return _smart_binop(op, u_prime, v_prime)

    # Aturan Perkalian (Product Rule): (u * v)' = u' * v + u * v'
    if op == '*':
        u, v = expr[1], expr[2]
        u_prime = sym_diff(u, var)
        v_prime = sym_diff(v, var)
        
        term1 = _smart_binop('*', u_prime, v)
        term2 = _smart_binop('*', u, v_prime)
        return _smart_binop('+', term1, term2)

    # Aturan Pembagian (Quotient Rule): (u / v)' = (u' * v - u * v') / v^2
    if op == '/':
        u, v = expr[1], expr[2]
        u_prime = sym_diff(u, var)
        v_prime = sym_diff(v, var)
        
        num = _smart_binop('-', _smart_binop('*', u_prime, v), _smart_binop('*', u, v_prime))
        den = _smart_binop('**', v, 2)
        return _smart_binop('/', num, den)

    # Aturan Pangkat (Power Rule + Chain Rule): (u^n)' = n * u^(n-1) * u'
    if op == '**':
        u, n = expr[1], expr[2]
        if isinstance(n, (int, float)):
            u_prime = sym_diff(u, var)
            coeff = _smart_binop('*', n, _smart_binop('**', u, n - 1))
            return _smart_binop('*', coeff, u_prime)

    # (CHAIN RULE)
    
    # sin(u)' = cos(u) * u'
    if op == 'sin':
        u = expr[1]
        return _smart_binop('*', ('cos', u), sym_diff(u, var))

    # cos(u)' = -sin(u) * u'
    if op == 'cos':
        u = expr[1]
        neg_sin = _smart_binop('*', -1, ('sin', u))
        return _smart_binop('*', neg_sin, sym_diff(u, var))

    # exp(u)' = exp(u) * u'
    if op == 'exp':
        u = expr[1]
        return _smart_binop('*', ('exp', u), sym_diff(u, var))

    # ln(u)' = (1 / u) * u'
    if op == 'ln':
        u = expr[1]
        return _smart_binop('*', _smart_binop('/', 1, u), sym_diff(u, var))

    raise ValueError(f"Operator tidak dikenal: {op}")


def _smart_binop(op, u, v):
    if isinstance(u, (int, float)) and isinstance(v, (int, float)):
        if op == '+': return u + v
        if op == '-': return u - v
        if op == '*': return u * v
        if op == '/': return u / v if v != 0 else ('/', u, v)
        if op == '**': return u ** v

    if op == '+':
        if u == 0: return v
        if v == 0: return u
    if op == '-':
        if v == 0: return u
        if u == v: return 0
    if op == '*':
        if u == 0 or v == 0: return 0
        if u == 1: return v
        if v == 1: return u
    if op == '/':
        if u == 0: return 0
        if v == 1: return u
    if op == '**':
        if v == 0: return 1
        if v == 1: return u

    return (op, u, v)


if __name__ == "__main__":
    expr1 = ('+', ('**', 'x', 2), ('*', 3, 'x'))
    print("f(x)   =", expr1)
    print("f'(x)  =", sym_diff(expr1, 'x'))

    print("-" * 40)

    expr2 = ('sin', ('**', 'x', 2))
    print("g(x)   =", expr2)
    print("g'(x)  =", sym_diff(expr2, 'x'))