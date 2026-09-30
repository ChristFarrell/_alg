df = lambda x: 4 * x**3 - 9 * x**2

x = 4.0               
learning_rate = 0.01  
max_iterations = 20  

print("Running Gradient Descent Algorithm:")
for i in range(max_iterations):
    gradient = df(x)
    
    new_x = x - (learning_rate * gradient)
    
    change = abs(new_x - x)
    x = new_x
    
    print(f"Iteration {i+1:02d}: x = {x:.6f} | Change = {change:.6f}")
    
    if change < 0.0001:
        print("--> The algorithm has converged (found the minimum point)!")
        break