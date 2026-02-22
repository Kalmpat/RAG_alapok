# Adatgyűjtés (szkenelés)
from langchain_community.document_loaders import PyPDFLoader, PyPDFDirectoryLoader
# Darabolás (chunkolás) recursive bekezdés -> szöveg -> mondatok -> szavak
from langchain_text_splitters import RecursiveCharacterTextSplitter
# Vektorizálás (vektorokká alakítás) szavak -> számok
#from langchain_openai.embeddings import OpenAIEmbeddings # ha van OPENAI API
from langchain_ollama import OllamaEmbeddings #ingyenes
# Vektor adatbázis  (Vector store)
from langchain_chroma import Chroma
# Nagy nyelvi modellhez
from langchain_ollama import OllamaLLM


"""# .env betöltése (fizetős api)
from dotenv import load_dotenv
load_dotenv()
"""


# Konfigurálás az adatok és az adatbázis elérése
DATA_PATH = r"data"
CHROMA_PATH = r"chroma_db"

#  Vektor modell
embeddings_model = OllamaEmbeddings(model="nomic-embed-text")

# Vektor adatbázis beállítása
vector_store = Chroma(
    collection_name="tananyagok",
    embedding_function=embeddings_model,
    persist_directory=CHROMA_PATH,
)

# Doksik betöltése
loader = PyPDFDirectoryLoader(DATA_PATH)
raw_documents = loader.load()

# Darabolás
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=300, #átfedés
    length_function=len,
    is_separator_regex=False,
)

chunks = text_splitter.split_documents(raw_documents)

vector_store.add_documents(documents=chunks)

# LLM modell
llm = OllamaLLM(temperature=0.5, model="llama3.2")

query = "Miről szól a tananyag"
retriever = vector_store.as_retriever(search_kwargs={"k": 3})
docs = retriever.invoke(query)
context_text = "\n\n---\n\n".join([doc.page_content for doc in docs])

prompt = f"""
    Az alábbi forrásanyag alapján válaszolj a kérdésre. 
    Ha a forrásban nincs benne a válasz, mondd azt, hogy nem tudod, ne találj ki semmit.
    
    Forrásanyag:
    {context_text}
    
    Kérdés: {query}
    Válasz:
    """

# Válasz generálása
response = llm.invoke(prompt)
print(response)


