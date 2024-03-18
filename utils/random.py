''' Random utils '''
from random import randrange

def get_random_number(start, end, step):
    ''' Get random number in defined range with specific step '''
    if start == end:
        return start

    if start > end:
        return randrange(end, start, step)

    return randrange(start, end, step)
