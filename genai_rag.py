# Adatgyűjtés (szkenelés)
from langchain_community.document_loaders import PyPDFLoader, PyPDFDirectoryLoader
from langchain_chroma import Chroma
# Darabolás (chunkolás) recursive bekezdés -> szöveg -> mondatok -> szavak
from langchain_text_splitters import RecursiveCharacterTextSplitter
# Vektorizálás (vektorokká alakítás) szavak -> számok
# from langchain_openai.embeddings import OpenAIEmbeddings # ha van OPENAI API
from dotenv import load_dotenv
import os
from google import genai

# Azonosításhoz
from uuid import uuid4

# Vektorizálás rész
from langchain_google_genai import GoogleGenerativeAIEmbeddings


# Json-höz
import json

from prompts import prompts
from sema import mermaid_sema, graphviz_sema, echart_sema, plantuml_sema, d2lang_sema
# Beállítások betöltése
#load_dotenv()
#api_key = os.getenv("GOOGLE_API_KEY")

#if not api_key:
    #print("Hiba: Hiányzik az API kulcs a .env fájlból!")



# Konfigurálás az adatok és az adatbázis elérése
DATA_PATH = r"data"
CHROMA_PATH = r"chroma_db"


def get_vector_store(api_key):
    #  Vektor modell
    embeddings_model = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        google_api_key=api_key
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
            # vector_store.add_documents(documents=chunks, ids=uuids)
    else:
        # Vektor adatbázis beállítása
        vector_store = Chroma(
            collection_name="tananyagok",
            embedding_function=embeddings_model,
            persist_directory=CHROMA_PATH,
        )
    return vector_store

# query = "Miről szól a tananyag?"

def delete_file(filename,api_key):
    # Embedding model
    embeddings_model = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        google_api_key=api_key
    )
    # Az adatbázis
    vector_store = Chroma(
        collection_name="tananyagok",
        embedding_function=embeddings_model,
        persist_directory=CHROMA_PATH,
    )

    # Útvonal megadása (join, ha megváltozna a mappa neve)
    target = os.path.join(DATA_PATH, filename)

    # Törlés
    vector_store.delete(where={"source": target})


def embed_file(filename,api_key):
    embeddings_model = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        google_api_key = api_key
    )
    loader = PyPDFLoader(filename)
    document = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=300,
        length_function=len,
        is_separator_regex=False,
    )

    chunks = text_splitter.split_documents(document)
    vector_store = Chroma(
        collection_name="tananyagok",
        embedding_function=embeddings_model,
        persist_directory=CHROMA_PATH,
    )

    uuids = [str(uuid4()) for _ in range(len(chunks))]
    vector_store.add_documents(documents=chunks, ids=uuids)



def process(query, api_key, model_name, selection_viz):
    client = genai.Client(api_key=api_key)
    vector_store = get_vector_store(api_key)

    retriever = vector_store.as_retriever(
        search_type="mmr",  # változatosság miatt
        search_kwargs={"k": 15, "fetch_k": 30}
    )
    docs = retriever.invoke(query)
    context_text = "\n\n---\n\n".join([doc.page_content for doc in docs])

    prompt = prompts(query, context_text, selection_viz)
    sema = mermaid_sema
    if selection_viz == "Mermaid":
        sema = mermaid_sema
    elif selection_viz == "Graphviz":
        sema = graphviz_sema
    elif selection_viz == "Echart":
        sema = echart_sema
    elif selection_viz == "Plantuml":
        sema = plantuml_sema


    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": sema,
        },
    )

    # print(response.text)

    #return response
    adatok = json.loads(response.text)
    # print(json.dumps(adatok, indent=4,ensure_ascii=False))

    # JSON mentése
    with open("chatviz.json", "w", encoding="UTF-8") as f:
        json.dump(adatok, f, indent=4, ensure_ascii=False)