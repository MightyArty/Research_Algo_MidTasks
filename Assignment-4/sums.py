"""
@Author:  Tom Shabalin
@ID:      321243339
@Mail:    tomshabalin95@gmail.com
@Date:    23/05/2024
@Description: Sums Assignment for the course "Research Algorithms"
"""

import heapq

def sorted_subset_sums(S):
    """
    Generates all subset sums of the input list S in ascending order.

    Args
    ------
    - S (list): A list of positive, distinct numbers.

    Yields
    ------
    - int: The next subset sum in ascending order.

    Examples
    --------
    >>> list(sorted_subset_sums([1, 2, 4]))
    [0, 1, 2, 3, 4, 5, 6, 7]

    >>> list(sorted_subset_sums([1, 2, 3]))
    [0, 1, 2, 3, 3, 4, 5, 6]

    >>> list(sorted_subset_sums([2, 3, 4]))
    [0, 2, 3, 4, 5, 6, 7, 9]

    >>> from itertools import islice
    >>> list(islice(sorted_subset_sums(range(100)), 5))
    [0, 0, 1, 1, 2]

    >>> from itertools import takewhile
    >>> list(takewhile(lambda x: x <= 6, sorted_subset_sums(range(1, 100))))
    [0, 1, 2, 3, 3, 4, 4, 5, 5, 5, 6, 6, 6, 6]

    >>> list(zip(range(5), sorted_subset_sums(range(100))))
    [(0, 0), (1, 0), (2, 1), (3, 1), (4, 2)]

    >>> from itertools import takewhile
    >>> len(list(takewhile(lambda x:x<=1000, sorted_subset_sums(list(range(90,100)) + list(range(920,1000))))))
    1104

    >>> list(sorted_subset_sums([8, 16, 24]))
    [0, 8, 16, 24, 24, 32, 40, 48]

    >>> list(sorted_subset_sums([1, 3, 5, 7]))
    [0, 1, 3, 4, 5, 6, 7, 8, 8, 9, 10, 11, 12, 13, 15, 16]

    >>> list(sorted_subset_sums([1, 2, 2]))
    [0, 1, 2, 2, 3, 3, 4, 5]

    >>> list(sorted_subset_sums([3, 6, 9]))
    [0, 3, 6, 9, 9, 12, 15, 18]
    """
    S = sorted(S)
    n = len(S)
    
    # Initialize a min-heap with the first element (0, empty subset)
    heap = [(0, ())]  # (current sum, tuple of used indices)
    seen_set = set(heap)
    
    while heap:
        current_sum, indices = heapq.heappop(heap)
        yield current_sum
        
        # Generate new sums by adding elements of S starting from the last used index
        last_index = indices[-1] if indices else -1
        for i in range(last_index + 1, n):
            new_sum = current_sum + S[i]
            new_indices = indices + (i,)
            new_state = (new_sum, new_indices)
            # Add new state to the heap if it hasn't been seen before
            if new_state not in seen_set:
                heapq.heappush(heap, new_state)
                seen_set.add(new_state)

if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
    from itertools import takewhile, islice
    for i in eval(input()):
        print(i, end=", ")
