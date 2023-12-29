from fpdf import FPDF

##-----------------------------------------------------------------------
#   CharacterSheetPrintout
#
#   Basic PDF format for making a quiz
##-----------------------------------------------------------------------
class CharacterSheetPrintout(FPDF):
    def header(self):
        #self.set_y(-15)
        return
        #self.image("/home/admin/explorey/printer/resources/etLogo.jpg", 38, 0, 30, 30)
        #self.ln(30)
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.multi_cell(0, 5, "Goblin Encounters LTD. 2023\nDaddy Santa sees you when you're naughty...", 0, 'C')
