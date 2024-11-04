from fpdf import FPDF


# -----------------------------------------------------------------------
#   GhostPrintout
#
#   Basic PDF format for printing a ghost record
# -----------------------------------------------------------------------
class GhostPrintout(FPDF):
    def header(self):
        #self.set_y(-15)
        return
        #self.image("/home/admin/explorey/printer/resources/etLogo.jpg", 38, 0, 30, 30)
        #self.ln(30)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.multi_cell(0, 5, "Ghost Workshop 2024\nWarning: Ectoplasm is not for oral consumption", 0, 'C')
