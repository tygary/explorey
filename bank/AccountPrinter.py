import cups
import os
import random
import json
import threading
from logger.logger import Logger
from PIL import Image, ImageDraw

from bank.AccountPrintout import AccountPrintout


# -----------------------------------------------------------------------
#   AdventurePrinter
#
#   Printer class for printing out adventures
#   printer.printAdventure(text)
# -----------------------------------------------------------------------
class AccountPrinter(object):
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

    def __create_share_printout(self):
        self.logger.log("Printer: creating share pdf")
        try:
            os.remove(self.tmpAccountPrintoutPath)
            self.logger.log("  Success")
        except OSError:
            self.logger.log("  Failure")
            pass

        pdf = AccountPrintout()
        pdf.set_line_width(0.2)
        pdf.set_margins(left=16, top=0, right=0)
        pdf.set_auto_page_break(False)

        pdf.add_page(orientation="P", format=(90, 115))
        pdf.set_font("Arial", "B", 16)
        pdf.multi_cell(0, 10, f"Stock Certificate", align="C")
        pdf.set_font("Arial", "", 12)
        pdf.cell(90, 4, ln=1)
        pdf.multi_cell(0, 10, f"This document certifies ownership of one (1) share of The Leech Mining Company, subject to all rules regulations and bylaws of the corporate charter as well as the stalk trading rules at ACME Bank.", align="C")
        pdf.cell(90, 4, ln=1)
        pdf.image("/home/admin/explorey/printer/resources/LeechLogo.jpg", 43, 74, 20, 20)

        pdf.output(self.tmpAccountPrintoutPath, "F")
        

    def __create_account_printout(self, account_number, balance, name_file_path):
        self.logger.log("Printer: creating account pdf")
        try:
            os.remove(self.tmpAccountPrintoutPath)
            self.logger.log("  Success")
        except OSError:
            self.logger.log("  Failure")
            pass

        pdf = AccountPrintout()
        pdf.set_line_width(0.2)
        pdf.set_margins(left=16, top=0, right=0)
        pdf.set_auto_page_break(False)

        pdf.add_page(orientation="P", format=(90, 115))
        pdf.set_font("Arial", "B", 16)
        pdf.multi_cell(0, 10, f"Account Details", align="C")
        pdf.set_font("Arial", "", 12)
        pdf.cell(90, 4, ln=1)
        pdf.multi_cell(0, 10, f"Bean Balance: {balance}", align="C")
        pdf.cell(90, 4, ln=1)

        # Render image and insert it
        grid_path = self.render_balanced_star_grid(account_number)
        pdf.image(grid_path, x=27, y=25, w=50)  # Adjust w/h/x/y as needed for scales

        pdf.image(name_file_path, x=27, y=85, w=50)  # Adjust w/h/x/y as needed for scales

        pdf.output(self.tmpAccountPrintoutPath, "F")

    def render_balanced_star_grid(self, account_number, cell_px=16, border_thickness=4, save_path="/home/admin/account_grid.png"):
        """
        Draws a 4x4 binary grid with uniform black borders, 1-bit color, safe for Star TUP900.
        """
        grid_cells = 4
        grid_px = grid_cells * cell_px
        total_px = grid_px + border_thickness

        img = Image.new("1", (total_px + 1, total_px + 1), 1)  # white 1-bit image
        draw = ImageDraw.Draw(img)

        bits = [int(b) for b in bin(account_number)[2:].zfill(16)]

        # Step 1: Draw filled black cells for bit=1
        for row in range(grid_cells):
            for col in range(grid_cells):
                idx = row * 4 + col
                if bits[idx] == 1:
                    x0 = col * cell_px
                    y0 = row * cell_px
                    x1 = x0 + cell_px
                    y1 = y0 + cell_px
                    draw.rectangle([x0, y0, x1, y1], fill=0)

        # Step 2: Draw vertical and horizontal grid lines
        for i in range(grid_cells + 1):
            x = i * cell_px
            y = i * cell_px

            # Vertical line
            draw.rectangle([x, 0, x + border_thickness, total_px], fill=0)
            # Horizontal line
            draw.rectangle([0, y, total_px, y + border_thickness], fill=0)

        img.save(save_path)
        return save_path

    def render_account_bitmap(self, account_number, cell_px=15, border_px=4, save_path="/home/admin/account_grid.png"):
        binary_str = bin(account_number)[2:].zfill(16)
        bits = [int(b) for b in binary_str]

        grid_px = 4 * cell_px
        img = Image.new("RGB", (grid_px, grid_px), "black")
        draw = ImageDraw.Draw(img)

        for row in range(4):
            for col in range(4):
                index = row * 4 + col
                if bits[index] == 0:
                    x0 = col * cell_px + border_px
                    y0 = row * cell_px + border_px
                    x1 = (col + 1) * cell_px - border_px
                    y1 = (row + 1) * cell_px - border_px
                    draw.rectangle([x0, y0, x1, y1], fill="white")

        img.save(save_path)
        return save_path

    def __ready_to_print(self):
        self.logger.log(
            "Printer: setting ready to print from %s to True" % self.ready_to_print
        )
        self.ready_to_print = True

    def printAccount(self, account_number, balance, name_file_path):
        self.logger.log(
            "Printer: trying to print account with ready status %s"
            % (self.ready_to_print)
        )
        if self.ready_to_print:
            self.__create_account_printout(account_number, balance, name_file_path)
            self.__print_account()
            self.ready_to_print = False
            t = threading.Timer(1.0, self.__ready_to_print)
            t.start()

    def printShare(self):
        self.logger.log(
            "Printer: trying to print share with ready status %s"
            % (self.ready_to_print)
        )
        if self.ready_to_print:
            self.__create_share_printout()
            self.__print_account()
            self.ready_to_print = False
            t = threading.Timer(1.0, self.__ready_to_print)
            t.start()
