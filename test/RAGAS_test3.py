import json
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import Faithfulness, ContextRecall, AnswerRelevancy, ContextPrecision, AnswerCorrectness
from google import genai
from ragas.llms import llm_factory
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.run_config import RunConfig


api_key = "api kulcs ide"
client = genai.Client(api_key=api_key)

ragas_llm = llm_factory(model="gemini-3.1-flash-lite", provider="google", client=client)
embeddings_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001", google_api_key=api_key)
ragas_embeddings = LangchainEmbeddingsWrapper(embeddings_model)

lassito_config = RunConfig(max_workers=1, max_retries=20, max_wait=120)

print("Results.json betöltése...")
with open("results.json", "r", encoding="utf-8") as f:
    data = json.load(f)


print("RAGAS mérés indítása a meglévő adatokon...")
ds = Dataset.from_list(data)
score = evaluate(
    ds,
    metrics=[Faithfulness(llm=ragas_llm), AnswerRelevancy(llm=ragas_llm, embeddings=ragas_embeddings),
             ContextRecall(llm=ragas_llm), ContextPrecision(llm=ragas_llm), AnswerCorrectness(llm=ragas_llm)],
    llm=ragas_llm,
    embeddings=ragas_embeddings,
    run_config=lassito_config
)

print("\nVégeredmény:")
print(score)