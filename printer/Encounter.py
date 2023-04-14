import time
from enum import IntEnum
import random

ENCOUNTERS = [
    [
        "The Drunken Innkeeper",
        "Your hero stops at an inn for the night and meets the rather drunken innkeeper. The innkeeper starts making judgey comments about your heroes' outfit.",
        "Have a Fabulousness score higher than 13",
        "Use an ability or item that can diffuse the situation without injuring the innkeeper.",
        "If you succeed in one of those, then you are able to diffuse the situation and book your room for the night.",
        "Otherwise, you get too upset at that innkeeper and punch them in the face. The town sheriff sees this and arrests you. You fail the encounter and spend the night in jail.",
    ],
    [
        "The Slippery Bridge",
        "Your party comes across a rickety old bridge over a deep ravine. The bridge looks dangerous to cross.",
        "Have a Sneakiness score higher than 11",
        "Use an ability or item to help you maintain balance while crossing the bridge.",
        "If you succeed, you make it across the bridge without incident and continue on your journey.",
        "Otherwise, you lose your footing and fall into the ravine below. You take significant damage and your party must use healing resources to revive you before continuing on your journey.  If you have no healing resources then you die.",
    ],
    [
        "The Mischievous Imp",
        "Your party enters a dark and creepy cave. Suddenly, you hear giggling and the sound of something running away. An imp appears and begins playing pranks on your party.",
        "Have a Craftiness score higher than 8",
        "Use an ability to outsmart the imp and catch it.",
        "If you succeed, you catch the imp and are able to continue on your journey without further incident.",
        "Otherwise, the imp continues to play pranks on your party, distracting and delaying you. Your party loses valuable time and resources as a result.",
    ],
    [
        "The Bridge Troll",
        "Your party comes upon a rickety bridge guarded by a troll. The troll demands a toll to cross.",
        "Pay the toll or have a Fabulousness score higher than 10 to talk your way across.",
        "Use an ability or item to trick or distract the troll.",
        "If you succeed in one of those, then you are able to cross the bridge.",
        "Otherwise, the troll attacks your party. You fail the encounter and must fight the troll.  The troll eats your pet salamander.",
    ],
    [
        "The Enchanted Forest",
        "Your party enters a beautiful and lush forest, but you quickly realize something is amiss. The trees seem to be moving and shifting around you, and you hear whispers in the wind.",
        "Have a Fabulousness score higher than 14 to understand the magical nature of the forest.",
        "Use an ability or item to navigate the enchanted forest.",
        "If you succeed in one of those, then you are able to safely navigate the forest.",
        "Otherwise, your party becomes lost and disoriented in the forest. You fail the encounter and must find your way out before nightfall.",
    ],
    [
        "The Locked Chest",
        "Your party comes across a locked chest on the side of the road. There is no sign of the owner.",
        "Have a Scrappiness score higher than 12 to break it open.",
        "Use an ability or item to pick the lock.",
        "If you succeed, the chest opens revealing some treasure.",
        "Otherwise, you can't pick the lock and must move on.",
    ],
    [
        "The Haunted House",
        "Your party comes across a seemingly abandoned house with strange noises coming from inside.",
        "Have a Scrappiness score higher than 14 to force the door open.",
        "Use an ability or item to break down the door.",
        "If you succeed, you enter the house and can investigate.",
        "Otherwise, you can't break down the door and must move on.",
    ],
    [
        "The Lost Key",
        "Your party arrives at a mysterious dungeon and finds the door locked. A nearby note says 'The key is lost in the nearby woods'.",
        "Have a Fabulousness score higher than 10 to find the key.",
        "Use an ability or item to pick the lock",
        "If you succeed, you find the key and unlock the door to continue your adventure.",
        "Otherwise, you are unable to find the key and must turn back. You fail the encounter and lose valuable time.",
    ],
    [
        "The Poisoned Water",
        "Your party reaches a river blocking your path. The water is poisonous and will damage anyone who tries to cross.",
        "Have a Scrappiness score higher than 7",
        "Use an ability or item to purify the water",
        "If you succeed, you successfully purify the water and can cross without taking damage.",
        "Otherwise, you take damage from the poisonous water and lose valuable time. You fail the encounter and must find another way around.",
    ],
    [
        "The Trapped Chest",
        "Your party discovers a treasure chest sitting alone in a room. But as you approach it, you notice a tripwire on the ground.",
        "Have a Scrappiness score higher than 12",
        "Use an ability or item to disarm the trap",
        "If you succeed, you safely disarm the trap and open the chest to discover its treasures.",
        "Otherwise, you trigger the trap and take damage from the explosion. You fail the encounter and lose valuable time.",
    ],
    [
        "The Charlatan",
        "Your party comes across a charismatic salesman who is selling potions that promise incredible results.",
        "Have a Fabulousness score higher than 11",
        "Use an ability or item to identify the authenticity of the potions",
        "If you succeed, you realize the potions are fake and avoid wasting your gold.",
        "Otherwise, you purchase the fake potions and suffer negative effects. You fail the encounter and lose valuable gold.",
    ],
    [
        "The Haunted Mansion",
        "Your party stumbles upon an abandoned mansion with a dark history. As you enter, the doors shut behind you and the lights flicker.",
        "Have a Craftiness score higher than 9",
        "Use an ability or item to dispel the ghosts haunting the mansion",
        "If you succeed, you dispel the ghosts and can continue exploring the mansion.",
        "Otherwise, the ghosts attack your party and you must flee the mansion. You fail the encounter and lose valuable time.",
    ],
    [
        "The Bridge Troll",
        "Your party reaches a bridge guarded by a troll who demands a toll for crossing.",
        "Have a Fabulousness score higher than 8",
        "Use an ability or item to persuade the troll to let you pass for free",
        "If you succeed, the troll is convinced and you can cross the bridge without paying the toll.",
        "Otherwise, you must pay the toll or fight the troll. You fail the encounter and lose your gold.",
    ],
    [
        "The Labyrinth",
        "Your party enters a labyrinth with confusing twists and turns. The walls look the same and it's easy to get lost.",
        "Have a Craftiness score higher than 14",
        "Use an ability or item to navigate the labyrinth without getting lost",
        "If you succeed, you successfully navigate the labyrinth and find the exit.",
        "Otherwise, you get lost in the labyrinth and waste valuable time. You fail the encounter and must try again.",
    ],
    [
        "The Sneaky Thief",
        "As your party makes their way through a crowded market, you suddenly feel a hand in your pocket. A pickpocket is trying to steal your valuables.",
        "Have a Sneakiness higher than 14 to catch the thief in the act and retrieve your valuables.",
        "Use an ability or item to track down the thief and retrieve your stolen valuables.",
        "If you succeed, you catch the thief and retrieve your stolen valuables. You can continue your journey with all your belongings intact.",
        "If you fail, the thief escapes with your valuables and you are left empty-handed. Lose all your items.",
    ],
    [
        "The Tricky Puzzle",
        "Your party enters a room with a large locked door. To proceed, you must solve a complex puzzle.",
        "Have a Craftiness higher than 12 to solve the puzzle.",
        "Use an ability or item to decipher the clues and solve the puzzle.",
        "If you succeed, you solve the puzzle and the door unlocks, allowing you to continue your journey.",
        "If you fail, you are unable to solve the puzzle and are stuck in the room.",
    ],
    [
        "The Intimidating Opponent",
        "Your party encounters a group of bandits blocking your path. Their leader steps forward and challenges you to a one-on-one fight.",
        "Roll a Scrappiness check higher than 16 to defeat the bandit leader in combat.",
        "Use an ability or item to gain an advantage in the fight against the bandit leader.",
        "If you succeed, you defeat the bandit leader and the rest of the bandits flee. You can continue on your journey without further interruption.",
        "If you fail, the bandit leader defeats you and takes all your belongings. You wake up later, battered and bruised, with nothing but the clothes on your back.",
    ],
    [
        "The Guarded Door",
        "Your hero comes across a heavily guarded door that appears to be locked. The guards tell your hero that they cannot enter without the proper clearance.",
        "Have a Craftiness higher than 15 to create a convincing forgery of the clearance documents.",
        "Use an ability or item to persuade the guards to let your hero through.",
        "If you succeed in one of those, then you are able to enter through the door.",
        "Otherwise, the guards deny your hero entry, and your hero must find another way around.",
    ],
    [
        "The Raging River",
        "Your hero comes across a raging river that is too wide and deep to cross on foot. There are no bridges or boats in sight.",
        "Have a Scrappiness higher than 12 to build a raft from nearby materials.",
        "Use an ability or item to swim across the river safely.",
        "If you succeed in one of those, then you are able to cross the river.",
        "Otherwise, your hero will be swept away by the river dies.",
    ],
    [
        "The Locked Chest",
        "Your hero comes across a locked chest that appears to be of great value. The lock on the chest is quite complex.",
        "Have a Sneakiness higher than 14 to pick the lock.",
        "Use an ability or item to break the lock and open the chest.",
        "If you succeed in one of those, then you are able to open the chest and see what's inside.",
        "Otherwise, your hero is unable to open the chest, and the valuable contents remain a mystery.",
    ],
    [
        "The Intimidating Thug",
        "Your hero encounters a tough-looking thug who demands payment for passage through the area.",
        "Have a Fabulousness higher than 10 to dazzle the thug with your hero's wealth and status.",
        "Use an ability or item to intimidate the thug and scare them away.",
        "If you succeed in one of those, then your hero can pass through the area without further trouble.",
        "Otherwise, the thug will demand payment or even attack your hero, leading to a difficult fight or a loss of valuable items.",
    ],
    [
        "The Locked Chest",
        "Your hero comes across a locked chest on their journey. It seems to be protected by a magical barrier. Your hero can either try to force it open or attempt to dispel the magic.",
        "Have a Craftiness score higher than 14 to dispel the magic",
        "Use an ability or item to pick the lock or break it open",
        "If you succeed in opening the chest, you find a valuable item inside.",
        "If you fail, the chest explodes and deals damage to your hero.",
    ],
    [
        "The Dark Forest",
        "Your hero finds themselves lost in a dark forest. They hear the sound of growling and rustling in the bushes. Your hero must either sneak past the creatures or fight them head-on.",
        "Have a Sneakiness score higher than 12 to sneak past the creatures",
        "Use an ability or item to sneak past the creatures",
        "If you succeed in sneaking past, you make it out of the forest unscathed.",
        "If you fail, the creatures attack and kill your hero.",
    ],
    [
        "The Cliffside",
        "Your hero is traveling along a cliffside path when they come across a narrow bridge. The bridge is old and rickety, and there's a large gap between the planks. Your hero can either try to cross the bridge carefully or attempt to jump across the gap.",
        "Have a Scrappiness score higher than 15 to make the jump",
        "Use an ability or item to cross the bridge",
        "If you succeed in crossing the bridge, you make it safely to the other side.",
        "If you fail, you fall into the gap and die.",
    ],
    [
        "The Royal Ball",
        "Your hero is invited to a grand royal ball. The king is looking for a new advisor, and your hero hopes to be chosen. Your hero can either try to impress the king with their Fabulousness or attempt to sabotage the other candidates.",
        "Have a Fabulousness score higher than 17 to impress the king",
        "Use an ability or item to sabotage the other candidates",
        "If you succeed in impressing the king, you are chosen as the new advisor and gain a powerful ally.",
        "If you fail, the other candidates are chosen, and you lose favor with the king.",
    ],
    [
        "The Goblin Lair",
        "Your hero stumbles upon a goblin lair. The goblins are hoarding a valuable treasure, but they won't part with it easily. Your hero can either try to negotiate with the goblins or fight them for the treasure.",
        "Have a Craftiness score higher than 12 to negotiate with the goblins",
        "Use an ability or item to fight the goblins",
        "If you succeed in negotiating, the goblins part with the treasure, and your hero gains a valuable item.",
        "If you fail, the goblins attack, and your hero takes damage.",
    ],
    [
        "The Scam Artist",
        "Your hero gets approached by a street vendor selling a seemingly rare and valuable item. However, upon closer inspection, the item is clearly a fake.",
        "Have a Scrappiness score higher than 13 to see through the vendor's scam and haggle them down to a fair price.",
        "Use an ability or item to convince the vendor to sell the item at a lower price.",
        "If you succeed in one of those, then you obtain the item at a reasonable price.",
        "Otherwise, you end up paying too much for the fake item and the vendor laughs all the way to the bank.",
    ],
    [
        "The Persuasive Politician",
        "Your hero attends a political rally where they are approached by a charismatic politician who is trying to win over voters. The politician's speech is full of logical fallacies, but many in the crowd are convinced by their charm.",
        "Have a Fabulousness score higher than 10 to deliver a counter-argument that wins over the crowd.",
        "Use an ability or item to distract the crowd from the politician's speech.",
        "If you succeed in one of those, then you successfully sway the crowd to your side.",
        "Otherwise, the politician's charm wins out and you are drowned out by the cheers of their supporters.",
    ],
    [
        "The Secret Society",
        "Your hero stumbles upon a secret society that is known for their exclusive membership and their strict initiation process. They are suspicious of outsiders and only allow those who can prove their worth to join.",
        "Have a Craftiness score higher than 13 to solve the society's initiation challenge.",
        "Use an ability or item to bribe one of the society's members to vouch for you.",
        "If you succeed in one of those, then you are able to join the society and gain access to their resources.",
        "Otherwise, you are seen as unworthy and are kicked out of the society without any further information.",
    ],
    [
        "The Sleeping Dragon",
        "Your hero comes across a dragon that is fast asleep in their lair. The dragon is blocking the path your hero needs to take, but waking the dragon could mean certain death.",
        "Have a Sneakiness score higher than 16 to sneak past the dragon without waking it up.",
        "Use an ability or item to distract the dragon and create a path to walk through.",
        "If you succeed in one of those, then you are able to get past the dragon without any trouble.",
        "Otherwise, the dragon wakes up and attacks you, causing a catastrophic failure.",
    ],
    [
        "The Locked Chest",
        "Your hero comes across a locked chest. It looks like it could contain some valuable loot. ",
        "Have a Craftiness score higher than 5 to pick the lock.",
        "Use an ability or item to break the lock.",
        "If you succeed, you open the chest and find some valuable treasure inside.",
        "Otherwise, you fail to open the chest and attract some unwanted attention. You will have to fight off the guards to escape.",
    ],
    [
        "The Puzzling Riddle",
        "Your hero encounters a wise old sage who challenges them to solve a riddle.",
        "Have a Craftiness score higher than 10 to solve the riddle.",
        "Use an ability or item to ask for help.",
        "If you succeed, the sage rewards you with a powerful item.",
        "Otherwise, the sage mocks you for your lack of intelligence and you lose some self-esteem.",
    ],
    [
        "The Angry Beast",
        "Your hero stumbles upon an angry beast that is blocking your path.",
        "Have a Scrappiness score higher than 15 to defeat the beast in combat.",
        "Use an ability or item to distract or pacify the beast.",
        "If you succeed, the beast calms down and you can continue on your journey.",
        "Otherwise, the beast attacks and injures you, forcing you to rest and recover before continuing.",
    ],
    [
        "The Devious Trap",
        "Your hero comes across a devious trap that could injure or kill them if triggered.",
        "Have a Scrappiness score higher than 5 to disarm the trap.",
        "Use an ability or item to disable the trap.",
        "If you succeed, you avoid the trap and continue on your journey safely.",
        "Otherwise, the trap triggers and you suffer some injuries, delaying your journey.",
    ],
    [
        "The Persuasive Merchant",
        "Your hero encounters a persuasive merchant who is trying to sell them some overpriced goods.",
        "Have a Fabulousness score higher than 10 to haggle and get a better price.",
        "Use an ability or item to charm or distract the merchant.",
        "If you succeed, you get a good deal on some valuable items.",
        "Otherwise, you end up paying too much and feel like you got ripped off.",
    ],
    [
        "The Lost Key",
        "Your hero needs to unlock a door to proceed, but the key has been lost. You see a small hole in the wall next to the door.",
        "Have a Craftiness score higher than 9 to fashion a makeshift key out of nearby materials.",
        "Use an ability or item to pick the lock.",
        "If you succeed in one of those, you are able to unlock the door and proceed. Otherwise, you are unable to unlock the door and must find another way around.",
        "If you try to force the door open, the noise alerts nearby guards and they catch you. You fail the encounter and are captured.",
    ],
    [
        "The Angry Shopkeeper",
        "Your hero enters a store to purchase an item, but the shopkeeper is extremely angry about something and is not willing to sell anything.",
        "Have a Fabulousness score higher than 9 to convince the shopkeeper that you have something they want to trade.",
        "Use an ability or item to calm the shopkeeper down.",
        "If you succeed in one of those, you are able to make your purchase and leave. Otherwise, the shopkeeper refuses to sell you anything and you have to leave the store empty-handed.",
        "If you try to steal the item, the shopkeeper catches you and alerts the authorities. You fail the encounter and are arrested.",
    ],
    [
        "The Tightrope",
        "Your hero needs to cross a wide ravine to reach the other side. There is a tightrope stretched across the ravine, but it is old and unstable.",
        "Have a Scrappiness score higher than 13 to repair the tightrope enough to safely cross.",
        "Use an ability or item to stabilize the tightrope.",
        "If you succeed in one of those, you are able to cross the tightrope and reach the other side. Otherwise, you lose your balance and fall into the ravine, taking damage and having to find another way around.",
        "If you try to cross the tightrope without repairing or stabilizing it, the tightrope breaks and you fall into the ravine, taking severe damage. You fail the encounter and have to find another way around.",
    ],
    [
        "The Persuasive Bandit",
        "Your hero is stopped by a bandit who demands all of your gold in exchange for passage through their territory.",
        "Have a Fabulousness score higher than 12 to convince the bandit that you are a powerful figure and not worth robbing.",
        "Use an ability or item to intimidate the bandit into letting you pass.",
        "If you succeed in one of those, you are able to pass through the bandit's territory unscathed. Otherwise, the bandit takes all of your gold and you have to find another way around.",
        "If you try to fight the bandit, they are more skilled than you expected and you are defeated. You fail the encounter and are left beaten and robbed.",
    ],
]


def getRandomMonster():
    return random.choice(ALL_MONSTERS)


class Encounter(object):
    title = ""
    prompt = ""
    option_a = ""
    option_b = ""
    pos_result = ""
    neg_result = ""

    def __init__(self):
        encounter = random.choice(ENCOUNTERS)
        self.title = encounter[0]
        self.prompt = encounter[1]
        self.option_a = encounter[2]
        self.option_b = encounter[3]
        self.pos_result = encounter[4]
        self.neg_result = encounter[5]

    def __str__(self):
        return f"{self.title}: {self.prompt}  Either: {self.option_a} OR {self.option_b} {self.pos_result} {self.neg_result}"
