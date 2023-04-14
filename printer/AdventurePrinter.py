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
        pdf.set_margins(left=16, top=0, right=0)
        pdf.set_auto_page_break(False)
        pdf.add_page(orientation='P', format=(90,220))
        pdf.set_font('Arial', '', 12)

        pdf.image("/home/admin/explorey/printer/resources/charactersheet.jpg", 15, 0, 75, 200)

        pdf.set_font('Arial', '', 12)
        pdf.cell(75, 4, ln=1)
        pdf.cell(6, 8)
        pdf.cell(0, 8, f"Name: __________________", align='L', ln=1)
        pdf.cell(6, 8)
        pdf.cell(0, 8, f"Species: {character.species}", align='L', ln=1)
        pdf.cell(6, 8)
        pdf.cell(0, 8, f"Profession: {character.class_name}", align='L', ln=1)
        pdf.cell(75, 4, ln=1)
        pdf.cell(0, 6, f"Skills:", align='L', ln=1)
        pdf.cell(75, 4, ln=1)
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(33, 8, f"{character.dex}", align='C')
        pdf.cell(48, 8, f"{character.wis}", align='C', ln=1)
        pdf.set_font('Arial', '', 12)
        pdf.cell(33, 6, f"Sneakiness", align='C')
        pdf.cell(48, 6, f"Craftiness", align='C', ln=1)
        pdf.cell(75, 10, ln=1)
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(33, 8, f"{character.con}", align='C')
        pdf.cell(48, 8, f"{character.cha}", align='C', ln=1)
        pdf.set_font('Arial', '', 12)
        pdf.cell(33, 6, f"Scrappiness", align='C')
        pdf.cell(48, 6, f"Fabulousness", align='C', ln=1)
        pdf.cell(75, 6, ln=1)
        pdf.cell(0, 6, f"Abilities:", align='L', ln=1)
        pdf.cell(75, 4, ln=1)
        pdf.cell(6, 8)
        pdf.cell(6, 8, f"{character.abilities[0]}", align='L', ln=1)
        pdf.cell(6, 8)
        pdf.cell(6, 8, f"{character.abilities[1]}", align='L', ln=1)
        pdf.cell(6, 8)
        pdf.cell(6, 8, f"{character.abilities[2]}", align='L', ln=1)
        pdf.cell(75, 4, ln=1)
        pdf.cell(0, 6, f"Items:", align='L', ln=1)
        pdf.cell(75, 4, ln=1)
        pdf.cell(6, 8)
        pdf.cell(0, 8, f"{character.items[0]}", align='L', ln=1)
        pdf.cell(6, 8)
        pdf.cell(0, 8, f"{character.items[1]}", align='L', ln=1)
        pdf.cell(6, 8)
        pdf.cell(0, 8, f"{character.items[2]}", align='L', ln=1)
        pdf.cell(75, 4, ln=1)
        pdf.cell(6, 8)
        pdf.cell(0, 8, f"Quest:", align='L', ln=1)
        pdf.cell(75, 4, ln=1)
        pdf.cell(6, 6)
        pdf.multi_cell(0, 6, f"{character.quest}", align='L')
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