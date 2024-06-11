"""
@Author:  Tom Shabalin
@ID:      321243339
@Mail:    tomshabalin95@gmail.com
@Date:    28/04/2024
@Description: Deep Sort Assignment for the course "Research Algorithms"
"""

def deep_sorted(x: any) -> str:
    """
    Sorts a deep data structure by keys.

    Args:
        x (any): The input deep data structure which contain lists, dictionaries, sets, and tuples.

    Returns:
        str: A string representation of the sorted deep data structure.

    Examples:
        >>> deep_sorted({"a": [3, 2, 1], "b": {"d": 4, "c": 3}, "c": (7, 6, 5)})
        '{"a": [1, 2, 3], "b": {"c": 3, "d": 4}, "c": (5, 6, 7)}'
        >>> deep_sorted(["c", "a", "b"])
        '[a, b, c]'
        >>> deep_sorted((3, 1, 2))
        '(1, 2, 3)'
        >>> deep_sorted({"a": 6, "b": [3, 6, [4, 9], 2, 7, 0], "c": 7})
        '{"a": 6, "b": [0, 2, 3, 6, 7, [4, 9]], "c": 7}'
        >>> deep_sorted({"a": {"b": [3, 2, 1], "c": (7, 6, 5)}, "d": {"e": {"f": {}}}})
        '{"a": {"b": [1, 2, 3], "c": (5, 6, 7)}, "d": {"e": {"f": {}}}}'
        >>> deep_sorted({"a": 6, "b": {"c": [3, 2, 1], "d": {"e": (7, 6, 5)}}})
        '{"a": 6, "b": {"c": [1, 2, 3], "d": {"e": (5, 6, 7)}}}'
        >>> deep_sorted({"a": {"b": {"c": [{"d": [3, 2, 1]}, 9, 8]}, "e": 7}})
        '{"a": {"b": {"c": [8, 9, {"d": [1, 2, 3]}]}, "e": 7}}'
        >>> deep_sorted({"z": [4, 3, 2, 1], "x": {"y": [9, 8, 7, 6], "w": (5, 4, 3, 2)}, "v": {"u": {"t": [13, 12, 11, 10], "s": (17, 16, 15, 14)}, "r": {"q": [21, 20, 19, 18], "p": (25, 24, 23, 22)}}})
        '{"v": {"r": {"p": (22, 23, 24, 25), "q": [18, 19, 20, 21]}, "u": {"s": (14, 15, 16, 17), "t": [10, 11, 12, 13]}}, "x": {"w": (2, 3, 4, 5), "y": [6, 7, 8, 9]}, "z": [1, 2, 3, 4]}'
    """
    if isinstance(x, dict):
        sorted_dict = sorted(x.items())
        return "{" + ", ".join(f'"{k}": {deep_sorted(v)}' for k, v in sorted_dict) + "}"
    elif isinstance(x, list):
        sorted_list = [deep_sorted(item) if isinstance(item, (list, tuple, set, dict)) else str(item) for item in x]
        sorted_list = sorted(sorted_list)
        return "[" + ", ".join(sorted_list) + "]"
    elif isinstance(x, tuple):
        sorted_tuple = [deep_sorted(item) if isinstance(item, (list, tuple, set, dict)) else str(item) for item in x]
        sorted_tuple = sorted(sorted_tuple)
        return "(" + ", ".join(sorted_tuple) + ")"
    elif isinstance(x, set):
        sorted_set = [deep_sorted(item) if isinstance(item, (list, tuple, set, dict)) else str(item) for item in x]
        sorted_set = sorted(sorted_set)
        return "{" + ", ".join(sorted_set) + "}"
    else:
        return repr(x)


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
    x = eval(input())
    print(deep_sorted(x))
