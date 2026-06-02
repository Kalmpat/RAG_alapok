import os.path

import streamlit as st
import json
import random
import pandas as pd
import os
from diagrams import mermaid
from zh_generator import zh_base, zh_generator, zh_javitokulcs_generator, mermaid_zh
from streamlit_pdf_viewer import pdf_viewer


st.title("📚 Jegyzetek")
#st.subheader("Összefoglalók:")

SUMMARY_PATH = "summaries"
PDFS_PATH = "pdfs"

if not os.path.exists(SUMMARY_PATH):
    os.makedirs(SUMMARY_PATH)

if not os.path.exists(PDFS_PATH):
    os.makedirs(PDFS_PATH)

cimek = []
adatok = []


# Flashcard reset
def reset_flashcards():
    st.session_state.kartya_indexe = 0
    st.session_state.felfedve = False


# JSON fájlok tartalmai
for file_name in os.listdir(SUMMARY_PATH):
    full_path = os.path.join(SUMMARY_PATH, file_name)
    with open(full_path, "r", encoding="utf-8") as f:
        tartalom = json.load(f)
        #print(f"Fájl neve: {file_name}")
        cim = tartalom['cim']
        adatok.append(tartalom)
        cimek.append(cim)
        #print(tartalom)
        #print(cim)

#print(cimek)




