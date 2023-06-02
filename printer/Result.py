import random

ITEMS = [
    [
        "Whiffle Whistle",
        "You found an item!  A small whistle that emits a faint, melodious tune when blown",
        "Sneakiness +1",
    ],
    [
        "Tickle Gloves",
        "You found an item!  A pair of gloves that tickle anyone they touch, causing uncontrollable laughter",
        "Scrappiness +1",
    ],
    [
        "Goblin Goggles",
        "You found an item!  Goggles that allow the wearer to see through walls, but only when they have been blessed by a goblin",
        "Craftiness +1",
    ],
    [
        "Cape of Dramatic Flair",
        "You found an item!  A flowing cape that billows dramatically even in the absence of wind",
        "Fabulousness +1",
    ],
    [
        "Bag of Endless Snacks",
        "You found an item!  A small bag that always produces your favorite snack, no matter how many times it's emptied",
        "Magical Ability: Infinite Snacking",
    ],
    [
        "Socks of Stealth",
        "You found an item!  Magical socks that muffle the wearer's footsteps, making them nearly silent",
        "Sneakiness +2",
    ],
    [
        "Bouncy Boots",
        "You found an item!  A pair of boots that allow the wearer to jump higher and bounce around like a kangaroo",
        "Scrappiness +2",
    ],
    [
        "Wand of Whimsy",
        "You found an item!  A wand that can turn mundane objects into amusing and harmless creatures for a short time",
        "Craftiness +2",
    ],
    [
        "Charm Bracelet of Charm",
        "You found an item!  A bracelet that enhances the wearer's charisma, making them more persuasive and charismatic",
        "Fabulousness +2",
    ],
    [
        "Singing Sword",
        "You found an item!  A magical sword that sings catchy tunes while in combat, boosting morale and confusing enemies",
        "Magical Ability: Battle Serenade",
    ],
    [
        "Gloves of Butterfingers",
        "You found an item!  A pair of gloves that make the wearer incredibly clumsy, but also surprisingly good at juggling",
        "Sneakiness -1, Craftiness +1",
    ],
    [
        "Wand of Wackiness",
        "You found an item!  A wand that creates amusing and unpredictable magical effects when waved around",
        "Magical Ability: Random Wackiness - Roll a d6.  If you roll an even number you get +3 to the next roll.  If you roll an odd number you get -3 to the next roll.",
    ],
    [
        "Goblet of Bottomless Laughter",
        "You found an item!  A goblet that fills with laughter instead of liquid, spreading joy and amusement to those who drink from it",
        "Fabulousness +2",
    ],
    [
        "Invisible Ink Pen",
        "You found an item!  A pen that writes with invisible ink, which can only be revealed by a magical feather duster",
        "Magical Ability: Invisible Writing",
    ],
    [
        "Mirror of Ridiculous Reflections",
        "You found an item!  A mirror that distorts the reflections of those who look into it, making them appear comically exaggerated",
        "Craftiness +1, Fabulousness +1",
    ],
    [
        "Tik-Tok Timepiece",
        "You found an item!  A pocket watch that manipulates time in small increments, causing minor time loops and déjà vu moments",
        "Magical Ability: Time Manipulation - Max 5 seconds",
    ],
    [
        "Hat of Hilarity",
        "You found an item!  A hat that tells funny jokes and humorous anecdotes when worn, creating a jovial atmosphere",
        "Fabulousness +1",
    ],
    [
        "Sneaky Shoes",
        "You found an item!  A pair of shoes that muffle all sounds when the wearer is sneaking, but also emit an embarrassing squeak when walking normally",
        "Sneakiness +2, Faulousness -1",
    ],
    [
        "Portable Cloud Pillow",
        "You found an item!  A magical pillow that creates a fluffy cloud to rest on, providing comfort and relaxation anywhere",
        "Craftiness +1",
    ],
    [
        "Cape of Confusion",
        "You found an item!  A cape that shrouds the wearer in an illusion of multiple copies, making it difficult for enemies to determine the real one",
        "Magical Ability: Illusory Clones - Max 2 clones for 1 minute",
    ],
    [
        "Giggling Gauntlets",
        "You found an item!  Magical gauntlets that emit uncontrollable giggles when the wearer clenches their fists",
        "Scrappiness +1",
    ],
    [
        "Quill of Quirkiness",
        "You found an item!  A quill that writes with its own unique personality, adding witty remarks and sarcastic comments to anything written",
        "Craftiness +1",
    ],
    [
        "Cloak of the Chameleon",
        "You found an item!  A cloak that changes its color to match the surroundings, but occasionally gets stuck in an embarrassing pattern",
        "Sneakiness +1",
    ],
    [
        "Dazzling Diva Tiara",
        "You found an item!  A tiara that enhances the wearer's stage presence, making them shine brighter and captivating their audience",
        "Fabulousness +1",
    ],
    [
        "Enchanted Feather Duster",
        "You found an item!  A feather duster that reveals hidden messages and secrets when used to brush away dust",
        "Magical Ability: Dust Divination",
    ],
    [
        "Potion of Perpetual Peculiarity",
        "You found an item!  A potion that causes the drinker to experience a random comical physical transformation for a short duration",
        "Magical Ability: Comical Transformations - Roll a D6.  DM decides what you transform into based up on the number rolled.",
    ],
    [
        "Cloak of Unseen Antics",
        "You found an item!  A cloak that grants the wearer the ability to turn invisible, but also emits sporadic bursts of colorful confetti",
        "Sneakiness +2",
    ],
    [
        "Wand of Whimsical Whistling",
        "You found an item!  A wand that produces catchy tunes when waved, causing those nearby to uncontrollably tap their feet and hum along",
        "Craftiness +2",
    ],
    [
        "Goblet of Endless Nourishment",
        "You found an item!  A goblet that magically refills itself with a hearty and delicious soup, perfect for never-ending feasts",
        "Magical Ability: Infinite Soup",
    ],
    [
        "Cape of Clumsy Levitation",
        "You found an item!  A cape that allows the wearer to levitate a few feet off the ground but also makes them float in comically erratic directions",
        "Fabulousness +2, Sneakiness -1",
    ],
    [
        "Jester's Juggling Balls",
        "You found an item!  A set of colorful juggling balls that never drop when thrown, even by those with no juggling skills",
        "Scrappiness +1, Craftiness +1",
    ],
    [
        "Chatterbox Amulet",
        "You found an item!  An amulet that grants the wearer the ability to speak and understand the language of animals, but also makes them talkative and gossip-loving",
        "Magical Ability: Animal Talk",
    ],
    [
        "Orb of Unpredictable Transformation",
        "You found an item!  An orb that transforms any object touched into a random, unexpected item for a short time",
        "Magical Ability: Transformative Chaos",
    ],
    [
        "Laughing Boots",
        "You found an item!  Boots that make a distinctive giggling sound with each step, causing everyone nearby to chuckle",
        "Sneakiness +1, Fabulousness +1",
    ],
    [
        "Cane of Comical Conjuring",
        "You found an item!  A cane that, when tapped on the ground, produces amusing and harmless magical effects, like squirting water or confetti showers",
        "Craftiness +2",
    ],
    [
        "Quizzical Crystal Ball",
        "You found an item!  A crystal ball that answers questions with riddles and enigmatic messages, rather than straightforward answers",
        "Magical Ability: Riddling Divination",
    ],
    [
        "Gloves of Mischievous Manipulation",
        "You found an item!  A pair of gloves that allow the wearer to subtly influence the thoughts and actions of others, but also cause harmless pranks to occur around them",
        "Craftiness +2",
    ],
    [
        "Whistle of Wandering",
        "You found an item!  A magical whistle that, when blown, summons a playful breeze that guides you to the nearest hidden treasure",
        "Magical Ability: Treasure Tracing",
    ],
    [
        "Spoon of Spontaneous Spilling",
        "You found an item!  A spoon that magically causes the food it touches to spill and splatter uncontrollably",
        "Craftiness +1, -1 Sneakiness",
    ],
    [
        "Shrieking Shoes",
        "You found an item!  A pair of shoes that emit a loud, ear-piercing shriek with every step, making sneaking nearly impossible.  But they're so stylish!",
        "Sneakiness -2, Fabulousness +2",
    ],
    [
        "Ring of Misplaced Trinkets",
        "You found an item!  A ring that constantly causes small objects in the vicinity to disappear and reappear in unexpected places",
        "Craftiness +1, Fabulousness -1",
    ],
    [
        "Belt of Unintentional Inflation",
        "You found an item!  A belt that, when worn, causes the wearer to slowly inflate like a balloon until someone lets the air out",
        "Fabulousness +1, Scrappiness -1",
    ],
    [
        "Socks of Slipping",
        "You found an item!  But it's cursed! A pair of socks that make the wearer's feet incredibly slippery, resulting in frequent accidental falls",
        "Sneakiness -1",
    ],
    [
        "Cursed Comb",
        "You found an item!  But it's cursed! A comb that tangles hair into impossible knots and makes it resistant to any attempts at styling",
        "Fabulousness -1",
    ],
    [
        "Jar of Never-Ending Sneezes",
        "You found an item!  A jar that, when opened, releases an endless stream of comically loud and frequent sneezes",
        "Scrappiness +1, Craftiness -1",
    ],
    [
        "Ring of the Clumsy Juggler",
        "You found an item!  A ring that compels the wearer to juggle random objects whenever they feel nervous or anxious",
        "Scrappiness +1, Sneakiness -1",
    ],
    [
        "Bag of Unreliable Holding",
        "You found an item!  A bag with a tendency to randomly teleport or spit out items when least expected",
        "Anytime you want to use an item, roll a D6.  Roll a 1 - Lose that item.  Roll 2-5 - Use the item like normal.  Roll 6 - press the Prize button and you pull out that item instead.",
    ],
    [
        "Cursed Mirror",
        "You found an item!  A mirror that reflects the viewer's image with amusing distortions, making them appear silly and exaggerated",
        "Fabulousness +1",
    ],
    [
        "Chattering Chalice",
        "You found an item!  A chalice that talks incessantly, narrating everything happening around it in a comically exaggerated manner",
        "Craftiness +1, Sneakiness -1",
    ],
    [
        "Gloves of Butterfingers",
        "You found an item!  A pair of gloves that make the wearer incredibly clumsy, causing them to frequently drop and fumble objects",
        "Scrappiness -2",
    ],
    [
        "Cloak of Unintentional Invisibility",
        "You found an item!  A cloak that turns the wearer invisible, but only when nobody is looking in their direction",
        "Sneakiness +1, Fabulousness -1",
    ],
    [
        "Amulet of Awkward Encounters",
        "You found an item!  An amulet that attracts embarrassing and awkward situations, making social interactions more difficult",
        "Fabulousness -2",
    ],
    [
        "Cursed Dice",
        "You found an item!  But it's cursed!  A set of dice that always roll low numbers, making success in games of chance nearly impossible",
        "Scrappiness -1",
    ],
    [
        "Wand of Whacky Wonders",
        "You found an item!  A wand that produces wild and uncontrollable magical effects, often with unintended and chaotic consequences",
        "Roll a d6 whenever you use magic.  1-2 - It fails spectacularly. 3-4 - It works normally. 5-6 - Whacky magical effects happen in your favor.",
    ],
    [
        "Cloak of Magnetism",
        "You found an item!  But it's cursed!  A cloak that attracts random metallic objects, causing them to stick to the wearer at the most inconvenient times",
        "Sneakiness -1",
    ],
    [
        "Hat of Distracting Hats",
        "You found an item!  A hat that spawns multiple smaller hats that orbit around the wearer's head, creating a distracting spectacle",
        "Fabulousness +1",
    ],
    [
        "Goblin's Grin Mask",
        "You found an item!  A mask that permanently freezes the wearer's face into a mischievous goblin grin, making it difficult to be taken seriously in serious situations",
        "Fabulousness +1, Scrappiness -1",
    ],
    [
        "Fairy in a Bottle",
        "You found an item!  A bottle that contains a fairy that can save you from death!",
        "Add one extra life to your character.",
    ],
]


