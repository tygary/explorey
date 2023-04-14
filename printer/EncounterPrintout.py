from fpdf import FPDF

##-----------------------------------------------------------------------
#   EncounterPrintout
#
#   Basic PDF format for making a quiz
##-----------------------------------------------------------------------
class EncounterPrintout(FPDF):
    def header(self):
        return
        # self.image("/home/admin/explorey/printer/resources/etLogo.jpg", 38, 0, 30, 30)
        # self.ln(30)
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.multi_cell(0, 5, "Goblin Encounters LTD 2023\nWe're totally not the ones who burned down your village...", 0, 'C')