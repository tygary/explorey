import cups
import os
import random
import json
from printer.BatsPrintout import BatsPrintout
import threading
from logger.logger import Logger

##-----------------------------------------------------------------------
#   Printer
#
#   Printer class for printing out adventures
#   printer.printAdventure(text)
##-----------------------------------------------------------------------
class BatsPrinter(object):
    conn = cups.Connection()
    printers = conn.getPrinters()
    printer_name = list(printers.keys())[0]
    tmpFactPath = "/home/admin/batsfact.pdf"
    tmpBadgePath = "/home/admin/exploreybadge.pdf"
    ready_to_print = True
    quotes = []

    logger = None

    def __init__(self):
        self.logger = Logger()
        with open("printer/batsQuotes.json", "r") as file:
            self.quotes = json.load(file)

    def __print_fact(self):
        self.logger.log("Printer: printing fact using %s" % self.printer_name)
        self.conn.cancelAllJobs(self.printer_name)
        self.conn.printFile(self.printer_name, self.tmpFactPath, "fact", {})

    def __print_badge(self):
        self.logger.log("Printer: printing badge using %s" % self.printer_name)
        self.conn.cancelAllJobs(self.printer_name)
        self.conn.printFile(self.printer_name, self.tmpBadgePath, "badge", {})

    def __create_fact(self):
        self.logger.log("Printer: creating pdf")
        try:
            os.remove(self.tmpFactPath)
            self.logger.log("  Success")
        except OSError:
            self.logger.log("  Failure")
            pass

        quote = self.__get_random_quote()

        title = "Congratulations!  You have created trash."
        desc = "Trash is a way of life, and you are a big part of it.  Trash wouldn't exist without you."

        pdf = BatsPrintout()
        pdf.set_margins(left=18, top=0, right=0)
        pdf.set_auto_page_break(False)

        pdf.add_page(orientation='P', format=(90,210))
        pdf.set_font('Arial', 'B', 16)
        pdf.multi_cell(0, 6, title, align='C')
        pdf.ln()

        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 6, desc, align='C')
        pdf.ln()

        pdf.ln()
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 6, "\"%s\"" % (quote["quote"]), align='C')
        pdf.multi_cell(0, 6, "-%s" % (quote["author"]), align='C')
        pdf.ln()

        pdf.output(self.tmpFactPath, 'F')

    def __create_badge(self):
        self.logger.log("Printer: creating pdf")
        try:
            os.remove(self.tmpBadgePath)
            self.logger.log("  Success")
        except OSError:
            self.logger.log("  Failure")
            pass
        title = "Explorey Badge"
        desc = "Congratulations!  You have earned your Explorey Badge.  You are now a certified Explorey Scout.  "
        grade = self.__get_random_grade()
        grade_str = "You earned %s " % (self.__get_a_for_grade(grade))
        quote = self.__get_random_quote()

        pdf = BatsPrintout()
        pdf.set_margins(left=18, top=0, right=0)
        pdf.set_auto_page_break(False)

        pdf.add_page(orientation='P', format=(90,140))
        pdf.set_font('Arial', 'B', 16)
        pdf.multi_cell(0, 6, title, align='C')
        pdf.ln()
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 6, desc, align='C')
        pdf.ln()
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 6, grade_str, align='C')
        pdf.set_font('Arial', '', 16)
        pdf.multi_cell(0, 6, grade, align='C')
        pdf.ln()
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 6, "\"%s\"" % (quote["quote"]), align='C')
        pdf.multi_cell(0, 6, "-%s" % (quote["author"]), align='C')
        pdf.ln()

        pdf.output(self.tmpBadgePath, 'F')

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

    def printfact(self):
        self.logger.log("Printer: trying to print fact with ready status %s" % (self.ready_to_print))
        if self.ready_to_print:
            self.__create_fact()
            self.__print_fact()
            self.ready_to_print = False
            t = threading.Timer(1.0, self.__ready_to_print)
            t.start()

    def printBadge(self):
        self.logger.log("Printer: trying to print badge with ready status %s" % (self.ready_to_print))
        if self.ready_to_print:
            self.__create_badge()
            self.__print_badge()
            self.ready_to_print = False
            t = threading.Timer(1.0, self.__ready_to_print)
            t.start()