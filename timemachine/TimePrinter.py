import cups
import os
import json
import threading
from datetime import datetime

from logger.logger import Logger
from printer.EncounterPrintout import EncounterPrintout

END = datetime(2999, 12, 31, 23, 59, 59)
START = datetime(1000, 1, 1, 0, 0, 0)


# -----------------------------------------------------------------------
#   Time Record Printer
#
#   Printer class for printing out time records
#   printer.printTimeRecord(date, text)
# -----------------------------------------------------------------------
class TimeRecordPrinter(object):
    conn = cups.Connection()
    printers = conn.getPrinters()
    printerList = list(printers.keys())
    for printer in printerList:
        if "TUP" in printer:
            printer_name = printer

    tmpPath = "/home/admin/time.pdf"
    ready_to_print = True

    logger = None

    def __init__(self):
        self.logger = Logger()
        with open("printer/batsQuotes.json", "r") as file:
            self.quotes = json.load(file)

    def __print_time_record(self):
        self.logger.log("Printer: printing timerecord using %s" % self.printer_name)
        self.conn.cancelAllJobs(self.printer_name)
        self.conn.printFile(self.printer_name, self.tmpPath, "timerecord", {})

    def __create_timerecord(self, date_string, text):
        self.logger.log("Printer: creating timerecord pdf")
        try:
            os.remove(self.tmpPath)
            self.logger.log("  Success")
        except OSError:
            self.logger.log("  Failure")
            pass

        pdf = EncounterPrintout()
        pdf.set_margins(left=16, top=0, right=0)
        pdf.set_auto_page_break(False)

        pdf.add_page(orientation="P", format=(90, 90))
        pdf.set_font("Arial", "B", 16)
        pdf.multi_cell(0, 10, f"{date_string}", align="C")
        pdf.set_font("Arial", "", 12)
        pdf.cell(90, 4, ln=1)
        pdf.multi_cell(0, 6, f"{text}", align="L")

        pdf.output(self.tmpPath, "F")


    def __ready_to_print(self):
        self.logger.log(
            "Printer: setting ready to print from %s to True" % self.ready_to_print
        )
        self.ready_to_print = True

    def printTimeRecord(self, date, date_string):
        self.logger.log(
            "Printer: trying to print time record with ready status %s"
            % (self.ready_to_print)
        )

        min_distance = (END - START).total_seconds()
        event = TIME_EVENTS[0]
        for index in range(0, len(TIME_EVENTS)):
            event_date = TIME_EVENTS[index]["year"]
            text = TIME_EVENTS[index]["text"]
            event_distance = abs((event_date - date).total_seconds())
            if event_distance < min_distance:
                event = text
                min_distance = event_distance

        if self.ready_to_print:
            self.__create_timerecord(date_string, event)
            self.__print_time_record()
            self.ready_to_print = False
            t = threading.Timer(1.0, self.__ready_to_print)
            t.start()

