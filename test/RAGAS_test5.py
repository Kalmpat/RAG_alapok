import os
import json
import re
import time
from uuid import uuid4

from google import genai



# FlashRank import
from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_classic.retrievers.document_compressors import CohereRerank
from langchain_community.document_compressors import FlashrankRerank

# Ragas
from ragas import evaluate
from ragas.metrics import Faithfulness, ContextRecall, AnswerRelevancy, ContextPrecision, AnswerCorrectness
from ragas.llms import llm_factory
from datasets import Dataset
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.run_config import RunConfig


from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings


from sema import mermaid_sema
from prompts import prompts


lassito_config = RunConfig(
    max_workers=1,
    max_retries=15,
    max_wait=120
)


# Konfiguráció
DATA_PATH = r"data"
CHROMA_PATH = r"chroma_db"
api_key = "api kulcs ide"
model_name = "gemini-2.5-flash-lite"


# LLM és embedding beállítása
client = genai.Client(api_key=api_key)

# RAGAS LLM - Geminivel
ragas_llm = llm_factory(
    model="gemini-3.1-flash-lite",
    provider="google",
    client=client
)

# RAGAS Embeddings – Gemini embedding
embeddings_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=api_key
)
ragas_embeddings = LangchainEmbeddingsWrapper(embeddings_model)


