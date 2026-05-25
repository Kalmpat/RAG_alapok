from google import genai
from langchain_classic.retrievers import MultiQueryRetriever

from RAGAS_test2 import vector_store, api_key


def query_expansion(query, doc, api_key, model_name):
    prompt = (f"A feladatod az, hogy a lenti kérdést fogalmazd át 5 különböző módon a pontosabb keresés érdekében. "
              f"Csak a kérdéseket add vissza, soronként elválasztva, sorszámozás nélkül.\n"
              f"Kérdés: {query}\n"
              f"Forrásanyag: {doc}")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
    )

    generated_text = response.text
    queries = [q.strip() for q in generated_text.split('\n') if q.strip()]

    return queries



retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 15, "fetch_k": 30}
)

# https://www.kaggle.com/code/ksmooi/langchain-multiqueryretriever-quick-reference
api_key = ""
client = genai.Client(api_key=api_key)
model = "gemini-2.5-flash-lite"
multi_query_retriever = MultiQueryRetriever.from_llm(
    retriever=retriever,
    llm=model,
    include_original=True
)