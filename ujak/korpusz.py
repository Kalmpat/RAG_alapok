import re
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def clean_text(text):
    # Oldalszámok és fejléc eltávolítása
    text = re.sub(r'^\d+\s+|\s+\d+$', ' ', text)
    # Szögletes zárójelek eltávolítása
    text = re.sub(r'\[.*?\]', '', text)
    # Felesleges szóközök eltávolítása
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

DATA_PATH = r"data"


loader = PyPDFDirectoryLoader(DATA_PATH)
raw_documents = loader.load()

for doc in raw_documents:
    doc.page_content = clean_text(doc.page_content)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100,
)
chunks = text_splitter.split_documents(raw_documents)

print(f"Összesen {len(chunks)} szelet készült \n")

for i, chunk in enumerate(chunks[:3]):
    print(f"{i+1}.(Oldal: {chunk.metadata.get('page', 'N/A')}) ")
    print(chunk.page_content)