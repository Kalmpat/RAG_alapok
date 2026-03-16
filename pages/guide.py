import streamlit as st




col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    st.title("ℹ️️ Útmutató", )
    st.header("Rendszer felépítése", divider='blue')
    st.subheader("Első fázis (indexelés)", divider='gray')
    container = st.container(border=True)
    with container:
        st.image("images/index.png", use_container_width=True)

    st.markdown(f"""
     **Lépései:**
    
     **1. A dokumentumok beolvasása:** feltöltjük a forrásanyagot és beolvassuk\n
     **2. A szöveg darabolása:** A szöveget feldaraboljuk, kisebb részekre (chunkolás), a pontosabb kereshetőség szempontjából\n
     **3. Vektorizálás:** a szöveget vektorokká (számsorokká) alakítjuk, hogy a gép számára érthető legyen\n
     **4. Vektoradatbázis:** A vektorokat, pedig a vektoradatbázisban tároljuk el (ChromaDB)\n
    
    """)

    st.info("A dokumentumok még, jelenleg pdf formátumúak")

    st.subheader("Második fázis (lekérdezés)", divider='gray')
    container = st.container(border=True)
    with container:
        st.image("images/lekérdezés.png")

    st.markdown(f"""
     **Lépései:**
    
     **1. Kérdés feldolgozása:** A felhasználó kérdését a rendszer szintén vektorizálja.\n
     **2. Releváns tartalom keresése:** Az adatbázisból (ChromaDB) kikeressük a kérdéshez leginkább illő szövegrészleteket.\n
     **3. Prompt összeállítása:** A kérdés és a kinyert kontextus egyesül egy komplex utasítássá az AI számára.\n
     **4. Válasz és vizualizáció:** Az LLM generálja a szöveges választ és a témához illő Mermaid diagramot.
    
    """)

    st.success(
        "A rendszer csak a megadott forrásanyagból dolgozik, így minimalizálva a téves információkat (hallucinálást).")

    st.header("Hogyan használjuk az alkalmazást?", divider='blue')

    st.markdown(f"""
        Az alkalmazásnak van egy bal oldali sávja, ahol megtalálhatjuk a menüpontokat
    
        **Menüpontok:**
    
        **1. 🏠 Kezdőlap**\n
        **2. 📄 Dokumentumok**\n
        **3. 💬 Chat + 📊 Vizualizáció**\n
        **4. 📚 Jegyzetek**\n
        **5. ℹ️️ Útmutató**\n
    
    """)

    st.subheader("🏠 Kezdőlap", divider='gray')
    st.markdown("""
    A kezdőlap célja az **orientáció**. Itt kapod meg az alapvető információkat arról, hogyan tudod a leghatékonyabban használni a rendszert.
    """)
    container = st.container(border=True)
    with container:
        st.image("images/home.png", caption='Kezdőlap')

    st.subheader("📄 Dokumentumok", divider='gray')
    st.markdown("""
    A Dokumentum menüpont célja a **tudásbázis létrehozása**. Itt töltheted fel a feldolgozni kívánt tananyagokat, amelyeket az AI elemez és strukturál. A folyamat végén a rendszer automatikusan készít egy **átfogó összefoglalót**, így már az interaktív kérdezés előtt átláthatod a dokumentum legfontosabb pontjait.
    """)

    container = st.container(border=True)
    with container:
        st.image("images/document.png", caption='Dokumentumok')

    st.markdown("""
        **Lépések:**
        1. Felhasználó feltölt egy forrásanyagot, a képen jól látható, hogy a browse files-ra kattintva, kiválaszthatja a dokumentumot
        2. A rendszer feldolgozza a forrásanyagot, a képen jól látszik, a forrásanyag alatt a feldolgozás
        3. A sikeresen feldolgozott dokumentációt, láthatjuk a forrásanyagok alatt, illetve egy rövid összefoglaló is látható, amit az AI legenerált         
    
    """)

    st.subheader("💬 Chat + 📊 Vizualizáció", divider='gray')
    st.markdown("""
    A Chat + Vizualizáció  menüpont célja a **a tudás átadása**. Itt történik igazából a rendszer lényegi eleme, miszerint tudunk beszélni az AI-jal, mellesleg még vizualizációt is készít nekünk a könnyebb megérthetőség szempontjából. 
    """)

    container = st.container(border=True)
    with container:
        st.image("images/chatviz.png", caption='A kezdőoldala')
    container = st.container(border=True)
    with container:
        st.image("images/chatviz2.png", caption='Működése')
    container = st.container(border=True)
    with container:
        st.image("images/chatviz3.png", caption='Ha nincs a tananyagban')

    st.info("A feltöltött forrásanyag alapján válaszol nekünk a mesterséges intelligencia")
    st.warning("Fejlesztés alatt, néha nem jól csinálja")

    st.subheader("📚 Jegyzetek", divider='gray')
    st.markdown("""
    A Jegyzetek  menüpont célja a **beszélgetések letöltése**. Itt történik a beszélgetések letöltése, ahol pdf dokumentációkat tudunk letölteni
    """)

    st.warning("Fejlesztés alatt")

    st.subheader("ℹ️️ Útmutató", divider='gray')
    st.markdown("""
    Az útmutató menüpont célja a **az alkamazás használata**. Itt történik egy rövid bemutatás az alkalmazásról, illetve a rendszer működéséről is
    """)

    st.header("Hogyan tegyünk fel jó kérdéseket?", divider='blue')

    st.markdown("""
        Először is a tananyaggal kapcsolatban legyen kérdésünk, ha nem így történik akkor a mesterséges intelligencia azonnal jelezni fogja számunkra.
        Olyan kérdéseket tegyünk fel, amik számunkra nem érhetőek ezáltal is könyebben segíthet az alkalmazás a megértésben
    """)

    st.header("Milyen diagramokat tudunk használni?", divider='blue')

    st.markdown("""
        A diagramokat (ábárkat) igazából a rendszer egy mermaid.js formátumban készíti el, amely megjelenítésre kerül a vizualizációs ablakban\n
        Az ábrák típusai:\n
        A folyamatábra\n
        A szekvenciadiagram\n
        Az állapotgép\n
        Az ER diagram\n
        A gondolattérkép\n
    
    """)

    st.info("A diagramok típusait nem tudjuk változtatni jelenleg")



