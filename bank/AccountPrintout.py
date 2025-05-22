from fpdf import FPDF

##-----------------------------------------------------------------------
#   AccountPrintout
#
#   Basic PDF format for making a quiz
##-----------------------------------------------------------------------
class AccountPrintout(FPDF):
    def header(self):
        #self.set_y(-15)
        return
        #self.image("/home/admin/explorey/printer/resources/etLogo.jpg", 38, 0, 30, 30)
        #self.ln(30)
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.multi_cell(0, 5, "Goblin Banking LTD. 2025\nHave you bean saving up?", 0, 'C')
