import cups
import os
import random
import json
import threading
from logger.logger import Logger

from bank.AccountPrintout import AccountPrintout


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

    tmpAccountPrintoutPath = "/home/admin/accountPrintout.pdf"
    ready_to_print = True

    logger = None

    def __init__(self):
        self.logger = Logger()

    def __print_account(self):
        self.logger.log("Printer: printing account using %s" % self.printer_name)
        self.conn.cancelAllJobs(self.printer_name)
        self.conn.printFile(self.printer_name, self.tmpAccountPrintoutPath, "account", {})


    def __create_account_printout(self, account_number, balance):
        self.logger.log("Printer: creating account pdf")
        try:
            os.remove(self.tmpAccountPrintoutPath)
            self.logger.log("  Success")
        except OSError:
            self.logger.log("  Failure")
            pass

        pdf = AccountPrintout()
        pdf.set_margins(left=16, top=0, right=0)
        pdf.set_auto_page_break(False)

        pdf.add_page(orientation="P", format=(90, 220))
        pdf.set_font("Arial", "B", 16)
        pdf.multi_cell(0, 10, f"Account Details", align="C")
        pdf.set_font("Arial", "", 12)
        pdf.cell(90, 4, ln=1)

        # --- Draw 4x4 Binary Grid for Account Number ---
        self.__draw_account_number_grid(pdf, account_number, x_start=20, y_start=25, cell_size=6)

        pdf.output(self.tmpAccountPrintoutPath, "F")

    def __draw_account_number_grid(self, pdf, account_number, x_start, y_start, cell_size):
        # Convert account number to 16-bit binary list
        binary_str = bin(account_number)[2:].zfill(16)
        bits = [int(b) for b in binary_str]

        # Set colors
        pdf.set_draw_color(0)  # black border
        pdf.set_fill_color(0)  # black fill for 1s

        for row in range(4):
            for col in range(4):
                index = row * 4 + col
                x = x_start + col * cell_size
                y = y_start + row * cell_size
                fill = bits[index]
                pdf.rect(x, y, cell_size, cell_size, style='FD' if fill else 'D')  # Fill and draw border if 1, only draw if 0

        # Draw outer border (optional – looks sharper)
        grid_size = 4 * cell_size
        pdf.rect(x_start, y_start, grid_size, grid_size)

    def __ready_to_print(self):
        self.logger.log(
            "Printer: setting ready to print from %s to True" % self.ready_to_print
        )
        self.ready_to_print = True

    def printAccount(self, account_number, balance):
        self.logger.log(
            "Printer: trying to print account with ready status %s"
            % (self.ready_to_print)
        )
        if self.ready_to_print:
            self.__create_account_printout(account_number, balance)
            self.__print_account()
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
