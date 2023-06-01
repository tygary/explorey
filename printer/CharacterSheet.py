import time
import math
from printer.DiceRoller import *
from enum import IntEnum


class CharType(IntEnum):
    DEX = 0  # Sneakiness
    WIS = 1  # Craftiness
    CON = 2  # Scrappiness
    CHA = 3  # Fabulousness


MAIN_QUESTS_BY_TYPE = [
    "Sneakiness Quest.",
    "Craftiness Quest.",
    "Scrappiness Quest.",
    "Fabulousness Quest.",
]

TURBULENT_QUESTS_BY_TYPE = [
    [
        "Sneak into a high-security prison just to leave a cake with a file in it for no particular reason",
        "Spend an entire day going unnoticed while wearing a bright yellow jumpsuit in a crowded city",
        "Successfully steal the hat off the head of a statue without getting caught",
        "Catch a fly with chopsticks",
        "Become a master pickpocket and steal people's left shoes",
        "Sneak into a movie theater dressed as a cardboard box",
        "Make it through an entire day without anyone realizing that I'm actually a cardboard cutout",
        "Sneak up on someone and give them a heart attack by yelling 'boo!'",
        "Infiltrate a secret society of tea enthusiasts and replace all their tea leaves with confetti",
        "Trick a group of knights into embarking on a quest to find the mythical 'Unicorn of Infinite Flatulence'",
        "Uncover the hidden treasure of a long-lost gnome civilization, consisting entirely of eccentric socks",
        "Steal a priceless artifact from a museum and replace it with a fake",
        "Sneak into a castle and replace all the paintings with pictures of cats",
        "Create a legendary treasure map that leads to a ridiculously mundane item",
        "Open a portal to a dimension of darkness and unleash its horrors upon the world",
    ],
    [
        "Write a novel about a sentient piece of toast",
        "Develop a secret society for people who love puns",
        "Perform a forbidden ritual to transform themself into an immortal being of pure darkness"
        "Create a potion that turns hair into various vibrant and uncontrollable colors",
        "Craft a magical amulet that attracts misplaced socks and causes them to reappear in inconvenient places",
        "Conjure illusions of a mischievous imp to follows people around and play harmless pranks on them",
    ],
    [
        "To become the goblin lord",
        "Break a world record for the most number of times bitten by mosquitoes without itching",
        "Out-drink a group of dwarves and win their respect",
    ],
    [
        "Seduce a powerful wizard or sorceress with your charm",
        "Become the ruler of a kingdom solely through the power of your charisma and fabulousness",
    ],
]
TIDY_QUESTS_BY_TYPE = [
    [
        "To become the nimblest onion skee-ball player in the town",
        "Perform an incredibly complex heist involing a giant onion, a rubber chicken, and a pair of socks",
        "Become a skilled tightrope walker and walk across the mystical 'Bridge of Doom'",
        "Join a traveling circus and become the world's greatest onion juggler",
        "Create a new form of dubstep dance that surpasses all known forms of dance",
        "Become the world's greatest escape artist and escape from a straightjacket while being chased by a bugbear",
        "Learn how to balance a spoon on my nose for 30 seconds while standing on one foot and singing Enya",
        "Successfully juggle flaming torches while riding a unicycle across a pit of lava",
    ],
    [
        "To study the interdimensional planes to discover the next new psychedelic trend",
        "Become the greatest bonsai tree artist in the world by creating a bonsai tree that looks like a bad dragon toy",
        "Design a hat that doubles as a birdhouse so that birds can live on my head",
        "Invent a new language using only animal sounds so that you can finally ask what your pet cat is thinking",
        "Create a machine that can turn water into coffee so that you can find existential peace",
        "Create a brand of potato chips that taste like pizza and sell them to all the stoners in the realm",
        "Build a robot that can do all my chores for me so that I can spend more time playing video games",
        "Become the world's first professional rock, paper, scissors player.  Winning a sponsorship from OfficeMax",
        "Write a self-help book for talking to animals and become a world-renowned animal whisperer",
    ],
    [
        "Become the world's greatest thumb wrestler and win the title of 'Thumb Wrestling Champion'",
        "Win a gladatorial battle against a giant hamster without using any weapons",
        "Survive a round in a boxing match with a kangaroo without getting knocked out",
        "Climb Mount Everest using only a paper clip and dental floss to prove that you can",
        "Become a champion arm wrestler and win the title of 'Arm Wrestling King'",
    ],
    [
        "To capture the heart of the common participant with lasers and bass music",
        "Become the most famous and beloved bard in the land, known for my epic tales of adventure and heroism",
        "Host a legendary party that everyone talks about for years, but no one can remember what exactly happened",
        "Write and perform a hit song that becomes a classic and is played at every tavern in the land",
    ],
]
QUEST_BY_TYPE = [
    TURBULENT_QUESTS_BY_TYPE[0] + TIDY_QUESTS_BY_TYPE[0],
    TURBULENT_QUESTS_BY_TYPE[1] + TIDY_QUESTS_BY_TYPE[1],
    TURBULENT_QUESTS_BY_TYPE[2] + TIDY_QUESTS_BY_TYPE[2],
    TURBULENT_QUESTS_BY_TYPE[3] + TIDY_QUESTS_BY_TYPE[3],
]