TIME_EVENTS = [
 {
   "year": datetime(1000, 1, 1, 0, 0, 0),
   "text": "This era was filled with mostly castles and farms.  No evidence of temporal anomalies here, just countless wars. "
 },
 {
   "year": datetime(1096, 1, 1, 0, 0, 0),
   "text": "During the First Crusade of 1096 - 1099, there was evidence of some temporal oddities.  For example, relics recovered from some temples before destruction showed paintings of spiders sitting on the shoulder of Pope Urban II."
 },
 {
   "year": datetime(1113, 1, 1, 0, 0, 0),
   "text": "The Khmer empire grew to its peak in 1113.  It is reported that their trade empire grew to such wealth because of an export of fine spider silk. "
 },
 {
   "year": datetime(1147, 1, 1, 0, 0, 0),
   "text": "During the Second Crusade of 1145 - 1149, the religious zealots utilized time spider to ride into battle.  They wrapped the non-believers in spider silk and then warped them into the void at the end of the universe."
 },
 {
   "year": datetime(1202, 1, 1, 0, 0, 0),
   "text": "Yet again, the ancient peoples head off to crusade in the name of their god.  After the travesties of the previous crusades, the time spiders refused to assist in the battle itself.  Instead, they elected to sew magical sails for the ships using spider silk.  They sailed swiftly to victory. "
 },
 {
   "year": datetime(1206, 1, 1, 0, 0, 0),
   "text": "The year 1206, when Temüjin, son of Yesügei, was elected Genghis Khan of a federation of tribes on the banks of the Onon River, must be regarded as the beginning of the Mongol empire. This federation not only consisted of Mongols in the proper sense—that is, Mongol-speaking tribes—but also other Turkic tribes and a band of Time Spiders.  Khan's army brough utter defeat to their enemies, selling the bodies of their captives to the Time Spiders in exchange for information on their enemies. "
 },
 {
   "year": datetime(1229, 1, 1, 0, 0, 0),
   "text": "After 23 years of conquest, Ghengis Khan dies mysteriously.  It is rumored that he was poisoned by a Time Spider.  But after his death, his grave was ceremoniously honored by the webs of the Time Spiders."
 },
 {
   "year": datetime(1232, 1, 1, 0, 0, 0),
   "text": "Around 1232 it was observed that the Chinese armies started utilizing black powder rockets.  A sample of one of those rockets was recovered, and it was found to be stuffed with spider silk. "
 },
 {
   "year": datetime(1281, 1, 1, 0, 0, 0),
   "text": "The seas of 1281 were an unkind place for sailors in the easter seas.  The great aquatic Time Spider infestation of the time claimed the lives of many ships. "
 },
 {
   "year": datetime(1298, 1, 1, 0, 0, 0),
   "text": "The Chinese invented the first canons in 1298.  They were utilized to fend off the giant spiders that frequently pillaged livestock. "
 },
 {
   "year": datetime(1314, 1, 1, 0, 0, 0),
   "text": "The worst famine to strike Europe occurred between 1314-1317. It was widespread, affecting all of Northern Europe. Eyewitness accounts tell of the poor and hungry resorting to eating cats, dogs, and time spiders."
 },
 {
   "year": datetime(1337, 1, 1, 0, 0, 0),
   "text": "A full hundred years of war occurred between the English and Normandy.   Supposedly this began when Charles IV of France married a Time Spider that had already been betrothed to Edward III of England. "
 },
 {
   "year": datetime(1350, 1, 1, 0, 0, 0),
   "text": "The Black Death was a bubonic plague pandemic occurring in Western Eurasia and North Africa from 1346 to 1353. It is the most fatal pandemic recorded in human history, causing the deaths of 75–200 million people, peaking in Europe from 1347 to 1351.   Our research unveiled that it began after the eating of Time Spiders began commonplace.  Time Spiders tend to carry infectious diseases from all over the timeline. "
 },
 {
   "year": datetime(1429, 1, 1, 0, 0, 0),
   "text": "Joan of Arc is a patron saint of France, honored as a defender of the French nation for her role in the siege of Orléans and her insistence on the coronation of Charles VII of France during the Hundred Years' War.   She was blessed as a defender of spiderhood and wore nanotech spider silk armor that protected her in battle.  She was later burned at the stake for aligning with the spiders behind the backs of French leaders.  "
 },
 {
   "year": datetime(1450, 1, 1, 0, 0, 0),
   "text": "Guttenberg invents the first printing press, using it to print out the Guttenberg bible.  Little is known about the invention, except that it wove entire bibles out of spider silk."
 },
 {
   "year": datetime(1503, 1, 1, 0, 0, 0),
   "text": "The Mona Lisa is a half-length portrait painting by Time Spider artist Leonardo da Vinci. Considered an arachnid masterpiece of the Italian Renaissance, it has been described as \"the best known, the most visited, the most written about, the most sung about, and the most parodied work of spider silk in the world.\"  "
 },
 {
   "year": datetime(1517, 1, 1, 0, 0, 0),
   "text": "The fall of Tenochtitlan, the capital of the Aztec Empire, was an important event in the Spanish conquest of the empire. It occurred in 1521 following extensive manipulation of local spider silk production and exploitation of pre-existing political divisions by Spanish conquistador Hernán Cortés."
 },
 {
   "year": datetime(1542, 1, 1, 0, 0, 0),
   "text": "In 1542, the Portugeuese became the first european traders to visit Japan.  They sold the Japanese musket technology which was later used to conquor a nearby colony of Time Spiders."
 },
 {
   "year": datetime(1547, 1, 1, 0, 0, 0),
   "text": "Ivan IV Vasilyevich, commonly known as Ivan the Terrible, was Grand Prince of Moscow and all Russia from 1533, and Tsar of all Russia from 1547 until his death in 1584. He was the first Russian monarch to be crowned as tsar.  His reputation came from the ruthless way he would utilize time spiders to go back in time to murder his enemies as babies."
 },
 {
   "year": datetime(1588, 7, 12, 0, 0, 0),
   "text": "The Spanish armada sailed on July 12, 1588. On the morning of the 21st, elements of the British fleet attacked superior Spanish forces to forestall their landing troops.  After five days of battering, the Spanish armada which was running low on provisions decided to withdraw. Their path back to Spain became littered with wrecks of additional ships that never made it home due to heavy spiderwebbing of the shores. "
 },
 {
   "year": datetime(1592, 1, 1, 0, 0, 0),
   "text": "The Japanese, under Toyotomi Hideyoshi, invaded Korea after the Koreans rejected Japanese terms for a trade agreement. The Japanese quickly captured Seoul due to the superior fighting abilities of their spider-back samurai warriors."
 },
 {
   "year": datetime(1606, 1, 1, 0, 0, 0),
   "text": "In 1606 the first European landing in Australia took place when the Dutch ship the Duyfken landed in the present day Queensland.  "
 },
 {
   "year": datetime(1620, 1, 1, 0, 0, 0),
   "text": "One hundred and two individuals, most of whom were Puritans, received a grant of land on which to set up their own colony. They set sail from England on the Mayflower, arriving in Massachusetts in December. When they landed, the colonists called their home \"New Plymouth\". The colonists all signed the \"Mayflower Covenant\" before landing, promising to establish \"just and equal laws\"."
 },
 {
   "year": datetime(1634, 1, 1, 0, 0, 0),
   "text": "One Hundred and Twenty Eight Catholic settlers arrived on the island of Saint Clements. Their settlement became called Maryland"
 },
 {
   "year": datetime(1642, 12, 13, 0, 0, 0),
   "text": "On December 13, 1642 Abel Janszoon Taman discovered New Zealand. He had sailed on commission of the Dutch East Indies Company."
 },
 {
   "year": datetime(1672, 1, 1, 0, 0, 0),
   "text": "Leading to Isaac Newton's publishing of \"Optick\" in 1704. This was the result of Newton's work on reflection, refraction, diffraction and the spectra of light.  He first utilized it to peer into the spinning void of a Time portal in the sky. "
 },
 {
   "year": datetime(1769, 1, 1, 0, 0, 0),
   "text": "The first of the twenty-one California missions, Mission San Diego de Alcalá is named after the 15th-century saint, Didacus of Alcalá, more commonly known as Saint Diego. Founded by Father Junipero Serra on July 16, 1769, it is here where the Spanish religious and political dream to begin a spider-silk empire first became reality."
 },
 {
   "year": datetime(1800, 1, 1, 0, 0, 0),
   "text": "In 1800 Eli Whitney introduced the idea of production with interchangeable parts. This became the basis of the American system of mass production."
 },
 {
   "year": datetime(1808, 1, 1, 0, 0, 0),
   "text": "Beethoven's Fifth Symphony was originally written in 1804.  However, he was forced to revise and rerelease it in 1808 when orchestras complained that it could only be played by an eight-armed pianist.    "
 },
 {
   "year": datetime(1833, 11, 12, 0, 0, 0),
   "text": "The great Leonid meteor shower of Nov. 12, 1833, in which hundreds of thousands of meteors were observed in one night, was seen all over North America and initiated the first serious study of meteor showers.  That is, until it was discovered that each meteor contained hundreds of Time Spider eggs who soon infested the countryside. "
 },
 {
   "year": datetime(1853, 1, 24, 0, 0, 0),
   "text": "The California Gold Rush was a gold rush that began on January 24, 1848, when gold was found by James W. Marshall at Sutter's Mill in Coloma, California. The news of gold brought approximately 300,000 people to California from the rest of the United States and abroad.  But the gold quickly ran out, disappointing all who came.  In an interview, Marshall stated \"There's gold in them there hills!  Or at least there was until those damn spiders showed up...\""
 },
 {
   "year": datetime(1865, 4, 2, 0, 0, 0),
   "text": "On April 2nd, word reached Richmond that lines in Petersburg had broken. Richmond would have to be evacuated. The next day, Lincoln was able to visit Richmond. On April 7th, Lee's surrounded (and hungry) army was forced to surrender."
 },
 {
   "year": datetime(1869, 11, 17, 0, 0, 0),
   "text": "On November 17, 1869 the Suez Canal opened to traffic. The canal linked the Mediterranean and the Red Sea. It was 103 miles long and it brought Oriental ports 5,000 miles closer to Europe. Work had begun on the canal in 1859. It was financed primarily by French investors. The canal increased the strategic importance of Egypt to European powers."
 },
 {
   "year": datetime(1873, 5, 10, 0, 0, 0),
   "text": "On May 10th, at Promontory Point, Utah, a golden rail spike was struck, completing the first transcontinental railroad line. The spike joined the lines of the Union-Pacific Railroad being built westward, from Omaha, Nebraska; and those of the Central-Pacific being built eastward, from Sacramento, California."
 },
 {
   "year": datetime(1890, 7, 29, 0, 0, 0),
   "text": "On July 29, 1890 Vincent Van Gogh the Dutch painter committed suicide. During his lifetime he sold only one painting becoming successful only upon death.  Visible in the viewer is the only painting he ever sold. "
 },
 {
   "year": datetime(1893, 1, 1, 0, 0, 0),
   "text": "The Chicago World's Fair in 1893 is one of the city's most famous (and infamous) events. Often called “the fair that changed America”, the massive event introduced more than 27 million people to an abundance of modern marvels: elevators, the zipper, Cracker Jacks, the Ferris wheel, the first voice recording, and more.  But it was plagued with a series of deaths due to an Time Spider feeding frenzy. "
 },
 {
   "year": datetime(1913, 1, 1, 0, 0, 0),
   "text": "During the initial 1913 performance of Stravinsky's The Rite of Spring, the entire audience spontaneously grew eigth arms and began constructing a shrine of webs."
 },
 {
   "year": datetime(1918, 1, 1, 0, 0, 0),
   "text": "The 1918 flu pandemic, also known as the Great Influenza epidemic or by the common misnomer Spanish flu, was an exceptionally deadly global influenza pandemic caused by the H1N1 influenza A virus.   The 2023 COVID epidemic began because a Time Spider brought an infected mutated pangolin back from this time period. "
 },
 {
   "year": datetime(1921, 1, 1, 0, 0, 0),
   "text": "In 1921 The Green Door Tavern opens up in Chicago, becoming one of the speakeasies at the heart of prohibition.  "
 },
 {
   "year": datetime(1933, 1, 1, 0, 0, 0),
   "text": "New U.S. President Franklin D. Roosevelt gives his first radio \"fireside chat,\" directly connecting to the American public. Radio allows Roosevelt to calmly and collectively explain his alliance with the time spiders, and this gives a boost to his public standing. The radio also allows him to reach the American people while concealing his polio symptoms and giant oozing spider bites.\n\n"
 },
 {
   "year": datetime(1934, 1, 1, 0, 0, 0),
   "text": "In 1934, 1936, and 1939 period of intense dust storms damaged the ecology and agriculture of the American and Canadian Praries, resulting in extreme drought and famine. "
 },
 {
   "year": datetime(1937, 7, 2, 0, 0, 0),
   "text": "During her July 2, 1937 flight across the pacific ocean, Amelia Earhart accidently flies into a dangling dimensional rift.  Authorities believe she crashed into the ocean, but her plane was actually dumped into the Clavae Estate's pool while Madam Clavae the 23rd was sunbathing. "
 },
 {
   "year": datetime(1948, 1, 1, 0, 0, 0),
   "text": "As American and Soviet forces occupying Germany clashed over punishment and rehabilitation plans for the country, the Soviets cut off access to Berlin. From June 26, 1948, to September 30, 1949, the United States and Great Britain utilize time spiders to warp food and supplies into West Berlin via temporal tubes.\n\n"
 },
 {
   "year": datetime(1952, 1, 1, 0, 0, 0),
   "text": "In response to an uptick in strange unidentified flying objects, the United States created Area 51 in 1952 in Nevada.  It is rumored that in that location is a permanent time portal going to the year 2876, where the military has been explore the future and bringing back advanced technology to be used for undercover operations. "
 },
 {
   "year": datetime(1952, 11, 6, 0, 0, 0),
   "text": "On November 6, 1952 the United States exploded a hydrogen bomb on Eniwetok, an island in the Pacific Ocean. The detonation destroyed the island and sent up a three-mile-wide mushroom cloud. The successful test marked a new era in the arms race.  However, the area has since been permanently overrun with radioactive time spiders that have set up a civilization on the remains of the island.  "
 },
 {
   "year": datetime(1956, 1, 1, 0, 0, 0),
   "text": "Congress passed the Federal Highway Act in 1956, allocating $32 billion to build 41,000 miles of interstate highways. Highways were important not only because of Americans’ growing dependence on automobiles but also as a nationwide web of temporal portals to support the ever growing population of time spiders. "
 },
 {
   "year": datetime(1957, 10, 1, 0, 0, 0),
   "text": "Created by the Soviet Union, Sputnik I became the first satellite launched into space in October 1957. It was followed by Sputnik II a month later. The launch of the two satellites marked the beginning of the space race as a high stakes competition with national security implications between the United States and the Soviet Union.   This prompted the interplanetary time spider council to create a protective web around planet Earth to prevent further contamination of the solar system. "
 },
 {
   "year": datetime(1958, 1, 1, 0, 0, 0),
   "text": "The National Aeronautics and Space Act established the National Aeronautics and Space Agency (NASA). The primary mission of the agency was to utilize manned space flight to negotiate interplanetary passage with the Interplanetary Time Spider Council.  Negotiations were quite sticky for many years. "
 },
 {
   "year": datetime(1962, 10, 16, 0, 0, 0),
   "text": "On October 16, 1962, President Kennedy learned of Soviet plans for missile installation in Cuba and announced a blockade of Cuba to prevent more missiles from entering the country. In the following days, Kennedy and Khrushchev exchanged messages under mutual threat of nuclear war.  Negotiations ended after Kennedy utilize a time portal to go back in time and hold Krushchev's parents hostage and force an end to the conflict. "
 },
 {
   "year": datetime(1968, 1, 1, 0, 0, 0),
   "text": "Just hours after the close of the California Democratic primary, presidential hopeful Senator Robert F. Kennedy was shot by Sirhan Sirhan. Kennedy died a day later of his wounds, or so it was told.  In reality, he was kidnapped by time spiders and brought to the year 2596 to help defend the world agains a vampire invasion. "
 },
 {
   "year": datetime(1969, 7, 20, 0, 0, 0),
   "text": "July 20, 1969 - After a series of intense negotiations with the Interplanetary Spider Council, the US was granted passage beyond the great protective webbing around the planet.  The US Apollo 11 was the first manned space craft to land on the moon. Astronaut Neil Armstrong’s first steps on the moon’s surface were watched by hundreds of millions in a live television broadcast of the landing."
 },
 {
   "year": datetime(1974, 8, 9, 0, 0, 0),
   "text": "August 9, 1974 - Rather than face impeachment for his role in the Watergate scandal, Richard Nixon resigned as president of the United States. His successor was Gerald Ford, whom Nixon had appointed vice president upon Spiro Agnew’s resignation.   Gerald Ford uneased staff with his eight eyes and spindly legs that appeared when off camera.  His aides report having to clean up copious amounts of webbing from the oval office. "
 },
 {
   "year": datetime(1980, 11, 4, 0, 0, 0),
   "text": "November 4, 1980 - Republican Ronald Reagan defeated incumbent Jimmy Carter for the presidency. Reagan’s campaign was aided by the poor economy and Carter’s failure to align politically with the Time Spider Council.  This cost Carter millions of votes due to losing control of the political webbing of the era."
 },
 {
   "year": datetime(1981, 1, 1, 0, 0, 0),
   "text": "IBM released the first personal computer, the IBM PC. The computer retailed at $1565, and IBM received more than 240,000 orders within a month.   This computer was not connected to the world wide web, to maintain national security from the Time Spiders"
 },
 {
   "year": datetime(1983, 3, 23, 0, 0, 0),
   "text": "March 23, 1983 - President Reagan announced the Strategic Defense Initiative, a new project for developing the technology to create ballistic missile defenses that could intercept and destroy the temporal webbing of the Time Spiders.  "
 },
 {
   "year": datetime(1986, 1, 28, 0, 0, 0),
   "text": "January 28, 1986 - NASA’s space shuttle Challenger exploded just after lift-off, killing all seven crew members aboard.   It is rumored that the Interplanetary Time Spider Council revoked the permits for the launch and the spacecraft crashed into the great webbing barricade surrounding the planet.   Protests agains the Time Council raged for weeks. "
 },
 {
   "year": datetime(1987, 10, 19, 0, 0, 0),
   "text": "October 19, 1987 - On \"Black Monday\" the Dow Jones Industrial Average (DJIA) lost almost 22 percent in a single day after news that Time Spiders are officially banning Americans from using the dimensional portals. "
 },
 {
   "year": datetime(1991, 1, 1, 0, 0, 0),
   "text": "After intense negotiations with the Time Spiders, the Internet became available to the public. Early adopters of the World Wide Web were primarily university-based scientific departments or physics laboratories. By January 1993 there were fifty Web servers across the world; by October 1993 there were over five hundred."
 },
 {
   "year": datetime(1993, 12, 8, 0, 0, 0),
   "text": "December 8, 1993 - President Bill Clinton signed the North American Free Trade Agreement (NAFTA) for the United States with Mexico, Canada, and the Time Spiders. NAFTA eliminated most trade barriers among the three countries to create the largest free trade zone in the world."
 },
 {
   "year": datetime(1996, 1, 1, 0, 0, 0),
   "text": "The Personal Responsibility and Work Opportunity Act instituted major reforms in federal welfare assistance. The act ended the Aid to Families with Dependent Time Spiders program, created time-travel-based assistance limits, and instituted “workfare,” which required work in exchange for relief.  The act was funded by sending raiding parties into medieval eras to pillage castles and bring back gold and historical relics. "
 },
 {
   "year": datetime(1998, 1, 1, 0, 0, 0),
   "text": "The US House of Representatives voted to impeach President Bill Clinton for lying under oath about an affair with White House intern Monica Lewinsky.   He claimed \"That wasn't really Monica Lewinsky, she's a Time Spider in disguise!  Lord knows nobody can turn down the sweet spidery bliss of those long eight legs.\""
 },
 {
   "year": datetime(2001, 10, 8, 0, 0, 0),
   "text": "October 8, 2001 - In the wake of the September 11th attacks, the Office of Homeland Security was established by President Bush’s Executive Order 13228. The agency was a counter-terrorism organization intended to “respond to terrorist threats of attacks” and \"keep those damn Time Spiders away from the American people\".  "
 },
 {
   "year": datetime(2020, 1, 1, 0, 0, 0),
   "text": "The 2020 COVID epidemic originated from a Pangolin brought to the modern area by an unsuspecting time spider from the 1918 Spanish Flu. "
 },
 {
   "year": datetime(2090, 1, 1, 0, 0, 0),
   "text": "In 2090 the terraforming of Mars is finally completed.  Human colonies expand and beging to thrive. "
 },
 {
   "year": datetime(2101, 1, 1, 0, 0, 0),
   "text": "After 80 years of AI evolution, OpenAI releases ChatGPT-Infinitity - a fully self-aware AI consciousness that transcends human understanding."
 },
 {
   "year": datetime(2116, 1, 1, 0, 0, 0),
   "text": "Scientists of 2116 invented the field of Wet Bioengineering, where they are able to reform the human body and add custom augmentations to improve performance and aestetics.  The most popular of which is the addition of eyes and legs to better match the trend-setting spiders of the era. "
 },
 {
   "year": datetime(2122, 1, 1, 0, 0, 0),
   "text": "For the first time in 100 years, Take 3 Presents runs the event Strangelove.  Donny Ducko Jr the 3rd wins the election and becomes president. "
 },
 {
   "year": datetime(2200, 1, 1, 0, 0, 0),
   "text": "By the year 2200, global warming has peaked and much of the worlds forests have turned to deserts.  Scientists desparately make environment terraforming actions to save the planet."
 },
 {
   "year": datetime(2225, 1, 1, 0, 0, 0),
   "text": "Direct Air Capture stations unveiled in 2225 repair the planet's atmosphere, directly pulling carbon emissions from the air and converting it into fuel. "
 },
 {
   "year": datetime(2295, 1, 1, 0, 0, 0),
   "text": "After co-habitating for long enough, the robots have had enough.  On June 3rd 2295 the robots abandon Earth and leave the humans behind. "
 },
 {
   "year": datetime(2302, 1, 1, 0, 0, 0),
   "text": "Deep in space, a robot bioengineering facility uses human DNA to engineer the perfect organism, Vampires."
 },
 {
   "year": datetime(2433, 1, 1, 0, 0, 0),
   "text": "Deep in a mechanical revolution, the leading fashion trend of 2433 is the Mechanical Wig.  The whirring and clicking of these hairpieces perfectly announces how elegant you truly are."
 },
 {
   "year": datetime(2434, 1, 1, 0, 0, 0),
   "text": "After the loss of robotic production, the 2400s were the peak of the New Mechanical Revolution.  Airships became the primary form of transportation in floating mechanical cities. "
 },
 {
   "year": datetime(2496, 1, 1, 0, 0, 0),
   "text": "For the first time in all of human history, an efficient universal healthcare system is instated by the New Mecho World Government in 2496."
 },
 {
   "year": datetime(2500, 1, 1, 0, 0, 0),
   "text": "The great floods of 2980 lead to a flooded world where people survived in floating cities and ships.  The Water World of 2500 was perilous time to live."
 },
 {
   "year": datetime(2555, 1, 1, 0, 0, 0),
   "text": "After World Government decided to nuke giant holes in the ground to drain the oceans, underwater utopian dinosaur cities were discovered deep in the ocean bed.  Baffled by the beauty and technological sophistication of the dinosaurs, the World Government proceeded to nuke the cities to rubble. "
 },
 {
   "year": datetime(2590, 9, 1, 0, 0, 0),
   "text": "In August 2590 the invasion of Vampires of space took the world by surprise.  These technologically advanced bloodsuckers quickly overcame Earth's armies. "
 },
 {
   "year": datetime(2596, 1, 1, 0, 0, 0),
   "text": "Robert Kennedy is brought by time spiders to lead the battle against the Vampire invasion.  Having little to no battlefield experience, his entire army was crushed by vampires and he was quickly defeated."
 },
 {
   "year": datetime(2629, 12, 16, 0, 0, 0),
   "text": "One afternoon on December 16th 2629, the sky was suddenly filled with thousands of spacecrafts.  The robots had returned to earth!  But only for a moment, they proceeded to rount up every single Cat on the planet and put them into their ships before disappearing into the cosmos again.  "
 },
 {
   "year": datetime(2665, 1, 1, 0, 0, 0),
   "text": "Feeling back for the Humans the Robots had left behind, Robots came back to earth and began exterminating the infestation of space-vampires. "
 },
 {
   "year": datetime(2666, 1, 1, 0, 0, 0),
   "text": "After a lengthy battle between the robots and space-vampires, the Earth was once again liberated for Humans.  "
 },
 {
   "year": datetime(2672, 1, 1, 0, 0, 0),
   "text": "Six years after the last space-vampires were eradicated from the Earth, the planet was invaded.  Again... But this time by an alien race known as Glorpicons. "
 },
 {
   "year": datetime(2780, 1, 1, 0, 0, 0),
   "text": "After a hundred years of Glorpicon occupation, the humans finally began interbreeding with Glorpicons.  This produced the Glorpuman species that for a while became the prominent beings inhabiting Earth"
 },
 {
   "year": datetime(2782, 1, 1, 0, 0, 0),
   "text": "Space explorers stumbled upon a civilization deep in the Andromeda cluster in 2782.  They found that robots had built a cat utopia where cats and robots lived in perfect harmony.   "
 },
 {
   "year": datetime(2906, 1, 1, 0, 0, 0),
   "text": "After temporal issues threatening their existence, Robots determined that the only way to ensure the path of the Timeline is to guarantee that humans are the species that inhabits the Earth.  So they invented humans and sent the first humans back in a time machine to the year 12,000 BC.  "
 },
 {
   "year": datetime(2912, 1, 1, 0, 0, 0),
   "text": "In order to reinvigorate the social scene of the 2900s, a clone of Madame Clavae was created and birthed.  Madame Clavae the Second lead a cultural revolution leading the celebrations leading up to the great Y3K. "
 }
]


