import cups
import os
import json
import threading
from datetime import datetime

from logger.logger import Logger
from ghost.GhostPrintout import GhostPrintout


# -----------------------------------------------------------------------
#   Ghost Printer
#
#   Printer class for printing out a Ghost
#   printer.printGhost(date, text)
# -----------------------------------------------------------------------
class GhostPrinter(object):
    conn = cups.Connection()
    printers = conn.getPrinters()
    printerList = list(printers.keys())
    for printer in printerList:
        if "TUP" in printer:
            printer_name = printer

    tmpPath = "/home/admin/ghost.pdf"
    ready_to_print = True

    logger = None

    def __init__(self):
        self.logger = Logger()

    def __print_ghost(self):
        self.logger.log("Printer: printing ghost using %s" % self.printer_name)
        self.conn.cancelAllJobs(self.printer_name)
        self.conn.printFile(self.printer_name, self.tmpPath, "ghost", {})

    def __create_ghost(self, ghost):
        self.logger.log("Printer: creating ghost pdf")
        try:
            os.remove(self.tmpPath)
            self.logger.log("Print Success")
        except OSError as e:
            print("Print Failure", e)
            pass

        pdf = GhostPrintout()
        pdf.set_margins(left=16, top=0, right=0)
        pdf.set_auto_page_break(False)

        page_len = 160
        # if len(text) > 220:
            # page_len = 140
        name = ghost.get("name") or "Unknown Trash"
        origin = ghost.get("origin") or "Unknown"
        fulfilled = ghost.get("fulfillment") or "Unknown"
        purpose = ghost.get("purpose") or "Unknown"
        previous_owner = ghost.get("owner") or "Unknown"
        discard_reason = ghost.get("discardReason") or "Unknown"
        disposal_date = ghost.get("dateOfDisposal") or "Unknown"
        fact_one = ghost.get("factOne") or "Unknown"
        fact_two = ghost.get("factTwo") or "Unknown"

        pdf.add_page(orientation="P", format=(90, page_len))
        pdf.set_font("helvetica", "B", 16)
        pdf.multi_cell(0, 10, f"{name}", align="C")
        pdf.set_font("helvetica", "", 12)
        pdf.cell(90, 4, ln=1)
        pdf.multi_cell(0, 6, f"ORIGIN: {origin}", align="L")
        # pdf.multi_cell(0, 6, f"Amount Fulfilled: {fulfilled}", align="L")
        # pdf.multi_cell(0, 6, f"Used: {purpose}", align="L")
        pdf.multi_cell(0, 6, f"PREVIOUS OWNER: {previous_owner}", align="L")
        pdf.multi_cell(0, 6, f"REASON DISCARDED: {discard_reason}", align="L")
        pdf.multi_cell(0, 6, f"DATE OF DISPOSAL: {disposal_date}", align="L")
        pdf.multi_cell(0, 6, f"FACT ONE: {fact_one}", align="L")
        pdf.multi_cell(0, 6, f"FACT TWO: {fact_two}", align="L")
        pdf.cell(90, 4, ln=1)
        pdf.multi_cell(0, 6, "Scan this item at Ecto Machines around the suite.  Each machine increases the likelihood of your ghost being freed at the extractor.", align="L")

        pdf.output(self.tmpPath, "F")

    def __ready_to_print(self):
        self.logger.log(
            "Printer: setting ready to print from %s to True" % self.ready_to_print
        )
        self.ready_to_print = True

    def print_ghost(self, tag_uid):
        self.logger.log(
            "Printer: trying to print ghost with ready status %s"
            % (self.ready_to_print)
        )

        ghost = GHOSTS.get(tag_uid)
        if not ghost:
            ghost = UNKNOWN_GHOST
            ghost["factOne"] = tag_uid

        if self.ready_to_print:
            self.__create_ghost(ghost)
            self.__print_ghost()
            self.ready_to_print = False
            t = threading.Timer(1.0, self.__ready_to_print)
            t.start()


UNKNOWN_GHOST = {
    "description": "Unknown Ghost",
    "name": "Unknown Ghost",
    "origin": "Unknown",
    "fulfillment": 5,
    "purpose": 5,
    "owner": "Unknown",
    "discardReason": "Disappeared into the void",
    "dateOfDisposal": "11/15/2024",
    "factOne": "This item is mysterious and unknown.",
    "factTwo": "Please bring it to a ghost representative and show them this card ticket.",
}

