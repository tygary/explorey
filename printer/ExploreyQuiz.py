from fpdf import FPDF

##-----------------------------------------------------------------------
#   ExploreyQuiz
#
#   Basic PDF format for making a quiz
##-----------------------------------------------------------------------
class ExploreyQuiz(FPDF):
    def header(self):
        self.image("/home/admin/explorey/printer/resources/etLogo.jpg", 38, 0, 30, 30)
        self.ln(30)
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.multi_cell(0, 5, "Explorey Torium 2022\nFind your inner glory", 0, 'C')