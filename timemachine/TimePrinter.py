import cups
import os
import json
import threading
from datetime import datetime

from logger.logger import Logger
from printer.EncounterPrintout import EncounterPrintout


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

        event = TIME_EVENTS[0][0]
        for index in range(0, len(TIME_EVENTS)):
            event_date = TIME_EVENTS[index][0]
            text = TIME_EVENTS[index][1]
            if event_date <= date:
                event = text

        if self.ready_to_print:
            self.__create_timerecord(date_string, event)
            self.__print_time_record()
            self.ready_to_print = False
            t = threading.Timer(1.0, self.__ready_to_print)
            t.start()

TIME_EVENTS = [
    [datetime(1000, 1, 1, 0, 0, 0), "There appears to be a temporal wall here.  We are unable to go back further."],
    [datetime(1980, 1, 1, 0, 0, 0), "A STUPID THING HAPPENED IN 1980"],
    [datetime(2000, 1, 1, 0, 0, 0), "A STUPID THING HAPPENED IN 2000"],
    [datetime(2500, 1, 1, 0, 0, 0), "A STUPID THING HAPPENED IN 2500"]
]

