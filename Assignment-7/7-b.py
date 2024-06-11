import sqlite3, requests

with open("poll.db", "wb") as file:
    response = requests.get("https://github.com/erelsgl-at-ariel/research-5784/raw/main/06-python-databases/homework/poll.db")
    file.write(response.content)

db = sqlite3.connect("poll.db")

def get_candidate_column(candidate: str) -> str:
    """
    Get the column name in the list_of_answers table for a given candidate.

    Parameter
    -------
    - candidate: str - The candidate's name.

    Returns
    -------
    - str - The column name in the list_of_answers table for the given candidate.
    """
    cursor = db.cursor()
    cursor.execute("""
    SELECT Variable
    FROM codes_for_questions
    WHERE Label = ?
    """, (candidate,))
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result else None

def net_support_for_candidate1(candidate1: str, candidate2: str) -> int:
    """
    This function calculates the net support for candidate1 over candidate2.

    Parameters
    ----------
    - candidate1: str - The first candidate's name.
    - candidate2: str - The second candidate's name.

    Returns
    -------
    - int - The net support for candidate1 over candidate2.

    Examples
    --------
    >>> net_support_for_candidate1("בני גנץ", "בנימין נתניהו")
    35

    >>> net_support_for_candidate1("בנימין נתניהו", "בני גנץ")
    -35

    >>> net_support_for_candidate1("בני גנץ", "גדעון סער")
    -51

    >>> net_support_for_candidate1("נפתלי בנט", "יאיר לפיד")
    41

    >>> net_support_for_candidate1("נפתלי בנט", "נפתלי בנט")
    0

    >>> net_support_for_candidate1("נפתלי בנט", "יולי אדלשטיין")
    113
    """
    column1 = get_candidate_column(candidate1)
    column2 = get_candidate_column(candidate2)

    if not column1 or not column2:
        raise ValueError("One or both candidates not found in the database.")
    
    cursor = db.cursor()
    
    # Count preferences for candidate1 over candidate2
    cursor.execute(f"""
    SELECT COUNT(*)
    FROM list_of_answers
    WHERE {column1} < {column2}
    """)
    count1 = cursor.fetchone()[0]
    
    # Count preferences for candidate2 over candidate1
    cursor.execute(f"""
    SELECT COUNT(*)
    FROM list_of_answers
    WHERE {column2} < {column1}
    """)
    count2 = cursor.fetchone()[0]
    
    # Calculate net support
    net_support = count1 - count2
    
    cursor.close()
    
    return net_support

def condorcet_winner() -> str:
    """
    Compute the Condorcet winner.

    Returns
    -------
    - str - The Condorcet winner.

    Examples
    --------
    >>> condorcet_winner()
    'נפתלי בנט'
    """
    cursor = db.cursor()
    cursor.execute("SELECT Label FROM codes_for_questions WHERE Variable LIKE 'Q6_%'")
    candidates = [row[0] for row in cursor.fetchall()]
    cursor.close()

    for candidate in candidates:
        wins_all_others = True
        for other_candidate in candidates:
            if candidate == other_candidate:
                continue
            net_support = net_support_for_candidate1(candidate, other_candidate)
            if net_support <= 0:
                wins_all_others = False
                break
        if wins_all_others:
            return candidate

    return "אין"


if __name__ == '__main__':
    # import doctest
    # doctest.testmod(verbose=True)
    party = input()
    if party == "condorcet_winner":
        print(condorcet_winner())
    else:
        candidate1,candidate2 = party.split(",")
        print(net_support_for_candidate1(candidate1,candidate2))