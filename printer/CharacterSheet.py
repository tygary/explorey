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
    "Go to the dance floor and show your moves.",
    "Go caroling somewhere else in the party.  Make up new words to a popular song and change the meaning.",
    "You must undertake a cold plunge. You may enter a warm chamber first, but then must plunge. It will be cold.",
    "Wrap some part of your body in giftwrap. Find someone to open it and sing to them while they unwrap you."
    # "Go pick as many blackberries as you can.  Prove to everyone that you are the ultimate scavenger. Hiss at anyone else picking blackberries.",
    # "Float your way to the bar.  Order a specialty cocktail from the secret menu.  Tell them it's your birthday.  ",
    # "Find the fastest vessel on the lake.  Commandeer it, and then challenge the ducks to a race.  Winner gets the worm.",
    # "Go to the DJ and ask if you can sing a karaoke song.  When they tell you no (because you know they will) do it anyways."
   #  "First Digit: I fly through the night with leathery wings.  What am I? Next Location: While journeying east, with music behind.  In a fork with a bust, near BIFF you will find.",
   # "First Clue:  Meow! Is it a cat?  How many lives does a cat have?  Next Location: Where fortunes get told and veggies grow old, a garden fence will lead to just what you need.",
   # "Next Location: When searching for food, a story you hear. If you see the brick wall your next clue is near.  First Clue: First line count to 3 or 8.  Second line count to 4 or 7.  Third line count to 3 or 4.  Fourth line count to 13 or 16",
   # "First Clue: What does a goblin call an onion? _ _ _ _ _  Next Location: A sextuple of sides, near a labryinth reside, the worshipers of hex will hold what's next.",
]

