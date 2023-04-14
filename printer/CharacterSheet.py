import time
from printer.DiceRoller import *
from enum import IntEnum


class CharType(IntEnum):
    DEX = 0
    WIS = 1
    CON = 2
    CHA = 3


QUEST_BY_TYPE = [
    "To become the nimblest skee-ball player",
    "To study the interdimensional planes",
    "To become the goblin lord",
    "To capture the heart of the common participant"
]

ALL_SPECIES = ["Bovine", "Lizard", "Human", "Goblin", "Aristo-cat", "Dragonborn", "Tabaxi", "Troll", "Fairy", "High-Elf", "Night-Elf", "Hobbit", "Duck", "Dog-Person", "Toad", "Gnome", "Tortoise", "Rabbit", "Fox-Librarian", "Owl", "Unicorn"]
CLASS_BY_TYPE = [
    # DEX
    ["Trapper", "Con Artist", "Pirate", "Burglar of Cats", "Spy", "Juggler", "Rock Stacker", "Vegetable Pruner", "Swindler"],
    # WIS
    ["Alchemist", "Brewmaster", "Scholar", "Cobbler", "Haberdasher", "Soup’r Stoner", "Potato Shaman", "Tinkerer", "Bog witch", "Garlic witch", "Illusionist", ],
    # CON
    ["Goat-Wrangler", "Frog-Wrangler", "Duck-Wrangler", "Frog-Wrestler", "Rock-Smasher", "Onion-Cutter", "Garlic-Smasher", "Wood-Gnawer"],
    # CHA
    ["Aristocrat", "Oracle", "Charlatan", "Frog Charmer", "Diva", "Jester", "Clown"]
]

MAGIC_ABILITIES = ["Create Illusion", "Shoot Fire", "Shoot Electricity", "Waterbend", "Debilitating Insult", "Spit Acid", "Charm", "Summon Vines", "Summon Unicorn", "Floating Lightshow", "Craft Item", "Summon Insects", "Turn Invisible", "Fly"]
PHYSICAL_ABILITIES = ["Pick Lock", "Spider Climb", "Craft Item", "Flaming Arrow", "Hide in Shadows", "Disguise Self", "Make Healing Soup"]
SILLY_ABILITIES = ["Apply Lubricant"]
ALL_ABILITIES = MAGIC_ABILITIES + PHYSICAL_ABILITIES

