import random

DUELS_BY_TYPE = [
    [
        "Duel of Scrappiness",
        "Two players battle to the death for the honor of becoming champion!  To emerge victorious your character must succeed on two out of three of these challenge.  For each roll, the higher number wins and you must re-roll if you tie.  A third party unbiased observer must act as DM and judge.",
        "Arm Wrestling: Each character rolls a number of dice based upon their scrappiness score.  0-9: 1 die, 10-14: 2 dice, 15-19: 3 dice, 20+: 4 dice.  ",
        "Onion Smashing: Each character must devise a strategy to use their abilities and items to smash as many onions as possible within 20 seconds.  DM decides how many dice (1-4) each player rolls based upon their strategy and any relevant skill scores.",
        "Entertaining the Goblin King: Each character must create a performance utilizing their abilities and items that will captivate and awe the great Goblin King.  DM decides how many dice (1-4) each player rolls based upon their strategy and any relevant skill scores.",
        "In a grand and impressive display, one player is victorious!  They are showered with prizes and glory.  Add +1 to each of your skills and get a prize from the machine.  The loser is hauled off to the dungeons and never heard from again.  Lose 1 life or create a new character...",
    ],
    [
        "Duel of Sneakiness",
        "Two players engage in a thrilling duel of shadows and stealth. To emerge victorious your character must succeed on two out of three of these challenge.  For each roll, the higher number wins and you must re-roll if you tie.  A third party unbiased observer must act as DM and judge.",
        "Silent Steps: Each character must navigate a complex obstacle course without making a sound. Roll a number of dice based on your Sneakiness score: 0-9: 1 die, 10-14: 2 dice, 15-19: 3 dice, 20+: 4 dice. The character with the highest total succeeds.",
        "Shadow Hideout: Players must outmaneuver each other to race cross a dimly lit chamber filled with hiding spots. Using their abilities and items, they strive to remain undetected while seeking opportunities to expose their opponent. The DM assigns a number of dice (1-4) based on strategies and relevant skill scores to determine the winner.",
        "Deception Dance: The players must showcase their mastery of deception and charm to win over the elusive Trickster Fairy. Through their performances, they aim to captivate the fairy and earn its favor. The DM assigns a number of dice (1-4) based on strategies and relevant skill scores to determine the winner.",
        "As the duel concludes, one player emerges victorious, basking in the glory of their sneaky triumph.  Add +1 to each of your skills and get a prize from the machine.  The loser is hauled off to the dungeons and never heard from again.  Lose 1 life or create a new character...",
    ],
    [
        "Duel of Craftiness",
        "Two competitors engage in a contest of wits and wisdom, where only the most cunning prevails. To emerge victorious your character must succeed on two out of three of these challenge.  For each roll, the higher number wins and you must re-roll if you tie.  A third party unbiased observer must act as DM and judge.",
        "Riddle Master: Each participant must solve a series of perplexing riddles, showcasing their intellectual prowess. Roll a number of dice based on your Craftiness score: 0-9: 1 die, 10-14: 2 dice, 15-19: 3 dice, 20+: 4 dice. The player with the highest total wins.",
        "Cook-Off: The competitors must prepare a delicious meal for the Goblin King, using their abilities and items to create a dish that will impress the king. The DM assigns a number of dice (1-4) to each player based on strategies and relevant skill scores to determine the winner.",
        "Scale the Tower: The competitors must race to the top of a tower, using their abilities and items to overcome obstacles and reach the finish line first. The DM assigns a number of dice (1-4) to each player based on strategies and relevant skill scores to determine the winner.",
        "As the duel reaches its climax, one player emerges as the crafty champion, celebrated for their superior intellect and cunning.   Add +1 to each of your skills and get a prize from the machine.  The loser is hauled off to the dungeons and never heard from again.  Lose 1 life or create a new character...",
    ],
    [
        "Duel of Fabulousness",
        "In the realm of captivating performances and dazzling charisma, two rivals vie for the title of the most enchanting.   To emerge victorious your character must succeed on two out of three of these challenge.  For each roll, the higher number wins and you must re-roll if you tie.  A third party unbiased observer must act as DM and judge.",
        "Glamour Showdown: Each contestant dazzles the audience with their charisma, charm, and alluring presence. Roll a number of dice based on your Fabulousness score: 0-9: 1 die, 10-14: 2 dice, 15-19: 3 dice, 20+: 4 dice. The player with the highest total wins over the spectators.",
        "Serenade of Hearts: The competitors must enchant the crowd with a mesmerizing musical performance, captivating listeners and igniting emotions. The DM assigns a number of dice (1-4) to each player based on strategies and relevant skill scores to determine the winner.",
        "Magical Duel: The competitors must battle each other using their magical abilities, showcasing their mastery of the arcane arts. The DM assigns a number of dice (1-4) to each player based on strategies and relevant skill scores to determine the winner.",
        "As the duel comes to a close, one player emerges as the epitome of fabulousness, showered with adoration and acclaim.  Add +1 to each of your skills and get a prize from the machine.  The loser is hauled off to the dungeons and never heard from again.  Lose 1 life or create a new character...",
    ],
]


class Encounter(object):
    title = ""
    prompt = ""
    challenge_1 = ""
    challenge_2 = ""
    challenge_3 = ""
    result = ""

    def __init__(self, type=-1):
        if type == -1:
            type = random.randint(0, 3)
        duel = DUELS_BY_TYPE[type]
        self.title = duel[0]
        self.prompt = duel[1]
        self.challenge_1 = duel[2]
        self.challenge_2 = duel[3]
        self.challenge_3 = duel[4]
        self.result = duel[5]

    def __str__(self):
        return f"{self.title}: {self.prompt}  Either: {self.option_a} OR {self.option_b} {self.pos_result} {self.neg_result}"
