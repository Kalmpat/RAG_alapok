import os
import streamlit as st
import json
from osszefoglalo import process
import time

DATA_PATH = r"data"


st.title(" 📄 Dokumentum")

st.header("Töltsd fel a dokumentumot!", divider='blue')

uploaded_files = st.file_uploader(
    "Dokumentáció feltöltése", accept_multiple_files=True, type="pdf"
)

new_file = False

st.warning("⚠️Figyelem! Mindig a legutoljára feltöltött tananyag alapján történik az összefoglaló készítése")

st.subheader("📚 Forrásanyagok")
if os.path.exists(DATA_PATH):
    files = os.listdir(DATA_PATH)
    for file in files:
        st.write(f"📄{file}")
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
                process(save_path)
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





