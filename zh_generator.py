import json
from google import genai
from genai_rag import get_vector_store
from sema import zh_sema, mermaid_sema
from fpdf import FPDF
import os
# Másoláshoz
import shutil

def zh_base(api_key, model_name):
    client = genai.Client(api_key=api_key)
    vector_store = get_vector_store(api_key)

    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 40, "fetch_k": 100}
    )
    docs = retriever.invoke(" ")
    context_text = "\n\n---\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
         Te egy tapasztalt oktatási asszisztens vagy.  

        Forrásanyag:
        {context_text}
        
        Feladatod lesz egy zárthelyi írása lesz
        - Pontosan 5 darab Igaz-Hamis kérdést (indoklással)
        - Pontosan 5 darab Feleletválasztós kérdést (A, B, C, D opciókkal, helyes betűjellel és indoklással)
        - Pontosan 3 darab Kifejtős kérdést (elvár kulcsszavakkal és mintaválasszal)
        
        Szabályok:
        - Csak a forrásanag alapján készítsd el és ne állíts valótlan dolgot
         Az alábbi JSON séma alapján készítsd el
    """


    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": zh_sema,
        },
    )

    adatok = json.loads(response.text)

    # JSON mentése
    with open("zh.json", "w", encoding="UTF-8") as f:
        json.dump(adatok, f, indent=4, ensure_ascii=False)


def zh_generator(data):
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

    # Cím
    pdf.set_font(base_font, "B", size=20)
    pdf.cell(0, 20, text="Zárthelyi dolgozat", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    # Részletek
    pdf.set_font(base_font, size=11)
    pdf.cell(90, 10, text="Név: __________________________", ln=False)
    pdf.cell(90, 10, text="Neptun kód: ___________________", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, text="Dátum: 20__.____.____.", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)

    # Igaz-Hamis
    pdf.set_font(base_font, "B", size=14)
    pdf.cell(0, 10, text="1. feladat: Igaz - Hamis állítások (Karikázza be a helyes választ!)", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    for i, item in enumerate(data.get("igaz_hamis_kerdesek", []), 1):
        pdf.set_font(base_font, "", size=11)
        pdf.multi_cell(0, 6, text=f"{i}. {item['allitas']}", align="J")
        pdf.ln(1)
        pdf.set_font(base_font, "B", size=10)
        pdf.multi_cell(0, 6, text="        IGAZ              HAMIS  ", align="L")
        pdf.ln(3)

    pdf.ln(5)

    # Feleletválasztós
    pdf.set_font(base_font, "B", size=14)
    pdf.cell(0, 10, text="2. feladat: Feleletválasztós kérdések", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    for i, item in enumerate(data.get("feleletvalaszto_kerdesek", []), 1):
        pdf.set_font(base_font, "", size=11)
        pdf.multi_cell(0, 6, text=f"{i}. {item['kerdes']}", align="J", new_x="LMARGIN", new_y="NEXT")
        pdf.multi_cell(0, 6, text=f"    A) {item['opcio_A']}", align="L", new_x="LMARGIN", new_y="NEXT")
        pdf.multi_cell(0, 6, text=f"    B) {item['opcio_B']}", align="L", new_x="LMARGIN", new_y="NEXT")
        pdf.multi_cell(0, 6, text=f"    C) {item['opcio_C']}", align="L", new_x="LMARGIN", new_y="NEXT")
        pdf.multi_cell(0, 6, text=f"    D) {item['opcio_D']}", align="L", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(4)

    # Kifejtős
    pdf.add_page()
    pdf.set_font(base_font, "B", size=14)
    pdf.cell(0, 10, text="3. feladat: Kifejtős kérdések", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font(base_font, size=11)
    pdf.ln(2)

    for i, item in enumerate(data.get("kifejtos_kerdesek", []), 1):
        pdf.multi_cell(0, 6, text=f"{i}. {item['kerdes']}", align="J")
        pdf.ln(2)
        for _ in range(4):
            pdf.cell(0, 6, text="_________________________________________________________________________________", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(5)

    pdf.output("zh.pdf")


    PDFS_PATH = "pdfs"
    if not os.path.exists(PDFS_PATH):
        os.makedirs(PDFS_PATH)
    shutil.copy("zh.pdf", os.path.join(PDFS_PATH, f"zh.pdf"))

    if os.path.exists("zh.pdf"):
        os.remove("zh.pdf")


def zh_javitokulcs_generator(data):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_margins(10, 10, 10)

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

    # Cím
    pdf.set_font(base_font, "B", size=20)
    pdf.cell(190, 20, text="Zárthelyi dolgozat - Javítókulcs", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    # Igaz-Hamis
    pdf.set_font(base_font, "B", size=14)
    pdf.cell(190, 10, text="1. feladat: Igaz - Hamis állítások (Karikázza be a helyes választ!)", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    for i, item in enumerate(data.get("igaz_hamis_kerdesek", []), 1):
        pdf.set_font(base_font, "", size=11)
        pdf.multi_cell(190, 6, text=f"{i}. {item['allitas']}", align="J", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)
        # Helyes válasz félkövér
        pdf.set_font(base_font, "B", size=11)
        valasz_szoveg = "IGAZ" if item['helyes_valasz'] else "HAMIS"
        pdf.multi_cell(190, 6, text=f"    Helyes válasz: {valasz_szoveg}", align="L", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)

        # Indoklás dőlt
        pdf.set_font(base_font, "I", size=11)
        pdf.multi_cell(190, 6, text=f"    Indoklás: {item['indoklas']}", align="J", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(3)

    pdf.ln(5)

    # Feleletválasztós
    pdf.set_font(base_font, "B", size=14)
    pdf.cell(190, 10, text="2. feladat: Feleletválasztós kérdések", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    for i, item in enumerate(data.get("feleletvalaszto_kerdesek", []), 1):
        pdf.set_font(base_font, "", size=11)
        pdf.multi_cell(190, 6, text=f"{i}. {item['kerdes']}", align="J", new_x="LMARGIN", new_y="NEXT")

        # Helyes opció betűjele félkövér
        pdf.set_font(base_font, "B", size=11)
        pdf.multi_cell(190, 6, text=f"    Helyes opció: {item['helyes_opcio']}", align="L", new_x="LMARGIN", new_y="NEXT")

        # Magyarázat dőlt
        pdf.set_font(base_font, "I", size=11)
        pdf.multi_cell(190, 6, text=f"    Magyarázat: {item['indoklas']}", align="J", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(3)

    # Kifejtős
    pdf.add_page()
    pdf.set_font(base_font, "B", size=14)
    pdf.cell(190, 10, text="3. feladat: Kifejtős kérdések", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    for i, item in enumerate(data.get("kifejtos_kerdesek", []), 1):
        pdf.set_font(base_font, "", size=11)
        pdf.multi_cell(190, 6, text=f"{i}. {item['kerdes']}", align="J", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)
        # Elvárt kulcsszavak listája
        pdf.set_font(base_font, "B", size=11)
        kulcsszavak = ", ".join(item.get("elvart_kulcsszavak", []))
        pdf.multi_cell(190, 6, text=f"    Elvárt kulcsszavak: {kulcsszavak}", align="L", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)

        # Mintaválasz
        pdf.set_font(base_font, "I", size=11)
        pdf.multi_cell(190, 6, text=f"    Mintaválasz: {item['mintavalasz']}", align="J", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(4)

    pdf.output("javitokulcs.pdf")


    PDFS_PATH = "pdfs"
    if not os.path.exists(PDFS_PATH):
        os.makedirs(PDFS_PATH)
    shutil.copy("javitokulcs.pdf", os.path.join(PDFS_PATH, f"javitokulcs.pdf"))

    if os.path.exists("javitokulcs.pdf"):
        os.remove("javitokulcs.pdf")


def mermaid_zh(api_key, model_name):
    client = genai.Client(api_key=api_key)
    vector_store = get_vector_store(api_key)

    retriever = vector_store.as_retriever(
        search_type="mmr",  # változatosság miatt
        search_kwargs={"k": 40, "fetch_k": 100}
    )
    docs = retriever.invoke(" ")
    context_text = "\n\n---\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
        Te egy tapasztalt oktatási asszisztens vagy. 
    
            Forrásanyag:
            {context_text}

            Szabályok:
            - Csak a megadott forrásanyagból dolgozz
            - Ha a forrásanyagban nincs benne a válasz, mondd pontosan ezt: "Sajnos erről nem találtam információt a tananyagban." és szigorúan tilos Mermaid diagramot generálnod
            - Próbálj meg, egyszerűen válaszolni, hogy a diákok számára a lehető legérthetőbb legyen
    
    
            Generálj egy érvényes Mermaid.js diagramot a kérdés témájához.
            Diagramtípusok kiválasztása:
    
            - mindmap: Ha a téma fogalmi felépítéséről, kategóriákról vagy részegységekről szól.
            - flowchart TD: Ha egy folyamatról, döntési mechanizmusról vagy logikai láncról van szó.
            - sequenceDiagram: Ha két vagy több szereplő közötti időrendi üzenetváltást kell szemléltetni.
            - stateDiagram-v2: Ha egy egység különböző állapotait mutatod be.
            - erDiagram / classDiagram: Ha adatszerkezetek közötti fix kapcsolatokat ábrázolsz.
    
            Szigorú szabályok:
            - Csomópontok legyenek rövidek, max 4-5 szó, maximálisan 8 csomópont legyen
            - Egy csomópont feliratát (pl. A[Szöveg]) csak az első előforduláskor definiáld, utána már csak az azonosítóját (pl. A) használd a nyilaknál!
            - A nyilak formátuma felirat esetén: A -->|Szöveg| B (Ez a legbiztosabb forma)
            - A csomópontok szövegeiben (a szögletes zárójelen belül) ne használj idézőjeleket, kerek zárójelet vagy vesszőt.
            - A Mermaid kódban a csomópontok feliratait idézőjelek nélkül add meg, pl: A[HDD] vagy B[HDD merevlemez].
            - A Mermaid kódban ne használj kerek zárójelet (), vesszőt vagy egyéb írásjelet még az idézőjeleken belül sem.
            Az alábbi JSON séma alapján készítsd el
    """


    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": mermaid_sema,
        },
    )

    adatok = json.loads(response.text)

    # JSON mentése
    with open("mermaid_zh.json", "w", encoding="UTF-8") as f:
        json.dump(adatok, f, indent=4, ensure_ascii=False)