
import time

# RAGAS kiértéléshez
from datasets import Dataset
from ragas import evaluate
from ragas.metrics.collections import Faithfulness, ContextRecall, AnswerRelevancy
from ragas.llms import LangchainLLMWrapper, llm_factory

# Adatgyűjtés (szkenelés)
from langchain_community.document_loaders import PyPDFLoader, PyPDFDirectoryLoader
from langchain_chroma import Chroma
# Darabolás (chunkolás) recursive bekezdés -> szöveg -> mondatok -> szavak
from langchain_text_splitters import RecursiveCharacterTextSplitter
# Vektorizálás (vektorokká alakítás) szavak -> számok
import os
from google import genai

# Azonosításhoz
from uuid import uuid4

# Vektorizálás rész
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from prompts import prompts

# Json-höz
import json

from sema import mermaid_sema, graphviz_sema, echart_sema, plantuml_sema, d2lang_sema


api_key = "api kulcs ide"
model_name = "gemini-2.5-flash"

DATA_PATH = r"data"
CHROMA_PATH = r"chroma_db"

# RAGAS LLM megmondás
from langchain_google_genai import ChatGoogleGenerativeAI

client = genai.Client(api_key=api_key)

ragas_llm = llm_factory(
    "gemini-2.5-flash",
    client=client
)


# Kérdések
test_samples = [
    {
        "question": "Mi az elektronikus levelezésnek a fő alkotóelemei?",
        "ground_truth": "User Agent: Ez a komponens felelős a levelek írásáért, szerkesztéséért és olvasásáért. Példák rá: Mozilla Thunderbird, Outlook, vagy a Mail alkalmazás. A kimenő és bejövő leveleket a szerveren tárolja. Levélszerverek: Itt található a felhasználó postaládája, amely tartalmazza a bejövő leveleket. A szerveren van a kimenő levelek várólistája is. Levelező protokoll (SMTP): A Simple Mail Transfer Protocol felelős az e-mailek továbbításáért a levélszerverek között. Ebben a folyamatban a küldő a kliens, a fogadó pedig a szerver."
    },


]







# Konfigurálás az adatok és az adatbázis elérése
DATA_PATH = r"data"
CHROMA_PATH = r"chroma_db"

# Adatbázis mentése
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

# Feldolgozás
def process(query, api_key, model_name, selection_viz):
    client = genai.Client(api_key=api_key)
    vector_store = get_vector_store(api_key)

    retriever = vector_store.as_retriever(
        search_type="mmr",  # változatosság miatt
        search_kwargs={"k": 15, "fetch_k": 30}
    )
    docs = retriever.invoke(query)
    contexts =[doc.page_content for doc in docs]
    context_text = "\n\n---\n\n".join(contexts)

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

    # A választ és a kontextust is visszaadjuk
    return adatok.get("answer", ""), contexts


results = []

for i,item in enumerate(test_samples):
    q = item["question"]

    print(f"\n--- [{i}] Kérdés: {q}")

    try:
        # Feldolgozás
        generated_answer, contexts = process(q, api_key, model_name, "Mermaid")

        results.append({
            "id": i,
            "question": q,
            "answer": generated_answer,
            "contexts": contexts,
            "ground_truth": item["ground_truth"],
            "top_context": contexts[0] if contexts else "",
        })


    except Exception as e:
        print(f"Hiba történt {e}")
        results.append({
            "id": i,
            "question": q,
            "answer": "",
            "contexts": [],
            "ground_truth": item["ground_truth"],
            "top_context": "",
        })
    time.sleep(5)

with open("results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)


# Kiértékelés
ds = Dataset.from_list(results)

score = evaluate(
    ds,
    metrics=[
        Faithfulness(),
        AnswerRelevancy(),
        ContextRecall()
    ],
    llm=ragas_llm
)

print("\n" + "=" * 40)
print("EREDMÉNYEK (0.0 - 1.0 skálán):")
print("-" * 40)
print(f"Hűség (Faithfulness):      {score['faithfulness']:.4f}")
print(f"Relevancia (Relevance):    {score['answer_relevance']:.4f}")
print(f"Visszahívás (Recall):       {score['context_recall']:.4f}")
print("=" * 40)