# Teszt kérdések
test_samples = [
    {
        "question": "Mi az adatkapcsolati réteg feladatai?",
        "ground_truth": "Az adatkapcsolati réteg feladatai közé tartozik a felsőbb rétegbeli protokollok kezelése, a folyamszabályozás, valamint a szomszédos csomópontok közötti megbízható adatátvitel biztosítása. További kulcsfontosságú feladata a keretezés, a keretekre vonatkozó ellenőrzőösszeg számítása, a helyi hálózaton való címzés, valamint a közeghozzáférés (multiple access) vezérlése."
    },
    {
        "question": "Milyen IP címosztályok léteznek?",
        "ground_truth": "Az IP-címosztályokat az osztályazonosító prefix határozza meg. Az A, B és C osztályok egyedi címzésre (unicast) szolgálnak: az A osztály prefixe 0, a B osztályé 10, a C osztályé pedig 110. A D osztály (prefix: 1110) a többes címzésre (multicast) fenntartott tartomány 224.0.0.0-tól 239.255.255.255-ig, míg az E osztály (prefix: 1111) kísérleti célokra fenntartott 240.0.0.0-tól 255.255.255.255-ig. Speciális címnek számít a hálózat címe (ahol a host azonosító csupa 0) és a broadcast cím (ahol a host azonosító csupa 1)."
    },
    {
        "question": "Milyen szállítási protokollok léteznek és mi a különbség köztük?",
        "ground_truth": "A szállítási réteg két alapvető protokollja az UDP (User Datagram Protocol) és a TCP (Transmission Control Protocol). Az UDP jellemzője, hogy összeköttetésmentes, „best-effort” típusú, megbízhatatlan átvitelt nyújt, nincs nyugtázás és sorrendhelyesség, viszont alacsony a késleltetése. Ezzel szemben a TCP kapcsolat-orientált, megbízható, sorrendhelyes és hibamentes szállítást biztosít (nyugtákkal és újraküldéssel), aminek ára a nagyobb késleltetés. Mindkét protokoll feladata a multiplexelés, amit a portszámok használatával valósítanak meg."
    },
    {
        "question": "Sorold fel a legfontosabb TCP feletti alkalmazásokat, protokollokat és a hozzájuk tartozó portszámokat!",
        "ground_truth": "A TCP protokoll felett számos alkalmazás és protokoll működik, melyek tipikus szerveroldali portszámai a következők: a fájlátvitelhez használt FTP (20-as port az adathoz, 21-es a vezérléshez), a távoli elérést biztosító SSH (22) és Telnet (23), valamint az e-mail küldésért felelős SMTP (25) és annak biztonságos változata, az SMTPS (465). A webes forgalmat a HTTP (80) és a biztonságos HTTPS (443) bonyolítja. A névfeloldást végző DNS az 53-as portot használja (TCP-n és UDP-n egyaránt). A levelek letöltéséhez a POP3 (110) és POP3S (995), míg a levelek eléréséhez az IMAP4 (143) és IMAP4S (993) protokollok tartoznak."
    },
    {
        "question": "Mi a különbség az analóg, a digitális és a bináris jelek között?",
        "ground_truth": "Minden fizikai közegen megjelenő jel valójában analóg, azaz folytonos jel, amely végtelen sok lehetséges értékkel rendelkezik (akkor is, ha korlátos a tartománya). Egy jel akkor digitális, ha annak értelmezzük: fontos jellemzője, hogy véges sok lehetséges értéke van (diszkrét állapotok), amelyekhez viszonyítunk. A bináris jel ennek egy konkrét formája, amely összesen két lehetséges értéket vehet fel (például 0 vagy 1, igaz vagy hamis, fekete vagy fehér pixel)."
    },
    {
        "question": "Sorold fel az ISO/OSI referenciamodell rétegeit és azok főbb jellemzőit!",
        "ground_truth": "Fizikai réteg: A fizikai közeg specifikációjáért és a bitek továbbításáért felelős (vonal kódolás, moduláció). Adatkapcsolati réteg: Feladata a bitsorozatok „keretezése”, a fizikai címek (MAC) kezelése és a közeghozzáférés vezérlése. Jellemző eszközei a bridge és a switch. Hálózati réteg: Egyedi linkek összefűzésével végpontok közötti csatornát hoz létre, logikai címzést (IP) és útvonalkeresést végez. Jellemző eszközei az útvonalválasztók (routerek). Szállítási réteg: Végpontok közötti hibamentes összeköttetést (hibás csomagok ismétlése, sorrend helyreállítása) és forgalomszabályozást biztosít. Viszonyréteg: A kapcsolat irányának és az összeköttetés felépítésének/lebontásának kezeléséért felel. Megjelenítési réteg: A felhasználói adatok ábrázolásával, adattömörítéssel és titkosítással foglalkozik. Alkalmazási réteg: A végpontokon futó alkalmazási programokat és protokollokat (pl. HTTP, FTP, SMTP) tartalmazza, melyek a felhasználót szolgálják ki."
    },
    {
        "question": "Mi az routing?",
        "ground_truth": "Az a mechanizmus, mely segítségével a szállítandó információ a megfelelő úton kerül továbbításra a végpontok között. Szűkebb értelemben magát az útvonalválasztást jelenti, tágabb értelemben pedig beleértjük a csomagok csomópontokon belüli továbbítását is (forward). A routing magában foglalja az útvonalválasztó módszereket, algoritmusokat és azokat megvalósító protokollokat. Legfőbb kihívásai, hogy a hálózat felépítése általában nem állandó (ezért adaptív módra van szükség), valamint a hálózat nagy mérete miatt gyakran nincs pontos és aktuális információ a teljes hálózat állapotáról.",
    },
    {
        "question": "Mi az a PCM, és melyek az A-D átalakítás főbb lépései?",
        "ground_truth": "A PCM (Pulse Code Modulation, impulzuskód-moduláció) egy eljárás, amelyet beszéddigitalizálásra (kódolás-dekódolás: kodek) használnak, és a mai A/D átalakítás alapját képezi. Célja egy bitsorozat előállítása egy folytonos feszültség-idő függvényből. Az A-D átalakítás lépései: sávszűrés, mintavétel, kvantálás és kódolás. A folyamat fordítottja a D-A átalakítás, amely a kvantálás inverz karakterisztikájával és sávszűréssel (simítás) állítja vissza az eredetihez nagyon hasonló jelet."
    },
    {
        "question": "Mi az elektronikus levelezésnek a fő alkotóelemei?",
        "ground_truth": "User Agent: Ez a komponens felelős a levelek írásáért, szerkesztéséért és olvasásáért. Példák rá: Mozilla Thunderbird, Outlook, vagy a Mail alkalmazás. A kimenő és bejövő leveleket a szerveren tárolja. Levélszerverek: Itt található a felhasználó postaládája, amely tartalmazza a bejövő leveleket. A szerveren van a kimenő levelek várólistája is. Levelező protokoll (SMTP): A Simple Mail Transfer Protocol felelős az e-mailek továbbításáért a levélszerverek között. Ebben a folyamatban a küldő a kliens, a fogadó pedig a szerver."
    },
    {
        "question": "Milyen tényezők befolyásolják a beszédminőséget a csomagkapcsolt hálózatokban, és mik ezek határértékei?",
        "ground_truth": "A beszédminőséget befolyásoló fő tényezők: Késleltetés (Delay): Megengedett maximum: Körülbelül 150 ms. Késleltetés-ingadozás (Jitter / Packet Delay Variance): Megengedett maximum: Néhány tíz ms. Csomagvesztés (Packet Loss): Megengedett maximum: Néhány %, de csak akkor tolerálható, ha: A kiesett beszédszegmensek rövidek (kb. 10 ms nagyságrendűek). A vesztések véletlenszerűen oszlanak meg az időben. Fontos megjegyzés, hogy a Video over IP esetében még ennél is szigorúbbak a követelmények."
    },
    {
        "question": "Sorold fel az érpáras kábelkategóriákat és jellemzőiket, valamint foglald össze az optikai szálak fő tulajdonságait!",
        "ground_truth": "Cat3: Főleg beszédátvitelre (telefon) és riasztóknak használják. (Elavult) 10 Mb/s-os Ethernet átvitelére képes. Cat5: 100 Mb/s sebességű Ethernet hálózatokhoz. Cat5e: 1 Gb/s sebességű Ethernet hálózatokhoz. Cat 6, 6a: 10 Gb/s sebességű Ethernet hálózatokhoz. Fontos jellemző: A kategóriák visszafele kompatibilisek egymással. Optikai szálak tulajdonságai: Működési elv: Nem elektromos jelet, hanem fényt továbbítanak (üveg vagy műanyag szálban), amely a szálon belül marad. Adója LED vagy lézer lehet. Sávszélesség: Hatalmas kapacitás (több tíz THz, akár több száz Gb/s – Tb/s sebesség). Csillapítás: Nagyon alacsony, akár 10 km-es távolság is áthidalható erősítő nélkül. Fizikai jellemzők: Vékony és könnyű, de viszonylag sérülékeny. Ára nem drágább a réznél. Zavartűrés: Nem zavarja az elektromágneses sugárzás és nem kelt EM sugárzást (nehezebb lehallgatni, zavartűrőbb)."
    },
    {
        "question": "Hogyan terjednek a rádióhullámok és melyek a fő terjedési módok jellemzői?",
        "ground_truth": "A rádióhullámok nagyban függnek a hullám frekvenciájától, 3 fő terjedési tulajdonsága: a talajhullámok, térhullámok, és az egyenes vonalú terjedés.Talajhullámok (Ground Wave Propagation): A Föld felszínét követő hullámok, amelyek 2 MHz frekvencia alatt jellemzőek. A látótávolságon túl is követik a felszínt; példa rá az AM rádió (pl. Kossuth: 540 kHz). Térhullámok (Sky Wave Propagation): Az ionoszféráról és a Földről is visszaverődnek, így akár több ezer kilométert is képesek áthidalni. Jellemző frekvenciatartományuk 2–30 MHz. Egyenes vonalú terjedés (Line-of-Sight Propagation): A 30 MHz feletti hullámokra jellemző, ahol az adónak és a vevőnek látnia kell egymást (mint a fény esetében). Előfordulhat visszaverődés, elhajlás vagy akadályon való áthaladás is."
    },
    {
        "question": "Hogyan működik a címfeloldás ARP-val és mi az az ARP tábla?",
        "ground_truth": "A címfeloldás folyamata ARP (Address Resolution Protocol) segítségével és az ARP tábla szerepe a hálózati kommunikációban az alábbiak szerint foglalható össze: Az ARP protokoll akkor lép működésbe, amikor egy hálózati eszköz (például „A” gép) ismeri a céleszköz („B” gép) IP-címét, de a kommunikációhoz szüksége van annak fizikai MAC-címére is. A folyamat két fő lépésből áll: ARP Request (Kérés): „A” eszköz egy üzenetet küld a hálózatnak, amelyben megadja a saját MAC- és IP-címét, valamint a céleszköz („B”) IP-címét. Mivel a cél MAC-címe ismeretlen, a cél hardvercíme (Target HA) 00:00:00:00:00:00. A kérést broadcast üzenetként küldi el, a keret fejlécében a cél MAC-címe FF:FF:FF:FF:FF:FF. ARP Reply (Válasz): „B” eszköz felismeri a saját IP-címét a kérésben, és válaszol. A válasz tartalmazza „B” saját MAC-címét. Ebben az üzenetben a cél már „A” eszköz konkrét MAC- és IP-címe lesz. Az ARP tábla, amely adatkapcoslati rétegbeli és IP címek párosát tárolja. Bejegyzéstípusok: Statikus: Manuálisan felvitt bejegyzés. Dinamikus: Az ARP címfeloldás eredményeként automatikusan jön létre. Gyorsítótár (cache) funkció: A tábla célja, hogy ne kelljen mindig lekérdezni a folyamatot. Élettartam: A dinamikus bejegyzések egy bizonyos idő után elévülnek és automatikusan törlődnek a táblából."
    },
    {
        "question": "Mik a leggyakoribb HTTP parancsok?",
        "ground_truth": "A leggyakoribb HTTP parancsok a következők: GET <URL>: Egy adott URL-en található tartalom lekérésére szolgál. HEAD: Hasonló a GET-hez, de az adatok helyett csak a metaadatokat adja vissza a szerver. POST: segítségével a kliens adatokat tud küldeni a szervernek. PUT: A POST-hoz hasonlóan adatküldésre, jellemzően fájlfeltöltésre alkalmas. DELETE: Egy adott URL-en található tartalom törlését kezdeményezi."
    },
    {
        "question": "Mi az a DHCP, mik az előnyei, és hogyan jelenik meg IPv6 környezetben?",
        "ground_truth": "A DHCP (Dynamic Host Configuration Protocol) segítségével IP-beállításokat oszthatunk ki vele dinamikusan. Előnyeihez tartozik, hogy a klienseket egyszerű beállítani, központilag módosítani és jellemző a mobilitás a hálózatok között. Fontos megjegyezni, hogy IPv6-ban is megjelenik: Stateless Address Autoconfiguration (SLAAC)"
    },


]