tab1, tab2, tab3 = st.tabs([
    "📚 Összefoglalók",
    "🗂️ Gyakorlás (Flashcard)",
    "📝 ZH generátor"
])
with tab1:
    if os.path.exists(SUMMARY_PATH):
        files = os.listdir(SUMMARY_PATH)


        if not files:
            st.info("Még nincsenek összefoglalók")
        else:

            for file in files:
                base_name = os.path.splitext(file)[0]
                json_path = os.path.join(SUMMARY_PATH, file)
                pdf_path = os.path.join(PDFS_PATH, f"{base_name}.pdf")

                with open(json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                with st.expander(f"{data['cim']}"):

                        col_left, col_right = st.columns([2, 3], gap="large")


                        with col_left:
                            pdf_viewer(pdf_path, height=400, key=f"pdf_{base_name}")

                        with col_right:
                            col_title, col_btn = st.columns([4, 1])
                            with col_title:
                                st.markdown(f"### 🎓 {data['cim']}" )
                            with col_btn:
                                # rb = read binary
                                with open(pdf_path,"rb") as f:
                                    st.download_button(
                                        label="🖨️ Letöltés",
                                        data=f,
                                        file_name=f"{data["cim"]}.pdf",
                                        mime="application/pdf",
                                        use_container_width=True,
                                        key=f"dl_{base_name}"
                                    )
                                #st.button("🖨️ Letöltés", key="dl_btn", use_container_width=True)

                            container = st.container(border=True)
                            with container:
                                st.write(data["leiras"])

                            #st.divider()
                            #st.markdown("**Kulcsszavak:**")

                            #kifejezesek = data["szakkifejezesek"]["definiciok"]
                            #sample_size = min(5, len(kifejezesek))
                            #rn = random.sample(kifejezesek, sample_size)
                            #badge_cols = st.columns(sample_size)
                            #for i, s in enumerate(rn):
                            #    with badge_cols[i]:
                            #       st.badge(s["kifejezes"], icon=":material/check:", color="orange")

                            st.write("")
                            st.info(f"**💡 Tipp a tanuláshoz:** {data['didaktikai_tipp']}")

with tab2:
    if cimek:
        option = st.selectbox("Válassz egy témát!", cimek, on_change=reset_flashcards)

        # Szelektálás next segítségével
        kivallasztott_json = next(
            item for item in adatok if item["cim"] == option
        )
        st.markdown("### Téma leírása:")
        st.write(kivallasztott_json["leiras"])
        st.markdown("---")
        definiciok_listaja = kivallasztott_json["szakkifejezesek"]["definiciok"]
        df = pd.DataFrame(definiciok_listaja)

        df = df.rename(
            columns={"kifejezes": "Kifejezés", "magyarazat": "Magyarázat"}
        )
        st.markdown("### Szakkifejezések:")
        tab1, tab2 = st.tabs(["📋 Definíciók", "📜 Tételek"])

        with tab1:
            st.markdown("### Definíciók:")
            st.dataframe(df, use_container_width=True)

            tetelek_listaja = kivallasztott_json["szakkifejezesek"]["tetelek"]
            df = pd.DataFrame(tetelek_listaja)

            df = df.rename(
                columns={"nev": "Név", "leiras": "Leírás"}
            )

        with tab2:
            st.markdown("### Tételek")
            st.dataframe(df, use_container_width=True)

        st.write("### 💡 Flashcard")
        st.divider()
        if "kartya_indexe" not in st.session_state:
            st.session_state.kartya_indexe = 0
        if "felfedve" not in st.session_state:
            st.session_state.felfedve = False

        option = st.selectbox(
            "Mit szeretnél gyakorolni?",
            ["Szakkifejezések", "Tételek"],
            key="flashcard_tipus_select",
            on_change=reset_flashcards
        )

        if option == "Szakkifejezések":
            aktualis_lista = kivallasztott_json["szakkifejezesek"]["definiciok"]
            kulcs_eleje = "kifejezes"
            kulcs_hatulja = "magyarazat"
        else:
            aktualis_lista = kivallasztott_json["szakkifejezesek"]["tetelek"]
            kulcs_eleje = "nev"
            kulcs_hatulja = "leiras"

        if st.session_state.kartya_indexe >= len(aktualis_lista):
            st.session_state.kartya_indexe = 0
            st.session_state.felfedve = False

        st.info(f"Kártya száma: {st.session_state.kartya_indexe + 1} / {len(aktualis_lista)}")

        container = st.container(border=True)
        with container:
            st.write("")
            st.write("")
            if st.session_state.felfedve:
                st.markdown(
                    f"<h3 style='text-align: center;'>{aktualis_lista[st.session_state.kartya_indexe][kulcs_hatulja]}</h3>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"<h3 style='text-align: center;'>{aktualis_lista[st.session_state.kartya_indexe][kulcs_eleje]}</h3>",
                    unsafe_allow_html=True,
                )
            st.write("")
            st.write("")

        col_left, col1, col2, col3, col_right = st.columns([2, 1, 1.2, 1, 1.8])

        with col1:
            if st.button("⬅️ Előző"):
                if st.session_state.kartya_indexe > 0:
                    st.session_state.kartya_indexe -= 1
                    st.session_state.felfedve = False
                    st.rerun()

        with col2:
            if st.button("Kártya fordítása 🔄"):
                st.session_state.felfedve = not st.session_state.felfedve
                st.rerun()
        with col3:
            if st.button("Következő ➡️"):
                if st.session_state.kartya_indexe < len(aktualis_lista) - 1:
                    st.session_state.kartya_indexe += 1
                    st.session_state.felfedve = False
                    st.rerun()
    else:
        st.info("Még nincsenek összefoglalók")

with tab3:
    if os.path.exists(SUMMARY_PATH):
        files = os.listdir(SUMMARY_PATH)


        if not files:
            st.info("Még nincsenek összefoglalók")
        else:
            st.subheader("ZH generátor:")
            st.info("""
                A gomb megnyomásával sikeresen tudsz a feltöltött dokumentumok segítségével zárthelyi dolgozatot generáltatni
            """)
            if "zh_kesz" not in st.session_state:
                st.session_state.zh_kesz = False


            if st.button("ZH és Javítókulcs generálása", use_container_width=True):
                with st.spinner("Készülödik"):
                    try:
                        zh_adatok = zh_base(st.session_state.api_key, st.session_state.model)
                        if zh_adatok is None or not isinstance(zh_adatok, dict):
                            if os.path.exists("zh.json"):
                                with open("zh.json", "r", encoding="UTF-8") as f:
                                    zh_adatok = json.load(f)
                            else:
                                raise ValueError("Nincs adat")
                        zh_generator(zh_adatok)
                        zh_javitokulcs_generator(zh_adatok)
                        st.session_state.zh_kesz = True
                        st.success("A zárthelyi dolgozat és a javítókulcs sikeresen elkészült!")
                    except Exception as e:
                        st.error(f"Hiba történt a generálás során: {e}")
                        st.session_state.zh_kesz = False

            if st.session_state.zh_kesz:
                col1, col2 = st.columns(2)
                with col1:
                    zh_pdf_path = os.path.join(PDFS_PATH, "zh.pdf")
                    if os.path.exists(zh_pdf_path):
                        with open(zh_pdf_path, "rb") as f:
                            st.download_button(
                                label="📥 Diák feladatlap letöltése (PDF)",
                                data=f,
                                file_name="Zarthelyi_Dolgozat.pdf",
                                mime="application/pdf",
                                use_container_width=True,
                                type="primary"
                            )

                with col2:
                    kulcs_pdf_path = os.path.join(PDFS_PATH, "javitokulcs.pdf")
                    if os.path.exists(kulcs_pdf_path):
                        with open(kulcs_pdf_path, "rb") as f:
                            st.download_button(
                                label="🔑 Tanári javítókulcs letöltése (PDF)",
                                data=f,
                                file_name="Zarthelyi_Javitokulcs.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )
