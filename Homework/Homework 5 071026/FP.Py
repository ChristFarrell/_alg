# CUSTOM MAP, FILTER, AND REDUCE (LOOP-FREE / RECURSIVE ONLY)

def my_map(func, lst):
    """Applies a function to each element in a list recursively."""
    if not lst:
        return []
    return [func(lst[0])] + my_map(func, lst[1:])

def my_filter(pred, lst):
    """Filters list elements based on a predicate function recursively."""
    if not lst:
        return []
    head = lst[0]
    tail_filtered = my_filter(pred, lst[1:])
    return [head] + tail_filtered if pred(head) else tail_filtered

def my_reduce(func, lst, initial=None):
    """Combines list elements from left to right recursively."""
    if initial is None:
        if not lst:
            raise TypeError("reduce() of empty sequence with no initial value")
        return my_reduce(func, lst[1:], lst[0])
    if not lst:
        return initial
    return my_reduce(func, lst[1:], func(initial, lst[0]))

# BUBBLE SORT WITHOUT LOOPS (USING DUAL RECURSION)

def bubble_pass(lst):
    """
    Inner recursive pass (replaces the inner loop):
    Compares adjacent elements and bubbles the largest value to the right.
    """
    if len(lst) <= 1:
        return lst

    head, second, tail = lst[0], lst[1], lst[2:]
    
    if head > second:
        # Swap order, continue recursion on remaining elements
        rest = bubble_pass([head] + tail)
        return [second] + rest
    else:
        # Order is correct, continue recursion on remaining elements
        rest = bubble_pass([second] + tail)
        return [head] + rest

def bubble_sort(lst, n=None):
    """
    Outer recursive pass (replaces the outer loop):
    Invokes bubble_pass n times until the list is fully sorted.
    """
    if n is None:
        n = len(lst)
        
    if n <= 1 or len(lst) <= 1:
        return lst

    # Perform one full pass
    lst_after_pass = bubble_pass(lst)
    
    # Recursively execute remaining passes
    return bubble_sort(lst_after_pass, n - 1)


# =====================================================================
# TESTING EXAMPLES
# =====================================================================

if __name__ == "__main__":
    print("=== 1. Testing my_map, my_filter, my_reduce ===")
    numbers = [1, 2, 3, 4, 5, 6]
    print("Input List:    ", numbers)
    print("my_map (^2):   ", my_map(lambda x: x ** 2, numbers))
    print("my_filter (evens):", my_filter(lambda x: x % 2 == 0, numbers))
    print("my_reduce (sum):  ", my_reduce(lambda acc, x: acc + x, numbers, 0))

    print("\n=== 2. Testing Bubble Sort (Loop-free) ===")
    unsorted = [64, 34, 25, 12, 22, 11, 90]
    print("Before Sort:   ", unsorted)
    print("After Sort:    ", bubble_sort(unsorted))