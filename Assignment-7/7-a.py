"""
@Author:  Tom Shabalin
@ID:      321243339
@Mail:    tomshabalin95@gmail.com
@Date:    10/06/2024
@Description: Public opinion poll analysis assignment for the course "Research Algorithms"
"""

import pandas as pd

codes_for_questions = pd.read_csv("https://raw.githubusercontent.com/erelsgl-at-ariel/research-5784/main/06-python-databases/homework/codes_for_questions.csv")
codes_for_answers = pd.read_csv("https://raw.githubusercontent.com/erelsgl-at-ariel/research-5784/main/06-python-databases/homework/codes_for_answers.csv")
list_of_answers = pd.read_csv("https://raw.githubusercontent.com/erelsgl-at-ariel/research-5784/main/06-python-databases/homework/list_of_answers.csv")

# Dictionary of party names and their values in the elections columns (codes_for_answers)
parties_dictionary = {'מחל': 1, 'פה': 2, 'שס': 3, 'כן': 4, 
                   'ב': 5, 'אמת': 6, 'ג': 7, 'ל': 8, 'ט': 9,
                    'ודעם': 10, 'ת': 11, 'מרצ': 12, 'עם': 13,
                    'יז': 14, 'ר': 15, 'מפלגה אחרת': 16, 'פתק לבן': 17
                    }

def support_in_one_party_elections(party: str) -> int:
    """
    Get the number of supports in one-party elections for the given party.
    Q2 questions in the survey.

    Parameters
    ----------
    - `party`: str - The party's name.

    Returns
    -------
    - `int`: The number of supports in one-party elections for the given party.

    Examples
    --------
    >>> support_in_one_party_elections('מחל')
    134
    >>> support_in_one_party_elections('ב')
    54
    >>> support_in_one_party_elections('פתק לבן')
    53
    >>> support_in_one_party_elections('פה')
    109
    >>> support_in_one_party_elections('ר')
    3
    >>> support_in_one_party_elections('עם')
    21
    >>> support_in_one_party_elections('מפלגה אחרת')
    11
    >>> support_in_one_party_elections('יז')
    3
    >>> support_in_one_party_elections('מפלגה לא קיימת')
    0
    """
    party_value = parties_dictionary.get(party, 0)
    
    # Calculate the number of supports
    supports = (list_of_answers['Q2'] == party_value).sum()
    return supports

def support_in_multi_party_elections(party: str) -> int:
    """
    Get the number of supports in multi-party elections for the given party.
    Q3 questions in the survey.

    Parameters
    ----------
    - `party`: str - The party's name.

    Returns
    -------
    - `int`: The number of supports in multi-party elections for the given party.

    Examples
    --------
    >>> support_in_multi_party_elections('מחל')
    162
    >>> support_in_multi_party_elections('ב')
    101
    >>> support_in_multi_party_elections('פה')
    131
    >>> support_in_multi_party_elections('פתק לבן')
    49
    >>> support_in_multi_party_elections('ר')
    13
    >>> support_in_multi_party_elections('עם')
    27
    >>> support_in_multi_party_elections('מפלגה אחרת')
    8
    >>> support_in_multi_party_elections('יז')
    32
    >>> support_in_multi_party_elections('מפלגה לא קיימת')
    0
    """
    party_value = parties_dictionary.get(party, 0)
    if not party_value:
        return 0

    # Count occurrences of this value in the dynamically constructed column
    multy_party_sum = int(list_of_answers[f'Q3_{party_value}'].sum())
    return multy_party_sum

def rank_parties_by_support(method):
    """
    Rank parties based on the support count from a given method.

    Parameters:
    - `method`: Function to calculate the support count for a party.

    Returns:
    - DataFrame with parties and their ranks.

    Examples
    --------
    >>> rank_parties_by_support(support_in_one_party_elections)
    מחל            1
    פה             2
    ב              3
    פתק לבן        4
    אמת            5
    כן             6
    ט              7
    ת              8
    ודעם           9
    עם            10
    ג             11
    מרצ           12
    ל             13
    שס            14
    מפלגה אחרת    15
    יז            16
    ר             17
    dtype: int64

    >>> rank_parties_by_support(support_in_multi_party_elections)
    מחל            1
    פה             2
    ב              3
    כן             4
    אמת            5
    ט              6
    מרצ            7
    ת              8
    פתק לבן        9
    שס            10
    ל             11
    יז            12
    ג             13
    ודעם          14
    עם            15
    ר             16
    מפלגה אחרת    17
    dtype: int64
    """
    supports = {party: method(party) for party in parties_dictionary}
    sorted_parties = sorted(supports, key=supports.get, reverse=True)
    ranks = {party: rank for rank, party in enumerate(sorted_parties, 1)}
    return pd.Series(ranks)

def parties_with_different_relative_order() -> tuple:
    """
    Check if there are 2 parties, that their relative order is different in both of the election methods.

    Returns
    -------
    - `tuple`: A tuple of two party names with different relative orders in both election methods, or `None` if none are found.
    
    >>> parties_with_different_relative_order()
    ('שס', 'ג')
    """
    rank_one_party = rank_parties_by_support(support_in_one_party_elections)
    rank_multi_party = rank_parties_by_support(support_in_multi_party_elections)
    
    for party1 in parties_dictionary:
        for party2 in parties_dictionary:
            if party1 != party2:
                if (rank_one_party[party1] < rank_one_party[party2] and rank_multi_party[party1] > rank_multi_party[party2]) or \
                    (rank_one_party[party1] > rank_one_party[party2] and rank_multi_party[party1] < rank_multi_party[party2]):
                    return (party1, party2)
    return None

if __name__ == '__main__':
    # import doctest
    # doctest.testmod(verbose=True)
    party = input()
    if party == "parties_with_different_relative_order":
        print(parties_with_different_relative_order())
    else:
        print(support_in_one_party_elections(party), support_in_multi_party_elections(party))