BEAUTY_SPECIES = [
    "Human",
    "Goblin",
    "Fairy",
    "Dwarf",
    "Pixie",
    "Leprechaun",
    "High-Elf",
    "Night-Elf",
    "Wood-Elf",
    "Hobbit",
    "Halfling",
    "Gnome",
    "Merfolk",
    "Vampire",
    "Fox-Librarian",
    "Unicorn",
    "Pegasus",
    "Aristo-cat",
    "Giant",
]
BEAST_SPECIES = [
    "Poltergeist",
    "Gargoyle",
    "Imp",
    "Goblin",
    "Lizard",
    "Bovine",
    "Tabaxi",
    "Duck",
    "Minotaur",
    "Werewolf",
    "Dog-Person",
    "Toad",
    "Tortoise",
    "Rabbit",
    "Owl",
    "Dragonborn",
    "Centaur",
    "Frog-Person",
    "Goat-Person",
    "Yeti",
    "Sasquatch",
    "Manticore",
]
ALL_SPECIES = BEAUTY_SPECIES + BEAST_SPECIES

CLASS_BY_TYPE = [
    # DEX
    [
        "Trapper",
        "Con Artist",
        "Pirate",
        "Burglar of Cats",
        "Spy",
        "Juggler",
        "Rock Stacker",
        "Vegetable Pruner",
        "Swindler",
        "Pickpocket",
        "Acrobat",
        "Tightrope Walker",
        "Sword Swallower",
    ],
    # WIS
    [
        "Alchemist",
        "Brewmaster",
        "Scholar",
        "Cobbler",
        "Haberdasher",
        "Soup’r Stoner",
        "Potato Shaman",
        "Tinkerer",
        "Bog witch",
        "Garlic witch",
        "Herbalist",
        "Beekeeper",
        "Baker",
        "Candlemaker",
        "Illusionist",
    ],
    # CON
    [
        "Goat-Wrangler",
        "Frog-Wrangler",
        "Duck-Wrangler",
        "Frog-Wrestler",
        "Rock-Smasher",
        "Onion-Cutter",
        "Garlic-Smasher",
        "Wood-Gnawer",
        "Boulder-Lifter",
        "Gate Guardian",
        "Black-Ops",
        "Carpenter",
        "Mason",
        "Lumberjack",
        "Survivalist",
    ],
    # CHA
    [
        "Aristocrat",
        "Oracle",
        "Charlatan",
        "Frog Charmer",
        "Diva",
        "Jester",
        "Clown",
        "Performance Artist",
        "Musical Prodigy",
        "Chef",
        "Sparkle Pony",
        "Lyft Driver",
        "Cultural Icon",
        "Influencer",
        "Food Critic",
        "Comedian",
        "Stage Manager",
        "School Teacher",
    ],
]

