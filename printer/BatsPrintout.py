from fpdf import FPDF

##-----------------------------------------------------------------------
#   BatsPrintout
#
#   Basic PDF format for making a quiz
##-----------------------------------------------------------------------
class BatsPrintout(FPDF):
    def header(self):
        self.image("/home/admin/explorey/printer/resources/bats.jpg", 38, 0, 30, 80)
        self.ln(30)
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.multi_cell(0, 5, "All Trash is Art", 0, 'C')