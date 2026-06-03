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
                - Csak a megadott forrásanyagból dolgozz.
                - Ha a forrásanyagban nincs benne a válasz, mondd pontosan ezt: "Sajnos erről nem találtam információt a tananyagban." és szigorúan tilos Mermaid diagramot generálnod.
                - Próbálj meg egyszerűen válaszolni, hogy a diákok számára a lehető legérthetőbb legyen.
        
                Diagramtípús kiválasztási logika (Kövesd szigorúan ebben a sorrendben!):
                - Ha a kérdés vagy a téma folyamatot, lépéseket, időrendet vagy ok-okozati összefüggést ír le (pl. "Hogyan működik...", "Mik a lépései...", "Mi történik ha..."): kötelezően `flowchart TD` típust használj!
                - Ha a téma interakciót vagy üzenetváltást mutat be entitások/szereplők között (pl. kliens-szerver, kérés-válasz): kötelezően`sequenceDiagram` típust használj!
                - Ha egy rendszer állapotait és az azok közötti átmeneteit mutatod be: kötelezően `stateDiagram-v2` típust használj!
                - Csupán akkor használhatsz `mindmap` típust, ha a téma tisztán statikus fogalmak csoportosítására, listázása vagy kategóriákba sorolása, és semmilyen folyamat vagy időrend nem fedezhető fel benne!
        
                Szigorú szintaktikai szabályok:
                - Válassz egyetlen diagramtípust a fenti szigorú logika alapján!
                - Maximálisan 6-8 csomópontot használhatsz, a feliratok legyenek rövidek (max 4-5 szó).
                - Ha `flowchart TD`: 
                    * Egy csomópont feliratát (pl. A[Szöveg]) csak a legelső előforduláskor definiáld! Utána már csak az azonosítóját (pl. A) használd.
                    * A nyilak formája KÖTELEZŐEN: A -->|Szöveg| B
                - Ha `mindmap`: csak behúzással jelöld a hierarchiát, ne használj nyilakat vagy kapcsoló szimbólumokat!
                - A csomópontok szövegében (zárójeleken belül) TILOS idézőjelet, kerek zárójelet (), vesszőt vagy egyéb írásjelet használni! Példa a helyes formára: A[HDD merevlemez]
        
                Az alábbi JSON séma alapján készítsd el.
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
                
                Diagramtípus kiválasztási logika:
                - Százalék / Megoszlás esetén: Használj kördiagramot (`"type": "pie"`), és ilyenkor egyidejűleg töröld  az `xAxis` és `yAxis` mezőket!
                - Mennyiségek összehasonlíása esetén: Használj oszlopdiagramot (`"type": "bar"`).
                
                Szigorú szabályok:
                - A színeket a series-en belül az itemStyle: {{ "color": "#HEX" }} objektummal kötelezően felülbírálni! Szigorúan tilos fakó vagy halvány színeket használni. Csak ezeket a modern, élénk HEX kódokat használhatod: "#5470C6" (élénkkék), "#91CC75" (élénkzöld), "#FAC858" (élénksárga), "#EE6666" (élénkpiros)
                - A tooltip nem lehet üres, kötelező elem: `"tooltip": {{ "trigger": "item" }}`.
                - Szigorúan tilos aposztrófot (') használni a kódolt JSON-on belül!
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
                        - State diagram: Ha egy egység különböző állapotait mutatod be.temtervet mutatsz be."
                       Szigorú szabályok:
                       - Válaszd ki a legmegfelelőbb diagramtípust az adatok jellegétől függően
                       - Tartalmazza a kezdő és záró tageket (@start... / @end...).
                       - Szintaktikailag helyes legyen
                       - A 'plantuml_code' értékében minden egyes PlantUML utasítás után használj valódi sortörést (\\n). A kód NEM lehet egyetlen folytonos sor szóközökkel elválasztva!
                       - Sequence diagram esetén a szereplőket szigorúan kisbetűs 'participant' kulcsszóval definiáld (Pl. `participant Szerver`), a nagybetűs verzió hibát okoz!
                      Az alábbi JSON séma alapján készítsd el
                      """
        return prompt

