from fpdf import FPDF


##-----------------------------------------------------------------------
#   ItemPrintout
#
#   Basic PDF format for making an Item
##-----------------------------------------------------------------------
class ItemPrintout(FPDF):
    def header(self):
        self.image("/home/admin/explorey/printer/resources/onion.png", 43, 0, 20, 20)
        self.ln(20)
        return

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)

        self.multi_cell(
            0,
            5,
            "Goblin Encounters LTD 2023\nGoblin Encounters LTD is not responsible for any loss of life, limb, or sanity due to cursed items.",
            0,
            "C",
        )
