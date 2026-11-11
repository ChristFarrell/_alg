# [Homework 6](https://github.com/ChristFarrell/_alg/blob/main/Homework/Homework%206%20141026/LambdaCalculus.py)

This homework was getting helped by AI Gemini for understanding.<br>
AI Gemini: https://share.gemini.google/l9WfqheZCA1o

On this homework, we asked to make Lambda-Calculus program. It's complete abstract syntax Tree (AST)-based interpreter for the untyped lambda calculus. This code simulates how a function-based computing machine processes data using beta-reduction with the Normal Order Evaluation (leftmost-outer) strategy. The code component is divided into several parts.

1. AST Constructors (Syntax Tree Constructors):
   In accordance with pure λ-calculus theory, all expressions are constructed from three basic elements: 
   - Var(name) -> Simple variable (x)
   - Abs(param, body) -> Abstraction/Function (λx. E)
   - App(func, arg) -> Function application/Invocation ($E_{1}$, $E_{2}$)

2. Readable Printer
   This function converts a complex AST dictionary structure into a human-readable lambda (λ) notation string.<br>
   For example: App(Abs("x", Var("x")), Var("a")) -> ((λx. x) a)

3. Variable Scoping & Capture-Avoiding Substitution
   - free_vars(term): Finds free variables (variables not bound by a lambda declaration)<br>
      Var: The variable itself, Abs: The free variable within the body minus the function parameter, App: The combination of the function's free variables and the arguments.
   - substitute(term, var_name, replacement): Replaces the variable var_name with the expression replacement<br>
      To avoid text collisions, the code automatically modifies the parameter by adding a prime symbol ('), for example, changing x to x'.

4. Evaluator (step_eval & run_interpreter)
   - Primary Reduction ($\beta$-reduction): When it encounters the pattern App(Abs(param, body), arg), it immediately replaces the parameter inside the body with arg using substitute
   - Leftmost-Outer Search: If no reduction has occurred yet, it evaluates the left side (func) first
   - Proceed to the Right: Once the left side is in its simplest form (Normal Form), it then evaluates the right side (arg)
   - Body Simplification: If there are no outer function applications, it steps inside the abstraction body (abs)
   The process will be looping until reaching the normal form that can't be to simplified anymore.

Result Explanation
1. Identity Function
   ```
   === Identity Function ===
   Input : ((λx. x) a)
   Step 1: a
   Status: Normal Form (Evaluation Complete)
   ```
   - Process: The function λx. x receives a as its argument.
   - Execution: Substitution $x \mapsto a$ is performed on the body $x$.
   - Final Result: a (Normal Form achieved in 1 step).

2. Church Logic
   ```
   === Church Logic: AND TRUE FALSE ===
   Input : (((λp. (λq. ((p q) p))) (λx. (λy. x))) (λx. (λy. y)))
   Step 1: ((λq. (((λx. (λy. x)) q) (λx. (λy. x)))) (λx. (λy. y)))
   Step 2: (((λx. (λy. x)) (λx. (λy. y))) (λx. (λy. x)))
   Step 3: ((λy. (λx. (λy. y))) (λx. (λy. x)))
   Step 4: (λx. (λy. y))
   Status: Normal Form (Evaluation Complete)
   ```
   The definitions: $\text{TRUE} = \lambda x. \lambda y. x \qquad \text{FALSE} = \lambda x. \lambda y. y \qquad \text{AND} = \lambda p. \lambda q. p \ q \ p$
   
   - ((λp. (λq. ((p q) p))) (λx. (λy. x))) is evaluated $\to$ $p$ is replaced by TRUE.
   - The second argument FALSE is passed into $q$.
   - The evaluation proceeds to TRUE FALSE TRUE $\to$ ((λx. (λy. x)) FALSE) TRUE.
   - TRUE selects its first argument, which is FALSE.
   - Final result is TRUE.

3. Church Arithmetic
   ```
   === Church Arithmetic: SUCC ONE ===
   Input : ((λn. (λf. (λx. (f ((n f) x))))) (λf. (λx. (f x))))
   Step 1: (λf. (λx. (f (((λf. (λx. (f x))) f) x))))
   Step 2: (λf. (λx. (f ((λx. (f x)) x))))
   Step 3: (λf. (λx. (f (f x))))
   Status: Normal Form (Evaluation Complete)
   ```
   The definitions: $\text{ONE} = \lambda f. \lambda x. f \ x \qquad \text{SUCC} = \lambda n. \lambda f. \lambda x. f \ (n \ f \ x)$
   
   - SUCC receives ONE as the argument $n$.
   - Parameter $n$ inside the body of SUCC is replaced by ONE.
   - Evaluation continues until the expression forms two applications of function $f$: $f(f(x))$.
   - Final Result: (λf. (λx. (f (f x)))), which represents the number 2 in Church Numerals.