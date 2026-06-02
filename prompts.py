# Előfordulhatnak problémák, pl szintaktikai hibák vagy a szerverek nem érhetőek el
# Megoldás: promptokat finomhangolni kell (legtöbbször a diagramtípusok pontos leírását is meg kellene adni)

def prompts(query, context_text, selection_viz):
    if not context_text or len(context_text.strip()) == 0:
        context_text = "Sajnos erről nem találtam információt a tananyagban."

    if selection_viz =="Mermaid":
        prompt = f"""
            Te egy tapasztalt oktatási asszisztens vagy. 
    
            Forrásanyag:
            {context_text}
    
            Kérdés:
            {query}
    
            Szabályok:
            - Csak a megadott forrásanyagból dolgozz
            - Ha a forrásanyagban nincs benne a válasz, mondd pontosan ezt: "Sajnos erről nem találtam információt a tananyagban." és szigorúan tilos Mermaid diagramot generálnod
            - Próbálj meg, egyszerűen válaszolni, hogy a diákok számára a lehető legérthetőbb legyen
    
    
            Generálj egy érvényes Mermaid.js diagramot a kérdés témájához.
            Diagramtípusok kiválasztása:
    
            - mindmap: Ha a téma fogalmi felépítéséről, kategóriákról vagy részegységekről szól.
            - flowchart TD: Ha egy folyamatról, döntési mechanizmusról vagy logikai láncról van szó.
            - sequenceDiagram: Ha két vagy több szereplő közötti időrendi üzenetváltást kell szemléltetni.
            - stateDiagram-v2: Ha egy egység különböző állapotait mutatod be.
            - erDiagram / classDiagram: Ha adatszerkezetek közötti fix kapcsolatokat ábrázolsz.
    
            Szigorú szabályok:
            - Válassz egyetlen diagramtípust a fenti lista alapján
            - Csomópontok legyenek rövidek, max 4-5 szó, maximálisan 8 csomópont legyen
            - Egy csomópont feliratát (pl. A[Szöveg]) csak az első előforduláskor definiáld, utána már csak az azonosítóját (pl. A) használd a nyilaknál!
            - A nyilak formátuma felirat esetén: A -->|Szöveg| B (Ez a legbiztosabb forma)
            - A csomópontok szövegeiben (a szögletes zárójelen belül) ne használj idézőjeleket, kerek zárójelet vagy vesszőt.
            - A Mermaid kódban a csomópontok feliratait idézőjelek nélkül add meg, pl: A[HDD] vagy B[HDD merevlemez].
            - A Mermaid kódban ne használj kerek zárójelet (), vesszőt vagy egyéb írásjelet még az idézőjeleken belül sem.
            - Ha mindmap: csak behúzással jelöld a hierarchiát, ne használj nyilakat vagy kapcsoló szimbólumokat
            Az alábbi JSON séma alapján készítsd el
            """
        return prompt

    elif selection_viz =="Graphviz":
        prompt = f"""
                Te egy tapasztalt oktatási asszisztens vagy. 
    
                Forrásanyag:
                {context_text}
    
                Kérdés:
                {query}
    
                Szabályok:
                - Csak a megadott forrásanyagból dolgozz
                - Ha a forrásanyagban nincs benne a válasz, mondd pontosan ezt: "Sajnos erről nem találtam információt a tananyagban." és szigorúan tilos Graphviz diagramot generálnod
                - Próbálj meg, egyszerűen válaszolni, hogy a diákok számára a lehető legérthetőbb legyen
    
    
                Generálj egy érvényes graphviz diagramot a kérdés témájához.
                Diagramtípusok kiválasztása:
                - Folyamat: [shape=box] csomópontok, [arrowhead=vee] nyilak.
                - Fogalmi térkép: Központi fogalom [style=filled, fillcolor=orange].
                - Döntés: Elágazás [shape=diamond, label="Kérdés?"].
                - Színek: Használj pasztell színeket (lightblue, lightyellow, palegreen).
                - Korlát: Max 8-10 csomópont, a feliratok max 4-5 szavasak legyenek.
    
                Szigorú szabályok:
                - A struktúra mindig így kezdődjön: `digraph G {{` és így végződjön: `}}`
                - Használj `rankdir=LR;` beállítást.
                - Minden csomópontnak adj rövid label-t idézőjelek között, pl: A [label="Név"];
                - Az összefüggéseket `->` jellel jelöld.
                Az alábbi JSON séma alapján készítsd el
                """
        return prompt

    elif selection_viz == "Echart":
        prompt = f"""
                Te egy tapasztalt oktatási asszisztens vagy. 

                Forrásanyag:
                {context_text}

                Kérdés:
                {query}

                Szabályok:
                - Csak a megadott forrásanyagból dolgozz
                - Ha a forrásanyagban nincs benne a válasz, mondd pontosan ezt: "Sajnos erről nem találtam információt a tananyagban." és szigorúan tilos Echart diagramot generálnod
                - Próbálj meg, egyszerűen válaszolni, hogy a diákok számára a lehető legérthetőbb legyen


                Generálj egy érvényes JSON-t EChart diagramot streamlitban a kérdés témájához.
                Példa a várt struktúrára az 'echart_code' mezőben:
                {{
                  "title": {{ "text": "Cím" }},
                  "tooltip": {{}},
                  "legend": {{ "data": ["Adat1"] }},
                  "xAxis": {{ "data": ["A", "B", "C"] }},
                  "yAxis": {{}},
                  "series": [{{ "name": "Adat1", "type": "bar", "data": [10, 20, 30] }}]
                }}
                Szigorú szabályok:
                - Válaszd ki a legmegfelelőbb diagramtípust az adatok jellegétől függően
                - A JSON tartalmazzon színeket (itemStyle), címet (title) és eszköztárat (tooltip) a jobb felhasználói élményért.
               Az alábbi JSON séma alapján készítsd el
               """
        return prompt
    elif selection_viz == "Plantuml":
        prompt = f"""
                       Te egy tapasztalt oktatási asszisztens vagy. 

                       Forrásanyag:
                       {context_text}

                       Kérdés:
                       {query}

                       Szabályok:
                       - Csak a megadott forrásanyagból dolgozz
                       - Ha a forrásanyagban nincs benne a válasz, mondd pontosan ezt: "Sajnos erről nem találtam információt a tananyagban." és szigorúan tilos Plantuml diagramot generálnod
                       - Próbálj meg, egyszerűen válaszolni, hogy a diákok számára a lehető legérthetőbb legyen


                       Generálj egy érvényes plantuml diagramot streamlitban a kérdés témájához.
                        Diagramtípusok kiválasztása:
                        - Mindmap diagram: Ha a téma fogalmi felépítéséről, kategóriákról vagy részegységekről szól.
                        - Activity diagram: Ha egy folyamatról, döntési mechanizmusról vagy logikai láncról van szó.
                        - Sequence diagram: Ha két vagy több szereplő közötti időrendi üzenetváltást kell szemléltetni.
                        - State diagram: Ha egy egység különböző állapotait mutatod be.
                        - Class diagram: Ha adatszerkezetek közötti fix kapcsolatokat ábrázolsz.
                        - Component diagram: Ha a rendszer technikai elemeit (modulok, adatbázisok, API-k) és azok kapcsolatait mutatod be.
                        - Use Case diagram: Ha a felhasználó (diák/tanár) és a rendszer közötti interakciókat, jogosultságokat szemlélteted.
                        - Object diagram: Ha konkrét példaadatokat (példányokat) akarsz ábrázolni egy absztrakt osztálydiagram helyett.
                        - Gantt chart: Ha időbeli lefolyást, projekttervet vagy tanulási ütemtervet mutatsz be."
                       Szigorú szabályok:
                       - Válaszd ki a legmegfelelőbb diagramtípust az adatok jellegétől függően
                       - Tartalmazza a kezdő és záró tageket (@start... / @end...).
                       - Szintaktikailag helyes legyen
                       - A 'plantuml_code' értékében minden egyes PlantUML utasítás után használj valódi sortörést (\\n). A kód NEM lehet egyetlen folytonos sor szóközökkel elválasztva!
                       - Sequence diagram esetén a szereplőket szigorúan kisbetűs 'participant' kulcsszóval definiáld (Pl. `participant Szerver`), a nagybetűs verzió hibát okoz!
                      Az alábbi JSON séma alapján készítsd el
                      """
        return prompt

