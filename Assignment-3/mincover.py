import subprocess, sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "cvxpy"], stdout=subprocess.DEVNULL)
subprocess.check_call([sys.executable, "-m", "pip", "install", "cvxopt"], stdout=subprocess.DEVNULL)

import networkx as nx, cvxpy, numpy as np, matplotlib.pyplot as plt
from networkx.algorithms import approximation
import random

def mincover(graph: nx.Graph) -> int:
    """
    The mincover function takes an undirected graph as input and finds the size of the smallest vertex cover, 
    which is the smallest subset of nodes such that every edge in the graph is adjacent to at least one node in the subset.

    Input:
    - graph: An undirected graph represented as a networkx Graph object.

    Output:
    - An integer representing the size of the smallest vertex cover. If a feasible cover is found, the function returns the size of the cover. 
    If no feasible cover exists, the function returns -1.
    """
    # Check for special cases:
    # Case 1: 1 edge
    if len(graph.edges()) == 1:
        return 1
    # Case 2: No edges
    if len(graph.edges()) == 0:
        return 0

    # Define variables
    n = len(graph.nodes())
    x = cvxpy.Variable(n, boolean = True)

    # Define constraints
    constraints = []
    for u, v in graph.edges():
        constraints.append(x[u] + x[v] >= 1) # At least one endpoint of each edge must be in the cover

    # Define objective function
    objective = cvxpy.Minimize(cvxpy.sum(x))

    # Define problem
    problem = cvxpy.Problem(objective, constraints)

    # Solve problem
    problem.solve(solver=cvxpy.GLPK_MI)

    # Check if solver status is optimal and solution exists
    if problem.status == 'optimal' and x.value is not None:
        # Return the size of the smallest cover
        return int(sum(x.value))
    else:
        # Return -1 if no feasible cover exists
        return -1

def generate_random_graph() -> nx.Graph:
    """
    Generate a random undirected graph with a random number of nodes and edges.

    Output:
    - A random undirected graph represented as a networkx Graph object.
    """
    num_nodes = random.randint(2, 50)
    num_edges = random.randint(0, min(num_nodes * (num_nodes - 1) // 2, 1000))
    graph = nx.gnm_random_graph(num_nodes, num_edges)
    return graph

def test_mincover():
    """
    Test the mincover function on 50 random graphs and record the number of nodes, edges, and the size of the minimum cover.

    Output:
    - A list of tuples containing the number of nodes, edges, and the size of the minimum cover for each random graph.
    """
    results = []
    for _ in range(50):
        graph = generate_random_graph()
        min_cover_size_found = mincover(graph)
        min_cover_size_approx = len(approximation.min_weighted_vertex_cover(G=graph, weight=None))
        results.append((len(graph.nodes()), len(graph.edges()), min_cover_size_found, min_cover_size_approx))
    return results


if __name__ == '__main__':
    edges=eval(input())
    graph = nx.Graph(edges)
    print(mincover((graph)))

    """
    For running the test cases, uncomment the following lines.
    When running this block, the test_mincover_on_random_graphs function will be executed, and you will get the output for each random graph that was generated in this form:
    Graph i: Nodes = n, Edges = m, Minimum Cover Size Found = k, Minimum Cover Size Approx = l.
    Where k is the size of the minimum cover found by the mincover function, and l is the size of the minimum cover found by the networkx min_weighted_vertex_cover function.
    """
    # test_results = test_mincover()
    # for i, result in enumerate(test_results, start=1):
    #     print(f"Graph {i}: Nodes = {result[0]}, Edges = {result[1]}, Minimum Cover Size Found = {result[2]}, Minimum Cover Size Approx = {result[3]}")