import json
import warnings
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import Faithfulness, ContextRecall, AnswerRelevancy, ContextPrecision, AnswerCorrectness
from google import genai
from ragas.llms import llm_factory
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.run_config import RunConfig

warnings.filterwarnings("ignore")

api_key = "api kulcs ide"
client = genai.Client(api_key=api_key)

ragas_llm = llm_factory(
    model="gemini-2.5-flash",
    provider="google",
    client=client
)


embeddings_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=api_key
)
ragas_embeddings = LangchainEmbeddingsWrapper(embeddings_model)

lassito_config = RunConfig(
    max_workers=1,
    max_retries=30,
    max_wait=180
)

# ─── DATA ─────────────────────────────
print("Results.json betöltése...")
with open("results.json", "r", encoding="utf-8") as f:
    data = json.load(f)


ds = Dataset.from_list(data)


print("\nBasic Metrikák")

basic_metrics = [
    Faithfulness(llm=ragas_llm),
    AnswerRelevancy(llm=ragas_llm, embeddings=ragas_embeddings),
    ContextRecall(llm=ragas_llm),
]

score_basic = evaluate(
    ds,
    metrics=basic_metrics,
    llm=ragas_llm,
    embeddings=ragas_embeddings,
    run_config=lassito_config
)

print("\nBasic eredmény:")
print(score_basic)


print("\nAdvanced metrikák")

advanced_metrics = [
    ContextPrecision(llm=ragas_llm),
    AnswerCorrectness(llm=ragas_llm),
]

score_advanced = evaluate(
    ds,
    metrics=advanced_metrics,
    llm=ragas_llm,
    embeddings=ragas_embeddings,
    run_config=lassito_config
)

print("\nAdvanced metrikák:")
print(score_advanced)