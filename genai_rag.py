# Adatgyűjtés (szkenelés)
from langchain_community.document_loaders import PyPDFLoader, PyPDFDirectoryLoader
from langchain_chroma import Chroma
# Darabolás (chunkolás) recursive bekezdés -> szöveg -> mondatok -> szavak
from langchain_text_splitters import RecursiveCharacterTextSplitter
# Vektorizálás (vektorokká alakítás) szavak -> számok
#from langchain_openai.embeddings import OpenAIEmbeddings # ha van OPENAI API
from dotenv import load_dotenv
import os
from google import genai

# Azonosításhoz
from uuid import uuid4

# Vektorizálás rész
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Beállítások betöltése
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("Hiba: Hiányzik az API kulcs a .env fájlból!")

client = genai.Client(api_key=api_key)

# Konfigurálás az adatok és az adatbázis elérése
DATA_PATH = r"data"
CHROMA_PATH = r"chroma_db"


#  Vektor modell
embeddings_model = GoogleGenerativeAIEmbeddings(
    model = "gemini-embedding-001",
    google_api_key = api_key
)

# Ha az adatbázis nem létezik
if not os.path.exists(CHROMA_PATH) or not os.listdir(CHROMA_PATH):

    # Doksik betöltése
    loader = PyPDFDirectoryLoader(DATA_PATH)
    raw_documents = loader.load()

    # Darabolás
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=300,  # átfedés
        length_function=len,
        is_separator_regex=False,
    )
    chunks = text_splitter.split_documents(raw_documents)

    # Azonosítás
    uuids = [str(uuid4()) for _ in range(len(chunks))]

    # Vektor adatbázis beállítása
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings_model,
        persist_directory=CHROMA_PATH,
        collection_name="tananyagok",
        ids=uuids
    )
    #vector_store.add_documents(documents=chunks, ids=uuids)
else:
    # Vektor adatbázis beállítása
    vector_store = Chroma(
        collection_name="tananyagok",
        embedding_function=embeddings_model,
        persist_directory=CHROMA_PATH,
    )

#query = "Miről szól a tananyag?"

def processing(query):


    retriever = vector_store.as_retriever(
        search_type="mmr",  # változatosság miatt
        search_kwargs={"k": 15, "fetch_k": 30}
    )
    docs = retriever.invoke(query)
    context_text = "\n\n---\n\n".join([doc.page_content for doc in docs])



    prompt = f"""
        Te egy tapasztalt oktatási asszisztens vagy. 
        
        Forrásanyag:
        {context_text}
        
        Kérdés:
        {query}
        
        Szabályok:
        - Csak a megadott forrásanyagból dolgozz
        - Ha a forrásanyagban nincs benne a válasz, mondd pontosan ezt: "Sajnos erről nem találtam információt a tananyagban.", ne találj ki semmit hozzá
        - Próbálj meg, egyszerűen válaszolni, hogy a diákok számára a lehető legérthetőbb legyen
        
        
        """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    #print(response.text)

    return response