# Chroma vektorizálás
if not os.path.exists(CHROMA_PATH) or not os.listdir(CHROMA_PATH):
    print("PDF fájlok beolvasása és vektorizálása...")
    loader = PyPDFDirectoryLoader(DATA_PATH)
    raw_documents = loader.load()


    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=300,
        length_function=len,
        is_separator_regex=False,
    )
    chunks = text_splitter.split_documents(raw_documents)
    uuids = [str(uuid4()) for _ in range(len(chunks))]

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings_model,
        persist_directory=CHROMA_PATH,
        collection_name="tananyagok",
        ids=uuids
    )
else:
    print("Meglévő Chroma adatbázis betöltése...")
    vector_store = Chroma(
        collection_name="tananyagok",
        embedding_function=embeddings_model,
        persist_directory=CHROMA_PATH,
    )


# Segédfüggvény retry logikával
def generate_with_retry(client, model_name, prompt, sema, retries=5, wait_sec=8):
    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_json_schema": sema,
                },
            )
            return json.loads(response.text)
        except Exception as e:
            error_str = str(e)
            if "503" in error_str or "429" in error_str:
                print(f"[{attempt+1}/{retries}] 503/429 hiba → újrapróbálás {wait_sec} másodperc múlva...")
                time.sleep(wait_sec)
            else:
                print(f"Hiba a generálás során: {error_str}")
                raise e
    raise RuntimeError("Sikertelen generálás többszöri próbálkozás után.")