USEFUL_ITEMS = ["Healing Potion", "Headlamp", "Carabiner", "Handcuffs", "Sword", "Longbow"]
JOKE_ITEMS = ["Shibari Rope", "Bag of Beans", "Footlong Dildo"]
PARAPHERNALIA = ["Happy Gas Tank", "Vial of Exciting Powder", "", "", "", "", "", "", "", "", "", "", "", "", "", ]
ALL_ITEMS = USEFUL_ITEMS + JOKE_ITEMS
comical_professions = ["Hippogriff Pilot", "Basilisk Makeup Artist", "Pixie Personal Shopper", "Cerberus Dog Walker", "Nymph Gardener", "Harpy Life Coach", "Gnome Home Stager", "Kelpie Waterpark Lifeguard", "Manticore Food Critic", "Yeti Ski Instructor", "Siren Voice Coach", "Dwarf Bartender", "Ogre Stand-up Comedian", "Werewolf Personal Trainer", "Griffin Air Traffic Controller", "Vampire Dentist", "Faun Piccolo Player", "Troll Bridge Toll Collector", "Pegasus Racehorse Jockey", "Cyclops Optometrist", "Frost Giant Ice Cream Vendor", "Imp Life Insurance Salesman", "Hydra Plumbing Specialist", "Sphinx Riddle Consultant", "Goblin Banker", "Mermaid Beach Lifeguard", "Centaur Horse Whisperer", "Phoenix Solar Panel Installer", "Chimera Florist", "Gorgon Fashion Photographer", "Satyr Wine Connoisseur", "Minotaur Bullfighter", "Unicorn Rainbow Painter", "Dragon Glass Blower", "Fairy Tale Editor", "Medusa Wig Maker", "Banshee Wedding Planner", "Naga Snake Charmer", "Golem Statue Restorer", "Brownie Baker", "Harpy Hair Stylist", "Kraken Seafood Chef", "Leviathan Cruise Ship Captain", "Leprechaun Goldsmith", "Mummy Archaeologist", "Orc Football Coach", "Pixie Interior Designer", "Sasquatch Foot Model", "Sylph Wind Turbine Technician", "Thunderbird Electrician", "Valkyrie HR Manager", "Will-o'-the-Wisp Candlemaker", "Yakshi Perfume Maker", "Zombie Nightclub Owner", "Amphiptere Aviary Specialist", "Basilisk Plumber", "Chimera Dentist", "Djinni Airline Pilot", "Ettin Personal Shopper", "Frost Giant Ski Resort Owner", "Gargoyle Architect", "Hippocampus Surf Instructor", "Invisible Manicurist", "Jinn Tailor", "Kobold Realtor", "Leshy Park Ranger", "Manticore Barber", "Naga Sushi Chef", "Ogre Personal Chef", "Phoenix Airplane Mechanic", "Quetzalcoatl Feather Duster", "Roc Cargo Carrier", "Siren Singer", "Troll Weightlifter", "Undine Aquarium Designer", "Vampire Nutritionist", "Werewolf Game Designer", "Xorn Geologist", "Yeti Snowplow Driver", "Zombie Makeup Artist", "Banshee Voice Actor", "Cerberus Security Guard", "Dragon Meteorologist", "Echidna Knitting Instructor", "Fairy Godmother", "Giant Ant Tamer", "Hobgoblin Estate Manager", "Imp Insurance Adjuster", "Jotunheim Winter Olympics Organizer", "Kitsune IT Support", "Leprechaun Accountant", ]
comical_items = ["Unicorn horn polish", "Dragon breath mints", "Invisible ink pen", "Fairy dust vacuum", "Goblin-sized smartphone", "Gorgon hairbrush", "Mermaid tail moisturizer", "Centaur horseshoe polish", "Phoenix fire extinguisher", "Sasquatch-sized hair gel", "Chimera pet grooming kit", "Kraken-sized rubber ducky", "Minotaur maze map", "Basilisk contact lenses", "Nymph plant identification book", "Siren earplugs", "Harpy feather duster", "Gnome garden gnome", "Kelpie water bottle", "Manticore tail comb", "Yeti snowshoes", "Dwarf mining pickaxe", "Ogre protein bars", "Werewolf silverware", "Griffin feather duster", "Vampire sunscreen", "Faun pan flute", "Troll rock climbing gear", "Pegasus flying goggles", "Cyclops eyeglass cleaner", "Frost Giant ice skates", "Imp pocket watch", "Hydra extra heads", "Sphinx riddle book", "Goblin calculator", "Medusa sunglasses", "Banshee earbuds", "Naga snake charming flute", "Golem toolkit", "Brownie cookie jar", "Harpy feather boa", "Leviathan snorkeling mask", "Leprechaun pot of gold", "Mummy sunscreen", "Orc protein powder", "Sasquatch-sized comb", "Satyr wine opener", "Thunderbird lightning rod", "Valkyrie shield", "Will-o'-the-Wisp flashlight", "Yakshi flower petals", "Zombie air freshener", "Amphiptere feather duster", "Chimera fang floss", "Djinni magic lamp charger", "Ettin two-sided toothbrush", "Frost Giant hot cocoa mix", "Gargoyle chisel", "Hippocampus snorkel", "Invisible ink eraser", "Jinn genie bottle cleaner", "Kobold measuring tape", "Leshy bird call whistle", "Manticore aftershave", "Naga sushi knife", "Ogre cookbook", "Phoenix sunscreen", "Quetzalcoatl feather duster", "Roc nest", "Siren microphone", "Troll dumbbell", "Undine fish food", "Vampire garlic spray", "Werewolf hairbrush", "Xorn diamond detector", "Yeti snowboard", "Zombie makeup remover", "Banshee karaoke machine", "Cerberus chew toy", "Dragon umbrella", "Echidna sewing kit", "Fairy wand", "Giant ant farm", "Hobgoblin tool belt", "Imp briefcase", "Jotunheim winter coat", "Kitsune fox mask", "Leprechaun lucky charm", "Mermaid treasure map"]


class CharacterSheet(object):
    dex = -1
    wis = -1
    con = -1
    cha = -1
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
            self.con = scores[2]
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
        if self.char_type == CharType.WIS or self.char_type == CharType.CHA:
            self.abilities = random.choices(MAGIC_ABILITIES, k=2) + random.choices(PHYSICAL_ABILITIES, k=1)
        else:
            self.abilities = random.choices(MAGIC_ABILITIES, k=1) + random.choices(PHYSICAL_ABILITIES, k=2)

    def __set_items(self):
        self.items = random.choices(ALL_ITEMS, k=3)

    def __set_quest(self):
        self.quest = QUEST_BY_TYPE[self.char_type]

    def __str__(self):
        return f"A {self.species} {self.class_name} on a quest to {self.quest}.  Sneakiness={self.dex} Craftiness={self.wis} Scrappiness={self.con} Fabulousness={self.cha} Abilities: {self.abilities} Items: {self.items}"
