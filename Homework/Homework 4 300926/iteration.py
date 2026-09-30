df = lambda x: 4 * x**3 - 9 * x**2

# Second derivative: f''(x) = 12x^2 - 18x (Curvature)
ddf = lambda x: 12 * x**2 - 18 * x

max_iterations = 20
tolerance = 0.0001 

print("==================================================")
print(" ALGORITHM 1: GRADIENT DESCENT")
print("==================================================")
x_gd = 4.0             
learning_rate = 0.01   

for i in range(max_iterations):
    gradient = df(x_gd)
    x_new = x_gd - (learning_rate * gradient)
    
    change = abs(x_new - x_gd)
    x_gd = x_new
    
    print(f"Iteration {i+1:02d}: x = {x_gd:.6f} | Change = {change:.6f}")
    
    if change < tolerance:
        print("--> Gradient Descent converged!\n")
        break


print("==================================================")
print(" ALGORITHM 2: NEWTON'S METHOD FOR OPTIMIZATION")
print("==================================================")
x_nt = 4.0          

for i in range(max_iterations):
    first_deriv = df(x_nt)
    second_deriv = ddf(x_nt)
    
    if second_deriv == 0:
        print("Error: Second derivative is zero, cannot divide.")
        break
        
    # Newton's method calculates its own perfect step size using the second derivative
    x_new = x_nt - (first_deriv / second_deriv)
    
    change = abs(x_new - x_nt)
    x_nt = x_new
    
    print(f"Iteration {i+1:02d}: x = {x_nt:.6f} | Change = {change:.6f}")
    
    if change < tolerance:
        print("--> Newton's Method converged!\n")
        break