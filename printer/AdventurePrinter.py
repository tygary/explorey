import cups
import os
import random
import json
from printer.CharacterSheetPrintout import CharacterSheetPrintout
from printer.EncounterPrintout import EncounterPrintout
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

    def __create_encounter(self, encounter):
        self.logger.log("Printer: creating encounter pdf")
        try:
            os.remove(self.tmpEncounterPath)
            self.logger.log("  Success")
        except OSError:
            self.logger.log("  Failure")
            pass

        title = "Encounter!!"
        desc = str(encounter)

        pdf = EncounterPrintout()
        pdf.set_margins(left=18, top=0, right=0)
        pdf.set_auto_page_break(False)

        pdf.add_page(orientation='P', format=(90,150))
        pdf.set_font('Arial', 'B', 16)
        pdf.multi_cell(0, 6, title, align='C')
        pdf.ln()

        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 6, desc, align='C')
        pdf.ln()

        pdf.output(self.tmpEncounterPath, 'F')

    def __create_character(self, character: CharacterSheet):
        self.logger.log("Printer: creating character pdf")
        try:
            os.remove(self.tmpCharacterPath)
            self.logger.log("  Success")
        except OSError:
            self.logger.log("  Failure")
            pass
        title = "Character!"
        desc = str(character)

        pdf = CharacterSheetPrintout()
        pdf.set_margins(left=0, top=0, right=0)
        pdf.set_auto_page_break(False)
        pdf.add_page(orientation='P', format=(90,140))

        pdf.image("/home/admin/explorey/printer/resources/etLogo.jpg", 38, 0, 30, 30)
        pdf.cell(0, 6, "TESTING???", ln=1)

        pdf.set_font('Arial', 'B', 16)
        pdf.multi_cell(0, 6, f"Name:_____________________", align='L')
        pdf.ln()

        pdf.cell(36, 6, "TEST", border=1, ln=0, align="R")
        pdf.cell(36, 6, "TEST", border=1, ln=0, align="R")
        pdf.ln()

        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 6, f"A {character.species} {character.class_name}", align='L')
        pdf.ln()

        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 6, f"Sneakiness: {character.dex} Craftiness: {character.wis}\nScrappiness: {character.con} Fabulousness: {character.cha}", align='L')
        pdf.ln()

        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 6,
                       f"Abilities:\n{character.abilities}",
                       align='L')
        pdf.ln()

        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 6,
                       f"Items:\n{character.items}",
                       align='L')
        pdf.ln()

        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 6,
                       f"Quest: {character.quest}",
                       align='L')
        pdf.ln()


        pdf.output(self.tmpCharacterPath, 'F')

    def __get_a_for_grade(self, grade):
        if "A" in grade:
            return "an"
        else:
            return "a"

    def __get_random_grade(self):
        grades = ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-"]
        return random.choice(grades)

    def __get_random_quote(self):
        return random.choice(self.quotes)

    def __ready_to_print(self):
        self.logger.log("Printer: setting ready to print from %s to True" % self.ready_to_print)
        self.ready_to_print = True

    def printEncounter(self, encounter):
        self.logger.log("Printer: trying to print encounter with ready status %s" % (self.ready_to_print))
        if self.ready_to_print:
            self.__create_encounter(encounter)
            self.__print_encounter()
            self.ready_to_print = False
            t = threading.Timer(1.0, self.__ready_to_print)
            t.start()

    def printCharacter(self, character):
        self.logger.log("Printer: trying to print character with ready status %s" % (self.ready_to_print))
        if self.ready_to_print:
            self.__create_character(character)
            self.__print_character()
            self.ready_to_print = False
            t = threading.Timer(1.0, self.__ready_to_print)
            t.start()