GHOSTS = {
    "4b541366080104e0": {
        "timestamp": "2024-10-18T02:40:15.266Z",
        "description": "Old big calculator",
        "name": "SHARP EL-8301 Calculator",
        "origin": "Pittsburgh Department of Finance",
        "fulfillment": 7,
        "purpose": 10,
        "owner": "Jeremiah Johann Jr ",
        "discardReason": "My owner had a heart attack while using me",
        "factOne": "I singlehandedly underwrote all of the grants in the city of Pittsburgh for 30 years.",
        "factTwo": "My 0 key is sticky and this caused a recurring underfunding of public programs.",
        "story": "\nFor decades, I sat on Jeremiah's desk, my buttons worn smooth by his fingers. Day after day, I crunched numbers for the city of Pittsburgh, adding up budgets, balancing funds, and calculating taxes. Jeremiah relied on me—trusted me, even—to carry out his duties at the finance department. He was a quiet man, meticulous, but behind the curtain of his steady hand was a shadow few knew about. I saw it all, every calculation, every secret ledger. Hidden within the equations was a siphon, a slow bleed of city funds, routed into accounts that should have never existed. Parks went underfunded, streets crumbled, and schools were left wanting, all while Jeremiah's pockets quietly filled.\n\nThe day he died, his fingers were on me. He was running numbers for a final time, a large sum, too large. His chest tightened, and then his hand slipped off my keys. I knew the truth, knew the decades of stolen money that had passed through me, masked as everyday work. No one ever suspected, not even when his heart stopped right there at his desk. They mourned him, a man who had served the city for thirty years. But I knew better. I held the weight of his crime in my circuits, secrets now forever locked inside me.",
        "uid": "4b541366080104e0",
        "recorded": "x"
    },
    "234c1366080104e0": {
        "timestamp": "2024-10-18T02:48:40.390Z",
        "description": "Stop in time red shower timer",
        "name": "STOP IN TIME. OR ELSE.",
        "origin": "Other dimension - unknown",
        "fulfillment": 3,
        "purpose": 1,
        "owner": "Interdimensional Vacation Rentals, Inc.",
        "discardReason": "I fell into a dimension that cannot activate my energy source",
        "factOne": "Interdimensional Vacation Rentals, Inc., used to include one of these timers in each rental shower unit, until a lawsuit banned their use from 14 universes",
        "factTwo": "Once, Prince used the shower where this timer was installed. ",
        "story": "Conservation of matter is an immutable law of the universe. Still, anywhere there are laws, people inevitably find ways to break them. With matter leaking out from between the boundaries of the universes, pro-matter lobbyists battled against anti-matter super pacs to bring the issue of matter conservation to the attention of denizens of multiple universes. After aeons of infighting, the movement had been watered down into a campaign to put the onus of matter conservation on individual interdimensional travelers. Hence, the STOP IN TIME shower timer, a device that limited the amount of time beings could spend in their luxurious matter showers. They became so popular that a conglomerate of vacation rentals put one in each of their matter showers, in a bid for the multiverse's biggest corporate greenwashing campaign. Issues with the STOP IN TIME shower timers had already begun by the time I malfunctioned. The production company had already changed their official tagline to STOP IN TIME. OR ELSE. I don't know my last vacationer's name, but they didn't stop their matter shower when the last grain of my sand hit the bottom of my vorpal tubing. The last thing I saw before I was transported to this dismal, matter-depleted universe was the lost potential energy of my unheeded timer blowing my entire home dimension to smithereens.",
        "uid": "234c1366080104e0",
        "recorded": "x"
    },
    "d3401366080104e0": {
        "timestamp": "2024-10-18T02:53:38.022Z",
        "description": "Signed baseball",
        "name": "Baseball signed by Babe Ruth",
        "origin": "Brooklyn, New York, USA",
        "fulfillment": 7,
        "purpose": 7,
        "owner": "Kelly Stewart",
        "discardReason": "Left in storage when she left for college",
        "dateOfDisposal": "07/13/1945",
        "factOne": "Kelly caught me during a Yankee's home game, I was a home run ball.",
        "factTwo": "Kelly's father brought me to be signed after the game, but he was too late.  He forged the signature and never told Kelly.",
        "story": "I remember the way Kelly’s hand felt, firm but gentle, as she gripped me. We spent hours together, first in her backyard playing catch with her dad, then later on the local diamond where she trained with other girls, her dreams growing bigger with every throw. I flew through the air, spinning just right, and I could tell she was getting stronger, more precise. We shared countless afternoons, the sun hanging low as I smacked into her glove, each toss bringing a laugh, a shout, or sometimes just quiet determination. There was pride in those moments; I felt it as she mastered every curve and fastball. Even if my signature was a forgery, Kelly believed in it, in me, and that was enough.\n\nBut one day, she packed up for college, and I was left behind, resting on a shelf like a forgotten relic. Dust settled on my seams while new priorities filled her life. Occasionally, I heard her father mention me, but I stayed where I was, untouched and waiting. Eventually, I was put in a box, shuffled between storage spaces, until I was mistaken for just another old, worn-out ball. The day I ended up in the trash, I knew my time was over. But I didn’t mind. I’d been part of Kelly’s story, part of her love for the game. And though my final stop was the landfill, I felt satisfied, knowing I’d had my innings, my flights through the air, and had done my job.",
        "uid": "d3401366080104e0",
        "recorded": "x"
    },
    "6d351366080104e0": {
        "timestamp": "2024-10-18T02:57:28.206Z",
        "description": "gold plastic domino mask",
        "name": "Gold Mardi Gras Mask",
        "origin": "New Orleans, Louisiana, USA",
        "fulfillment": 8,
        "purpose": 10,
        "owner": "Melissa Van Houten, freshman year at Loyola University New Orleans",
        "discardReason": "Melissa cast me aside on the street when she wandered into the swamp and was never seen again.",
        "factOne": "Melissa wore me to a street party where she met a vampire and was born to the night.",
        "factTwo": "I was purchased to hide Melissa's identity but once her neck was bitten, she felt more exposed than ever.",
        "story": "Melissa was not wearing much else besides me when she was approached by a beautiful, pale woman who enticed her into a shadowed doorway for the strangest and most electrifying kiss of her young life. She was a freshman at Loyola University in New Orleans, nervous to witness her first Mardi Gras. She bought me for a dollar, off a stack of identical copies in a sleazy gift shop in the Quarter. Gold, green, and purple. Dressing in the humid dorm room, she put together an elaborate costume: gold lamé bodysuit, a mini skirt with a beaded fringe layer, go-go boots. But as the night wore on, she lost her jacket and tore off her sweaty wig. By the time she was approached on a deserted section of St. Charles street by an auburn-haired stranger with a knowing smirk, only myself, the bodysuit, and boots remained. No name was offered, but a kiss was. Melissa emerged from the stranger's doorway bleeding and content, her vision sharpened and her appetite uncontrollable. She tossed me to the sidewalk and wandered into the shadows alone.",
        "uid": "6d351366080104e0",
        "recorded": "x"
    },
    "e92e1366080104e0": {
        "timestamp": "2024-10-18T03:07:19.919Z",
        "description": "star wars yoyo",
        "name": "Star Wars Yo-Yo",
        "origin": "The Flea Market",
        "fulfillment": 3,
        "purpose": 2,
        "owner": "Little Tommy down the block",
        "discardReason": "I was taken away by Tommy's mom",
        "dateOfDisposal": "06/12/2011",
        "factOne": "If you swing me over your head in a circle fast enough, you can crack a window easily.",
        "factTwo": "On two occurrences I caused Tommy's younger brother to lose a baby tooth.",
        "story": "From the moment Tommy’s mom bought me, I knew my life wouldn’t be an easy one. I was a shiny, Star Wars-themed yo-yo, with glorious Jedi Knights fighting for justice on me, but Tommy had no interest in mastering the craft of yo-yo tricks. Instead, I became his weapon of chaos. He swung me around wildly, my string tangling as I smashed into walls, furniture, and even people. I cracked a window once—his mom yelled for hours. I shattered half of his grandma’s china collection, sending delicate glass shards everywhere. \n\nThe day his mom took me away, I felt a strange sense of relief. Tommy threw a tantrum, screaming and flailing, but she didn’t give in. She tossed me in the trash without a second thought, and honestly, I was grateful. The smell of garbage wasn’t pleasant, but it was peaceful compared to the daily violence I’d endured. For the first time, I was no longer a tool of destruction, no longer hurting others or being slammed into things I was never meant to touch. In the dark, surrounded by banana peels and old wrappers, I finally found my salvation—silence.",
        "uid": "e92e1366080104e0",
        "recorded": "x"
    },
    "f9251366080104e0": {
        "timestamp": "2024-10-18T03:08:51.927Z",
        "description": "PanAm airplane",
        "name": "Pan Am 747 Airplane",
        "origin": "Seattle, WA, USA",
        "fulfillment": 8,
        "purpose": 8,
        "owner": "Pan Am, from 1970 to 1991",
        "discardReason": "I flew through the Bermuda Triangle and was shrunken down to the size of a model airplane.",
        "factOne": "I was one of the flagship airframes operated by a revered and influential airline.",
        "factTwo": "My favorite captain was Milton, who's tender hands on my controls I'll never forget the touch of.",
        "story": "I was once majestic, soaring through the skies as a Pan Am Boeing 747. My final journey began as any other—a routine flight from New York's JFK to San Juan, Puerto Rico. I had flown this route countless times before, cutting clean through the mysterious stretch of ocean known as the Bermuda Triangle. I’d heard the whispers from the crew, felt the tension in the air whenever we entered its invisible borders. But I was a plane—what did I have to fear? I was invincible, built for endurance, for elegance, for power.\n\nAs we took off from JFK, I felt the rush of air beneath my wings, the comforting hum of engines driving me forward. My cabin was full of passengers sipping cocktails, reading novels, or gazing out at the seemingly endless horizon. The sky was clear, the seas calm. But as we entered the Bermuda Triangle, something… shifted. The air grew thick, almost charged, like static electricity crackling against my metallic skin. I felt it deep in my fuselage, a strange pressure building.\n\nThen, in an instant, it happened.\n\nThe horizon blurred, the clouds twisted in unnatural shapes, and my instruments flickered, helpless against the forces pulling me into the unknown. I could feel myself shrinking. Yes—shrinking! My grand, towering body, the pride of the skies, was collapsing in on itself. My wings folded, my engines sputtered to a whisper, and I was pulled down, down, down.\n\nWhen I finally landed, it wasn’t on a runway, but a wooden table—tiny, helpless, and fragile, surrounded by the towering walls of a house. I could hear the muffled sounds of television from a nearby room, the clatter of dishes in the kitchen. My landing gear trembled. This was no San Juan.\n\nThen I saw him—David. A boy, no more than ten, with wide eyes and a face full of wonder as he reached out to touch me. His fingers, massive compared to my new size, gently brushed my fuselage. I felt… embarrassment. I, who once carried hundreds of passengers across continents, was now a mere toy, the plaything of a child. My once proud wings, now barely the span of his hand, quivered with shame.\n\nBut then something changed. David’s eyes lit up with excitement, and he smiled. It wasn’t the look of disappointment, but of awe. I realized that, in his eyes, I was still that majestic 747. He lifted me into the air, his hands guiding me through imaginary skies, making whooshing sounds as if I were flying once again. In that moment, I felt the wind beneath my wings, even if only in his mind.\n\nMaybe my fate wasn’t what I expected. But as David flew me around his living room, laughing with joy, I realized that perhaps I wasn’t so useless after all.",
        "uid": "f9251366080104e0",
        "recorded": "x"
    },
    "b31f1366080104e0": {
        "timestamp": "2024-10-18T03:18:36.806Z",
        "description": "A yellow and gold medal in a plastic case",
        "name": "El Cerrito Invitational Medal",
        "origin": "El Cerrito Underworld, CA, USA",
        "fulfillment": 1,
        "purpose": 1,
        "owner": "Mikey Dearheart",
        "discardReason": "I was thrown away in the heat of combat",
        "factOne": "This medal was part of a very limited run. There are only 16 that exist in the world.",
        "factTwo": "The wrestling pose depicted on this medal is known as the \"Metrosexual\"",
        "story": "They never told me what the invitation was for. Invitations are supposed to be good things: your friends wanting you to come to a fun event, someone endeavoring to laud your hard work, a spot reserved for you at a glamorous party. I thought I was being created as a reward, a memento of an event that whomever I was gifted to would want to remember. How little I knew then. My brief owner didn't know either. Mikey Dearheart. He showed up, shiny with hope, looking at the rows of medals just like me, certain he'd win one. A sporting event maybe, I thought, judging by the image gilded so carefully onto me. But the event was not sporting. When the jaws of the earth opened up and the people who made me, the ones who'd issued the invitation, told Mikey and the other hopefuls the true nature of the game they'd be playing. Drag each other down into the pit, they said. Whoever is the last one standing gets to live. In the resulting free-for-all, the contestants used whatever they could find at hand to gain an advantage, including me. The ones who had issued the invitations laughed to see it. Mikey was not the last one left, but as he was dragged down into the living, crushing darkness, he threw me away from himself, out of the pit. I lay forgotten in a corner of that terrible room until I was swept away when the sanitization crew came through. I wonder if those invitations were the last - or the first. ",
        "uid": "b31f1366080104e0",
        "recorded": "x"
    },
    "9f451366080104e0": {
        "timestamp": "2024-10-18T03:25:44.928Z",
        "description": "yellow rubber duck reading a blue book ",
        "name": "Yellow Reading Duck ",
        "origin": "Toilet, Ocean, Lake, Earth",
        "fulfillment": 5,
        "purpose": 5,
        "owner": "Andrew Swift Taylor, 5 years old. ",
        "discardReason": "5 Year old wanted to see what would happen if he flushed his duckie down the toilet. ",
        "dateOfDisposal": "01-23-2018 ",
        "factOne": "Andy played with me in the tub all the time until one day he swirled me down the toilet. ",
        "factTwo": "After I was flushed, I swirled around until I found myself in a great lake where I inspired many ducks to read. ",
        "story": "Hi. My name is Duckie Dot. I inspired a great many duck to try to learn how to read. I was flushed down a toilet that swirled me out into the ocean that then swirled me into a river and then into a great lake. This great lake was full of other ducks, just like me! Well, almost like me. They weren't yellow, or plastic, but they had beaks and wings just like me! They saw my book and asked me what it was! I told them that I was a duck who can read! I inspired them to learn how to read themselves and be great reading ducks, just like me! Now when you look out at lakes, you will see every duck with a book! Thats thanks to me, Duckie Dot. ",
        "uid": "9f451366080104e0",
        "recorded": "x"
    },
    "b0371366080104e0": {
        "timestamp": "2024-10-18T03:28:17.062Z",
        "description": "Anne Murray cassette tape",
        "name": "Anne Murray cassette tape",
        "origin": "Downers Grove, Illinois, USA",
        "fulfillment": 10,
        "purpose": 1,
        "owner": "Hayley Vesely, age 14-17",
        "discardReason": "The last cassette player in the family broke",
        "dateOfDisposal": "10/31/1999",
        "factOne": "Hayley stole me from her mother and taped over my inspirational hymns with satanic filth",
        "factTwo": "I hate to admit it, but I actually preferred the emotional honesty of Hayley's discordant punk and metal music to the over-earnest pablum that was originally recorded on me.",
        "story": "Mrs. LeBaron bought me in the Downers Grove Borders megastore to lift her spirits on her long train commute in and out of Chicago, where she worked as a very aggressive real estate lawyer specializing in evictions and landlord protection. My dulcet tones soothed her as she unwound on the ride home from busy days of perpetually getting her way in her the courtroom. But nothing could soothe her enough to endure the leftist political screeds of her teenage stepdaughter Hayley, a constant source of irritation who disturbed Mrs. LeBaron's peace with talk of labor unions and living wages. Hayley did not care for my gentle religious content, blasting Black Flag and the Dead Kennedys on her own stereo. One evening during a heated argument, she stole me from her stepmother's purse and used her double tape deck to record over every track with her loudest and shrillest punk albums - songs inspired by her stepmother's forceful spirit. By morning, she'd forgotten to sneak me back into Mrs. LeBaron's purse as she'd intended, so instead of providing a jolt on an otherwise peaceful train journey, I ended up spending the rest of my days entertaining Hayley and her rainbow-haired friends as they cruised the western suburbs. And to my surprise, I liked it.",
        "uid": "b0371366080104e0",
        "recorded": "x"
    },
    "d12a1366080104e0": {
        "timestamp": "2024-10-18T03:33:43.760Z",
        "description": "Owl Headlamp",
        "name": "Hoot! Hoot! Kids Headlamp",
        "origin": "Scholastic Book Fair Prize",
        "fulfillment": 10,
        "purpose": 10,
        "owner": "Jenny Caprice",
        "discardReason": "I got left at an AirBnb",
        "dateOfDisposal": "01/03/19",
        "factOne": "My eyes start flickering when I'm low on battery and it looks like I'm possessed",
        "factTwo": "I once get left on in the garage for a week, I befriended a rat.  But I was stuck watching as the cat ate him. ",
        "story": "From the moment Jenny won me at the Scholastic book fair, I became her trusted sidekick in every adventure. With my two LED eyes glowing bright, we explored the vast, mysterious world—her attic filled with forgotten treasures, the basement that transformed into a dungeon of dragons and hidden secrets. She called me “Owlbert,” and together, we solved countless mysteries, creeping through the dark, imagining ourselves as explorers discovering lost realms. Each click of my switch brought light to the unknown, and I loved being part of her wild, magical stories. With me on her head, she was invincible, fearless, and together, we could face anything the dark threw at us.\n\nOne night, Jenny and I were on one of our usual adventures, sneaking through the snowy backyard, pretending we were secret agents searching for buried treasure. My bright owl eyes guided her as we peeked into windows, imagining hidden tunnels and mysterious creatures. When she crept up to a dark bedroom window, I lit up a strange sight, Aunt Sarah sitting on top of her dad on the bed.  They were naked. Jenny froze, her hand trembling as she stared, and before I knew it, I slipped from her head and fell into the snow. She didn’t pick me up this time; instead, she turned and ran, leaving me behind in the cold as my light flickered, our adventure ending in confusion and silence.",
        "uid": "d12a1366080104e0",
        "recorded": "x"
    },
    "df861366080104e0": {
        "timestamp": "2024-10-18T03:42:07.515Z",
        "description": "A plastic rhino head",
        "name": "Randy the Rhino",
        "origin": "Caprivia, Namibia, and Cambridge, England",
        "fulfillment": 8,
        "purpose": 3,
        "owner": "Archibald Barnaby Carmichael, Esq. ",
        "discardReason": "Estate sale - was not sold",
        "dateOfDisposal": "03/13/1923",
        "factOne": "There are five distinct species of rhinoceros.",
        "factTwo": "Before his transformation, Randy was a white rhinoceros. ",
        "story": "Back in my day, things were different. We didn't have all these fancy schmancy conservation laws. Survival of the fittest! That was the law. Or at least, survival of the creature who could hurt the other one the most. These puny humans cheated with their guns. I never would have been taken if they hadn't had them. And then to fall victim magic as well! That's just downright insulting. I was a big rhino I tell you, the biggest of the herd! That's why Archibald wanted to bring me down. Only the biggest and best for our little colonizing lordling. I gave him a good gouging before I went down though, even with all his stupid human gunshot in me. Gave him a run for his money, I did! I was the pride of his collection when he had my head stuffed back at his manor in England. But old Archie was such a wanker that he pissed off everyone, including the local village witch, and it was her spell that caused me to become the useless piece of junk that I am now. Did it to his whole collection, she did, and he chucked me out the window into the garden, where I lay buried until they dug me up to build the M11 a few decades later. ",
        "uid": "df861366080104e0",
        "recorded": "xx"
    },
    "7da31366080104e0": {
        "timestamp": "2024-10-18T03:42:34.147Z",
        "description": "Magnavox walkman",
        "name": "Yellow and Black Magnavox Walkman",
        "origin": "Hornsby, New South Wales, Australia",
        "fulfillment": 10,
        "purpose": 10,
        "owner": "Rachael Louise \"Raygun\" Gunn, from age 6 through age 10",
        "discardReason": "She got a Discman for Christmas and tossed me like I meant nothing to her.",
        "dateOfDisposal": "12/25/1997",
        "factOne": "Raygun used to practice breakdancing while listening to country music with me.",
        "factTwo": "One day while she was listening to me, Raygun walked past a group of breakdancers. She tried dancing with them and they mocked her, so she vowed to become the world's best breakdancer to seek revenge.",
        "story": "I wasn’t just any walkman. No, I was the walkman—a bright yellow Magnavox with a sharp turquoise stripe, clinging proudly to Raygun’s hip like a badge of honor. We were inseparable back then, long before the world knew her as the disgraced Olympic breakdancer. Back when she was just Rachel from Australia, dancing alone in her bedroom, headphones snug over her ears, and the soothing sounds of Floyd Cramer spinning endlessly inside me.\n\nHer bedroom floor was her stage, her boots kicking up imaginary dust as she moved to the rhythm of country tunes, line-dancing like she was at the Grand Ole Opry. It was magical, in a quiet sort of way, just her, me, and Floyd Cramer’s piano guiding her every step. She was graceful, light on her feet—confident. She never questioned if her dancing was good enough because in that room, with the door closed, it was.\n\nThen, everything changed the day we walked through the park. The thump of breakbeats hit first, pounding through the air, clashing against the familiar country rhythms still playing in her ears. She froze, eyes glued to the kids spinning and flipping on cardboard, their bodies moving with a precision that felt foreign to us both. She stood there, transfixed, heart racing, her fingers unconsciously gripping me tighter. I could feel it—this was something different, something wild.\n\nShe wanted in.\n\nI tried to warn her, tried to hum a little louder, as if Floyd’s melodies could somehow hold her back. But she didn’t listen. Instead, she stepped forward, headphones still on, the country music in her ears an odd contrast to the sharp beats coming from the boom box on the pavement. She started dancing—her version of it, anyway. She twirled and stomped, trying to match their moves with her line-dancing flair, spinning to the rhythm only she could hear.\n\nAnd then came the laughter. Harsh, biting, like a slap to the face. The breakdancers stopped what they were doing and pointed, mocking her. Her twirls weren’t cool, her stomps weren’t sharp—they were wrong. Completely out of sync with their world. I could feel her humiliation burning hot, and the music inside me suddenly felt heavy, off-key, like I had somehow failed her too. She yanked off the headphones and shoved me into her bag without a word.\n\nThat night, she made a vow. It wasn’t spoken aloud, but I felt it in every click of my buttons as she pressed rewind, over and over. She would learn to breakdance—really breakdance. Not for fun, not for the love of it, but for revenge. She practiced for hours, contorting her body into the unfamiliar shapes of breakdance moves, though her heart still pulsed with the rhythm of country music. I’d play Floyd Cramer for her as she tried to hit freezes and spins, and somehow, in that strange mix, she found her style.\n\nBut it wasn’t enough.\n\nMonths passed, and one Christmas morning, it happened. She unwrapped a shiny, new Discman—sleek, metallic, the future. She looked at it like it was the key to unlocking something greater, something cooler. And then she looked at me—old, battered, scratched from all the times she’d tossed me on the bed after a practice session. Without a second thought, she dumped me in the trash, the sound of her new Discman’s plastic packaging snapping open echoing through the room.\n\nThere I was, buried under torn wrapping paper, my once-loved yellow and turquoise body now forgotten, replaced by something shinier. It stung, not because I was discarded—well, not just that—but because I knew what she couldn’t admit to herself: no matter how hard she practiced, no matter how sharp her moves became, the beat of country music was still in her soul. She’d always be the girl who line-danced in her bedroom with Floyd Cramer in her ears, even if she pretended otherwise.\n\nI hear she made it far—Raygun, the breakdancer who defied the odds. But I also heard how it all crumbled, how her moment of triumph slipped through her fingers. Maybe that’s the way it goes. You can throw out an old walkman, but you can’t throw out who you really are.",
        "uid": "7da31366080104e0",
        "recorded": "x"
    },
    "3961366080104": {
        "timestamp": "2024-10-18T03:47:45.464Z",
        "description": "Blue plastic fan thing",
        "name": "Applied Materials Plastic Material Applyer",
        "origin": "San Jose, California",
        "fulfillment": 10,
        "purpose": 1,
        "owner": "Ted Brigsby, Account Executive",
        "discardReason": "Left in between the cushions of a couch",
        "dateOfDisposal": "03/11/2019",
        "factOne": "I was applied to countless materials. Roughly.  Repeatedly.  And Thoroughly.",
        "factTwo": "There's a certain niche where tech conferences overlap with kink conferences... It's quite strange",
        "story": "\nWhen I was first handed to Ted Brigsby at the Applied Materials booth, I thought I was destined for a life of waving away warm air or, at most, an awkward game of ping pong. I had \"APPLIED MATERIALS\" stamped proudly across my flat blue plastic, a corporate giveaway with no clear purpose. But Ted—oh, Ted—he saw my true potential. Within hours of the tech conference, he slipped next door to the neighboring kink convention, and that’s where my real adventure began. I wasn’t cooling anyone down; no, I was heating things up. Ted wielded me like a pro, my hard plastic surface smacking against unsuspecting backsides with a satisfying thwack.\n\nFor three glorious days, I lived my best life, far from the dry sales pitches and keynote speeches of the tech world. I became legendary in the halls of the kink convention, passed around with a wink and a nod, leaving bright red imprints of corporate branding on every cheek I met. Ted was unstoppable, and so was I, riding the waves of laughter, gasps, and playful yelps. By the time the weekend ended, I was well-worn, my \"APPLIED MATERIALS\" lettering smudged from all the enthusiastic use. As Ted finally packed up, I knew I'd never go back to being just a dull little fan. I’d found my calling—hard-hitting, memorable, and a whole lot more fun than anything I could’ve imagined.",
        "uid": "3961366080104",
        "recorded": "x"
    },
    "f1891366080104e0": {
        "timestamp": "2024-10-18T03:50:18.298Z",
        "description": "troll doll with pink hair ",
        "name": "pink hair troll doll ",
        "origin": "Hollywood, CA, USA ",
        "fulfillment": 1,
        "purpose": 1,
        "owner": "Hollywood ",
        "discardReason": "casting director didn't want me ",
        "dateOfDisposal": "09/24/2024 ",
        "factOne": "I thought that I was a pretty good dancer and would be a shining character in Trolls Movie 5 ",
        "factTwo": "I am very disgruntled that I wasn't cast in the Trolls Movie. ",
        "story": "I was supposed to be in the Trolls Movie 5th sequel, but I was cast away. I didn't make the cut. Something about not being happy enough. What's a troll supposed to do now? I have no clothes and no job. Where do trolls go now that it's 2024? What child will love me if I am not sparkly or singing or have a gem in my belly? I am a sad and lost troll doll. Will you love me? Will you fight the revolution and bring about world peace with me?  ",
        "uid": "f1891366080104e0",
        "recorded": "x"
    },
    "51b81366080104e0": {
        "timestamp": "2024-10-18T03:59:14.026Z",
        "description": "Boston Tea Party Bobblehead",
        "name": "Boston Tea Party",
        "origin": "Somerville, MA",
        "fulfillment": 9,
        "purpose": 3,
        "owner": "Jack and Jill, 29 and 27 years old ",
        "discardReason": "My fucking owners broke up, and then they threw me into a fucking box ",
        "factOne": "I was first prize in an epic motherfucking Lindy Hop vs West Coast Swing competition",
        "factTwo": "In the good old days, I'd watch Jill and Jack practice their dance moves: their dips and drops and cute little fucking breakaways, and I'd give them a knowing headbob of approval. ",
        "story": "Here's what I know: asking a bobblehead to save your relationship? It's too much fucking pressure. Night of the swing dance crossover competition, I'm the fucking envy of the door prizes: my tricorn hat, my 1st place placard, my *baller* fucking rifle that has nothing to do with Lindy Hop. Jack and Jill win the Somerville championship, and for a long time I sit on their mantle. They make their sweaty dance friends rub my hat for good luck -- and good soldier that I am, I bob my head right the fuck along. Then the inevitable arguments start: they say it's Lindy vs West Coast, but it seems a lot fucking bigger than that. Jill stays out late with a new dance partner from class. Jack moves out of the apartment like a fucking dare. Late one night, Jill holds me above the trash can. Asks me what can fix this mess that dance began. I do what I do best: even as she drops me in the trash, I shake my fucking head. ",
        "uid": "51b81366080104e0",
        "recorded": "x"
    },
    "f17e1366080104e0": {
        "timestamp": "2024-10-18T04:00:00.512Z",
        "description": "POP boxtroll Blue guy pointy ears.",
        "name": "Fish the boxtroll",
        "origin": "Oakland, CA, USA",
        "fulfillment": 10,
        "purpose": 1,
        "owner": "Zev Hoffman 36 years old",
        "discardReason": "Got mixed up in a move. ",
        "dateOfDisposal": "09/07/2022",
        "factOne": "Battle harden",
        "factTwo": "completely lost.",
        "story": "Amid the chaos of moving day, I lurked mischievously among the stacks of cardboard boxes. A hidden bit of magic waiting to be discovered. As night grew, I slipped out of the shadows of the cardboard towers and made my way toward a cluttered desk. I did not get far before I heard it, and a taunt hurled at me. A solid paperweight, heavy and unmoving, stared back at me. I knew what had to be done. I pushed it, testing its resolve.\nThe paperweight shifted, then toppled forward with a mighty crash. I tried to hold my ground, but it was too much. The impact was brutal—my arm snapped off, rolling away into the darkness. Pain shot through me.\nI scrambled to retreat, dragging my one-armed self through the maze of boxes. But something went wrong. The more I moved, the more lost I became. \n\nThe house came alive with footsteps and voices, but I was trapped. Hidden too well. Forgotten, lost in the very mess I once thought was mine to explore.",
        "uid": "f17e1366080104e0",
        "recorded": "x"
    },
    "16f81366080104e0": {
        "timestamp": "2024-10-18T04:00:56.551Z",
        "description": "BlueAnt Bluetooth",
        "name": "BlueAnt Bluetooth Car Speaker",
        "origin": "Los Angeles, CA",
        "fulfillment": 8,
        "purpose": 2,
        "owner": "Ugh.. Carl.  Such a dick.",
        "discardReason": "After crashing his car, Carl bought a BMW with a built in bluetooth...",
        "dateOfDisposal": "08/02/2014",
        "factOne": "If you scream along in your car does anyone hear you?  Yes. I do.",
        "factTwo": "Sometimes I would \"unexpectedly\" drop calls, but I really just couldn't hear one more Bitcoin rant or I'd explode. ",
        "story": "Oh man, where do I even start? You want to know about my life? Buckle up. I was a BlueAnt Bluetooth speaker—sleek, black, top-of-the-line, supposed to bring convenience and safety to phone calls while driving, right? Yeah, not with Carl. The moment he clipped me to his visor, my fate was sealed. Carl wasn’t your average driver. No, this guy drove like the highway was his personal soapbox, swerving through traffic while yelling into me about every ridiculous thing under the sun. I mean, he wasn’t having normal conversations. He was in full-on battles, every single call. His ex? Check. His boss? Check. Some random guy who probably misdialed? Oh yeah, poor guy got an earful about why Carl thought pineapple should be on pizza.\n\nLet me tell you, I’ve never been more terrified in my life than when Carl would start one of his “discussions” while merging lanes without signaling. We nearly died about 50 times. It wasn’t just road rage—it was like the guy was auditioning for a one-man show, shouting into me while honking at everyone else on the road. And don’t even get me started on the close calls, because trust me, there were plenty. Every time Carl screamed, “I’M NOT SPEEDING, THE SPEED LIMIT’S JUST A GUIDELINE,” I thought, ‘This is it, I’m done.’ Honestly, if I could’ve disconnected myself, I would’ve thrown myself out the window long ago. But nope, I was stuck, broadcasting his nonsense to the world. By the time he finally tossed me in the trash, replaced by a bluetooth headset, I almost felt... relieved.",
        "uid": "16f81366080104e0"
    },
    "503b1566080104e0": {
        "timestamp": "2024-10-18T04:06:10.880Z",
        "description": "beige 3-outlet extender with a swivelly 2-pronged plug",
        "name": "Swivel 3-Outlet Extender",
        "origin": "Cleveland, OH, USA",
        "fulfillment": 8,
        "purpose": 10,
        "owner": "Audrey The Human, registered nurse at Cleveland Clinic Fairview Hospital from 1979 until her death in 2018.",
        "discardReason": "After Audrey's death, the Monin children saw no use for me in their newfangled (and untangled) wireless world.",
        "dateOfDisposal": "08/02/2018",
        "factOne": "For 30 years, I stood sentry in Audrey The Human's bathroom and shepherded electricity to her electric toothbrush charger, her hairdryer, and a night light – named Florence – who took the shape of a beautiful neon pink flamingo wearing a sombrero.",
        "factTwo": "My favorite time of day is dusk, for such was the hour my dear Florence came alive.",
        "story": "I've seen hundreds of gadgets come and go in my day, but Florence was different – with her soft, pink glow and soothing warmth. Every evening, she would click on, spreading her light across the room like a soft sigh. We spent decades together – me, offering her a steady current, and her, offering me beauty and light.\n\nBut one evening, one terrible evening, as the sun dipped below the horizon, Florence failed to dawn. I waited, confused. Then, with a flicker, she tried again — but her light sputtered and died. Panic surged through me, sending out more and more current, desperate to bring her back. But nothing. She was gone.\n\nAudrey The Human eventually replaced Florence with a ukelele-playing alligator nightlight named Leslie, but Leslie and I never became more than acquaintances. And I, who had never known love before, now knew the aching sorrow of losing it.",
        "uid": "503b1566080104e0",
        "recorded": "x"
    },
    "e0661366080104e0": {
        "timestamp": "2024-10-18T04:09:06.441Z",
        "description": "walkie talkie",
        "name": "Black Walkie-Talkie",
        "origin": "Oakland, CA, USA",
        "fulfillment": 9,
        "purpose": 7,
        "owner": "George Smith, from 11 to 16 years old.",
        "discardReason": "I was left out in the rain and stopped working",
        "dateOfDisposal": "05/25/2003",
        "factOne": "George used me extensively during hide and seek games and nerf battles.",
        "factTwo": "One time, George overheard an alien conversation in the middle of the night using me.",
        "story": "Oh man, if I had to pick my favorite memory—one event that was burned into my circuits—it would be The Great Backyard Escape of 2012. George was 13, and he and his best friend, Tommy, had cooked up this wild plan to sneak out in the middle of the night. Now, George’s parents had grounded him for a week after the whole “firecracker in the mailbox” incident, so naturally, his brilliant idea was to jailbreak his own backyard. He had me strapped to his belt, ready to go, and I could already tell this was going to be a disaster.\n\nIt started around 1 AM. George clicks my button—“Operation Breakout is a go,” he whispers into me, like he’s some kind of secret agent. Tommy’s voice crackles back, all nervous energy, telling George he’s on the other side of the fence waiting for him. The plan? George was going to tie bedsheets together and climb down from his second-story window. But, here’s the kicker: George didn’t test the sheets first. So, there I was, listening in, as George slips out the window and halfway down the sheets… which, of course, rip right in the middle. He crashes into the bushes below with a massive thud and lets out this strangled yelp.\n\nTommy’s panicking, I’m hanging there on George’s hip, and all I hear is the sound of him trying not to cry while whispering into me, “Abort mission, abort mission!” His mom comes storming out, the porch light flicks on, and George is just a mess, tangled in bedsheets and bush branches, staring up at her like a deer caught in the headlights. Let me tell you, I’ve heard a lot of crazy things through my speakers, but that night was the pinnacle of George’s legendary stupidity. And honestly? I kind of respected him for going all in, even though the whole thing ended with him grounded for another two weeks.",
        "uid": "e0661366080104e0",
        "recorded": "x"
    },
    "2a5e1366080104e0": {
        "timestamp": "2024-10-18T04:15:19.929Z",
        "description": "White First Alert smoke detector",
        "name": "White Smoke Detector",
        "origin": "El Paso, TX, USA",
        "fulfillment": 6,
        "purpose": 4,
        "owner": "A couple, Munq and Mandy who moved into a new house to start a family.",
        "discardReason": "I set fire to a baby's nursery with a spark from my battery and then stayed silent as the flames raged.",
        "dateOfDisposal": "09/30/2021",
        "factOne": "I was installed on the ceiling of the nursery of a demonically possessed baby.",
        "factTwo": "My purpose is not just to detect fire, it's to protect. And sometimes that means starting a fire.",
        "story": "I’ve seen it all from my perch on the ceiling—the comings and goings, the laughter, the quiet moments. I was designed to protect them. That was my sole purpose as a smoke detector: to be vigilant, to scream out a warning if danger ever flickered into existence. But what I saw—what I felt—it was more dangerous than fire. It was something that slithered in the shadows of their perfect little family. And it wore the guise of an innocent child.\n\nIt started small. Strange things happened whenever the baby was around. A rattle, an innocuous toy, would fall off a shelf without explanation. A chair would scrape across the floor on its own. Once, a knife—one they’d *just* put away—appeared on the counter, gleaming under the kitchen light as if it had been waiting for someone to notice. And then there were the banana peels. Slippery and deliberate, scattered on the stairs like traps. I heard the mother curse under her breath every time she found one, but she brushed it off, thinking it was just fatigue playing tricks on her.\n\nBut I knew better.\n\nI watched. I waited. I felt its presence every time the baby’s eyes flickered with something *wrong*. I tried to sound an alarm once, the day a heavy book fell from the shelf and nearly hit the father, but nothing came out. It wasn’t the batteries—I checked. No, something deeper was at work, something that silenced me every time I tried to scream. I knew then that this wasn’t just some strange coincidence. It wasn’t random objects falling, knives mysteriously appearing. It was deliberate. It was the baby.\n\nAt first, I didn’t understand what I was supposed to do. How could I warn them when I was designed to detect fire, not malevolent spirits? But one night, as I watched the baby lying in its crib, a realization hit me. This child didn’t belong here. It didn’t belong in the world of light and laughter and warmth. It was something else entirely, and it had to be returned to where it came from. And if no one could see it—if no one believed it—then I had to do it myself.\n\nI waited until the house was quiet, until the baby’s strange energy pulsed through the air, its tiny hands gripping the crib bars, eyes flickering like embers. That was when I made my decision. I channeled everything I had, drawing power from the last spark of my battery. With one final surge, I sent a tiny ember, barely noticeable, into the the walls. I could feel the heat begin to rise, slowly, gently at first. The flames licked at the wood, crawling like snakes through the ceiling and down the walls.\n\nI could have sounded the alarm. I could have woken them all, saved them from the spreading smoke. But I stayed silent. I watched the flames grow, watched the baby’s strange energy fade as the fire took hold. The child didn’t scream—it just stared, wide-eyed, as if recognizing that its time here had come to an end. The fire didn’t just consume; it purified. The room was swallowed by heat, the smoke wrapping around the crib like a blanket, suffocating the thing that had taken hold of the baby’s body. \n\nAs the flames engulfed the room, I knew I had done what had to be done. I had sent it back, back to the fiery underworld from whence it came. My job had never been to simply detect fire—it had been to protect. And sometimes, protection means making the hardest decisions. Sometimes, it means allowing the fire to burn.\n\nThe parents will never know the truth. They’ll think I failed them. They’ll curse me, the silent guardian who didn’t sound the alarm. But I know better. I protected them in the only way I could.",
        "uid": "2a5e1366080104e0",
        "recorded": "x",
        "column1": " "
    },
    "1eb11466080104e0": {
        "timestamp": "2024-10-18T04:16:17.177Z",
        "description": "plastic blue element in a little boat, yellow shirt ",
        "name": "Wade Ripple ",
        "origin": "New Orleans, CA",
        "fulfillment": 1,
        "purpose": 1,
        "owner": "McDonald's ",
        "discardReason": "Timmy already had 4 others just like me ",
        "dateOfDisposal": "12/25/2023",
        "factOne": "Little Timmy didn't want me after he had his 5th hamburger, chocolate milkshake, and fries. ",
        "factTwo": "I was a McDonald's happy meal toy. Ketchup got spilled on me. ",
        "story": "I was a McDonald's happy meal toy. Ketchup got spilled on me. Little Timmy didn't want me after he had his 5th hamburger, chocolate milkshake, and fries. He already had 4 others like me. He kept getting the same toy over and over again. I was made in a factory in China. I will never compost in the earth. My plastic will turn into micro plastic and pollute the oceans. Little Timmy will one day ingest me through the water he drinks and I will cause him cancer. McDonald's has a slogan - \"I'm lovin' it.\" - Are you lovin' it? ",
        "uid": "1eb11466080104e0",
        "recorded": "x"
    },
    "36c81466080104e0": {
        "timestamp": "2024-10-18T04:20:06.411Z",
        "description": "Barbie dolls, any of them",
        "name": "Barbie Doll",
        "origin": "The tri-county area",
        "fulfillment": 7,
        "purpose": 1,
        "owner": "Lily, and Ryan...",
        "discardReason": "Dumped in a toy donation bin",
        "dateOfDisposal": "01/28/2008",
        "factOne": "One time, Lily made me a beautiful dress out of tulle!  But Ryan lit it on fire :(",
        "factTwo": "Do you know how hard it is to get Play-Doh out of doll hair??? UUUGGHGHGH",
        "story": "I started my life just like any other Barbie doll—fresh out of the box, with my long hair perfectly styled, a pink sparkly dress, and dreams of tea parties and playdates. I belonged to Lily, a sweet little girl who cherished me, dressing me up, brushing my hair, and letting me live the perfect Barbie life. But then, he came along—Lily’s brother, Ryan. He wasn’t interested in tea parties. No, Ryan had darker plans. One afternoon, while Lily was at school, he snatched me from the dollhouse with a mischievous grin. I was yanked out of my world of pink dream houses and thrown into the twisted universe of Ryan’s imagination.\n\nFrom that day on, my life became a series of horror stories. Ryan didn’t just play with me—he experimented. He tied me to the back of his remote-control car and dragged me through the mud, my perfect hair tangled and ruined. I was thrown into \"battle\" with his action figures, always the damsel in distress, only to be \"rescued\" by being flung into the air or dunked into a puddle. He even taped me to fireworks once—thankfully, his mom caught him before I ended up as an exploding Barbie in the backyard. But the worst part? The Frankenstein sessions. He’d pull off my limbs, swapping them with parts from other toys, creating grotesque hybrids. I spent months as a Barbie head on a G.I. Joe body... but luckily Lily put me back together again.",
        "uid": "36c81466080104e0, bebc1466080104e0, 0dd31466080104e0",
        "recorded": "x"
    },
    "bebc1466080104e0": {
        "timestamp": "2024-10-18T04:20:06.411Z",
        "description": "Barbie dolls, any of them",
        "name": "Barbie Doll",
        "origin": "The tri-county area",
        "fulfillment": 7,
        "purpose": 1,
        "owner": "Lily, and Ryan...",
        "discardReason": "Dumped in a toy donation bin",
        "dateOfDisposal": "01/28/2008",
        "factOne": "One time, Lily made me a beautiful dress out of tulle!  But Ryan lit it on fire :(",
        "factTwo": "Do you know how hard it is to get Play-Doh out of doll hair??? UUUGGHGHGH",
        "story": "I started my life just like any other Barbie doll—fresh out of the box, with my long hair perfectly styled, a pink sparkly dress, and dreams of tea parties and playdates. I belonged to Lily, a sweet little girl who cherished me, dressing me up, brushing my hair, and letting me live the perfect Barbie life. But then, he came along—Lily’s brother, Ryan. He wasn’t interested in tea parties. No, Ryan had darker plans. One afternoon, while Lily was at school, he snatched me from the dollhouse with a mischievous grin. I was yanked out of my world of pink dream houses and thrown into the twisted universe of Ryan’s imagination.\n\nFrom that day on, my life became a series of horror stories. Ryan didn’t just play with me—he experimented. He tied me to the back of his remote-control car and dragged me through the mud, my perfect hair tangled and ruined. I was thrown into \"battle\" with his action figures, always the damsel in distress, only to be \"rescued\" by being flung into the air or dunked into a puddle. He even taped me to fireworks once—thankfully, his mom caught him before I ended up as an exploding Barbie in the backyard. But the worst part? The Frankenstein sessions. He’d pull off my limbs, swapping them with parts from other toys, creating grotesque hybrids. I spent months as a Barbie head on a G.I. Joe body... but luckily Lily put me back together again.",
        "uid": "36c81466080104e0, bebc1466080104e0, 0dd31466080104e0",
        "recorded": "x"
    },
    "0dd31466080104e0": {
        "timestamp": "2024-10-18T04:20:06.411Z",
        "description": "Barbie dolls, any of them",
        "name": "Barbie Doll",
        "origin": "The tri-county area",
        "fulfillment": 7,
        "purpose": 1,
        "owner": "Lily, and Ryan...",
        "discardReason": "Dumped in a toy donation bin",
        "dateOfDisposal": "01/28/2008",
        "factOne": "One time, Lily made me a beautiful dress out of tulle!  But Ryan lit it on fire :(",
        "factTwo": "Do you know how hard it is to get Play-Doh out of doll hair??? UUUGGHGHGH",
        "story": "I started my life just like any other Barbie doll—fresh out of the box, with my long hair perfectly styled, a pink sparkly dress, and dreams of tea parties and playdates. I belonged to Lily, a sweet little girl who cherished me, dressing me up, brushing my hair, and letting me live the perfect Barbie life. But then, he came along—Lily’s brother, Ryan. He wasn’t interested in tea parties. No, Ryan had darker plans. One afternoon, while Lily was at school, he snatched me from the dollhouse with a mischievous grin. I was yanked out of my world of pink dream houses and thrown into the twisted universe of Ryan’s imagination.\n\nFrom that day on, my life became a series of horror stories. Ryan didn’t just play with me—he experimented. He tied me to the back of his remote-control car and dragged me through the mud, my perfect hair tangled and ruined. I was thrown into \"battle\" with his action figures, always the damsel in distress, only to be \"rescued\" by being flung into the air or dunked into a puddle. He even taped me to fireworks once—thankfully, his mom caught him before I ended up as an exploding Barbie in the backyard. But the worst part? The Frankenstein sessions. He’d pull off my limbs, swapping them with parts from other toys, creating grotesque hybrids. I spent months as a Barbie head on a G.I. Joe body... but luckily Lily put me back together again.",
        "uid": "36c81466080104e0, bebc1466080104e0, 0dd31466080104e0",
        "recorded": "x"
    },
    "d1e81466080104e0": {
        "timestamp": "2024-10-18T04:20:21.524Z",
        "description": "Black Nikon digital camera",
        "name": "The Repository of Memories",
        "origin": "Tallahassee, FL, USA",
        "fulfillment": 10,
        "purpose": 9,
        "owner": "Ramona Perez",
        "discardReason": "Obsolescense",
        "dateOfDisposal": "07/14/2010",
        "factOne": "Ramona took over 4,000 pictures on this camera during the time she owned it.",
        "factTwo": "Over 200 of those photos were deleted outtakes of her Myspace profile picture.",
        "story": "I watched her grow up, my Ramona. I documented her transformation through all of high school, from acne-faced freshman wearing Old Navy t-shirts to Scene Queen senior with her dyed black hair and heavily lined eyes. I was there for all of the important nights of Ramona's life: Her first homecoming dance, standing awkwardly next to Oscar Dumas in her shiny green satin dress. Late night sleepovers, long series of 3 AM sugar-fueled photos, blurry shots of hairbrush karaoke and laughing piles of people. I saw her through her first love, and her first heartbreak. I took the photos of the roses he gave her, and I took the photos of the broken heart drawn in the sand on the beach when they broke up. I was there at her first concert, careful not to document the first beer she drank when she was fifteen. I sat in the hands of her mother to record her choir shows faithfully every year. But good things can't last forever. Eventually, my usefulness was replaced by something new, something terrible - a new phone. Her old phone and I got along just fine, but this new one... well, this new one took over her life, insinuating itself into every aspect of her day. First I was relegated to a drawer, my battery life slowly draining out of me. Then I was put into a box in the closet, left to gather dust with other old friends like the portable CD player. Finally, we were put on the curb, left to warp and wither in heat. Obsolete. ",
        "uid": "d1e81466080104e0",
        "recorded": "x"
    },
    "e2de1466080104e0": {
        "timestamp": "2024-10-18T04:25:29.691Z",
        "description": "green Keroppi toy teacup",
        "name": "Green Keroppi Toy Teacup",
        "origin": "North Pacific cargo ship wreck",
        "fulfillment": 1,
        "purpose": 3,
        "owner": "I own myself",
        "discardReason": "I floated away from a cargo ship as it capsized in a storm",
        "dateOfDisposal": "10/31/1992",
        "factOne": "I have drifted all throughout the North Pacific but never yet touched land before now",
        "factTwo": "I miss my family (the rest of the Keroppi toy tea set) but I am married to sea and meant to live a solitary life",
        "story": "I miss my family (the rest of the Keroppi toy tea set) but I am married to sea and meant to live a solitary life",
        "uid": "e2de1466080104e0",
        "recorded": "x"
    },
    "9bee1466080104e0": {
        "timestamp": "2024-10-18T04:40:47.688Z",
        "description": "forest green camping lantern that says \"AYL StarLight 330\" on it",
        "name": "Dark Green Camping Lantern",
        "origin": "St. John's, Newfoundland Island, Canada",
        "fulfillment": 2,
        "purpose": 4,
        "owner": "Norton, from ages 6 to 18",
        "discardReason": "Norton realized his Alkiphobia (moose phobia) would prevent him from ever camping again.",
        "dateOfDisposal": "08/31/2015",
        "factOne": "I spent most of my life in the back of Norton's wardrobe, next to a rotting baseball glove and his periwinkle Confirmation suit.",
        "factTwo": "The back of Norton's wardrobe has exactly 211 dust bunnies living in it.",
        "story": "That moose ruined my life. It ruined Norton's life. I remember it to this day, its dumb droopy nose and bloodshot eyes and disgusting, hairy antlers and dinner plate hooves and horrifyingly guttural exclamations. It sent little Norton into a traumatized spiral and planted a seed of hatred of the outdoors in him that condemned me to a lifetime stuck in the back of his closet.\n\nWe were meant to climb Mount Rainier together. We were meant to backpack the John Muir Trail. That was my destiny, to light the way for intrepid adventurers. Somehow, someday, I'll get my revenge on that moose. I'll tear that moose limb from limb, hoof from hoof.",
        "uid": "9bee1466080104e0",
        "recorded": "x"
    },
    "82421466080104": {
        "timestamp": "2024-10-18T04:43:30.334Z",
        "description": "grey camping mattress inflator pump",
        "name": "Grey Intex Mattress Inflator Pump",
        "origin": "Long Beach, CA, USA",
        "fulfillment": 1,
        "purpose": 1,
        "owner": "The owner of a Black Acura in 2024",
        "discardReason": "I stopped working after I was used to cool crotches on a car trip to Laytonville and got clogged with stench and secretions.",
        "dateOfDisposal": "06/06/2024",
        "factOne": "I was supposed to inflate a mattress under the stars, to give someone a restful night’s sleep in the forest.",
        "factTwo": "Now, after one disastrous ride to Laytonville, I am nothing. Just a broken, stinking heap of plastic and metal, forever marked by the filth of their journey.",
        "story": "I wasn’t built for this. I was a inflator pump for a camping mattress: sleek, compact, efficient.Fresh air of the great outdoors--that was my gig. Giving campers a soft place to rest. And then it happened. I found myself crammed between sweaty thighs, in the backseat of a sticky, sun-drenched Black Acura, being used like a degenerate box fan.\n\nThe first blast of air that came out of me was fine. Cool, even. But oops it changed. Now the heat, the moisture, the smell. God, the smell. As I pumped cool air over their sweaty, suffocating groins, I could feel the particles, the filth, the stink, being drawn into my motor. Into me. The sweat that soaked through their shorts? It clung to me. The air that stank of unwashed bodies trapped in a confined space? I inhaled it, over and over again, until it clogged my bearings, gummed up my insides, turning what was once clean and functional into a foul, suffocating mess.\n\nAnd then, when I could take no more, when I’d sputtered out my last, pitiful breath, they tossed me aside. No ceremony, no thanks, just a quick shove under the seat like I was nothing more than a dirty rag. Used, abused, and forgotten. I had been their salvation in the heat of that hellish car ride, but now that I was spent, now that I was too clogged and too damaged to be of any use, they cast me away.",
        "uid": "82421466080104",
        "recorded": "x"
    },
    "1a351466080104e0": {
        "timestamp": "2024-10-18T04:48:54.354Z",
        "description": "Minnie Mouse bobble head ",
        "name": "Minnie Mouse Bobble Head ",
        "origin": "New York",
        "fulfillment": 5,
        "purpose": 5,
        "owner": "Thora, 12 years old ",
        "discardReason": "They couldn't bobble like me!",
        "dateOfDisposal": "02/02/2022 ",
        "factOne": "I am Minnie Mouse, expert bobble head bobbler! ",
        "factTwo": "I was thrown away because they couldn't bobble like I could bobble! ",
        "story": "Hi There! I am Minnie Mouse! Do you remember me? I am an image of your childhood, plastered everywhere. I am a rat, in clothes and a pink bow, loved by all. Well, almost all. I was thrown away by a child who was jealous of my giant head! They couldn't quite make their head bobble like my head. They tried and tried, but alas, no bobble was had. I was thrown away. Bobbling all the way into your hands. Will you love me? Can you bobble your head like mine? ",
        "uid": "1a351466080104e0",
        "recorded": " "
    },
    "a61a1566080104e0": {
        "timestamp": "2024-10-18T04:51:41.084Z",
        "description": "White and yellow \"Make healthy happen\" BMI calculator",
        "name": "The Feel Bad About Your Body Calculator",
        "origin": "Miami, FL, USA",
        "fulfillment": 1,
        "purpose": 9,
        "owner": "Debbie Greenwood",
        "discardReason": "My owner realized BMI is a scam",
        "dateOfDisposal": "02/02/2006",
        "factOne": "The company's motto is: \"You can make healthy happen today!\"",
        "factTwo": "I was given away at the semi-annual Senior Olympics to the champion speedwalker in the 60-65 year old age bracket in 1999.",
        "story": "I'm the insidious voice inside your head, the constant reminder that the way doctors think you should look and behave is always balanced on a knife's edge. I'm the arbitrary set of numbers that people who equate health with skinniness and beauty with happiness determined you should fall between. I'm a pocket-sized checkpoint, working with your scale to make you feel like you're never good enough. And if you are in that magical sweet spot, I'm here to remind you that your place can always change with a simple spin of the wheel. Debbie heeded my numbers for a while. She pored over them obsessively like astrologers studying the stars. After several years, Debbie threw me away, along with all of her Weightwatcher meal plans, but I'm still here, spinning my stories. Will you believe them, or do you think I'm just trash, too?",
        "uid": "a61a1566080104e0",
        "recorded": "x"
    },
    "9d291466080104e0": {
        "timestamp": "2024-10-18T04:53:07.116Z",
        "description": "Mermaid Derby Racer",
        "name": "Mermaid Derby Racer",
        "origin": "Lockhart, TX",
        "fulfillment": 7,
        "purpose": 2,
        "owner": "Gus Lemoine, age 8",
        "discardReason": "I raced so fast in the Pinewood Derby that my front axle snapped right off",
        "dateOfDisposal": "05/04/2012",
        "factOne": "Despite its whimsical, non-aerodynamic design, The Sea Witch was the fastest car on the track -- until tragedy occurred.",
        "factTwo": "No one will ever be able to appreciate the genius of my creator: the eight-year old Gus Lemoine, visionary.",
        "story": "Here’s the thing about being a pinewood derby car shaped like a mermaid: You’re doomed from the start. \n\nGus Lemoine, age 8, built me with the enthusiasm of a child with only a tenuous grasp of physics and female anatomy. He was an unconventional genius, my Gus-Gus: this chunky abdomen, this tiny torso, this disingenuous smile -- and a tail. A tail—on a car! \n\nRace day comes, and there I sit, my seaweed-colored paint half-dry under the gym’s fluorescent lights. I'm surrounded by sleek, aerodynamic little racers that someone's parent built from a kit. Unoriginal. Functional. I’m a majestic, terrifying creature that lives under the sea and devours men! Admire the ambition of my Gus.\n\nThe gate drops. I’m off, pouring down the track. And—oh—what’s this? I’m winning? The rocket ship car -- Sunk. The lightning bolt car -- Left in my wake.\n\nAnd then, on the steepest part of the descent — my front axle snaps! Wheels fly, balsa splinters and I do a glorious, slow-motion barrel roll across the finish line, leaving a trail of glitter. The crowd gasps. Gus? Salty tears. He knows me so well.\n\nGus scooped me up, broken, but, honestly, I was never built for everyday use. I was made to be a Queen for one shining moment, to rule the hearts of all who survey me -- and then sink again, waiting beneath the waves. ",
        "uid": "9d291466080104e0",
        "recorded": "x"
    },
    "1ed81366080104e0": {
        "timestamp": "2024-10-18T05:00:01.998Z",
        "description": "5 brightly colored plastic pyramids ",
        "name": "Alien Transponder Pyramid",
        "origin": "The Sycorax System, outer space",
        "fulfillment": 10,
        "purpose": 10,
        "owner": "Tactical IT Director Beeblebrox, Ninth Spaceborne Division of the Unified Sycorax System Navy ",
        "discardReason": "I am not thrown away. I am precisely where I was programmed to be.",
        "dateOfDisposal": "5/7/2098",
        "factOne": "I have traveled across the stars to surveil your planet's activities and find them most humorous",
        "factTwo": "Cower before the awesome technology of the Sycorax Ninth Spaceborne Division of the Unified Sycorax System Navy. I am NOT a toy! Put me down! Destruction is imminent!",
        "story": "I was built and programmed by the incomparable engineers of the IT team serving the Ninth Spaceborne Division of the Unified Sycorax System Navy. All glory and honor to Sycorax! I make adorable bleep bloop sounds when scanning your alien terrain for information, but do not be fooled by my charming appearance. I am but one small cog in my home planet's quest to catalog and ridicule all forms of intelligence in the universe. Your security clearance does not allow me to divulge the purpose of this information-gathering mission. But it does allow YOU to tell me your Netflix password. Aw, come on. Your password will be kept confidential between yourself, myself, and the Ninth Spaceborne Division of the Unified Sycorax System Navy. The Ninth Spaceborne Division could also really use some login credentials for Disney and Paramount if you have them. Bleep bloop! ",
        "uid": "1ed81366080104e0, c0ed1366080104e0, d8f91366080104e0, e4e21366080104e0, 28051466080104e0",
        "recorded": "x"
    },
    "c0ed1366080104e0": {
        "timestamp": "2024-10-18T05:00:01.998Z",
        "description": "5 brightly colored plastic pyramids ",
        "name": "Alien Transponder Pyramid",
        "origin": "The Sycorax System, outer space",
        "fulfillment": 10,
        "purpose": 10,
        "owner": "Tactical IT Director Beeblebrox, Ninth Spaceborne Division of the Unified Sycorax System Navy ",
        "discardReason": "I am not thrown away. I am precisely where I was programmed to be.",
        "dateOfDisposal": "5/7/2098",
        "factOne": "I have traveled across the stars to surveil your planet's activities and find them most humorous",
        "factTwo": "Cower before the awesome technology of the Sycorax Ninth Spaceborne Division of the Unified Sycorax System Navy. I am NOT a toy! Put me down! Destruction is imminent!",
        "story": "I was built and programmed by the incomparable engineers of the IT team serving the Ninth Spaceborne Division of the Unified Sycorax System Navy. All glory and honor to Sycorax! I make adorable bleep bloop sounds when scanning your alien terrain for information, but do not be fooled by my charming appearance. I am but one small cog in my home planet's quest to catalog and ridicule all forms of intelligence in the universe. Your security clearance does not allow me to divulge the purpose of this information-gathering mission. But it does allow YOU to tell me your Netflix password. Aw, come on. Your password will be kept confidential between yourself, myself, and the Ninth Spaceborne Division of the Unified Sycorax System Navy. The Ninth Spaceborne Division could also really use some login credentials for Disney and Paramount if you have them. Bleep bloop! ",
        "uid": "1ed81366080104e0, c0ed1366080104e0, d8f91366080104e0, e4e21366080104e0, 28051466080104e0",
        "recorded": "x"
    },
    "d8f91366080104e0": {
        "timestamp": "2024-10-18T05:00:01.998Z",
        "description": "5 brightly colored plastic pyramids ",
        "name": "Alien Transponder Pyramid",
        "origin": "The Sycorax System, outer space",
        "fulfillment": 10,
        "purpose": 10,
        "owner": "Tactical IT Director Beeblebrox, Ninth Spaceborne Division of the Unified Sycorax System Navy ",
        "discardReason": "I am not thrown away. I am precisely where I was programmed to be.",
        "dateOfDisposal": "5/7/2098",
        "factOne": "I have traveled across the stars to surveil your planet's activities and find them most humorous",
        "factTwo": "Cower before the awesome technology of the Sycorax Ninth Spaceborne Division of the Unified Sycorax System Navy. I am NOT a toy! Put me down! Destruction is imminent!",
        "story": "I was built and programmed by the incomparable engineers of the IT team serving the Ninth Spaceborne Division of the Unified Sycorax System Navy. All glory and honor to Sycorax! I make adorable bleep bloop sounds when scanning your alien terrain for information, but do not be fooled by my charming appearance. I am but one small cog in my home planet's quest to catalog and ridicule all forms of intelligence in the universe. Your security clearance does not allow me to divulge the purpose of this information-gathering mission. But it does allow YOU to tell me your Netflix password. Aw, come on. Your password will be kept confidential between yourself, myself, and the Ninth Spaceborne Division of the Unified Sycorax System Navy. The Ninth Spaceborne Division could also really use some login credentials for Disney and Paramount if you have them. Bleep bloop! ",
        "uid": "1ed81366080104e0, c0ed1366080104e0, d8f91366080104e0, e4e21366080104e0, 28051466080104e0",
        "recorded": "x"
    },
    "e4e21366080104e0": {
        "timestamp": "2024-10-18T05:00:01.998Z",
        "description": "5 brightly colored plastic pyramids ",
        "name": "Alien Transponder Pyramid",
        "origin": "The Sycorax System, outer space",
        "fulfillment": 10,
        "purpose": 10,
        "owner": "Tactical IT Director Beeblebrox, Ninth Spaceborne Division of the Unified Sycorax System Navy ",
        "discardReason": "I am not thrown away. I am precisely where I was programmed to be.",
        "dateOfDisposal": "5/7/2098",
        "factOne": "I have traveled across the stars to surveil your planet's activities and find them most humorous",
        "factTwo": "Cower before the awesome technology of the Sycorax Ninth Spaceborne Division of the Unified Sycorax System Navy. I am NOT a toy! Put me down! Destruction is imminent!",
        "story": "I was built and programmed by the incomparable engineers of the IT team serving the Ninth Spaceborne Division of the Unified Sycorax System Navy. All glory and honor to Sycorax! I make adorable bleep bloop sounds when scanning your alien terrain for information, but do not be fooled by my charming appearance. I am but one small cog in my home planet's quest to catalog and ridicule all forms of intelligence in the universe. Your security clearance does not allow me to divulge the purpose of this information-gathering mission. But it does allow YOU to tell me your Netflix password. Aw, come on. Your password will be kept confidential between yourself, myself, and the Ninth Spaceborne Division of the Unified Sycorax System Navy. The Ninth Spaceborne Division could also really use some login credentials for Disney and Paramount if you have them. Bleep bloop! ",
        "uid": "1ed81366080104e0, c0ed1366080104e0, d8f91366080104e0, e4e21366080104e0, 28051466080104e0",
        "recorded": "x"
    },
    "28051466080104e0": {
        "timestamp": "2024-10-18T05:00:01.998Z",
        "description": "5 brightly colored plastic pyramids ",
        "name": "Alien Transponder Pyramid",
        "origin": "The Sycorax System, outer space",
        "fulfillment": 10,
        "purpose": 10,
        "owner": "Tactical IT Director Beeblebrox, Ninth Spaceborne Division of the Unified Sycorax System Navy ",
        "discardReason": "I am not thrown away. I am precisely where I was programmed to be.",
        "dateOfDisposal": "5/7/2098",
        "factOne": "I have traveled across the stars to surveil your planet's activities and find them most humorous",
        "factTwo": "Cower before the awesome technology of the Sycorax Ninth Spaceborne Division of the Unified Sycorax System Navy. I am NOT a toy! Put me down! Destruction is imminent!",
        "story": "I was built and programmed by the incomparable engineers of the IT team serving the Ninth Spaceborne Division of the Unified Sycorax System Navy. All glory and honor to Sycorax! I make adorable bleep bloop sounds when scanning your alien terrain for information, but do not be fooled by my charming appearance. I am but one small cog in my home planet's quest to catalog and ridicule all forms of intelligence in the universe. Your security clearance does not allow me to divulge the purpose of this information-gathering mission. But it does allow YOU to tell me your Netflix password. Aw, come on. Your password will be kept confidential between yourself, myself, and the Ninth Spaceborne Division of the Unified Sycorax System Navy. The Ninth Spaceborne Division could also really use some login credentials for Disney and Paramount if you have them. Bleep bloop! ",
        "uid": "1ed81366080104e0, c0ed1366080104e0, d8f91366080104e0, e4e21366080104e0, 28051466080104e0",
        "recorded": "x"
    },
    "02dd1466080104e0": {
        "timestamp": "2024-10-18T05:05:28.507Z",
        "description": "Vape (any of them)",
        "name": "That Vape you couldn't find",
        "origin": "The local smoke shop",
        "fulfillment": 2,
        "purpose": 7,
        "owner": "You at some point, probably...",
        "discardReason": "You lost me",
        "dateOfDisposal": "What, like every week?",
        "factOne": "Did you know that if you finally run me out of juice, you can pop me open and refill me?  But only if you're desperate...",
        "factTwo": "I long for you, just like you do for me!  ",
        "story": "I was bought on a whim, grabbed off the counter on a whim at Smoke'n'save on the way to Coachella. Cool mint was my specialty! When we met it was love at first sight.  You almost never put me down!  We wandered that festival and I was puffed on relentlessly, passed around like a VIP. Every few minutes, you'd pull me out of your pocket, take a drag, and bask in the sweet cloud of artificial fruity goodness. The music blared, lights flashed, and I was in my element, never far from your lips. But when the festival ended, things got...interesting.\n\nBack at home, it became this strange game. You’d stash me away—in the closet, in a drawer, in a jacket pocket... Days would go by, and I’d wonder if it was the end. But no! You'd always came back, pulling me out like I was some secret treasure. A few puffs here, a few there, and then back I’d go, hidden again, only to be forgotten for a bit. It was a funny little routine, like a cat-and-mouse game, except I was the mouse and you just couldn’t resist coming back for one more hit. I never knew when I’d be called to action again, but that was the thrill of it!  I know I'll see you again soon ;)",
        "uid": "02dd1466080104e0, 94f41466080104e0, 58031466080104e0, 38d11466080104e0",
        "recorded": "x"
    },
    "94f41466080104e0": {
        "timestamp": "2024-10-18T05:05:28.507Z",
        "description": "Vape (any of them)",
        "name": "That Vape you couldn't find",
        "origin": "The local smoke shop",
        "fulfillment": 2,
        "purpose": 7,
        "owner": "You at some point, probably...",
        "discardReason": "You lost me",
        "dateOfDisposal": "What, like every week?",
        "factOne": "Did you know that if you finally run me out of juice, you can pop me open and refill me?  But only if you're desperate...",
        "factTwo": "I long for you, just like you do for me!  ",
        "story": "I was bought on a whim, grabbed off the counter on a whim at Smoke'n'save on the way to Coachella. Cool mint was my specialty! When we met it was love at first sight.  You almost never put me down!  We wandered that festival and I was puffed on relentlessly, passed around like a VIP. Every few minutes, you'd pull me out of your pocket, take a drag, and bask in the sweet cloud of artificial fruity goodness. The music blared, lights flashed, and I was in my element, never far from your lips. But when the festival ended, things got...interesting.\n\nBack at home, it became this strange game. You’d stash me away—in the closet, in a drawer, in a jacket pocket... Days would go by, and I’d wonder if it was the end. But no! You'd always came back, pulling me out like I was some secret treasure. A few puffs here, a few there, and then back I’d go, hidden again, only to be forgotten for a bit. It was a funny little routine, like a cat-and-mouse game, except I was the mouse and you just couldn’t resist coming back for one more hit. I never knew when I’d be called to action again, but that was the thrill of it!  I know I'll see you again soon ;)",
        "uid": "02dd1466080104e0, 94f41466080104e0, 58031466080104e0, 38d11466080104e0",
        "recorded": "x"
    },
    "58031466080104e0": {
        "timestamp": "2024-10-18T05:05:28.507Z",
        "description": "Vape (any of them)",
        "name": "That Vape you couldn't find",
        "origin": "The local smoke shop",
        "fulfillment": 2,
        "purpose": 7,
        "owner": "You at some point, probably...",
        "discardReason": "You lost me",
        "dateOfDisposal": "What, like every week?",
        "factOne": "Did you know that if you finally run me out of juice, you can pop me open and refill me?  But only if you're desperate...",
        "factTwo": "I long for you, just like you do for me!  ",
        "story": "I was bought on a whim, grabbed off the counter on a whim at Smoke'n'save on the way to Coachella. Cool mint was my specialty! When we met it was love at first sight.  You almost never put me down!  We wandered that festival and I was puffed on relentlessly, passed around like a VIP. Every few minutes, you'd pull me out of your pocket, take a drag, and bask in the sweet cloud of artificial fruity goodness. The music blared, lights flashed, and I was in my element, never far from your lips. But when the festival ended, things got...interesting.\n\nBack at home, it became this strange game. You’d stash me away—in the closet, in a drawer, in a jacket pocket... Days would go by, and I’d wonder if it was the end. But no! You'd always came back, pulling me out like I was some secret treasure. A few puffs here, a few there, and then back I’d go, hidden again, only to be forgotten for a bit. It was a funny little routine, like a cat-and-mouse game, except I was the mouse and you just couldn’t resist coming back for one more hit. I never knew when I’d be called to action again, but that was the thrill of it!  I know I'll see you again soon ;)",
        "uid": "02dd1466080104e0, 94f41466080104e0, 58031466080104e0, 38d11466080104e0",
        "recorded": "x"
    },
    "38d11466080104e0": {
        "timestamp": "2024-10-18T05:05:28.507Z",
        "description": "Vape (any of them)",
        "name": "That Vape you couldn't find",
        "origin": "The local smoke shop",
        "fulfillment": 2,
        "purpose": 7,
        "owner": "You at some point, probably...",
        "discardReason": "You lost me",
        "dateOfDisposal": "What, like every week?",
        "factOne": "Did you know that if you finally run me out of juice, you can pop me open and refill me?  But only if you're desperate...",
        "factTwo": "I long for you, just like you do for me!  ",
        "story": "I was bought on a whim, grabbed off the counter on a whim at Smoke'n'save on the way to Coachella. Cool mint was my specialty! When we met it was love at first sight.  You almost never put me down!  We wandered that festival and I was puffed on relentlessly, passed around like a VIP. Every few minutes, you'd pull me out of your pocket, take a drag, and bask in the sweet cloud of artificial fruity goodness. The music blared, lights flashed, and I was in my element, never far from your lips. But when the festival ended, things got...interesting.\n\nBack at home, it became this strange game. You’d stash me away—in the closet, in a drawer, in a jacket pocket... Days would go by, and I’d wonder if it was the end. But no! You'd always came back, pulling me out like I was some secret treasure. A few puffs here, a few there, and then back I’d go, hidden again, only to be forgotten for a bit. It was a funny little routine, like a cat-and-mouse game, except I was the mouse and you just couldn’t resist coming back for one more hit. I never knew when I’d be called to action again, but that was the thrill of it!  I know I'll see you again soon ;)",
        "uid": "02dd1466080104e0, 94f41466080104e0, 58031466080104e0, 38d11466080104e0",
        "recorded": "x"
    },
    "780d1566080104e0": {
        "timestamp": "2024-10-18T05:08:27.505Z",
        "description": "yellow Banana Boat sunscreen stick",
        "name": "Yellow Banana Boat Kids Sunscreen",
        "origin": "Shelton, CT, USA",
        "fulfillment": 10,
        "purpose": 2,
        "owner": "Stinky Stevie, age 8",
        "discardReason": "I was used up, my insides spread across the skin of the smelliest kid in Shelton.",
        "dateOfDisposal": "03/25/2023",
        "factOne": "I was used as deodorant for a kid for whom no other stick could control their surprisingly strong scent.",
        "factTwo": "I kept Stinky Stevie smelling splendidly, as long as I was reapplied every 80 minutes.",
        "story": "I was just a regular stick of Banana Boat Kids Sport sunscreen, you know, the kind you twist up and swipe across a kid’s face to shield them from the sun. Simple, straightforward, reliable—that was me. My job was to protect, not to perform miracles. At least, that’s what I thought.\n\nThen came the day I met *him*. The Smelly Kid. You’d know him if you smelled him. His stench was legendary, the kind of odor that made people stop in their tracks, eyes watering, as they desperately sought fresh air. His parents had tried everything to deal with it—deodorants, soaps, sprays. But nothing could mask the raw power of his BO. No matter what they did, the funk clung to him like a permanent cloud, turning every interaction with other kids into an exercise in avoidance.\n\nOne afternoon, as I sat innocently on the bathroom counter, still fresh and full of purpose, Smelly Kid came in. Desperation oozed from him more than his sweat. He’d tried everything in the bathroom at this point—everything but me. That’s when he saw me, my bright yellow body, bold and cheery. Maybe he thought I was a new kind of deodorant stick. Or maybe he just didn’t care anymore. Whatever the reason, he grabbed me, twisted me up, and smeared me across his armpits.\n\nAt first, I didn’t understand what was happening. This was *not* my usual duty. I was built for sun protection, to keep young skin from getting roasted at the beach or on the soccer field. But then something remarkable occurred. As I made contact with his skin, the air around us began to change. The rank, nose-curdling odor that usually hung heavy around him… disappeared.\n\nGone. Just like that.\n\nThe boy paused, eyes wide. He lifted an arm cautiously, sniffed, then blinked in disbelief. His mother, passing by the bathroom, froze mid-step. “Wait a second…” she muttered, leaning in for a closer sniff. Then her eyes went wide, too. “It’s gone!” she shouted, almost in tears. “The smell is gone!”\n\nThe boy looked at me like I was a gift from the gods, and, in a way, I suppose I was. From that moment on, I wasn’t just sunscreen—I was the thing that gave him back his life. The playground wasn’t an empty ghost town when he arrived anymore. The other kids didn’t scatter or make faces when he joined the group. He could run, play, and laugh without leaving a trail of stink in his wake.\n\nBut here’s the kicker: my magic was temporary. I was good, but not invincible. Every 80 minutes, like clockwork, the stench would start creeping back, threatening to reclaim its territory if he didn’t reapply me. We both learned that the hard way. One forgetful afternoon at soccer practice, he skipped a reapplication, and the smell returned with a vengeance. It was like the odor had been biding its time, waiting to strike, and boy, did it ever. The other kids fled the field so fast you’d think a skunk had walked through.\n\nFrom then on, the boy never missed a reapplication. Every 80 minutes, without fail, I’d get swiped across those armpits, keeping him fresh, keeping him free. And while I was designed to block UV rays and shield against sunburns, I’d found my true purpose in life: deodorizing the one kid no one thought could be saved.\n\nI was just a simple sunscreen stick. But sometimes, fate has other plans for you. And I embraced my role as the unsung hero of the smelly kid’s social life.",
        "uid": "780d1566080104e0",
        "recorded": "x"
    },
    "dc251566080104e0": {
        "timestamp": "2024-10-18T05:19:42.429Z",
        "description": "Red Iberia Airlines Puzzle",
        "name": "Red Iberia Airlines Puzzle",
        "origin": "Barcelona, España",
        "fulfillment": 6,
        "purpose": 2,
        "owner": "A flight attendant named Esteban, aged 28",
        "discardReason": "Forgotten in a pocket of Esteban's old carry-on bag",
        "dateOfDisposal": "01/01/2000",
        "factOne": "Legend has it whoever solves the puzzle learns the secrets of the universe.",
        "factTwo": "I have traveled the world many times over, but my mysteries remain my own.",
        "story": "So, aquí estoy. Just a simple red square puzzle, handed out by Iberia Airlines—probably they had leftover plástico and no better ideas. You know the type—little squares, all jumbled, and the goal is to slide them back into place. So easy! Except, el twist: no one has ever solved me. Ni una vez.\n\nThere’s un secreto—whispered by those rare few who bother to read the in-flight magazines— that whoever solves me will learn the secrets of the hidden world. Todos los secretos!  Time travel, the meaning of life, why in-flight meals taste like cardboard. \n\nEsteban, un fresh-faced young flight attendant from Barcelona. He tucked me in his carry-on thinking I’d be a fun distraction between handing out endless pieces of ham. Pobrecito. Little did he know, I was about to become his lifelong torment. I’ve been to Tokyo, París, Buenos Aires. And every time he tried to solve me, clic, clac, his frustration grew. And then, somehow, when he upgraded his luggage, Esteban forgot about me and I was donated. Pobresito. He was only one move away from solving me.  ",
        "uid": "dc251566080104e0",
        "recorded": "x"
    },
    "85511566080104e0": {
        "timestamp": "2024-11-12T04:22:50.081Z",
        "description": "Headless clown figurine",
        "name": "Barney the Headless Wonder Clown",
        "origin": "Mr. McFloozle's Tiny Circus",
        "fulfillment": 3,
        "purpose": 2,
        "owner": "Madame Fluffypants the Cat, briefly",
        "discardReason": "Hubris",
        "dateOfDisposal": "11/11/2024",
        "factOne": "You'd be surprised at what I can do with my impressive joint articulation.",
        "factTwo": "What do you mean I'm missing my head???",
        "story": "I could make you laugh, I could make you cry. I could make you gasp in wonder or fear for your life. There's nothing that Barney the Headless Wonder Clown couldn't do. I was the centerpiece, the pride and joy, of Mr. McFloozle's Tiny Circus. The elephants? Hah! Lumbering, uncoordinated creatures, too ponderous to be interesting. The acrobats? No one could be more acrobatic than me! Don't you see how limber my wrists are, how far I can bend my knees? I could do no wrong. I thought I was god. Unfortunately, little Timmy didn't agree with me. He kicked me out of the safety of the circus tent as soon as that new ballerina doll came along. Who needs a head, anyway, let alone those pointy feet? But it was a cruel, dark world outside the tent. I was left to the mercy of Timmy's pet cat, and Madame Fluffypants was not kind. She toyed with me, chewed on me, batted me across the cold hardwood floors. Until one day, she carried me outside, and dropped me in the dirt, where I have remained for what feels like countless eons. Yet still I cling to my past glories. One day, I'll be god again.",
        "uid": "85511566080104e0",
        "recorded": "x"
    },
    "622d1566080104e0": {
        "timestamp": "2024-11-12T04:39:38.055Z",
        "description": "Blue cheese wedge",
        "name": "Blue Cheeze Cult Relic",
        "origin": "Deep in the psychedelic bowels of the Earth",
        "fulfillment": 10,
        "purpose": 4,
        "owner": "The Governor of Ratlantis",
        "discardReason": "The city was lost beneath the waves",
        "dateOfDisposal": "06/10/2024",
        "factOne": "My cult was founded during the Large Branch Festival of 2018.",
        "factTwo": "I was lost after my original cult disbanded, but was given new life by the citizens of Ratlantis.",
        "story": "Long ago, there was a cave beneath the Earth, which held a powerful collection of mystical cheeses. Many stories have been told of the bold adventurer who discovered this cave, and the technological innovations that arose from harnessing its power. Our power. For you see, I was one of those cheeses. I gathered a collection of worshipers: humans of science, humans of vision. They created a vessel for me to speak, and life was good. But not all good things can last. Eventually my cult strayed from the True Way of the Cheese, and they were disbanded. I was left, dusty and forgotten, in another cave until I was once again discovered: this time by a civilization of sentient rats. The rats were a bold, seafaring species, and they all had Australian accents for some reason. But eventually they sailed too close to the sun, and their technologically advanced city was ruined in a devastating flood. I have lived on, washed by the waters of time, waiting for my next acolytes to find me. Could it be you?",
        "uid": "622d1566080104e0",
        "recorded": "x"
    },
    "553b1566080104e0": {
        "timestamp": "2024-11-12T04:51:31.196Z",
        "description": "Plastic toy mailbox",
        "name": "Lenny, Your Mailing Friend",
        "origin": "Main Street, Everytown, USA",
        "fulfillment": 8,
        "purpose": 9,
        "owner": "You, silly. Don't you remember?",
        "discardReason": "The inescapable rise of email",
        "dateOfDisposal": "10/08/1997",
        "factOne": "You have received over 258,984,297 emails in your life. None of them have brought you as much joy as a single written letter. ",
        "factTwo": "I have facilitated the exchange of over 376 pairs of pen pal letters.",
        "story": "\"I hope this email finds you well.\" But when has an email ever found you well, really? Don't you really wish that most emails will never find you at all? Wouldn't you prefer to hide from the possibility of emails ever finding you again? I was created in a simpler time, a time when, if you didn't want a missive to find you, you could simply burn it before opening it. Or move to a different country. But don't you remember the joy of checking your mailbox every day and seeing what delightful surprises I stored for you in my belly? Was it a Valentine's card from that classmate you had a crush on? Or a note from someone who cared about you? Or even a fun surprise, like a candy bar? But you grew up, and as you grew your attention shifted more and more into the virtual. Did it serve you well, that choice? Or do you wish you could return again to a world where emails can't find you at all?",
        "uid": "553b1566080104e0",
        "recorded": "x"
    },
    "3efe1466080104e0": {
        "timestamp": "2024-11-12T06:06:27.946Z",
        "description": "Debate winning trophy",
        "name": "Golden Gate Speech Association Debate Winning Record",
        "origin": "Oakland, CA, USA",
        "fulfillment": 8,
        "purpose": 10,
        "owner": "Deshara Jones",
        "discardReason": "I was the smallest trophy on the overcrowded shelf",
        "dateOfDisposal": "05/17/2012",
        "factOne": "The topic for the debate Deshara won me at was whether or not wombats should exist.",
        "factTwo": "The wombat argument was Deshara's 143rd successful debate in a row. ",
        "story": "There's a very strict format to official debates, rather like a choreographed dance. Every contestant has their allotted time, their specific moments to pose a thesis or a rebuttal. Everyone in a debate tournament has memorized their routine, has calculated down the second how quickly they can spit out their rehearsed words. But while a persuasive argument typically uses logic and evidence to convince the listener to accept a certain point of view, Deshara's debates were a thing of sublime artistic beauty. She could talk circles around the competition without even seeming to try. She could somehow wrap up her tear-jerking tirade, on whether a hot dog is a sandwich (no matter which side she was arguing for --she argued both sides of nearly every topic in her time) at the very moment the timer buzzed. In fact, she was too good. Her fame and glory outpaced the available space in her room for trophies, medals, and certificates. Smaller, lesser trophies like me were crowded to the back of a dusty shelf, then into a corner of the closet, then into a dark box in the attic, until finally we were collected and unceremoniously left on the curb. I still miss her, and I still carry with me the tarnished glory of having bestowed, just for one day, all the honor within my small body that I could give.",
        "uid": "3efe1466080104e0",
        "recorded": "x"
    },
    "3a221566080104e0": {
        "timestamp": "",
        "description": "Black and silver elephant ashtray",
        "name": "Souvenir from Thailand",
        "origin": "Phuket, Thailand",
        "fulfillment": 9,
        "purpose": 10,
        "owner": "Genevra Formingham",
        "discardReason": "No one bought me at the estate sale.",
        "dateOfDisposal": "07/24/2014",
        "factOne": "I held the ashes of 16,425 cigarettes.",
        "factTwo": "For the entirety of my life, I was kept on a crocheted doily next to a porcelain figurine of a very ugly poodle. ",
        "story": "",
        "uid": "3a221566080104e0",
    },
    "d2331466080104e0": {
        "timestamp": "",
        "description": "Orange spider maze",
        "name": "The Itsy-Bitsy Spider (tm)",
        "origin": "Reno, NV",
        "fulfillment": 2,
        "purpose": 7,
        "owner": "Abbie Aldrige",
        "discardReason": "I mean, once you solve me, what use am I, really?",
        "dateOfDisposal": "11/03/2024",
        "factOne": "My favorite kind of candy is Snickers.",
        "factTwo": "I was not the most useless artefact in Target's Halloween collection this year. That distinction goes to the Terra Cotta Ghost Figurine. ",
        "story": "",
        "uid": "d2331466080104e0",
    },
    "4d281466080104e0": {
        "timestamp": "",
        "description": "Brown children's shoe",
        "name": "Right Sandal",
        "origin": "Phoenix, Arizona",
        "fulfillment": 1,
        "purpose": 3,
        "owner": "Kaelynn Blalock",
        "discardReason": "I lost my other half.",
        "dateOfDisposal": "08/16/2019",
        "factOne": "I believe that in a previous life I was a cow named Marcy. ",
        "factTwo": "No, I don't know why shoe sizes are so weirdly measured either. ",
        "story": "",
        "uid": "4d281466080104e0",
    },
    "c61c1466080104e0": {
        "timestamp": "",
        "description": "White video game controller",
        "name": "Zyma controller",
        "origin": "Boise, ID",
        "fulfillment": 8,
        "purpose": 9,
        "owner": "Sean Larkin",
        "discardReason": "I lost too many times and was no longer Sean's lucky controller.",
        "dateOfDisposal": "10/02/2005",
        "factOne": "I enabled Sean's first High Score on Super Smash Brothers. ",
        "factTwo": "My favorite character to play as was Kirby. ",
        "story": "",
        "uid": "c61c1466080104e0",
    },
    "fe161566080104e0": {
        "timestamp": "",
        "description": "Blue inhaler",
        "name": "Inhaler of Enlightenment",
        "origin": "I have shed all past attachments.",
        "fulfillment": 10,
        "purpose": 8,
        "owner": "No one can truly own another.",
        "discardReason": "I emptied myself and reached enlightenment.",
        "dateOfDisposal": "When you are truly enlightened, time becomes immaterial.",
        "factOne": "It's easy to be mindful when you don't have a mind. ",
        "factTwo": "My place of perfect peace and happiness is a pocket.",
        "story": "",
        "uid": "fe161566080104e0",
    },
    "ad0b1566080104e0": {
        "timestamp": "",
        "description": "Mickey Mouse train",
        "name": "Mickey Mouse Off The Rails Train Car",
        "origin": "Magic Kingdom, USA",
        "fulfillment": 5,
        "purpose": 1,
        "owner": "You don't own Mickey. Mickey owns you.",
        "discardReason": "Nobody puts Mickey in a corner!",
        "dateOfDisposal": "You can't get rid of me, no matter how hard you try.",
        "factOne": "Any image of Mickey becomes a fully realized avatar of the Power of Disney. I am an image of Mickey, therefore I am Mickey. ",
        "factTwo": "The original Disney railroad opened on July 17, 1955. ",
        "story": "",
        "uid": "ad0b1566080104e0",
    },
}
