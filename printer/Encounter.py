import time
from enum import IntEnum
import random

comical_encounters = ["A mischievous pixie steals the group's shoes and hides them in a nearby tree.",
                      "A talking horse mistakes one of the party members for its long-lost owner and refuses to leave their side.",
                      "A clumsy ogre accidentally knocks over the party's campfire while trying to be friendly.",
                      "The group is ambushed by a gang of goblins who are more interested in trading jokes than fighting.",
                      "A group of friendly ghosts offer to guide the party through a haunted forest, but they keep forgetting where they're going.",
                      "A giant chicken thinks one of the party members is its chick and won't stop following them around.",
                      "The group discovers a magical fountain that causes everyone who drinks from it to start speaking in rhyming couplets.",
                      "A group of mischievous fairies replace all of the party's weapons with harmless replicas.",
                      "The party stumbles upon a group of friendly giants who love nothing more than playing hide and seek.",
                      "The group finds a cursed mirror that makes everyone who looks into it appear as a comically exaggerated version of themselves.",
                      "A grumpy old troll insists on telling the party his life story, whether they want to hear it or not.",
                      "A mischievous leprechaun offers the party a pot of gold, but only if they can answer his riddles correctly.",
                      "A group of mischievous imps offer to help the party with their quest, but they keep causing more trouble than they solve.",
                      "The party comes across a group of bickering wizards who are having an argument about the proper way to cast a spell.",
                      "A friendly dragon offers to let the party ride on its back, but it keeps sneezing uncontrollably mid-flight.",
                      "The group discovers a portal to a parallel universe where they are all evil versions of themselves.",
                      "A friendly giantess takes a shine to one of the party members and won't stop trying to give them giant bear hugs.",
                      "The party accidentally stumbles into the middle of a goblin wedding ceremony and is mistaken for the entertainment.",
                      "A mischievous gnome offers to lead the party to a treasure trove, but only if they agree to let him play a series of pranks on them along the way.",
                      "The group comes across a group of talking animals who are having a heated debate about the best way to prepare a carrot stew."]


class Difficulty(IntEnum):
    EASY = 0
    MED = 1
    HARD = 2
    IMPOSSIBLE = 3


class Monster(object):
    def __init__(self, name, difficulty):
        self.name = name
        self.difficulty = difficulty


ALL_MONSTERS = [
    Monster("", Difficulty.EASY),
    Monster("", Difficulty.EASY),
    Monster("", Difficulty.EASY),
    Monster("", Difficulty.EASY),
    Monster("", Difficulty.EASY),
    Monster("", Difficulty.EASY),
    Monster("", Difficulty.EASY),
    Monster("", Difficulty.EASY),
    Monster("", Difficulty.EASY),
]

CHALLENGES_BY_SKILL = [
    # DEX - Sneakiness
    [""],
    # WIS - Craftiness
    [],
    # CON - Scrappiness
    [],
    # CHA - Fabulousness
    []
]


def getRandomMonster():
    return random.choice(ALL_MONSTERS)


class Encounter(object):
    required_skill = -1
    dc = 15

    def __init__(self):
        self.monster = getRandomMonster()

    def __str__(self):
        return f"An Encounter"



