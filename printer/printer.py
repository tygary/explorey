import cups
import os
import random
import json
from printer.ExploreyQuiz import ExploreyQuiz
import threading
from logger.logger import Logger

##-----------------------------------------------------------------------
#   Printer
#
#   Printer class for printing out adventures
#   printer.printAdventure(text)
##-----------------------------------------------------------------------
class Printer(object):
    conn = cups.Connection()
    printers = conn.getPrinters()
    printer_name = list(printers.keys())[0]
    tmpQuizPath = "/home/admin/exploreyquiz.pdf"
    tmpBadgePath = "/home/admin/exploreybadge.pdf"
    ready_to_print = True
    quotes = []

    logger = None

    def __init__(self):
        self.logger = Logger()
        with open("explorey/src/quotes.json", "r") as file:
            self.quotes = json.load(file)

    def __print_quiz(self):
        self.logger.log("Printer: printing quiz using %s" % self.printer_name)
        self.conn.cancelAllJobs(self.printer_name)
        self.conn.printFile(self.printer_name, self.tmpQuizPath, "quiz", {})

    def __print_badge(self):
        self.logger.log("Printer: printing badge using %s" % self.printer_name)
        self.conn.cancelAllJobs(self.printer_name)
        self.conn.printFile(self.printer_name, self.tmpBadgePath, "badge", {})

    def __create_quiz(self):
        self.logger.log("Printer: creating pdf")
        try:
            os.remove(self.tmpQuizPath)
            self.logger.log("  Success")
        except OSError:
            self.logger.log("  Failure")
            pass

        title = "Welcome to the Explorey Torium"
        desc = "To earn your Explorey Badge, find the answers to the following questions:"
        question_one = "1) How many wizards exist in the mirror dimension?"
        question_two = "2) Who sits on a throne of fur next to the snail?"
        question_three = "3) What color is the goobely gotch in the foobley lair?"
        question_four = "4) Who is the founder of the Explorey Torium?"
        question_five = "5) What is the smarglesplort?"
        ending = "When you have found all of the answers, pick up the telephone and dial 9."

        pdf = ExploreyQuiz()
        pdf.set_margins(left=18, top=0, right=0)
        pdf.set_auto_page_break(False)

        pdf.add_page(orientation='P', format=(90,210))
        pdf.set_font('Arial', 'B', 16)
        pdf.multi_cell(0, 6, title, align='C')
        pdf.ln()

        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 6, desc, align='C')
        pdf.ln()

        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 6, question_one, align='L')
        pdf.ln()

        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 6, question_two, align='L')
        pdf.ln()

        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 6, question_three, align='L')
        pdf.ln()

        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 6, question_four, align='L')
        pdf.ln()

        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 6, question_five, align='L')
        pdf.ln()

        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 6, ending, align='C')
        pdf.ln()

        pdf.output(self.tmpQuizPath, 'F')

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

        pdf = ExploreyQuiz()
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

    def printQuiz(self):
        self.logger.log("Printer: trying to print quiz with ready status %s" % (self.ready_to_print))
        if self.ready_to_print:
            self.__create_quiz()
            self.__print_quiz()
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