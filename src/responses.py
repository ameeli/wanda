from random import shuffle

def make_mw_responses():
    """Fakes mind wandering dataset and return a list of inputs."""
    
    five = '5' * 8
    six = '6' * 21
    seven = '7' * 13

    pairs = ['1, 2', '1, 3', '1, 4', '1, 4', '1, 8', '1, 8', '1, 8', '1, 9']

    fives = list(five)
    sixes = list(six)
    sevens = list(seven)

    for num in fives:
        pairs.append('1, ' + num)

    for num in sixes:
        pairs.append('1, ' + num)

    for num in sevens:
        pairs.append('1, ' + num)

    return pairs


def make_not_mw_responses():
    """Fakes mind wandering dataset and return a list of inputs."""

    five = '5' * 6
    six = '6' * 12
    seven = '7' * 18
    eight = '8' * 16
    nine = '9' * 7

    pairs = ['2, 3', '2, 4', '2, 10']

    fives = list(five)
    sixes = list(six)
    sevens = list(seven)
    eights = list(eight)
    nines = list(nine)

    for num in fives:
        pairs.append('2, ' + num)

    for num in sixes:
        pairs.append('2, ' + num)

    for num in sevens:
        pairs.append('2, ' + num)   

    for num in eights:
        pairs.append('2, ' + num)    

    for num in nines:
        pairs.append('2, ' + num)

    return pairs


mind_wandering = make_mw_responses()
not_mind_wandering = make_not_mw_responses()
combined_pairs = mind_wandering + not_mind_wandering
shuffle(combined_pairs)



