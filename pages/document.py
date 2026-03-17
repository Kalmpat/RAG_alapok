import os
import streamlit as st
import json

from genai_rag import delete_file, embed_file
from osszefoglalo import process_document
import time

DATA_PATH = r"data"
#st.set_page_config(layout="wide")

if not st.session_state.api_key:
    st.warning("⚠️ Kérlek, add meg az API kulcsot az oldalsávon!")
    st.stop()


st.title(" 📄 Dokumentum")

st.header("Töltsd fel a dokumentumot!", divider='blue')

uploaded_files = st.file_uploader(
    "Dokumentáció feltöltése", accept_multiple_files=True, type="pdf"
)

new_file = False

st.warning("Figyelem! Mindig a legutoljára feltöltött tananyag alapján történik az összefoglaló készítése")


st.subheader("📚 Forrásanyagok")
if os.path.exists(DATA_PATH):
    files = os.listdir(DATA_PATH)
    if not files:
        st.info("Nincsenek feltöltött tananyagok")
    else:
        container = st.container(border=True)
        with container:
            for file in files:
                col1, col2 = st.columns([8, 1])
                with col1:
                    st.markdown(f"<div style='padding-top: 5px;'>📄{file}</div>", unsafe_allow_html=True)
                with col2:
                    if st.button("Törlés", key=f"del_{file}", type="primary", use_container_width=True):
                        with st.spinner(f"{file} törlése...."):
                            try:
                                delete_file(file, st.session_state.api_key)

                                file_path = os.path.join(DATA_PATH, file)
                                if os.path.exists(file_path):
                                    os.remove(file_path)
                                if os.path.exists("tananyag.json"):
                                    os.remove("tananyag.json")

                                if "my_uploader" in st.session_state:
                                    del st.session_state["my_uploader"]

                                st.success(f"{file} törölve!")
                                time.sleep(1)
                                st.rerun()

                            except Exception as e:
                                st.error(e)

else:
    os.mkdir(DATA_PATH)
    st.write("Még nincsenek forrásanyagok")

# Felöltés
if uploaded_files:
    for uploaded_file in uploaded_files:
        save_path = os.path.join("data", uploaded_file.name)

        # Ha nincs ott a fájl akkor dolgozuk fel
        if not os.path.exists(save_path):
            # Mentés
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Feldolgozás egyesével
            with st.spinner(f"Feldolgozás: {uploaded_file.name}..."):
                process_document(save_path,st.session_state.api_key,st.session_state.model)
                embed_file(save_path, st.session_state.api_key)
                st.success(f"Kész: {uploaded_file.name}")
            new_file = True

if new_file:
    st.rerun()

def stream_data(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.05)


if os.path.exists("tananyag.json"):
    container = st.container(border=True)
    with container:
        with open("tananyag.json", "r", encoding="UTF-8") as f:
            data = json.load(f)
            st.header("Összefoglaló:", divider='gray')

            #st.subheader("Cím")
            st.subheader(f"🎓{data["cim"]}")
            #st.subheader("Leírás")
            st.write_stream(stream_data(data["leiras"]))
            #for s in data["szakkifejezesek"]["fogalmak"]:
                #st.write(s)
            st.subheader("📖 Kulcsfogalmak és magyarázatok")
            for s in data["szakkifejezesek"]["definiciok"]:
                sor = f"- **{s['kifejezes']}**: {s['magyarazat']}"
                st.write_stream(stream_data(sor))
                #st.markdown(f"- **{s['kifejezes']}**: {s['magyarazat']}")

            st.subheader("📜 Fontos Tételek")
            for t in data["szakkifejezesek"]["tetelek"]:
                st.write(f"### {t["nev"]}")
                st.write_stream(stream_data(t["leiras"]))

            st.subheader("🔗 Összefüggések")
            info_placeholder = st.empty()
            full_info = ""
            for word in data["osszefuggesek"].split(" "):
                full_info += word + " "
                info_placeholder.info(full_info)
                time.sleep(0.04)

            st.subheader("💡 Tanulási tipp")
            success_placeholder = st.empty()
            full_tip = ""
            for word in data["didaktikai_tipp"].split(" "):
                full_tip += word + " "
                success_placeholder.success(full_tip)
                time.sleep(0.04)


            #st.write(json.dumps(data, indent=4, ensure_ascii=False))









