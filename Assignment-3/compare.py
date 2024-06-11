"""
@Author:  Tom Shabalin
@ID:      321243339
@Mail:    tomshabalin95@gmail.com
@Date:    10/05/2024
@Description: Compare Assignment for the course "Research Algorithms"
"""

import numpy as np
from scipy.optimize import root
from numpy.linalg import solve
import timeit
import matplotlib.pyplot as plt

def solve_with_root(a:np.ndarray, b:np.ndarray):
    """
    Solve a system of linear equations using scipy.optimize.root.

    Parameters:
    a (np.ndarray): Coefficient matrix.
    b (np.ndarray): Dependent variable values.

    Returns:
    np.ndarray: Solution to the system of linear equations.

    >>> a = np.array([[1, 2], [3, 4]])
    >>> b = np.array([5, 6])
    >>> solve_with_root(a, b)
    array([-4. ,  4.5])

    >>> a = np.array([[1, 1, 1], [0, 2, 5], [2, 5, -1]])
    >>> b = np.array([6, -4, 27])
    >>> solve_with_root(a, b)
    array([ 5.,  3., -2.])

    >>> a = np.array([[4.17022005e+02, 7.20324493e+02, 1.14374817e-01], [3.02332573e+02, 1.46755891e+02, 9.23385948e+01], [1.86260211e+02, 3.45560727e+02, 3.96767474e+02]])
    >>> b = np.array([538.816734,  419.1945144, 685.2195004])
    >>> solve_with_root(a, b)
    array([0.95256244, 0.19637041, 1.10880338])

    >>> a = np.array([[863.75998557, 284.90596523,  73.25638808], [763.23720433, 452.7190576,  542.29687401], [726.63578283, 848.90510761, 768.19997781]])
    >>> b = np.array([733.14372332, 241.9864247,  720.30869255])
    >>> solve_with_root(a, b)
    array([ 0.25688458,  2.25722062, -1.79968626])
    """
    
    def equation_to_solve(x):
        return a.dot(x) - b

    def equation_to_solve_wrapper(x):
        return equation_to_solve(x)

    initial_guess = np.zeros(a.shape[1])

    try:
        solution = root(equation_to_solve_wrapper, initial_guess)

        if solution.success:
            return solution.x
        else:
            raise ValueError(f'Failed to find solution: {solution.message}')
    except Exception as e:
        print(f'Failed to solve with root: {e}')
        return None

def test_solve_with_root():
    """
    Testing the solve_with_root function with random input matrices a and b.
    While comparing the output to numpy.linalg.solve, the function will print the input matrices and the output solutions.
    """
    # First generate random input matrices a and b
    for i in range(30):
        np.random.seed(i)
        
        # Generate random values between 0 and 1, and scale them to a larger range
        scaling_factor = 1000
        a = np.random.rand(3, 3) * scaling_factor
        b = np.random.rand(3) * scaling_factor

        # Solve using solve_with_root()
        solution_root = solve_with_root(a, b)

        # Solve using numpy.linalg.solve()
        solution_numpy = solve(a, b)

        print(f'--------Input--------')
        print(f'Matrix a:\n{a}')
        print(f'Vector b:\n{b}')

        # Compare solutions
        print(f'--------Output--------')
        if np.allclose(solution_root, solution_numpy):
            print(f'Test {i + 1}: Both methods produced the same solution.\nThe solution for solve_with_root: {solution_root}.\nThe solution for numpy.linalg.solve: {solution_numpy}.\n')
        else:
            print(f'Test {i + 1}: The solution obtained from two methods are different.\nThe solution for solve_with_root: {solution_root}.\nThe solution for numpy.linalg.solve: {solution_numpy}.\n')

def compare_solution_methods():
    """
    Compare the running time of solve_with_root and numpy.linalg.solve for different input sizes.
    """
    batch_size = 50
    max_size = 1000
    input_sizes = range(1, max_size + 1, batch_size)
    time_solve_with_root = []
    time_numpy_solve = []

    for size in input_sizes:
        # Generate random input matrices a and b for each batch
        a_batch = np.random.rand(size, size, batch_size)
        b_batch = np.random.rand(size, batch_size)

        batch_solve_with_root_time = 0.0
        batch_numpy_solve_time = 0.0

        for i in range(batch_size):
            # Measure running time for solve_with_root
            start_time = timeit.default_timer()
            solution = solve_with_root(a_batch[:, :, i], b_batch[:, i])
            end_time = timeit.default_timer()

            if solution is not None:
                batch_solve_with_root_time += end_time - start_time

                # Measure running time for numpy.linalg.solve
                start_time = timeit.default_timer()
                solve(a_batch[:, :, i], b_batch[:, i])
                end_time = timeit.default_timer()
                batch_numpy_solve_time += end_time - start_time
        
        if batch_solve_with_root_time > 0:
            time_solve_with_root.append(batch_solve_with_root_time / batch_size)
            time_numpy_solve.append(batch_numpy_solve_time / batch_size)

    # Plot the graph
    if time_solve_with_root:
        plt.plot(input_sizes[:len(time_solve_with_root)], time_solve_with_root, label='solve_with_root')
    if time_numpy_solve:
        plt.plot(input_sizes[:len(time_numpy_solve)], time_numpy_solve, label='numpy.linalg.solve')
    plt.xlabel('Input Size')
    plt.ylabel('Running Time (seconds)')
    plt.title('Comparison of Solution Methods')
    plt.legend()
    plt.savefig("comparison.png")
    plt.show()

if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
    # test_solve_with_root()
    # compare_solution_methods()
