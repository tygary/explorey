import random


def roll_d6():
    return random.randrange(1, 6, 1)


def roll_3d6():
    return roll_d6() + roll_d6() + roll_d6()


def roll_d8():
    return random.randrange(1, 8, 1)


def roll_d10():
    return random.randrange(1, 10, 1)


def roll_d12():
    return random.randrange(1, 12, 1)


def roll_d20():
    return random.randrange(1, 20, 1)


def roll_d100():
    return random.randrange(1, 100, 1)
