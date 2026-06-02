import streamlit as st

cols = st.columns([1, 4, 1])
with cols[1]:
    st.title("ℹ️ Útmutató")
    st.markdown("Ismerd meg az alkalmazás működését és hozd ki belőle a maximumot!")
    st.divider()

    tab1, tab2, tab3 = st.tabs(["🗄️ Rendszer felépítése", "📖 Használati útmutató", "💡 Tippek & Diagramok"])

    # Rendszer felépítése
    with tab1:
        st.subheader("Hogyan működik a RAG rendszer?")

        # 1 fázis
        with st.expander("1️⃣ Indexelés – Adatbeviteli fázis"):
            container = st.container(border=True)
            with container:
                st.image("images/index.png", use_container_width=True)
            st.markdown("""
            **Lépései:**
            
            **1. Dokumentum beolvasása** – Feltöltjük a PDF forrásanyagot és beolvassuk a tartalmát.
            
            **2. Chunkolás** – A szöveget kisebb egységekre daraboljuk a pontosabb kereshetőség érdekében.
            
            **3. Vektorizálás** – A szövegrészleteket vektorokká (számsorokká) alakítjuk a `gemini-embedding-001` modellel.
            
            **4. Tárolás** – A vektorokat a **ChromaDB** vektoradatbázisban tároljuk el.
            """)
            st.info("Jelenleg csak PDF formátumú dokumentumok tölthetők fel.")

        # 2. fázis
        with st.expander("2️⃣ Lekérdezés – Válaszadási fázis"):
            container = st.container(border=True)
            with container:
                st.image("images/lekérdezés.png", use_container_width=True)
            st.markdown("""
            **Lépései:**

            1. **Kérdés feldolgozása** – A felhasználó kérdését a rendszer szintén vektorizálja.

            2. **Releváns tartalom keresése** – A ChromaDB-ből kikeressük a kérdéshez leginkább illő szövegrészleteket.

            3. **Prompt összeállítása** – A kérdés és a kinyert kontextus egyesül egy komplex utasítássá az AI számára.

            4. **Válasz és vizualizáció** – Az LLM generálja a szöveges választ és a témához illő diagramot.
            """)
            st.success("A rendszer csak a megadott forrásanyagból dolgozik, minimalizálva a téves információkat (hallucinálást).")

    # Felhasználói útmutató
    with tab2:
        st.subheader("Az alkalmazás kezelése")

        with st.container(border=True):
            st.markdown("### 1️⃣ API kulcs beállítása")
            st.write("Add meg a Gemini API kulcsodat a bal oldali beállításoknál. Nélküle az AI funkciók nem működnek.")

        with st.container(border=True):
            st.markdown("### 2️⃣ Dokumentum feltöltése")
            st.write(
                "Nyisd meg a Dokumentum oldalt és tölts fel egy PDF fájlt. Ez alkotja a tudásbázist, amiből az AI kizárólag válaszol.")

        with st.container(border=True):
            st.markdown("### 3️⃣ Kérdés feltevése")
            st.write(
                "A Chat és Vizualizáció oldalon írd be a kérdésedet. A RAG rendszer releváns szövegrészleteket keres, majd ezek alapján ad választ.")

        with st.container(border=True):
            st.markdown("### 4️⃣ Diagram értelmezése")
            st.write(
                "Minden választ automatikusan ábrává alakít a jobb érthetőségért. A diagram típusa a kérdés témájához igazodik.")

        with st.container(border=True):
            st.markdown("### 5️⃣ Jegyzetek letöltése")
            st.write("A tanulási eredményeidet a Jegyzetek oldalon PDF formátumban töltheted le.")

        st.divider()
        st.warning("⚠️ Egyszerre egy dokumentum az aktív tananyag!")

    # Tippek és Motorok
    with tab3:
        st.subheader("🎯 Hogyan kérdezzünk jól?")

        col_q1, col_q2 = st.columns(2)
        with col_q1:
            st.markdown("""
                **✅ Jó kérdések:**
                - "Mi a kapcsolat az OSI modell és a TCP/IP között?"
                - "Magyarázd el a háromutas kézfogást folyamatábrán!"
                - "Mi az elektronikus levelezésnek a fő alkotóelemei?"
                - "Milyen állapotai vannak egy TCP kapcsolatnak?"
            """)
        with col_q2:
            st.markdown("""
                **❌ Kerülendő:**
                - "Szia, mizu?" — nem általános chat.
                - "Mi volt a tegnapi meccs eredménye?" — csak a PDF-ből dolgozik.
                - Nagyon hosszú, több összetett kérdést egybegyúró mondatok.
            """)

        st.divider()

        st.subheader("🛠️ Támogatott vizualizációs motorok")
        st.write("A rendszer az alábbi négy független motor segítségével képes ábrákat generálni:")

        v_col1, v_col2, v_col3, v_col4 = st.columns(4)

        with v_col1:
            with st.container(border=True):
                st.markdown("### 🐚 Mermaid")
                st.caption("Folyamatok, szekvenciák, állapotgépek és mindmapek deklaratív leírására.")
                st.markdown("")
        with v_col2:
            with st.container(border=True):
                st.markdown("### 🕸️ Graphviz")
                st.caption("Komplex irányított gráfok, döntési fák és hálózati topológiák egyedi formázására.")
                st.markdown("")
        with v_col3:
            with st.container(border=True):
                st.markdown("### 📊 ECharts")
                st.caption("Interaktív, egérrel mozgatható statisztikai diagramok (oszlop, vonal, pite) JSON alapon.")
                st.markdown("")
        with v_col4:
            with st.container(border=True):
                st.markdown("### 📐️ PlantUML")
                st.caption("Szoftvertervezési és mérnöki ábrák (Usecase, Class, Component, Gantt) generálására.")

        st.divider()

        # Mérnöki transzparencia: Mi történik, ha elromlik?
        st.subheader("🧠 Stabilitás és hibakezelés")
        st.info("""
        **Mérnöki megjegyzés a generálásról:**
        Mivel a diagramok kódját a Nyelvi Modell (LLM) valós időben generálja, ritkán előfordulhatnak szintaktikai hibák, vagy külső renderelő szerverek átmeneti elérhetetlensége. 

        A háttérben a rendszer **szigorú rendszerszintű szabályokkal (System Prompts) és egyedi JSON sémákkal** kényszeríti ki a helyes szintaxist (pl. PlantUML sortörések kezelése, Mermaid tiltott karakterek szűrése), minimalizálva a hibás ábrák megjelenését.
        """)

        st.caption("Minden diagram valós időben, a megadott prompt-specifikációk alapján épül fel.")