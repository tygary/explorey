import random

#
# The Bat Queen: Your party stumbles upon the den of the great Trash Bat Queen, a powerful god of the underworld. At the heart of the cavern lies the slumbering giant, but behind it lie riches untold.
# To emerge victorious from this boss battle, your party must navigate through the following challenges and suceed on at least two out of three:

# 1. The Elusive Shadows: As you try to sneakily cross the cavern, you hear a scurrying of wingbeats floods as you become engulfed in a swarm of bats.  If anyone in your party has a Sneakiness score of 17 or higher, then you are able to slip through the swarm unharmed.  Otherwise, your party is clawed up and injured by the swarm.
# 2. The Queen Awakens: The Bat Queen stirs awake and starts opening her eyes.  You have one brief moment to use an ability or item to distract her before she fully awakens.  If you fail, she will attack your party with her powerful claws.
# 3. Fight or Flight: Your only chance is to scare the Bat Queen into running back into the underworld.  Use an ability or item to convince her to leave.  If you succeed, she will flee.  If you fail, she stays to guard her treasure.

# If you fail two or more of these challenges, then your party is defeated and your characters lose a life.
# If Bat Queen stayed, but you succeeded on the other two challenges, then you are able to escape with your life.
# If you succeeded on all three, then you frolic gleefully in the mountains of riches.  Increase all of your skills by +1 and get a prize.