PUNISHMENTS = [
    [
        "Pure Luck",
        "You escape unharmed.",
        "You live to quest another day.",
    ],
    [
        "Pure Luck",
        "You escape unharmed.",
        "You live to quest another day.",
    ],
    [
        "Pure Luck",
        "You escape unharmed.",
        "You live to quest another day.",
    ],
    [
        "Loudspeaker Voice",
        "You are cursed!  Your voice becomes amplified to a deafening volume, causing everything they say to be heard by everyone within a mile.",
        "-2 Sneakiness",
    ],
    [
        "Game Show Voice",
        "You are cursed!  Your voice becomes permanently altered to the voice of a Game Show Host.",
        "+1 D6 to any roll when using the Game Show Voice. -1 D6 if you do not.",
    ],
    [
        "Curse of the Bumbling Blunder",
        "You are cursed!  Your future attempts at being sneaky turn into a series of clumsy and noisy mishaps.",
        "-2 Sneakiness",
    ],
    [
        "Forgetful Fingers",
        "You are cursed!  Your hands become unusually uncoordinated, resulting in a string of failed attempts at scrappy actions.",
        "-2 Scrappiness",
    ],
    [
        "Slippery Slope",
        "You are cursed!  Your sneaky maneuvers are hindered by an unfortunate tendency to slip and slide, making them prone to comedic falls.",
        "-2 Sneakiness",
    ],
    [
        "Pratfall Master",
        "You are cursed!  Your scrappy actions often result in them tripping, stumbling, and performing unintentional acrobatic feats.",
        "-2 Scrappiness, +1 Fabulousness",
    ],
    [
        "Crafting Clumsiness",
        "You are cursed!  No matter how hard the you try, your crafty creations always end up being comically off-balance or structurally unsound.",
        "-2 Craftiness",
    ],
    [
        "Mischievous Curse",
        "You are cursed!  You stumble into a cursed mushroom patch and are now afflicted with a mischievous curse. Your voice can only create silly sound effects. ",
        "Speak only with silly sound effects",
    ],
    [
        "Gravity Shuffle",
        "You are cursed!  You accidentally trigger a magical device that alters gravity in your immediate vicinity. Now, whenever you move, you experience unpredictable changes in gravity that make your movements awkward and uncoordinated.",
        "-2 Scrappiness",
    ],
    [
        "Clumsy Potion",
        "You are cursed!  While rummaging through an box, you accidentally knock over a vial labeled 'Clumsy Elixir.' As you inhale the fumes, you suddenly find yourself becoming incredibly clumsy, causing frequent mishaps and dropped items.",
        "-2 Craftiness",
    ],
    [
        "Tickle Curse",
        "You are cursed!  A mischievous sprite decides to play a prank on you by casting a tickle curse. From now on, at random intervals, you uncontrollably burst into fits of uncontrollable laughter, making it difficult to concentrate on tasks.",
        "-2 Craftiness",
    ],
    [
        "Fashion Disaster",
        "You are cursed!  You unknowingly put on a cursed garment that causes your clothing to become mismatched and outlandish. This makes it challenging to maintain a fabulous appearance and leaves others questioning your sense of style.",
        "-2 Fabulousness",
    ],
    [
        "Bewitched Shadows",
        "You are cursed!  You inadvertently stumble into an enchanted grove where your shadow takes on a life of its own. It becomes mischievous and frequently sabotages your sneaky attempts, making it difficult to remain unnoticed.",
        "-2 Sneakiness",
    ],
    [
        "Potion of Uncontrollable Giggles",
        "You are cursed!  You mistakenly ingest a potion meant for a giggling competition, causing you to burst into uncontrollable fits of giggles at inappropriate moments. This makes it difficult to maintain a serious demeanor or execute sneaky actions.",
        "-2 Sneakiness",
    ],
    [
        "Squeaky Shoes",
        "You are cursed!  As you step on an ancient trap, your shoes magically transform into squeaky toys. Your attempts at stealth now draw attention due to the constant squeaking sound they emit.",
        "-2 Sneakiness",
    ],
    [
        "Butterfly Whispers",
        "You are cursed!  An enchanted butterfly lands on your shoulder and whispers distracting and nonsensical information into your ear. Its constant chatter hampers your concentration, making it harder to execute sneaky actions.",
        "-2 Sneakiness",
    ],
    [
        "Singing Spellbook",
        "You are cursed!  While exploring a magical library, you inadvertently open a book that contains a singing spell. The spellbook now insists on serenading you at every opportunity, causing distractions and making it challenging to focus on tasks.",
        "-2 Craftiness",
    ],
    [
        "Inflated Ego",
        "You are cursed!  You stumble upon a magical artifact that temporarily inflates your ego to enormous proportions. Your arrogance hampers your ability to work well with others, leading to reduced scrappiness in team interactions.",
        "-2 Scrappiness",
    ],
    [
        "Potion of Avian Transformation",
        "You accidentally drink a potion intended for a bird, causing a sudden and complete transformation into a comical chicken.",
        "Change your species to Chicken.  Lose 1 Scrappiness.",
    ],
    [
        "Goblin's Mischievous Spell",
        "A mischievous goblin casts a spell on you, causing a bizarre magical mishap that transforms you into a whimsical and slightly clumsy gnome.",
        "Change your species to Gnome.  Lose 1 Sneakiness.",
    ],
    [
        "Curse of the Quacking Duck",
        "You are cursed by a vengeful witch, resulting in a peculiar transformation into an eccentric and quacking mallard duck.",
        "Change your species to Mallard Duck.  Quack at the start of each sentence.",
    ],
    [
        "Mystical Shapeshifting Amulet",
        "You stumble upon a mystical amulet that triggers an uncontrollable shapeshifting spell, turning you into a mischievous and tail-wagging raccoon.",
        "Change your species to Raccoon. Lose 1 Fabulousness. Gain 1 Sneakiness.",
    ],
    [
        "Wizard's Botched Experiment",
        "A wizard's experiment gone awry causes you to undergo a bizarre transformation, turning you into a slightly dim-witted yet lovable ferret.",
        "Change your species to Ferret",
    ],
    [
        "Cursed Cuckoo Clock",
        "You unknowingly wind up at a cursed cuckoo clock that emits a mysterious enchantment, causing you to transform into a tiny and melodious songbird.",
        "Change your species to Songbird.  Lose 2 Scrappiness.  Whistle a lot.",
    ],
    [
        "Bewitched Bunny Ears",
        "You don a pair of seemingly innocent bunny ears, only to discover they possess a magical enchantment that turns you into a hopping and carrot-craving rabbit.",
        "Change your species to Rabbit.  Speak like Bugs Bunny.",
    ],
    [
        "Enchanted Pixie Dust",
        "A mischievous pixie sprinkles you with enchanted pixie dust, leading to an unexpected transformation into a miniature and mischievous sprite.",
        "Change your species to Sprite.  You can now fly!  But you're tiny and easily crushed.  -3 Scrappiness.",
    ],
    [
        "Jinxed Jester's Mask",
        "You wear a jester's mask with a hidden curse, causing you to undergo a whimsical and slightly clumsy transformation into a giggling and accident-prone harlequin.",
        "Change your species to Clown.  Does everything have to be a joke to you?",
    ],
    [
        "Mystical Mermaid's Scales",
        "You come into contact with a mystical mermaid's scales, triggering a watery transformation that turns you into a merperson, complete with a fishy tail and aquatic abilities.",
        "Change your species to Merperson.  You can now breathe underwater!  But you're not very good at walking on land.  -3 Sneakiness.",
    ],
    [
        "The Sneaky Squirrel",
        "A mischievous squirrel with a penchant for shiny things steals one of your prized possessions right under your nose.",
        "You lose one item. Cross it out from your character sheet.",
    ],
    [
        "The Mysterious Portal",
        "You inadvertently step through a mysterious portal that temporarily disrupts the fabric of reality. When you emerge on the other side, one of your items has vanished into thin air.",
        "You lose one item. Cross it out from your character sheet.",
    ],
    [
        "The Misplaced Bag",
        "In a moment of distraction, you set down your bag of belongings, only to find it mysteriously disappear when you turn your back. It seems someone or something has made off with one of your items.",
        "You lose one item. Cross it out from your character sheet.",
    ],
    [
        "The Sticky Fingers Gnome",
        "A mischievous gnome with sticky fingers sneaks into your camp at night and pilfers one of your cherished items, leaving you none the wiser until morning.",
        "You lose one item. Cross it out from your character sheet.",
    ],
    [
        "The Vengeful Ghost",
        "A vengeful ghost with a fondness for pranks haunts your belongings, causing one of your items to vanish into the ethereal realm.",
        "You lose one item. Cross it out from your character sheet.",
    ],
    [
        "The Peculiar Poltergeist",
        "A mischievous poltergeist takes a liking to one of your items and plays a series of elaborate tricks, leading to its disappearance.",
        "You lose one item. Cross it out from your character sheet.",
    ],
    [
        "The Enchanted Illusion",
        "You encounter an illusionary treasure chest filled with tantalizing items. However, as you reach for one of them, the illusion dissipates, leaving you empty-handed.",
        "You lose one item. Cross it out from your character sheet.",
    ],
    [
        "The Ravenous Gremlins",
        "A group of ravenous gremlins descends upon your belongings, consuming one of your items in their insatiable appetite for random objects.",
        "You lose one item. Cross it out from your character sheet.",
    ],
    [
        "The Peculiar Portkey",
        "You accidentally activate a peculiar magical artifact, transporting one of your items to an unknown location, never to be seen again.",
        "You lose one item. Cross it out from your character sheet.",
    ],
    [
        "The Clumsy Companion",
        "A clumsy companion accidentally knocks one of your items off a ledge, causing it to plummet into an abyss below, beyond your reach.",
        "You lose one item. Cross it out from your character sheet.",
    ],
]
DEATHS = [
    [
        "Fool's Gold",
        "You stumble upon a hidden chamber filled with what appears to be an enormous treasure hoard. Excitedly, you dive into the pile of gold coins, only to realize it's an illusion. The coins are actually a pit of sharp rocks.",
        "You have died.  Lose 1 life or make a new character...",
    ],
    [
        "Raging Munchkins",
        "You come across a seemingly harmless group of adorable munchkins. Unbeknownst to you, they are notorious for their fierce territorial nature. They attack with unexpected ferocity, overwhelming you and ultimately causing your demise.",
        "You have died.  Lose 1 life or make a new character...",
    ],
    [
        "Cursed Mirror Maze",
        "You find yourself trapped in a mirror maze, enchanted with a deadly curse. The mirrors distort reality and disorient you, making it impossible to find your way out. As time passes, you succumb to starvation and exhaustion.",
        "You have died.  Lose 1 life or make a new character...",
    ],
    [
        "The Bottomless Pit",
        "In the depths of a dark cavern, you accidentally step onto an illusory surface, plunging into a seemingly endless pit. Despite your best efforts, you fall to your demise, unable to escape the gaping void.",
        "You have died.  Lose 1 life or make a new character...",
    ],
    [
        "Summoned Abyssal Beast",
        "While investigating an ancient artifact, you unknowingly trigger a summoning spell. From the depths of the underworld, a massive and terrifying abyssal beast materializes. It swallos you whole.",
        "You have died.  Lose 1 life or make a new character...",
    ],
    [
        "The Mimic's Grasp",
        "You encounter what appears to be a treasure chest filled with riches. Unfortunately, it's a cleverly disguised mimic that clamps its jaws around you, draining your life force until your body succumbs to the relentless assault.",
        "You have died.  Lose 1 life or make a new character...",
    ],
    [
        "With the Herd",
        "You run away from the party and get lost in the woods.  You stumble upon a quaint cow farm.  You decide to stay and live with the cows.  You are now a cow.",
        "You have lost the adventuring spirit.  Lose 1 life or make a new character...",
    ],
    [
        "Slippery Banana Peel",
        "You step on a discarded banana peel, causing you to lose your balance and tumble into an unfortunate chain of events that ultimately leads to your demise.",
        "You have died.  Lose 1 life or make a new character...",
    ],
    [
        "Potion Mishap",
        "In an attempt to drink a healing potion, you accidentally grab a potion labeled 'Inflation Elixir.' The result is catastrophic as you rapidly expand in size until you explode with a loud 'pop,' leaving nothing but a cloud of smoke behind.",
        "You have died.  Lose 1 life or make a new character...",
    ],
    [
        "Singing Siren's Song",
        "You encounter a mesmerizing siren whose enchanting voice compels you to follow her melodic song. You blissfully wander off a cliff, lost in a trance, and meet a rather melodramatic end.",
        "You have died.  Lose 1 life or make a new character...",
    ],
    [
        "Doomed by Quackery",
        "You fall prey to a seemingly innocent group of quacking ducks. What you don't realize is that they are actually highly trained assassins in disguise. Their synchronized attacks overwhelm you, leading to an unexpected and bizarre demise.",
        "You have died.  Lose 1 life or make a new character...",
    ],
    [
        "Tangled by Enchanted Yarn",
        "You unwittingly disturb a magical ball of yarn that ensnares you in its endless loops. Despite your best efforts to escape, the more you struggle, the more entangled you become until you're wrapped from head to toe and meet an unfortunate end.",
        "You have died.  Lose 1 life or make a new character...",
    ],
    [
        "Inexplicable Chicken Stampede",
        "You unwittingly stumble upon a hidden chicken sanctuary and accidentally disrupt their peaceful gathering. The startled chickens go into a frenzy, creating a chaotic stampede that overtakes you and leads to an undignified demise.",
        "You have died.  Lose 1 life or make a new character...",
    ],
    [
        "Foolish Fortune Teller",
        "You seek guidance from a mysterious fortune teller who proclaims that your destiny lies in a life of mundane tasks like sorting socks and baking pies. The prediction resonates with you, and you find yourself abandoning the adventuring life to pursue domestic bliss.",
        "You have lost the adventuring spirit. Lose 1 life or make a new character...",
    ],
    [
        "Permanently Polymorphed",
        "During your side-quest, a spell goes awry and you find yourself permanently transformed into a creature completely unsuited for adventuring, like a humble garden gnome or a tiny tree squirrel. Unable to continue your heroic journey, you resign yourself to a new life.",
        "You have lost the adventuring spirit. Lose 1 life or make a new character...",
    ],
    [
        "Absurdly Cursed Treasure",
        "You stumble upon a legendary treasure chest rumored to grant immense power. However, as you open it, you find nothing but a note that reads, 'Congratulations! You've won the Curse of Extreme Mundanity.' From that moment on, you find yourself utterly unremarkable, losing all motivation for adventuring.",
        "You have lost the adventuring spirit. Lose 1 life or make a new character...",
    ],
    [
        "The Inexplicable Lure of Puns",
        "You encounter a jovial bard whose every word is a pun. Despite your best efforts, you find yourself completely enamored with their wordplay, spending hours engaged in pun-filled conversations. Eventually, you realize that your passion for adventuring has been replaced by an insatiable thirst for clever wordplay.",
        "You have lost the adventuring spirit. Lose 1 life or make a new character...",
    ],
    [
        "Permanent Dancing Curse",
        "You inadvertently trigger a trap that casts a permanent dancing enchantment upon you. No matter what you do, you find yourself compelled to dance incessantly, making adventuring a rather impractical pursuit. You bid farewell to the life of a hero and embrace a new rhythm.",
        "You have lost the adventuring spirit. Lose 1 life or make a new character... Or go dance it off.",
    ],
    [
        "Obsessed with Collecting Marbles",
        "You come across an enigmatic merchant who offers you an exquisite marble. Once you accept, an inexplicable obsession with collecting marbles consumes your every waking moment. You abandon your adventuring ambitions to become the world's greatest marble enthusiast.",
        "You have lost the adventuring spirit. Lose 1 life or make a new character...",
    ],
]


class Result(object):
    title = ""
    description = ""
    effect = ""

    def __init__(
        self,
        success=True,
    ):
        if success:
            result = random.choice(ITEMS)
            self.title = result[0]
            self.description = result[1]
            self.effect = result[2]
        else:
            if random.random() < 0.2:
                result = random.choice(DEATHS)
                self.title = result[0]
                self.description = result[1]
                self.effect = result[2]
            else:
                result = random.choice(PUNISHMENTS)
                self.title = result[0]
                self.description = result[1]
                self.effect = result[2]