# Reranking berakása FlashRank
#compressor = FlashrankRerank(top_n=10)

retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 15, "fetch_k": 30}
)

# Reranking berakása FlashRank
#compression_retriever = ContextualCompressionRetriever(
#    base_compressor=compressor,
#    base_retriever=retriever
#)


# Reranking berakása Cohere
#compressor = CohereRerank(
#    cohere_api_key="",
#    model="rerank-v4.0-pro",  # A legújabb modell
#    top_n=10
#)

#compression_retriever = ContextualCompressionRetriever(
#    base_compressor=compressor, base_retriever=retriever
#)


# Feldolgozás
results = []

for i, item in enumerate(test_samples):
    q = item["question"]
    print(f"\n[{i+1}] Kérdés: {q}")

    #docs = compression_retriever.invoke(q)
    docs = retriever.invoke(q)
    contexts = [doc.page_content for doc in docs]
    context_text = "\n\n---\n\n".join(contexts)
    prompt = prompts(q, context_text, "Mermaid")

    try:
        adatok = generate_with_retry(client, model_name, prompt, mermaid_sema)
        answer = adatok.get("answer", "")
        print("Generálás sikeres")
    except Exception as e:
        print(f"Hiba a generálás során: {e}")
        answer = ""

    results.append({
        "id": i,
        "question": q,
        "answer": answer,
        "contexts": contexts,
        "ground_truth": item["ground_truth"],
        "top_context": contexts[0] if contexts else "",
    })

    time.sleep(2)


