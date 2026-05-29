import json
from fpdf import FPDF
import os
# Másoláshoz
import shutil


#with open("tananyag.json", "r", encoding="utf-8") as f:
#    data = json.load(f)

def pdf_generator(data, base_name):
    pdf = FPDF()
    pdf.add_page()

    font_path = r"C:\Windows\Fonts\arial.ttf"
    font_bold_path = r"C:\Windows\Fonts\arialbd.ttf"
    font_italic_path = r"C:\Windows\Fonts\ariali.ttf"

    if os.path.exists(font_path):
        pdf.add_font("ArialHU", "", font_path)
        pdf.add_font("ArialHU", "B", font_bold_path)
        pdf.add_font("ArialHU", "I", font_italic_path)
        base_font = "ArialHU"
    else:
        base_font = "helvetica"


    pdf.set_font(base_font, "B", size=20)
    pdf.cell(0, 20, text=data["cim"], align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font(base_font, size=12)
    pdf.multi_cell(0, 8, text=data["leiras"], align="J")
    pdf.ln(5)


    pdf.set_font(base_font, "B", size=14)
    pdf.cell(0, 10, text="Szakkifejezések és Definíciók:", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font(base_font, size=11)
    for def_obj in data["szakkifejezesek"]["definiciok"]:
        pdf.set_font(base_font, "B")
        pdf.write(5, f"{def_obj['kifejezes']}: ")
        pdf.set_font(base_font, "")
        pdf.multi_cell(0, 5, text=def_obj['magyarazat'], align="J")
        pdf.ln(2)

    pdf.add_page()
    pdf.set_font(base_font, "B", size=14)
    pdf.cell(0, 10, text="Kidolgozott Tételek:", new_x="LMARGIN", new_y="NEXT")

    for tetel in data["szakkifejezesek"]["tetelek"]:
        pdf.set_font(base_font, "B", size=12)
        pdf.cell(0, 8, text=tetel["nev"], new_x="LMARGIN", new_y="NEXT")
        pdf.set_font(base_font, size=11)
        pdf.multi_cell(0, 6, text=tetel["leiras"], align="J")
        pdf.ln(4)


    pdf.ln(5)
    pdf.set_font(base_font, "B", size=12)
    pdf.cell(0, 8, text="Összefüggések:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font(base_font, size=11)
    pdf.multi_cell(0, 6, text=data["osszefuggesek"], align="J")

    pdf.ln(5)
    pdf.set_font(base_font, "B", size=12)
    pdf.cell(0, 8, text="Didaktikai tipp:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font(base_font, "I", size=11)
    pdf.multi_cell(0, 6, text=data["didaktikai_tipp"], align="J")

    pdf.output("tananyag.pdf")
    #print("A PDF elkészült: tananyag.pdf")

    PDFS_PATH = "pdfs"
    if not os.path.exists(PDFS_PATH):
        os.makedirs(PDFS_PATH)
    shutil.copy("tananyag.pdf", os.path.join(PDFS_PATH, f"{base_name}.pdf"))