BOSSES = [
    [
        "The Bat Queen",
        "Your party stumbles upon the den of the great Trash Bat Queen, a powerful god of the underworld. At the heart of the cavern lies the slumbering giant, but behind it lie riches untold.",
        "The Elusive Shadows: As you try to sneakily cross the cavern, you hear a scurrying of wingbeats floods as you become engulfed in a swarm of bats.  If anyone in your party has a Sneakiness score of 17 or higher, then you are able to slip through the swarm unharmed.  Otherwise, your party is clawed up and injured by the swarm.",
        "The Queen Awakens: The Bat Queen stirs awake and starts opening her eyes.  You have one brief moment to use an ability or item to distract her before she fully awakens.  If you fail, she will attack your party with her powerful claws.",
        "Fight or Flight: Your only chance is to scare the Bat Queen into running back into the underworld.  Use an ability or item to convince her to leave.  If you succeed, she will flee.  If you fail, she stays to guard her treasure.",
        "If you fail two or more of these challenges, then your party is defeated and your characters lose a life.  If Bat Queen stayed, but you succeeded on the other two challenges, then you are able to escape with your life.  If you succeeded on all three, then you frolic gleefully in the mountains of riches.  Increase all of your skills by +1 and get a prize.",
    ][
        "The Labyrinthian Minotaur",
        "Deep within the labyrinthine maze, your party encounters the fearsome Minotaur, a formidable creature with immense strength and cunning. At the heart of the maze lies a hidden treasure, guarded fiercely by the beast.",
        "The Thunderous Charge: The Minotaur charges with lightning speed, attempting to trample anyone in its path. Only those with a Scrappiness score of 15 or higher can dodge the devastating charge and avoid being knocked unconscious.",
        "Navigating the Maze: The labyrinth is filled with intricate traps and illusions designed to disorient intruders. Your party must use an ability or item to unravel the maze's secrets and find the correct path to the treasure. Failure to decipher the maze's riddles and traps may lead to being lost or falling into a deadly pit.",
        "Artifacts of Distraction: The Minotaur is known for its short attention span and susceptibility to distractions. Your party must use an ability or item to create a diversion, redirecting the Minotaur's attention away from the treasure and onto a tantalizing decoy. Failure to distract the Minotaur may result in a relentless pursuit and fierce confrontation.",
        "The outcome of the challenges determines your party's fate. Failing two or more challenges leads to defeat and the loss of a life. Succeeding in at least two challenges allows your party to escape the maze, but without the treasure. If you succeed in all three challenges, the Minotaur concedes defeat, granting you access to the treasure and enhancing your skills by +1 as a token of respect.",
    ],
    [
        "The Mischievous Imp King",
        "In the enchanted realm, your party stumbles upon the whimsical domain of the Mischievous Imp King, a diminutive but cunning ruler of the fae. Hidden within his magical abode lies a coveted artifact of immense power.",
        "Dance of Deception: The Imp King summons illusions and misdirection, attempting to confuse and confound your party. Those with a Fabulousness score of 16 or higher can resist the enchantments and see through the illusions unscathed.",
        "Trickery and Traps: The Imp King delights in setting clever traps and snares to outwit intruders. Your party must use an ability or item to counteract the Imp King's trickery and avoid falling into his cunningly crafted traps. Failure to navigate the devious traps may result in being captured or disoriented.",
        "Imaginary Foe: The Imp King has a peculiar weakness—he fears imaginary foes more than real threats. Your party must use an ability or item to conjure an illusion of a terrifying creature, convincing the Imp King to flee or cower in fear. Failure to create a convincing illusion may trigger the Imp King's mischievous retaliation or subject your party to his playful pranks.",
        "The fate of your party is determined by the challenges' outcomes. Failing two or more challenges leads to defeat and the loss of a life. Succeeding in at least two challenges allows your party to escape the Imp King's realm, albeit empty-handed. If you succeed in all three challenges, the Imp King admires your wit and cunning, granting you the artifact and bestowing a magical boon upon your party members.",
    ],
    [
        "The Dread Pirate Captain",
        "On the treacherous seas, your party comes face to face with the infamous Dread Pirate Captain, a cunning and ruthless marauder known for plundering countless ships. A legendary treasure awaits in the captain's secret hideout.",
        "Blade of Steel: The Dread Pirate Captain wields a deadly cutlass with lightning speed. Only those with a Dexterity score of 14 or higher can match the captain's skill in swordplay and avoid being disarmed or wounded.",
        "Navigating the Perilous Ship: The pirate's vessel is a maze of treacherous decks, rigged with traps and hidden dangers. Your party must use an ability or item to unravel the ship's labyrinthine layout, avoiding deadly pitfalls and finding the path to the captain's quarters. Failure to navigate the ship successfully may result in being captured or ambushed.",
        "Charismatic Parley: The Dread Pirate Captain is not easily swayed, but your party can attempt to negotiate with charm and diplomacy. Use an ability or item to engage the captain in a persuasive conversation, convincing them to surrender the treasure or strike a deal. Failure to win over the captain's trust may lead to a fierce battle or a desperate escape.",
        "The outcome of these challenges determines the fate of your party. Failing two or more challenges results in defeat and the loss of a life. Succeeding in at least two challenges allows your party to escape the pirate ship, albeit empty-handed. If you succeed in all three challenges, the Dread Pirate Captain, impressed by your skills and cunning, willingly surrenders the treasure and offers you a place among their crew.",
    ],
    [
        "The Maniacal Alchemist",
        "In a secluded laboratory, your party encounters the Maniacal Alchemist, a brilliant yet unhinged genius obsessed with concocting volatile potions. Within the laboratory lies a cache of experimental elixirs and rare ingredients.",
        "Acidic Eruption: The Alchemist hurls vials of corrosive acid with pinpoint accuracy. Only those with a Craftiness score of 16 or higher can react swiftly enough to shield themselves from the deadly projectiles and prevent severe burns.",
        "Maze of Mystery: The laboratory is a labyrinth of twisting corridors and hidden chambers, protected by intricate puzzles and traps. Your party must use an ability or item to solve the riddles, deactivate the traps, and navigate through the maze to reach the inner sanctum. Failure to unravel the secrets of the maze may result in being trapped or exposed to dangerous experiments.",
        "Mental Manipulation: The Maniacal Alchemist possesses a fragile psyche susceptible to mental manipulation. Use an ability or item to exploit their vulnerabilities and sway their actions in your favor. Failure to influence the Alchemist's mind may trigger their wrath or unleash unpredictable reactions from their volatile potions.",
        "The outcome of these challenges determines your party's destiny. Failing two or more challenges leads to defeat and the loss of a life. Succeeding in at least two challenges allows your party to escape the laboratory, but without the rare ingredients. If you succeed in all three challenges, the Maniacal Alchemist, impressed by your wits and resourcefulness, grants you access to the cache of elixirs and imparts a fraction of their alchemical knowledge.",
    ],
    [
        "The Gourmet Ogre Chef",
        "In the heart of a peculiar forest, your party stumbles upon the culinary domain of the Gourmet Ogre Chef, a fearsome creature with a refined taste for exotic delicacies. Hidden within the chef's kitchen lies a coveted recipe book filled with extraordinary culinary secrets.",
        "Culinary Combat: The Ogre Chef wields a colossal meat cleaver with exceptional skill. Only those with a Scrappiness score of 18 or higher can withstand the onslaught of powerful strikes and prevent being rendered unconscious or disarmed.",
        "Mystical Ingredients: The kitchen is an enchanting array of mystical ingredients and strange utensils. Your party must use an ability or item to identify and utilize the ingredients correctly, following the cryptic recipes and avoiding culinary disasters. Failure to handle the ingredients appropriately may result in transforming into bizarre creatures or consuming inedible concoctions.",
        "Flattery and Flambé: The Gourmet Ogre Chef can be easily swayed by flattery and appreciation of their culinary skills. Use an ability or item to engage the chef in conversation, showering them with compliments and admiration. Failure to win the chef's favor may lead to a fiery culinary duel or a swift ejection from the kitchen.",
        "The outcome of these challenges dictates your party's fate. Failing two or more challenges results in defeat and the loss of a life. Succeeding in at least two challenges allows your party to escape the kitchen, but without the coveted recipe book. If you succeed in all three challenges, the Gourmet Ogre Chef, delighted by your appreciation for fine cuisine, willingly shares the recipe book and treats your party to a sumptuous feast.",
    ],
    [
        "The Grand Illusionist",
        "In the heart of a mystical theater, your party encounters the enigmatic Grand Illusionist, a master of deception and grand spectacle. Within the theater's depths lies a secret chamber containing untold arcane artifacts.",
        "Illusory Assault: The Illusionist conjures a mesmerizing array of illusory creatures and spells to confuse and disorient intruders. Only those with a Fabulousness score of 15 or higher can discern the illusions and resist their disorienting effects.",
        "Theater of Tricks: The chamber is a stage of intricate mechanisms and concealed traps, designed to test the wit and ingenuity of adventurers. Your party must use an ability or item to unravel the theater's mechanisms, solve the puzzles, and unveil the path to the hidden artifacts. Failure to decipher the theater's secrets may result in being trapped or subjected to relentless illusions.",
        "Charm and Prestidigitation: The Grand Illusionist is drawn to the allure of captivating performances and exceptional magic. Use an ability or item to showcase your party's charm and magical prowess, entertaining the Illusionist and distracting them from guarding the artifacts. Failure to impress the Illusionist may trigger a spectacular showdown or a series of confounding illusions.",
        "The outcome of these challenges shapes your party's destiny. Failing two or more challenges leads to defeat and the loss of a life. Succeeding in at least two challenges allows your party to escape the theater, but without the arcane artifacts. If you succeed in all three challenges, the Grand Illusionist, captivated by your performances and skills, bestows the artifacts upon your party, along with a secret technique or spell as a token of respect.",
    ],
    [
        "The Mischievous Trickster",
        "In a whimsical realm, your party crosses paths with the mischievous Trickster, a prankster extraordinaire with a penchant for elaborate tricks and illusions. Hidden within their domain lies a cache of valuable trinkets and treasures.",
        "Prankster's Gauntlet: The Trickster unleashes a series of cunning and bewildering pranks upon your party. Only those with a Sneakiness score of 17 or higher can evade the pranks unscathed and avoid being humiliated or entangled in humorous mishaps.",
        "Mirror Maze: The Trickster's realm is filled with a perplexing mirror maze, distorting perceptions and disorienting adventurers. Your party must use an ability or item to navigate the maze, finding the correct path amidst the illusions and reflections. Failure to find the way may result in endless wandering or encountering more pranks.",
        "The Jester's Coin: The Trickster presents a challenge involving a magical coin that constantly changes its appearance. Your party must use an ability or item to determine the true nature of the coin, unveiling its hidden power or significance. Choosing incorrectly may trigger more pranks or a frustrating setback.",
        "The outcome of these challenges shapes your party's destiny. Failing two or more challenges leads to defeat and the loss of a life. Succeeding in at least two challenges allows your party to escape the Trickster's realm, but without the cache of treasures. If you succeed in all three challenges, the Trickster, impressed by your ability to find laughter in chaos, willingly shares the cache of treasures and leaves behind a parting prank as a memento of the encounter.",
    ],
    [
        "The Enigmatic Chessmaster",
        "Within a mysterious chamber, your party encounters the enigmatic Chessmaster, a master strategist known for their unparalleled skill in the ancient game of chess. The chamber holds a coveted artifact, hidden within a complex puzzle.",
        "Checkmate Challenge: The Chessmaster challenges your party to a game of chess, with high stakes and dire consequences. Only those with a Craftiness score of 16 or higher can match wits with the Chessmaster and avoid being outmaneuvered or trapped on the chessboard.",
        "Mystic Key: The artifact is locked away, and the key to unlock its case is hidden somewhere in the chamber. Your party must use an ability or item to uncover the secret compartment, retrieve the key, and access the artifact. Failure to find the key may result in being trapped or facing a more difficult chess game.",
        "Mind Control: The Chessmaster possesses a powerful mind control ability, capable of influencing the actions of others. Your party must use an ability or item to resist the Chessmaster's mental manipulation, maintaining control over your own decisions and ensuring a fair match. Succumbing to the mind control may lead to unfavorable chess moves or compromising positions.",
        "The outcome of these challenges shapes your party's fate. Failing two or more challenges leads to defeat and the loss of a life. Succeeding in at least two challenges allows your party to escape the chamber, but without the coveted artifact. If you succeed in all three challenges, the Chessmaster, impressed by your strategic prowess, willingly surrenders the artifact and imparts a fragment of their chess mastery to your party.",
    ],
    [
        "The Treacherous Goblin King",
        "Deep within the treacherous Goblin Kingdom, your party confronts the malevolent Goblin King, a cunning and ruthless ruler who seeks to expand his domain. The throne room is adorned with stolen treasures, guarded by his loyal goblin subjects.",
        "Goblin Challenge: The Goblin King challenges your party to a duel of cunning and agility, testing your ability to outmaneuver his crafty tactics. Only those with a Sneakiness score of 16 or higher can match the goblin king's evasiveness and avoid falling into his clever traps.",
        "Hidden Passages: The Goblin King's throne room is riddled with secret passages and concealed doorways. Your party must use an ability or item to discover the hidden paths, bypassing the goblin guards and making your way closer to the stolen treasures. Failure to find the passages may lead to ambushes or prolonged confrontations with the goblins.",
        "Charm of Goblin Friendship: The Goblin King is susceptible to a rare charm, known as the Charm of Goblin Friendship. Your party must use an ability or item to harness the charm's power and win over the loyalty of some goblin subjects. Successfully persuading the goblins may turn the tide of the battle in your favor, while failure may result in increased hostility and a tougher fight.",
        "The outcome of these challenges determines your party's fate. Failing two or more challenges leads to defeat and the loss of a life. Succeeding in at least two challenges allows your party to escape the Goblin Kingdom, but without the stolen treasures. If you succeed in all three challenges, the Goblin King, impressed by your cunning, agrees to relinquish the treasures and pledges to withdraw his forces from nearby territories.",
    ],
    [
        "The Bovine Deity: Moojesticus",
        "In a sacred pasture, your party encounters the divine presence of Moojesticus, the mighty Cow God, revered by bovines far and wide. The pasture is adorned with offerings and surrounded by mystical energy.",
        "Hoof of Grace: Moojesticus challenges your party to a test of agility and elegance. Only those with a Dexterity score of 15 or higher can match the graceful movements of the divine cows and earn the Cow God's favor. Failure to demonstrate grace may result in disapproval and divine retribution.",
        "The Sacred Bellow: Moojesticus summons forth a barrier of sound, resonating with powerful vibrations. Your party must use an ability or item to harmonize with the sacred bellow, neutralizing its effects and opening a path to the divine altar. Failure to attune to the sound may cause disorientation or physical discomfort.",
        "The Offering of Fresh Grass: To appease Moojesticus, your party must present an offering of the freshest and most succulent grass from the pasture. Use an ability or item to gather and present the grass. Failure to provide an adequate offering may provoke the Cow God's displeasure and a challenging confrontation.",
        "The outcome of these challenges determines your party's fate. Failing two or more challenges leads to disfavor and the loss of divine blessings. Succeeding in at least two challenges allows your party to earn the respect of Moojesticus and receive a divine boon. If you succeed in all three challenges, the Cow God grants you access to their divine wisdom and bestows upon your party a blessing of bountiful harvests and eternal moo-errific fortune.",
    ],
    [
        "The Elusive Sasquatch: Bigfooticus",
        "Deep within the dense forest, your party encounters the legendary Sasquatch, known as Bigfooticus, a massive and elusive creature of myth and mystery. The air is thick with an aura of primal energy as you approach the Sasquatch's domain.",
        "Stealth in the Shadows: Bigfooticus tests your party's ability to move undetected through the forest. Only those with a Sneakiness score of 16 or higher can navigate the terrain with utmost stealth, avoiding the keen senses of the Sasquatch. Failure to remain unseen may trigger a furious response from the mighty creature.",
        "Forest Survival: The Sasquatch challenges your party to prove their resourcefulness in the wilderness. You must use an ability or item to demonstrate your craftiness in gathering food, starting a fire, or constructing a makeshift shelter. Failure to showcase your survival skills may result in the Sasquatch perceiving you as a threat.",
        "The Language of the Wild: To communicate and earn the trust of Bigfooticus, your party must decipher the intricate language of the forest. Use an ability or item to understand and respond to the Sasquatch's calls, imitating the sounds of the wilderness. Failure to connect with the creature on a primal level may escalate the encounter into a fierce battle.",
        "The outcome of these challenges determines your party's fate. Failing two or more challenges may lead to the Sasquatch considering you intruders and initiating an aggressive assault. Succeeding in at least two challenges allows your party to establish a mutual understanding with Bigfooticus and gain its respect. If you succeed in all three challenges, the Sasquatch may reveal its hidden knowledge and share ancient forest secrets, granting your party protection and guidance within its domain.",
    ],
]


class Boss(object):
    title = ""
    desc = ""
    challenge_1 = ""
    challenge_2 = ""
    challenge_3 = ""
    result = ""

    def __init__(self):
        encounter = random.choice(BOSSES)
        self.title = encounter[0]
        self.desc = encounter[1]
        self.challenge_1 = encounter[2]
        self.challenge_2 = encounter[3]
        self.challenge_3 = encounter[4]
        self.result = encounter[5]

    def __str__(self):
        return (
            self.title
            + "\n"
            + self.desc
            + "\n"
            + self.challenge_1
            + "\n"
            + self.challenge_2
            + "\n"
            + self.challenge_3
            + "\n"
            + self.result
        )
