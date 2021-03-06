'''Utilities'''

SUFFIXES = {1: 'st', 2: 'nd', 3: 'rd'}
def get_ordinal(i: int) -> str:
    # Adapted from https://codereview.stackexchange.com/questions/41298/producing-ordinal-numbers
    if 10 <= i % 100 <= 20:
        return 'th'
    else:
        return SUFFIXES.get(i % 10, 'th')