with open("results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)


# RAGAS Kiértékelés
print("\nRAGAS kiértékelés indítása...")
ds = Dataset.from_list(results)

metrics_list = [
    Faithfulness(llm=ragas_llm),
    AnswerRelevancy(llm=ragas_llm, embeddings=ragas_embeddings),
    ContextRecall(llm=ragas_llm),
    ContextPrecision(llm=ragas_llm),
    AnswerCorrectness(llm=ragas_llm)
]

all_scores = {}
for metric in metrics_list:
    print(f"\n→ {metric.name} mérése...")
    score = evaluate(
        ds,
        metrics=[metric],
        llm=ragas_llm,
        embeddings=ragas_embeddings,
        run_config=lassito_config
    )

    raw_val = score[metric.name]
    final_val = raw_val[0] if isinstance(raw_val, list) else raw_val

    all_scores[metric.name] = final_val

    print(f"  Eredmény: {final_val:.4f}")
    print("  Várakozás 65 másodpercet (rate limit)...")
    time.sleep(65)
print("\nEredmények (0.0 - 1.0 skálán):")
print(f"Hűség (Faithfulness):              {all_scores.get('faithfulness', 0):.4f}")
print(f"Relevancia (AnswerRelevancy):      {all_scores.get('answer_relevancy', 0):.4f}")
print(f"Visszahívás (ContextRecall):       {all_scores.get('context_recall', 0):.4f}")
print(f"Kontextus Precizitás (ContextPrec):{all_scores.get('context_precision', 0):.4f}")
print(f"Válasz Helyessége (Correctness):   {all_scores.get('answer_correctness', 0):.4f}")