MAGIC_ABILITIES = [
    "Create Illusion",
    "Shoot Fire",
    "Shoot Electricity",
    "Waterbend",
    "Debilitating Insult",
    "Spit Acid",
    "Charm",
    "Summon Vines",
    "Summon Unicorn",
    "Floating Lightshow",
    "Craft Item",
    "Summon Insects",
    "Turn Invisible",
    "Fly",
    "Levitation",
    "Turn into Chicken",
    "Invisibility",
    "Create Fire",
    "Teleportation",
    "Mind reading",
    "Create Visual Illusion",
    "Create Ice",
    "Cow Summoning",
    "Shape shifting",
    "Summon Ghosts",
    "Telekinesis",
    "Instantaneously Grow Plants",
    "Talk to Animals",
    "Summon Fog",
    "Summon Rainstorm",
    "Summon Lightning",
    "Telepathy",
    "Create Earthquake",
    "Clairvoyance",
    "Pyrokinesis",
    "Hydrokinesis",
    "Electrokinesis",
]
PHYSICAL_ABILITIES = [
    "Pick Lock",
    "Spider Climb",
    "Craft Item",
    "Flaming Arrow",
    "Hide in Shadows",
    "Disguise Self",
    "Make Healing Soup",
    "Cut Onions",
    "Mash Potatoes",
    "Milk Cows",
    "Brew Beer",
    "Brew Kombucha",
    "Brew Coffee",
    "Throw Net",
]
SILLY_ABILITIES = [
    "Apply Lubricant",
    "Juggle Fruit",
    "Sing Badly",
    "Talk to Inanimate Objects",
    "Eat Spicy Food Without Crying",
    "Tell Terrible Jokes",
    "Write with Both Hands",
    "Hula Hoop",
    "Balance a Spoon on Your Nose",
    "Juggle Chainsaws",
    "Contort into a Pretzel",
    "Twerk Like a Pro",
    "Make a Perfect Sandwich",
    "Bend Spoons with Mind",
    "Sneeze on Command",
    "Play the Kazoo Like a Virtuoso",
    "Wishful Thinking",
    "Make a Perfect Omelette","
]
ALL_ABILITIES = MAGIC_ABILITIES + PHYSICAL_ABILITIES + SILLY_ABILITIES

USEFUL_ITEMS = [
    "Healing Potion",
    "Headlamp",
    "Carabiner",
    "Handcuffs",
    "Sword",
    "Longbow",
    "Rope",
    "A disguise kit",
    "A grappling hook",
    "A lockpick set",
    "A bottle of strong alcohol",
    "A cart",
    "A shovel",
    "A pair of sturdy boots",
    "A map of the region",
    "A small mirror",
    "A hand-held fan",
    "A deck of playing cards",
    "A pocket watch",
    "A magnifying glass",
    "A first-aid kit",
    "A pen and paper",
    "A frying pan",
    "A bag of marbles",
    "A bag of cow feed",
    "A cow costume",
    "Bag of holding",
    "Grappling hook",
    "Lockpicks",
    "Healing potion",
    "Smoke bomb",
    "Sleeping bag",
    "Magnifying glass",
    "Magic wand",
    "Stink bomb",
    "Bottled lightning",
    "Fishing net",
    "Whetstone",
    "Spyglass",
    "Rope ladder",
    "Poisoned dart",
    "Slingshot",
    "Caltrops",
    "Flint and steel",
    "Glowing mushroom",
    "Petrified frog",
    "Healing potion",
    "Invisibility cloak",
    "Pocket mirror",
    "Lockpicks",
    "Rope and grappling hook",
    "Flashlight",
    "Smoke bomb",
    "Whetstone",
    "Bandage",
    "Magnifying glass",
    "Fire starter",
    "Water canteen",
    "Map of the region",
    "Poison antidote",
    "Climbing gloves",
    "Glowing crystal",
    "Gas mask",
    "Winged boots",
    "Charm amulet",
    "Sonic whistle",
]
JOKE_ITEMS = [
    "Shibari Rope",
    "Bag of Beans",
    "Footlong Dildo",
    "Box of glitter",
    "Broken compass",
    "Rubber chicken",
    "Singing fish",
    "Inflatable palm tree",
    "Whoopee cushion",
    "Fake mustache collection",
    "Glow-in-the-dark sunglasses",
    "Unicorn horn headband",
    "Nose pencil sharpener",
    "Banana phone",
    "Giant inflatable dinosaur",
    "Disco ball keychain",
    "Mood ring",
    "Flashing LED shoelaces",
    "Tie-dye bandana",
    "Fake vampire teeth",
    "Rainbow wig",
    "Fanny pack with built-in speakers",
    "Glowing hula hoop",
]
ALL_ITEMS = USEFUL_ITEMS + JOKE_ITEMS


# Classes:
# Sneakiness - Brawny / Sly - Dex
# Scrappiness - Brawny / Showy - Con
# Craftiness - Bookish / Sly - Wis
# Fabulousness - Bookish / Showy - Cha

