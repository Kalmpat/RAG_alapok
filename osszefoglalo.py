from dotenv import load_dotenv
import os
# Google AI-hoz
from google import genai
# Adatgyűjtés (szkenelés)
from langchain_community.document_loaders import PyPDFLoader, PyPDFDirectoryLoader
from sema import tananyag_sema

# JSON-höz
import json

# Betöltés
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("Nincs API kulcs")
    exit(1)

client = genai.Client(api_key=api_key)

# Konfigurálás az adatok eléréséhez
DATA_PATH = r"data"

if not os.path.exists(DATA_PATH):
    print("Hiba, nem található az fájl")
    exit(1)


def process(file_path):
    # Doksik betöltése
    # loader = PyPDFDirectoryLoader(DATA_PATH)
    loader = PyPDFLoader(file_path)
    raw_documents = loader.load()
    full_text = "\n".join([page.page_content for page in raw_documents])
    # print(f"PDF beolvasva, karakterek száma: {len(full_text)}")

    prompt = f"""
        Te egy oktatási asszisztens vagy. 
        A feladatod, hogy az alábbi forrásanyag alapján készíts egy strukturált, könnyen tanulható egyszerű összefoglalót diákok számára.
        Csak olyan dolgokat rakjál bele, ami a forrásanyagban is szerepel

        Forrásanyag:
        {full_text}

        Az összefoglalót az alábbi JSON séma alapján készíts el
        """

    #print("\nÖsszefoglaló generálása\n")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": tananyag_sema,
        },
    )

    # print(response.text)

    # JSON feldolgozása
    adatok = json.loads(response.text)
    # print(json.dumps(adatok, indent=4,ensure_ascii=False))

    # JSON mentése
    with open("tananyag.json", "w", encoding="UTF-8") as f:
        json.dump(adatok, f, indent=4, ensure_ascii=False)