TURBULENT_QUESTS_BY_TYPE = [
    #  [
    #     "Stealthily replace a town's public holiday decorations with outrageous pornographic ones overnight.",
    #     "Secretly reprogram holiday robots at a toy factory to cause a comical yet chaotic toy uprising.",
    #     "Sneak into a high-security vault to steal a legendary snow crystal rumored to control winter itself.",
    #     "Conspire with ice sprites to freeze over a famous landmark, claiming it as your own winter palace.",
    #     "Replace a city's entire supply of hot chocolate with a potion that temporarily makes them speak like goblin chipmunks.",
    #     "Cast an illusion spell over a town, making everyone believe they're in a winter fairy tale, meanwhile you plunder.",
    #     "Sneak into the lair of the Ice Witch to borrow (without asking) her wand of endless frost.",
    #     "Secretly replace all holiday music in a city with your own hypnotic tunes to control the masses.",
    #     "Orchestrate a grand heist to steal Santa's sleigh and take it for a joyride across the globe.",
    #     "Construct an enormous ice castle in the middle of a city overnight, declaring yourself the Frost Monarch.",
    #     "Host an extravagant masquerade ball for all the mythical creatures of winter lore, becoming the host of legends.",
    #     "Invent a ludicrously overpowered snow cannon, capable of creating instant winter wonderlands anywhere.",
    #     "Challenge the Aurora Borealis to a color contest, using magical lights to outshine the natural phenomenon.",
    #     "Build a secret underground city made entirely of ice, complete with frozen waterways and glowing ice sculptures.",
    #     "Set up a secret base at the North Pole, claiming to be a long-lost winter deity and starting your own holiday.",
    #     "Brew an incredibly potent elixir that grants temporary holiday-themed superpowers to those who dare to drink it."
    # ],
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
        "Write a novel about a sentient pinecone",
        "Develop a secret society for people who love fancy creepy holidays all year round",
        "Perform a forbidden ritual to transform themself into an immortal being of pure generosity"
        "Create a potion that turns anything it touches red and green",
        "Craft a magical amulet that attracts forgotten socks and causes them to reappear in inconvenient places",
        "Conjure illusions of a mischievous doll that follows people around and play harmless pranks on them",
    ],
    [
        "To become the yeti lord",
        "Break a world record for the most yetis fit in a phone booth",
        "Out-drink a group of yetis and win their respect",
        "Set the world record for most snowballs thrown in 5 minutes",
        "Build a castle in the mountains and become the king of the frost squirrels",
        "Build a castle in the sand and act like a crab for the rest of your days",
        "Become an onion pirate and sail the seas in search of the legendary 'Onion of Golden Wonder'",
        "Get so good at Shibari that you can unravel string theory",
        "Win a bareknuckle brawl against a goblin sheriff without spilling your drink",
        "Punch a tumbleweed so hard it turns into a perfectly usable wagon wheel",
        "Wrestle a wild enchanted bull and ride it straight into a town festival without getting thrown once",
        "Survive an entire outlaw siege armed only with a frying pan and a lot of stubbornness",
        "Drag an entire broken-down stagecoach across the desert just to make it to poker night",
        "Challenge a sand elemental to a wrestling match — and pin it in three moves",
        "Hold your ground against a gang of bandit wizards during a magical dust storm",
        "Survive being buried alive in a collapsed mine and dig yourself out using only your bare hands and spite",
        "Become a legend by winning 100 bar fights — and buying a round of drinks after each one",
        "Break a cursed ghost horse's saddle streak by riding it through the Badlands under a blood moon",
    ],
    [
        "Seduce a royal penguin with your charm",
        "Become the ruler of a kingdom solely through the power of your charisma and fabulousness",
        "Become a world renowned DJ that only plays the Top 100 hits",
        "Become so incredibly impressive that everyone grovels at your feet",
        "Capture the heart of the abominable snowman and become the first person to marry one",
        "Befriend a unicorn and train it to be your personal steed",
        "Grow a polycule so large that you can throw a festival with only your metamores",
        "Taste every flavor in the world and decide once and for all which flavor is the best",
    ],
]
TIDY_QUESTS_BY_TYPE = [
    [
        "To become the nimblest gift wrapper in the town",
        "Perform an incredibly complex heist involing a giant onion, a frozen chicken, and a pair of socks",
        "Become a skilled tightrope walker and walk across the mystical 'Bridge of Icy Doom'",
        "Join a traveling circus and become the world's greatest sad clown on stilts",
        "Create a new form of dubstep dance that surpasses all known forms of dance",
        "Become the world's greatest escape artist and escape from a straightjacket while being chased by a bugbear",
        "Learn how to balance a spoon on my nose for 30 seconds while standing on one foot and singing Enya",
        "Successfully juggle flaming torches while riding a unicycle across a pit of lava",
        "Steal the sheriff’s badge without them noticing — and leave behind a fancier replacement",
        "Sneak into a goblin bandit camp just to replace all their wanted posters with flattering portraits",
        "Win a horse race by secretly swapping every other rider’s saddle for whoopee cushions",
        "Pickpocket a rattlesnake’s rattler and live to tell the tale",
        "Slip into the governor’s mansion during a fancy ball and switch all the hors d'oeuvres with beans on toast",
        "Sneak across a desert battlefield wearing nothing but a barrel and a winning smile",
        "Replace a notorious outlaw’s bullets with jellybeans without getting caught",
        "Leave a trail of fake gold nuggets across the prairie to lead a gang of greedy goblins straight into a cactus patch",
        "Sneak into a wizard’s tower during a sandstorm just to swap his magic staff with a giant spaghetti noodle",
        "Convince a group of bounty hunters that you’re actually a famous tumbleweed salesman",
    ],
    [
        "To study the interdimensional planes to discover how to take drugs that enhance the effects of other drugs that enhance the effects of other drugs",
        "Become the greatest bonsai tree artist in the world by creating a bonsai tree that looks like a sinister ice castle",
        "Design a hat that doubles as a birdhouse so that birds can live on my head",
        "Invent a new language using only animal sounds so that you can finally ask what your pet cat is thinking",
        "Create a machine that can turn water into coffee so that you can find existential peace",
        "Create a new kind of snow cone that tastes like pizza and helps relax your social anxiety",
        "Build a robot that can do all my chores for me so that I can spend more time playing video games",
        "Become the world's first professional rock, paper, scissors player.  Winning a sponsorship from OfficeMax",
        "Write a self-help book for talking to animals and become a world-renowned animal whisperer",
        "Invent a hat that predicts the weather based on the mood of nearby birds",
        "Master the lost art of brewing tea so calming it puts angry ghosts to sleep",
        "Discover how to grow a cactus that blooms into functional furniture",
        "Build an entire moving castle powered solely by awkward silences",
        "Design a map that shows not where treasure is buried — but where people lost their car keys",
        "Write the definitive cookbook for edible magical spells (with optional vegan versions)",
        "Invent a mirror that gives brutally honest advice instead of reflections",
        "Create a library where every book rearranges itself to match your mood",
        "Become the first person to teach owls how to knit tiny sweaters for charity",
        "Develop a method to turn awkward small talk into a renewable energy source",
    ],
    [
        "Become the world's greatest thumb wrestler and win the title of 'Thumb Wrestling Champion'",
        "Win a gladatorial battle against a giant yeti without using any weapons",
        "Survive a round in a boxing match with a kangaroo without getting knocked out",
        "Climb Mount Everest using only a paper clip and dental floss to prove that you can",
        "Become a champion arm wrestler and win the title of 'Arm Wrestling King'",
        "Prove your high school bully wrong by conquering the world and becoming the supreme ruler of all",
        "Live a simple life of cutting onions and crushing your enemies",
        "Save the world from a giant meteor by punching it into a million pieces",
        "Win a county pie-eating contest without getting a single stain on your shirt",
        "Survive a barroom brawl and straighten your vest before anyone notices you were in a fight",
    ],
    # [
    #     "To capture the icy heart of the frosty yeti with enchanted melodies and bass beats",
    #     "Become the most renowned and beloved frost minstrel in the frozen wilderness, celebrated for epic tales of snowbound adventure and heroism",
    #     "Host a legendary winter celebration that echoes through the ice caverns for years, leaving everyone with frosty memories they can't quite recall",
    #     "Compose and perform a hit snow ballad that becomes a classic, echoing through every frost-kissed tavern in the land",
    #     "To uncover the ancient incantation that will transform you into a frosty unicorn, roaming the snowy plains with a magical horn",
    #     "Become the realm's supreme Frost DJ, spinning beats that resonate through glaciers and win the title of 'Chill Master'",
    #     "Consume a magical elixir and become the world's greatest frost wizard, wielding the power of ice and snow",
    #     "Summon an ice spirit to become your new frosty companion and explore the wintry realms together",
    # ]

    [
        "To capture the heart of the common participant with lasers and bass music",
        "Become the most famous and beloved bard in the land, known for my epic tales of adventure and heroism",
        "Host a legendary party that everyone talks about for years, but no one can remember what exactly happened",
        "Write and perform a hit song that becomes a classic and is played at every tavern in the land",
        "To find the magical spell that will transform you into a unicorn",
        "Become the world's greatest DJ and win the title of 'DJ Supreme'",
        "Boof a magical potion and become the world's greatest wizard",
        "Summon a demon to become your new best friend",
        "Talk your way out of being eaten by a kraken (and get its autograph)",
        "Start a cult that's really just a book club with better snacks",
        "Earn a magical title like 'Grand Magnificent Herald of Wonder' that people actually use seriously",
            "Tour the world giving motivational speeches to dragons, pirates, and ghosts",
            "Get your face carved into a mountain",
            "Become the most celebrated storyteller in all known kingdoms",
"Win a sharpshooting contest against a goblin riding a giant chicken"
"Tame a legendary wild mustang that leaves a trail of sparkles behind it",
"Become the first person to ride a sand dragon across the open desert (and survive)",
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
    # "Icy Human",
    # "Glacial Fairy",
    # "Snow Dwarf",
    # "Arctic Pixie",
    # "Reindeer",
    # "Frosty Dark Elf",
    # "Mirth Elemental",
    # "Frostwood Mutant Raccoon",
    # "Frost Hobbit",
    # "Snow Halfling",
    # "Frost Gnome",
    # "Coldwater Merfolk",
    # "Regular Vampire",
    # "Arctic Fox-Librarian",
    # "Glacier Unicorn",
    # "Frost Pegasus",
    # "Icicle Aristocat",
    # "Nocturnal Party Cat",
    # "Ice Giant",
# ]

BEAST_SPECIES = [
    "Poltergeist",
    "Gargoyle",
    "Imp",
    "Goblin",
    "Lizard",
    "Bovine",
    "Tabaxi",
    "House Cat",
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
    # "Animated Snow Ball",
    # "Frost Gargoyle",
    # "Chill Imp",
    # "Frost Goblin",
    # "Ten Lizards in a Trenchcoat",
    # "Frost Rat King",
    # "Sexy Leopard Person feeling cold",
    # "Gargantuan House Cat",
    # "Chimney Mimic",
    # "Frost Minotaur",
    # "Glacial Werewolf",
    # "Christmas Elemental",
    # "Coal Toad",
    # "Gingerbread Person",
    # "Baby Krampus",
    # "Arctic Owl",
    # "Enchanted Nutcracker",
    # "Glacier Centaur",
    # "Coniferous Ent",
    # "Hoar-front Yeti Person",
    # "Snow Yeti",
    # "Basic Banshee",
    # "Frost Manticore",



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
        "Emotion Surgeon",
        "Swindler",
        "Pickpocket",
        "Acrobat",
        "Team Mascot",
        "Sushi Chef",
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
        # "Holiday Inventor",
        "Bureaucrat",
        "Union Organizer",
        "Knife Sharpener",
        "Warlord",
        "Villain",
        "Mob Boss",
        # "System Architect",
        # "Landscape Architect",
        # "Winter Druid",
        # "Explorey Monk",
        # "Riddle Paladin",
        "Brainwasher",
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
        # "Wilderness Survival Instructor",
        "Meathead",
        "Duck Masseus",
        # "Frost Wrestler",
        "Exterminator",
        "Onion Barista",
        "Garlic-Smasher",
        "Wood-Gnawer",
        "Eco Terrorist",
        "Snorkeler",
        "Palace Guard",
        "Yeti Brawler",
        "Dark Cultist",
        "Personal Shopper",
        "Competitive Eater",
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
        # "Ice Queen",
        "Accordion Player",
        "Mid-Level Manager",
        "Cat  Charmer",
        # "Xmas Trap Producer",
        # "Reindeer Trainer",
        # "Snow Dancer",
        # "Sleigh Master",
        "Dance Soldier",
        "Conceptual Artist",
        "Snack Enchanter",
        "Candy Warlock",
        "Sparkle Pony",
        "Interior Decorator",
        "Cultural Icon",
        "Cultural Critic",
        # "Soothsay",
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
    "Freeze Item",
    "Melt Ice",
    # "Disappear",
    # "Ice Wall",
    # "Peppermint Ray",
    # "Holiday Parade",
    # "Snowstorm Surge",
    # "Yuletide Charm",
    # "Icicle Dagger",
    # "Summon Energy Wolves",
    "Charm Beast",
    # "Snow Camouflage",
    "Invisibility",
    # "Good Good Cookin'",
    # "Uproarious Laughter",
    # "Conjure Toy Army",
    # "Temporary Invincible",
    # "Poisoned Kiss",
    "Teleporting Nose",
    "Adhesive Skin",
    "Turn into Rock",
    # "Hack Computers",
    "Heal Wounds",
    "Resurrect",
    "Excellent Lying",
    # "Summon Ice Witches",
    "Shoot Fireworks",
    # "Answer Riddles"
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
    # "Red Glowing Nose",
    "See Around Corners",
    "Double Jump",
    "Craft Item",
    "Hotdog Fingers",
    "Retractable Hair",
    "Chug Drinks",
    "Prune Trees",
    "Become Very Heavy",
    "Talk to Animals",
    "Prepare Feast",
    "Great Throws",
    # "One-Touch Kill",
    "Badass Jumpkick",
    "Resist Frost",
    "Resist Cold"
]
# SILLY_ABILITIES = [
#     # "Pro Gift Wrapper",
#     # "Build Snowman",
#     "Balance Rocks",
#     # "Decorate Tree",
#     # "Untangle Strand",
#     # "Ice Cookies",
#     # "Caroling",
#     # "Use Packing Tape",
#     # "Hang Mistletoe",
#     "Smoke Hella Weed",
#     "Knit Ugly Sweater",
#     "Mimic Reindeer",
#     "Calligraphy",
#     "Guess Favorite Movie",
#     "Guess Zodiac Sign",
#     "Dodge Snowball",
#     "Ok Snowboarding",
#     "Ski Black Diamond"
# ]

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
    "Make a Perfect Omelette",
    "Summon a Single Pigeon"
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
    "Animal Charm",
    "Tuba",
    "Axe",
    "Birdhouse",
    "Postcard from Mom",
    "Map of Labyrinth",
    "Fresh Fish",
    "Dried Fish",
    "Wrapped Gift",
    "Gingerbread Cookies",
    "Book of Riddles",
    "Parachute",
    "Loaded Gun",
    "Adorable Kitten",
    "Enchanted Spellbook",
    "Cute Cake",
    "Magic Snowglobe",
    "Rope",
    "Loaded Dice",
    "Drugs for Birds",
    "Small Bomb",
    "Flamethrower",
    "Kerosene",
    "Poisoned Cookie",
    "Poisoned Fish",
    "Crampons",
    # "Seal of the Ice King",
    "Healing Potion",
    "Bottle of Fine Scotch",
    "Flagard of Gin",
    "Grappling Hook",
    "Invisibility Cloak",
    "Emergency Blanket",
    # "Pyramids of Giza",
    # "Dragon in a Bottle",
    # "A Nobel Prize",
    "Beast Repellent",
    # "Job Offer from Google",
    "Magic Carpet",
    "Genius Talking Fish",
    # "Total Darkness",
    # "Merriment",
    "Baseball Bat",
    # "Rocket Launcher",
    # "GPS Tracker",
    # "Bag of Children",
    # "Lightsaber",
    # "Gravity Gloves",
    # "Freezeray Gun",
    # "Ghostbusters Trap",
    "Headlamp",
    "Smoke bomb",
    "Sleeping bag",
    "Winged boots",
    "Charm amulet",
    # "Sonic whistle",
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
    # "String Lights",
    # "Singing Fruitcake",
    # "Snowman-shaped Soap",
    # "Gingerbread House",
    # "Santa Costume",
    # "Costume Boots",
    # "Jingle Bells",
    "Frisbee",
    # "Candy Cane Toothpaste",
    "Ugly Sweater",
    # "Leaking Snow Globe",
    # "Evergreen Air Freshener",
    # "Eggnog",
    "Rat in a Cage",
    "Captive Goblin",
    "Confetti Cannon",
    "Karaoke Machine",
    "Vibrator",
    # "Reindeer Antler",
    "Sack of Onions",
    # "Lump of Coal",
    # "Laptop",
    # "Yule Log",
    # "Cuddle Dome",
    # "Chimney",
    # "Christmas Presents"
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
SPACES_PER_ROW = 72
CHAR_TO_SPACE_RATIO = SPACES_PER_ROW / CHARS_PER_ROW
CHARS_PER_SECTION = CHARS_PER_ROW * 7
CHARS_SHORTER = CHARS_PER_ROW * 3

def buffer_str(str, des_length=CHARS_PER_SECTION):
    length = len(str)
    if length < des_length:
        additional_spaces = math.ceil(
            (des_length - length) * CHAR_TO_SPACE_RATIO
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
    lives = 1

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

        if self.species in ["House Cat", "Tabaxi", "Aristo-cat"]:
            self.lives = 9

    def __set_class_name(self):
        self.class_name = random.choice(CLASS_BY_TYPE[self.char_type])

    def __set_abilities(self):
        self.abilities = random.sample(ALL_ABILITIES, 3)
        # if self.char_type == CharType.WIS or self.char_type == CharType.CHA:
        #     self.abilities = random.choices(MAGIC_ABILITIES, k=2) + random.choices(
        #         PHYSICAL_ABILITIES, k=1
        #     )
        # else:
        #     self.abilities = random.choices(MAGIC_ABILITIES, k=1) + random.choices(
        #         PHYSICAL_ABILITIES, k=2
        #     )

    def __set_items(self):
        self.items = random.sample(ALL_ITEMS, 3)

    def __set_quest(self, levers=None):
        # levers[3] - 0 is Turbulent, 1 is Tidy
        if levers is not None:
            if levers[2] is 0:
                self.quest = random.choice(TURBULENT_QUESTS_BY_TYPE)
            else:
                self.quest = random.choice(TIDY_QUESTS_BY_TYPE)
        else:
            self.quest = random.choice(QUEST_BY_TYPE[self.char_type])
        self.quest = buffer_str(self.quest, CHARS_SHORTER)

    def __str__(self):
        return f"A {self.species} {self.class_name} on a quest to {self.quest}.  Sneakiness={self.dex} Craftiness={self.wis} Scrappiness={self.con} Fabulousness={self.cha} Abilities: {self.abilities} Items: {self.items}"



for i in range(20):
    # levers = [random.randint(0, 1) for _ in range(4)]
    # print(levers)
    # char = CharacterSheet(levers=levers)
    char = CharacterSheet()
    print(char)
    print()