# Levers:
# 0: Bookish / Brawny
# 1: Sly / Showy
# 2: Tidy / Turbulent
# 3: Beauty / Beast

CHARS_PER_ROW = 30
SPACES_PER_ROW = 54
CHAR_TO_SPACE_RATIO = SPACES_PER_ROW / CHARS_PER_ROW
CHARS_PER_SECTION = CHARS_PER_ROW * 4


def buffer_str(str):
    length = len(str)
    if length < CHARS_PER_SECTION:
        additional_spaces = math.ceil(
            (CHARS_PER_SECTION - length) * CHAR_TO_SPACE_RATIO
        )
        return str + " " * additional_spaces + "."
    else:
        return str


class CharacterSheet(object):
    dex = 10
    wis = 10
    con = 10
    cha = 10
    char_type = -1
    class_name = ""
    species = ""
    abilities = []
    items = []
    quest = ""
    main_quest = ""

    def __init__(self, char_type=-1, levers=None):
        if levers is not None:
            # levers[0] - 1 is Bookish, 0 is Brawny
            # levers[1] - 1 is Sly, 0 is Showy
            if levers[0] == 1 and levers[1] == 1:
                char_type = CharType.WIS
            elif levers[0] is 1 and levers[1] is 0:
                char_type = CharType.CHA
            elif levers[0] is 0 and levers[1] is 1:
                char_type = CharType.DEX
            elif levers[0] is 0 and levers[1] is 0:
                char_type = CharType.CON

        if char_type < 0:
            char_type = random.randint(0, 3)
        self.main_quest = buffer_str(MAIN_QUESTS_BY_TYPE[char_type])

        self.char_type = char_type
        self.__set_scores()
        self.__set_species()
        self.__set_class_name()
        self.__set_abilities()
        self.__set_items()
        self.__set_quest()

    def __set_scores(self):
        scores = [roll_3d6(), roll_3d6(), roll_3d6(), roll_3d6()]
        scores.sort()
        highest = scores.pop()
        random.shuffle(scores)

        if self.char_type == CharType.DEX:
            self.dex = highest
            self.wis = scores[0]
            self.con = scores[1]
            self.cha = scores[2]
        elif self.char_type == CharType.WIS:
            self.wis = highest
            self.cha = scores[0]
            self.con = scores[1]
            self.dex = scores[2]
        elif self.char_type == CharType.CON:
            self.con = highest
            self.wis = scores[0]
            self.dex = scores[1]
            self.cha = scores[2]
        elif self.char_type == CharType.CHA:
            self.cha = highest
            self.wis = scores[0]
            self.con = scores[1]
            self.dex = scores[2]

    def __set_species(self, levers=None):
        if levers is not None:
            # levers[2] - 1 is Beauty, 0 is Beast
            if levers[3] is 1:
                self.species = random.choice(BEAUTY_SPECIES)
            else:
                self.species = random.choice(BEAST_SPECIES)
        else:
            self.species = random.choice(ALL_SPECIES)

    def __set_class_name(self):
        self.class_name = random.choice(CLASS_BY_TYPE[self.char_type])

    def __set_abilities(self):
        self.abilities = random.choices(ALL_ABILITIES, k=3)
        # if self.char_type == CharType.WIS or self.char_type == CharType.CHA:
        #     self.abilities = random.choices(MAGIC_ABILITIES, k=2) + random.choices(
        #         PHYSICAL_ABILITIES, k=1
        #     )
        # else:
        #     self.abilities = random.choices(MAGIC_ABILITIES, k=1) + random.choices(
        #         PHYSICAL_ABILITIES, k=2
        #     )

    def __set_items(self):
        self.items = random.choices(ALL_ITEMS, k=3)

    def __set_quest(self, levers=None):
        # levers[3] - 0 is Turbulent, 1 is Tidy
        if levers is not None:
            if levers[2] is 0:
                self.quest = random.choice(TURBULENT_QUESTS_BY_TYPE)
            else:
                self.quest = random.choice(TIDY_QUESTS_BY_TYPE)
        else:
            self.quest = random.choice(QUEST_BY_TYPE[self.char_type])
        self.quest = buffer_str(self.quest)

    def __str__(self):
        return f"A {self.species} {self.class_name} on a quest to {self.quest}.  Sneakiness={self.dex} Craftiness={self.wis} Scrappiness={self.con} Fabulousness={self.cha} Abilities: {self.abilities} Items: {self.items}"
