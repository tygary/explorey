import cups
import os
import random
import json
from printer.CharacterSheetPrintout import CharacterSheetPrintout
from printer.EncounterPrintout import EncounterPrintout
from printer.ItemPrintout import ItemPrintout
import threading
from logger.logger import Logger
from printer.CharacterSheet import CharacterSheet


# -----------------------------------------------------------------------
#   AdventurePrinter
#
#   Printer class for printing out adventures
#   printer.printAdventure(text)
# -----------------------------------------------------------------------
class AdventurePrinter(object):
    conn = cups.Connection()
    printers = conn.getPrinters()
    printerList = list(printers.keys())
    for printer in printerList:
        if "TUP" in printer:
            printer_name = printer

    tmpEncounterPath = "/home/admin/encounter.pdf"
    tmpCharacterPath = "/home/admin/character.pdf"
    tmpResultPath = "/home/admin/result.pdf"
    tmpBossPath = "/home/admin/boss.pdf"
    tmpDuelPath = "/home/admin/duel.pdf"
    ready_to_print = True
    quotes = []

    logger = None

    def __init__(self):
        self.logger = Logger()
        with open("printer/batsQuotes.json", "r") as file:
            self.quotes = json.load(file)

    def __print_encounter(self):
        self.logger.log("Printer: printing encounter using %s" % self.printer_name)
        self.conn.cancelAllJobs(self.printer_name)
        self.conn.printFile(self.printer_name, self.tmpEncounterPath, "encounter", {})

    def __print_character(self):
        self.logger.log("Printer: printing character using %s" % self.printer_name)
        self.conn.cancelAllJobs(self.printer_name)
        self.conn.printFile(self.printer_name, self.tmpCharacterPath, "character", {})

    def __print_result(self):
        self.logger.log("Printer: printing result using %s" % self.printer_name)
        self.conn.cancelAllJobs(self.printer_name)
        self.conn.printFile(self.printer_name, self.tmpResultPath, "result", {})

    def __print_boss(self):
        self.logger.log("Printer: printing boss using %s" % self.printer_name)
        self.conn.cancelAllJobs(self.printer_name)
        self.conn.printFile(self.printer_name, self.tmpBossPath, "boss", {})

    def __print_duel(self):
        self.logger.log("Printer: printing duel using %s" % self.printer_name)
        self.conn.cancelAllJobs(self.printer_name)
        self.conn.printFile(self.printer_name, self.tmpDuelPath, "duel", {})

    def __create_encounter(self, encounter):
        self.logger.log("Printer: creating encounter pdf")
        try:
            os.remove(self.tmpEncounterPath)
            self.logger.log("  Success")
        except OSError:
            self.logger.log("  Failure")
            pass

        pdf = EncounterPrintout()
        pdf.set_margins(left=16, top=0, right=0)
        pdf.set_auto_page_break(False)

        pdf.add_page(orientation="P", format=(90, 200))
        pdf.set_font("Arial", "B", 16)
        pdf.multi_cell(0, 10, f"{encounter.title}", align="C")
        pdf.set_font("Arial", "", 12)
        pdf.cell(90, 4, ln=1)
        pdf.multi_cell(0, 6, f"{encounter.prompt}", align="L")
        pdf.cell(90, 4, ln=1)
        pdf.multi_cell(0, 6, f"{encounter.connecting_phrase}", align="L")
        pdf.cell(6, 6, f"A: ", align="L")
        pdf.multi_cell(0, 6, f"{encounter.option_a}", align="L")
        pdf.cell(6, 6, f"B: ", align="L")
        pdf.multi_cell(0, 6, f"{encounter.option_b}", align="L")
        pdf.cell(90, 4, ln=1)
        pdf.multi_cell(0, 6, f"{encounter.pos_result}", align="L")
        pdf.cell(90, 4, ln=1)
        pdf.multi_cell(0, 6, f"{encounter.neg_result}", align="L")

        pdf.output(self.tmpEncounterPath, "F")

    def __create_character(self, character: CharacterSheet):
        self.logger.log("Printer: creating character pdf")
        try:
            os.remove(self.tmpCharacterPath)
            self.logger.log("  Success")
        except OSError:
            self.logger.log("  Failure")
            pass

        pdf = CharacterSheetPrintout()
        pdf.set_margins(left=16, top=0, right=0)
        pdf.set_auto_page_break(False)
        pdf.add_page(orientation="P", format=(90, 310))
        pdf.image(
            "/home/admin/explorey/printer/resources/charactersheet.png", 15, 10, 75, 280
        )
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, f"Character Sheet", align="C", ln=1)

        left_align = 2
        pdf.set_font("Arial", "", 12)
        pdf.cell(75, 4, ln=1)
        pdf.cell(left_align, 6)
        pdf.cell(0, 6, f"Name: __________________", align="L", ln=1)
        pdf.cell(left_align, 6)
        pdf.cell(0, 6, f"Species: {character.species}", align="L", ln=1)
        pdf.cell(left_align, 6)
        pdf.cell(0, 6, f"Profession: {character.class_name}", align="L", ln=1)
        pdf.cell(75, 4, ln=1)
        pdf.cell(0, 6, f"Skills:", align="L", ln=1)
        pdf.cell(75, 4, ln=1)
        pdf.set_font("Arial", "B", 14)
        pdf.cell(33, 6, f"{character.dex}", align="C")
        pdf.cell(48, 6, f"{character.wis}", align="C", ln=1)
        pdf.set_font("Arial", "", 12)
        pdf.cell(33, 6, f"Sneakiness", align="C")
        pdf.cell(48, 6, f"Craftiness", align="C", ln=1)
        pdf.cell(75, 10, ln=1)
        pdf.set_font("Arial", "B", 14)
        pdf.cell(33, 6, f"{character.con}", align="C")
        pdf.cell(48, 6, f"{character.cha}", align="C", ln=1)
        pdf.set_font("Arial", "", 12)
        pdf.cell(33, 6, f"Scrappiness", align="C")
        pdf.cell(48, 6, f"Fabulousness", align="C", ln=1)
        pdf.cell(75, 4, ln=1)
        pdf.cell(0, 10, f"Abilities:", align="L", ln=1)
        pdf.cell(left_align, 6)
        pdf.cell(6, 6, f"{character.abilities[0]}", align="L", ln=1)
        pdf.cell(left_align, 6)
        pdf.cell(6, 6, f"{character.abilities[1]}", align="L", ln=1)
        pdf.cell(left_align, 6)
        pdf.cell(6, 6, f"{character.abilities[2]}", align="L", ln=1)
        pdf.cell(75, 4, ln=1)
        pdf.cell(0, 10, f"Items:", align="L", ln=1)
        pdf.cell(left_align, 6)
        pdf.cell(0, 6, f"{character.items[0]}", align="L", ln=1)
        pdf.cell(left_align, 6)
        pdf.cell(0, 6, f"{character.items[1]}", align="L", ln=1)
        pdf.cell(left_align, 6)
        pdf.cell(0, 6, f"{character.items[2]}", align="L", ln=1)
        pdf.cell(75, 4, ln=1)
        pdf.cell(0, 10, f"Life Goal:", align="L", ln=1)
        pdf.cell(left_align, 6)
        pdf.multi_cell(0, 6, f"{character.quest}", align="L")
        pdf.cell(75, 4, ln=1)
        pdf.cell(0, 10, f"Main Quest:", align="L", ln=1)
        pdf.cell(left_align, 6)
        pdf.multi_cell(0, 6, f"{character.main_quest}", align="L")
        pdf.cell(75, 6, ln=1)
        pdf.cell(0, 10, f"Quest Stamps:", align="L", ln=1)
        pdf.set_font("Arial", "", 9)
        left_side = 35
        right_side = 100
        pdf.cell(left_side, 4, f"Blessing of Onions", align="L")
        pdf.cell(right_side, 4, f"Blessing of Potatoes", align="L", ln=1)
        pdf.cell(left_side, 4, f"+3 Sneakiness", align="L")
        pdf.cell(right_side, 4, f"+3 Craftiness", align="L", ln=1)
        pdf.cell(left_side, 4, f"+1 Life", align="L")
        pdf.cell(right_side, 4, f"+1 Life", align="L", ln=1)
        pdf.cell(75, 12, ln=1)
        pdf.cell(left_side, 4, f"Blessing of Rutabaga", align="L")
        pdf.cell(right_side, 4, f"Blessing of Carrots", align="L", ln=1)
        pdf.cell(left_side, 4, f"+3 Scrappiness", align="L")
        pdf.cell(right_side, 4, f"+3 Fabulousness", align="L", ln=1)
        pdf.cell(left_side, 4, f"+1 Life", align="L")
        pdf.cell(right_side, 4, f"+1 Life", align="L", ln=1)
        pdf.cell(75, 14, ln=1)
        pdf.output(self.tmpCharacterPath, "F")

    def __create_result(self, result):
        self.logger.log("Printer: creating result pdf")
        try:
            os.remove(self.tmpResultPath)
            self.logger.log("  Success")
        except OSError:
            self.logger.log("  Failure")
            pass

        pdf = ItemPrintout()
        pdf.set_margins(left=16, top=0, right=0)
        pdf.set_auto_page_break(False)
        pdf.add_page(orientation="P", format=(90, 130))

        pdf.set_font("Arial", "B", 16)
        pdf.multi_cell(0, 10, f"{result.title}", align="C")

        pdf.set_font("Arial", "", 12)
        pdf.cell(75, 4, ln=1)
        pdf.multi_cell(0, 6, f"{result.description}", align="C")
        pdf.cell(75, 4, ln=1)
        pdf.set_font("Arial", "B", 12)
        pdf.multi_cell(0, 6, f"{result.effect}", align="C")
        pdf.output(self.tmpResultPath, "F")

    def __create_boss(self, boss):
        self.logger.log("Printer: creating boss pdf")
        try:
            os.remove(self.tmpBossPath)
            self.logger.log("  Success")
        except OSError:
            self.logger.log("  Failure")
            pass

        pdf = EncounterPrintout()
        pdf.set_margins(left=16, top=0, right=0)
        pdf.set_auto_page_break(False)
        pdf.add_page(orientation="P", format=(90, 380))

        pdf.set_font("Arial", "B", 16)
        pdf.multi_cell(0, 10, f"{boss.title}", align="C")

        pdf.set_font("Arial", "", 12)
        pdf.cell(75, 4, ln=1)
        pdf.multi_cell(0, 6, f"{boss.desc}", align="L")
        pdf.cell(75, 4, ln=1)
        pdf.multi_cell(
            0,
            6,
            f"To emerge victorious from this boss battle, your party must navigate through the following challenges and suceed on at least two out of three:",
            align="L",
        )
        pdf.cell(75, 4, ln=1)
        pdf.multi_cell(0, 6, f"1 - {boss.challenge_1}", align="L")
        pdf.cell(75, 4, ln=1)
        pdf.multi_cell(0, 6, f"2 - {boss.challenge_2}", align="L")
        pdf.cell(75, 4, ln=1)
        pdf.multi_cell(0, 6, f"3 - {boss.challenge_3}", align="L")
        pdf.cell(75, 4, ln=1)
        pdf.multi_cell(0, 6, f"{boss.result}", align="L")
        pdf.output(self.tmpBossPath, "F")

    def __create_duel(self, duel):
        self.logger.log("Printer: creating duel pdf")
        try:
            os.remove(self.tmpDuelPath)
            self.logger.log("  Success")
        except OSError:
            self.logger.log("  Failure")
            pass

        pdf = EncounterPrintout()
        pdf.set_margins(left=16, top=0, right=0)
        pdf.set_auto_page_break(False)
        pdf.add_page(orientation="P", format=(90, 330))
        pdf.set_font("Arial", "B", 16)
        pdf.multi_cell(0, 10, f"{duel.title}", align="C")
        pdf.set_font("Arial", "", 12)
        pdf.cell(75, 4, ln=1)
        pdf.multi_cell(0, 6, f"{duel.prompt}", align="L")
        pdf.cell(75, 4, ln=1)
        pdf.multi_cell(0, 6, f"1 - {duel.challenge_1}", align="L")
        pdf.cell(75, 4, ln=1)
        pdf.multi_cell(0, 6, f"2 - {duel.challenge_2}", align="L")
        pdf.cell(75, 4, ln=1)
        pdf.multi_cell(0, 6, f"3 - {duel.challenge_3}", align="L")
        pdf.cell(75, 4, ln=1)
        pdf.multi_cell(0, 6, f"{duel.result}", align="L")
        pdf.output(self.tmpDuelPath, "F")

    def __ready_to_print(self):
        self.logger.log(
            "Printer: setting ready to print from %s to True" % self.ready_to_print
        )
        self.ready_to_print = True

    def printEncounter(self, encounter):
        self.logger.log(
            "Printer: trying to print encounter with ready status %s"
            % (self.ready_to_print)
        )
        if self.ready_to_print:
            self.__create_encounter(encounter)
            self.__print_encounter()
            self.ready_to_print = False
            t = threading.Timer(1.0, self.__ready_to_print)
            t.start()

    def printCharacter(self, character):
        self.logger.log(
            "Printer: trying to print character with ready status %s"
            % (self.ready_to_print)
        )
        if self.ready_to_print:
            self.__create_character(character)
            self.__print_character()
            self.ready_to_print = False
            t = threading.Timer(1.0, self.__ready_to_print)
            t.start()

    def printResult(self, result):
        self.logger.log(
            "Printer: trying to print result with ready status %s"
            % (self.ready_to_print)
        )
        if self.ready_to_print:
            self.__create_result(result)
            self.__print_result()
            self.ready_to_print = False
            t = threading.Timer(1.0, self.__ready_to_print)
            t.start()

    def printBoss(self, boss):
        self.logger.log(
            "Printer: trying to print boss with ready status %s" % (self.ready_to_print)
        )
        if self.ready_to_print:
            self.__create_boss(boss)
            self.__print_boss()
            self.ready_to_print = False
            t = threading.Timer(1.0, self.__ready_to_print)
            t.start()

    def printDuel(self, duel):
        self.logger.log(
            "Printer: trying to print duel with ready status %s" % (self.ready_to_print)
        )
        if self.ready_to_print:
            self.__create_duel(duel)
            self.__print_duel()
            self.ready_to_print = False
            t = threading.Timer(1.0, self.__ready_to_print)
            t.start()
