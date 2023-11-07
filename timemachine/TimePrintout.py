from fpdf import FPDF


# -----------------------------------------------------------------------
#   TimePrintout
#
#   Basic PDF format for printing a time record
# -----------------------------------------------------------------------
class TimePrintout(FPDF):
    def header(self):
        #self.set_y(-15)
        return
        #self.image("/home/admin/explorey/printer/resources/etLogo.jpg", 38, 0, 30, 30)
        #self.ln(30)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.multi_cell(0, 5, "Timeless Emporium 2023\nFeaturing Time Flavored Play-doh", 0, 'C')
