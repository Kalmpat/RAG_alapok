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
    teljes_adat = json.load(f)

data2 = teljes_adat[25:]
print(f"RAGAS mérés 2/2 ({25 + 1}-{25 + len(data2)} kérdések)...")
ds2 = Dataset.from_list(data2)
score2 = evaluate(
    ds2,
    metrics=[Faithfulness(llm=ragas_llm), AnswerRelevancy(llm=ragas_llm, embeddings=ragas_embeddings),
             ContextRecall(llm=ragas_llm), ContextPrecision(llm=ragas_llm), AnswerCorrectness(llm=ragas_llm)],
    llm=ragas_llm,
    embeddings=ragas_embeddings,
    run_config=lassito_config
)
print("\nA második 25 részeredménye:")
print(score2)
# Mentés a második résznek:
score2.to_pandas().to_csv("ragas_2_resz.csv", index=False)