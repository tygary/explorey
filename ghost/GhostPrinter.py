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
            self.logger.log("  Success")
        except OSError:
            self.logger.log("  Failure")
            pass

        pdf = GhostPrintout()
        pdf.set_margins(left=16, top=0, right=0)
        pdf.set_auto_page_break(False)

        page_len = 90
        # if len(text) > 220:
            # page_len = 140

        pdf.add_page(orientation="P", format=(140, page_len))
        pdf.set_font("helvetica", "B", 16)
        pdf.multi_cell(0, 10, f"Name:  {ghost['name']}", align="C")
        pdf.set_font("helvetica", "", 12)
        pdf.cell(90, 4, ln=1)
        pdf.multi_cell(0, 6, f"Origin: {ghost['origin']}", align="L")
        pdf.multi_cell(0, 6, f"Amount Fulfilled: {ghost['fulfillment']}", align="L")
        pdf.multi_cell(0, 6, f"Used: {ghost['purpose']}", align="L")
        pdf.multi_cell(0, 6, f"Previous Owner: {ghost['owner']}", align="L")
        pdf.multi_cell(0, 6, f"Reason Discarded: {ghost['discardReason']}", align="L")
        pdf.multi_cell(0, 6, f"Date of Disposal: {ghost['dateOfDisposal']}", align="L")
        pdf.multi_cell(0, 6, f"Fact One: {ghost['factOne']}", align="L")
        pdf.multi_cell(0, 6, f"Fact Two: {ghost['factTwo']}", align="L")

        pdf.multi_cell(0, 6, "This is a bunch of footer information that will tell you to go to the next machines and then play the game and win it.", align="L")

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
    "discardReason": "Unknown",
    "dateOfDisposal": "11/11/2024",
    "factOne": "This is a fact about the item.",
    "factTwo": "This is a fact about the item.",
}

GHOSTS = {
    # "uid": {
    #     {
    #         "description": "Old big calculator",
    #         "name": "SHARP EL-8301 Calculator",
    #         "origin": "Pittsburgh Department of Finance",
    #         "fulfillment": 7,
    #         "purpose": 10,
    #         "owner": "Jeremiah Johann Jr ",
    #         "discardReason": "My owner had a heart attack while using me",
    #         "dateOfDisposal": "11/11/2024",
    #         "factOne": "I singlehandedly underwrote all of the grants in the city of Pittsburgh for 30 years.",
    #         "factTwo": "My 0 key is sticky and this caused a recurring underfunding of public programs.",
    #     }
    # }
}
