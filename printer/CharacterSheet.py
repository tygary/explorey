import time
from printer.DiceRoller import *
from enum import IntEnum


class CharType(IntEnum):
    DEX = 0
    WIS = 1
    CON = 2
    CHA = 3


QUEST_BY_TYPE = [
    [
        "To become the nimblest skee-ball player",
        "Perform an incredibly complex heist",
        "Become a skilled tightrope walker",
        "Join a traveling circus",
        "Create a new form of dance",
        "Become the world's greatest escape artist",
        "Sneak into a high-security prison just to leave a cake with a file in it for no particular reason",
        "Spend an entire day going unnoticed while wearing a bright yellow jumpsuit in a crowded city",
        "Successfully steal the hat off the head of a statue without getting caught",
        "Catch a fly with chopsticks",
        "Learn how to balance a spoon on my nose for 30 seconds",
        "Become a master pickpocket and steal people's left shoes",
        "Sneak into a movie theater dressed as a cardboard box",
        "Successfully juggle flaming torches while riding a unicycle",
        "Make it through an entire day without anyone realizing that I'm actually a cardboard cutout",
        "Sneak up on someone and give them a heart attack by yelling 'boo!'",
    ],
    [
        "To study the interdimensional planes",
        "Become the greatest bonsai tree artist in the world",
        "Design a hat that doubles as a birdhouse",
        "Invent a new language using only animal sounds",
        "Create a machine that can turn water into coffee",
        "Write a novel about a sentient piece of toast",
        "Develop a secret society for people who love puns",
        "Create a brand of potato chips that taste like pizza",
        "Build a robot that can knit sweaters",
        "Become the world's first professional rock, paper, scissors player",
        "Write a self-help book for talking to animals",
    ],
    [
        "To become the goblin lord",
        "Become the world's greatest thumb wrestler",
        "Win an eating contest without getting sick",
        "Survive a round in a boxing match with a kangaroo",
        "Climb Mount Everest using only a paper clip and dental floss",
        "Out-drink a group of dwarves",
        "Break a world record for the most number of times bitten by mosquitoes without itching",
        "Survive a game of Russian roulette",
        "Become a champion arm wrestler",
        "Enter and win a hot dog eating competition",
        "Swim across a pool of Jell-O",
    ],
    [
        "To capture the heart of the common participant",
        "Become the most popular influencer in the realm",
        "Get a million followers on your social media accounts",
        "Design the most fashionable and iconic outfit ever seen",
        "Become the face of a high-end beauty brand",
        "Host a legendary party that everyone talks about for years",
        "Star in a popular and critically acclaimed play",
        "Convince a dragon to lend you its hoard for your fabulous fashion line",
        "Seduce a powerful wizard or sorceress with your charm",
        "Write and perform a hit song that becomes a classic",
        "Become the ruler of a kingdom solely through the power of your charisma and fabulousness",
    ],
]

ALL_SPECIES = [
    "Bovine",
    "Lizard",
    "Human",
    "Goblin",
    "Aristo-cat",
    "Dragonborn",
    "Tabaxi",
    "Troll",
    "Fairy",
    "High-Elf",
    "Night-Elf",
    "Hobbit",
    "Duck",
    "Dog-Person",
    "Toad",
    "Gnome",
    "Tortoise",
    "Rabbit",
    "Fox-Librarian",
    "Owl",
    "Unicorn",
]
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
    ],
    # CHA
    ["Aristocrat", "Oracle", "Charlatan", "Frog Charmer", "Diva", "Jester", "Clown"],
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
    "Invisibility",
    "Teleportation",
    "Mind reading",
    "Create Visual Illusion",
    "Create Ice",
    "Cow Summoning",
    "Shape shifting",
    "Telekinesis",
    "Instantaneously Grow Plants",
    "Talk to Animals",
    "Summon Rainstorm",
    "Telepathy",
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

    def __init__(self, char_type=-1):
        if char_type < 0:
            char_type = random.randint(0, 3)
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

    def __set_species(self):
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

    def __set_quest(self):
        self.quest = random.choice(QUEST_BY_TYPE[self.char_type])

    def __str__(self):
        return f"A {self.species} {self.class_name} on a quest to {self.quest}.  Sneakiness={self.dex} Craftiness={self.wis} Scrappiness={self.con} Fabulousness={self.cha} Abilities: {self.abilities} Items: {self.items}"