"""
@Author:  Tom Shabalin
@ID:      321243339
@Mail:    tomshabalin95@gmail.com
@Date:    23/05/2024
@Description: Traveling Salesman Problem Assignment for the course "Research Algorithms"
"""

from enum import Enum, auto
from typing import Callable, List, Tuple, Union
from itertools import permutations

DistanceMatrix = List[List[float]]
CityNames = List[str]
OutputType = Union[List[Union[int, str]], float]

class OutputTypes(Enum):
    PATH = auto()
    LENGTH = auto()


def tsp_solver(algorithm: Callable, distances: DistanceMatrix, city_names: Union[None, CityNames] = None,
               output_type: str = OutputTypes.PATH) -> OutputType:
    """
    Solves the Traveling Salesman Problem using the specified algorithm.

    Args
    -----
    - algorithm (Callable): The TSP solving algorithm to use.
    - distances (DistanceMatrix): A square matrix representing distances between cities.
    - city_names (Optional[CityNames]): A list of city names corresponding to the indices in the distances matrix.
    - output_type (str): The desired output type: "path" or "length".

    Returns
    -----
    - Union[List[int], float]: The solution to the TSP, either the path or the length of the path.

    Examples
    -----
    >>> tsp_solver(naive_tsp, [[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]], output_type=OutputTypes.PATH) in ([0, 1, 3, 2, 0], [0, 2, 3, 1, 0])
    True

    >>> tsp_solver(naive_tsp, [[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]], output_type=OutputTypes.LENGTH)
    80.0

    >>> tsp_solver(nearest_neighbor_tsp, [[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]], output_type=OutputTypes.PATH)
    [0, 1, 3, 2, 0]

    >>> tsp_solver(nearest_neighbor_tsp, [[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]], output_type=OutputTypes.LENGTH)
    80.0

    >>> tsp_solver(naive_tsp, [[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]], city_names=["A", "B", "C", "D"], output_type=OutputTypes.PATH) in (['A', 'B', 'D', 'C', 'A'], ['A', 'C', 'D', 'B', 'A'])
    True

    >>> tsp_solver(nearest_neighbor_tsp, [[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]], city_names=["A", "B", "C", "D"], output_type=OutputTypes.LENGTH)
    80.0

    >>> tsp_solver(naive_tsp, [[0, 2, 9, 10], [1, 0, 6, 4], [15, 7, 0, 8], [6, 3, 12, 0]], city_names=["A", "B", "C", "D"], output_type=OutputTypes.PATH) in (['A', 'B', 'D', 'C', 'A'], ['A', 'C', 'D', 'B', 'A'])
    True

    >>> tsp_solver(nearest_neighbor_tsp, [[0, 2, 9, 10], [1, 0, 6, 4], [15, 7, 0, 8], [6, 3, 12, 0]], city_names=["A", "B", "C", "D"], output_type=OutputTypes.LENGTH)
    33.0

    >>> tsp_solver(nearest_neighbor_tsp, [[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]], output_type="INVALID")
    Traceback (most recent call last):
        ...
    ValueError: Invalid output type. Please choose either 'PATH' or 'LENGTH'.

    >>> tsp_solver(naive_tsp, [], output_type=OutputTypes.PATH)
    Traceback (most recent call last):
        ...
    ValueError: Distance matrix cannot be empty.

    >>> tsp_solver(naive_tsp, [[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]], city_names=["A", "B", "C", "D"], output_type=OutputTypes.PATH) in (['A', 'B', 'D', 'C', 'A'], ['A', 'C', 'D', 'B', 'A'])
    True

    >>> tsp_solver(naive_tsp, [[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]], city_names=["A", "B", "C", "D"], output_type=OutputTypes.PATH) in (['A', 'B', 'D', 'C', 'A'], ['A', 'C', 'D', 'B', 'A'])
    True

    >>> tsp_solver(naive_tsp, [[0, -10, 15, 20], [-10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]], output_type=OutputTypes.LENGTH)
    60.0

    >>> tsp_solver(nearest_neighbor_tsp, [[0, -10, 15, 20], [-10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]], output_type=OutputTypes.LENGTH)
    60.0
    """
    if not distances:
        raise ValueError("Distance matrix cannot be empty.")
    
    num_cities = len(distances)
    if city_names is None:
        city_names = list(range(num_cities))

    index_to_name = {idx: name for idx, name in enumerate(city_names)}

    path, dist = algorithm(distances)

    if output_type == OutputTypes.PATH:
        named_path = [index_to_name[idx] for idx in path]
        return named_path
    elif output_type == OutputTypes.LENGTH:
        return float(dist)
    else:
        raise ValueError("Invalid output type. Please choose either 'PATH' or 'LENGTH'.")


def naive_tsp(distances: DistanceMatrix) -> Tuple[List[int], float]:
    """
    Naive algorithm to solve the Traveling Salesman Problem.

    Args
    -----
    - distances (DistanceMatrix): A square matrix representing distances between cities.

    Returns
    -----
    - Tuple[List[int], float]: The shortest path and its length.

    Examples
    -----
    >>> naive_tsp([[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]]) in [([0, 1, 3, 2, 0], 80.0), ([0, 2, 3, 1, 0], 80.0)]
    True
    >>> naive_tsp([[0, 2, 9, 10], [1, 0, 6, 4], [15, 7, 0, 8], [6, 3, 12, 0]]) in [([0, 1, 3, 2, 0], 21.0), ([0, 2, 3, 1, 0], 21.0)]
    True
    """
    num_cities = len(distances)
    min_path = None
    min_dist = float('inf')

    # Generate all permutations of cities
    for path in permutations(range(num_cities)):
        # Calculate total distance for the current permutation
        total_dist = 0
        for i in range(num_cities - 1):
            total_dist += distances[path[i]][path[i + 1]]
        total_dist += distances[path[-1]][path[0]]  # Add distance from last city back to the starting city

        # Update minimum distance and path if necessary
        if total_dist < min_dist:
            min_dist = total_dist
            min_path = list(path) + [path[0]]  # Add starting city to the end of the path

    return min_path, float(min_dist)


def nearest_neighbor_tsp(distances: DistanceMatrix) -> Tuple[List[int], float]:
    """
    Nearest Neighbor algorithm to solve the Traveling Salesman Problem.
    https://en.wikipedia.org/wiki/Nearest_neighbour_algorithm

    Args
    -----
    - distances (DistanceMatrix): A square matrix representing distances between cities.

    Returns
    -----
    - Tuple[List[int], float]: The path and its length calculated using the nearest neighbor heuristic.

    Examples
    -----
    >>> nearest_neighbor_tsp([[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]])
    ([0, 1, 3, 2, 0], 80.0)
    >>> nearest_neighbor_tsp([[0, 2, 9, 10], [1, 0, 6, 4], [15, 7, 0, 8], [6, 3, 12, 0]])
    ([0, 1, 3, 2, 0], 33.0)
    """
    num_cities = len(distances)
    visited = [False] * num_cities
    path = [0]
    visited[0] = True
    total_dist = 0

    for _ in range(num_cities - 1):
        last = path[-1]
        nearest = None
        min_dist = float('inf')

        for i in range(num_cities):
            if not visited[i] and 0 < distances[last][i] < min_dist:
                nearest = i
                min_dist = distances[last][i]

        path.append(nearest)
        visited[nearest] = True
        total_dist += min_dist

    total_dist += distances[path[-1]][path[0]]  # Add distance from last city back to the starting city
    path.append(0)

    return path, float(total_dist)


if __name__ == '__main__':
    import doctest
    print(doctest.testmod(verbose=True))
