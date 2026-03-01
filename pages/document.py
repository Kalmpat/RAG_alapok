import os
import streamlit as st

DATA_PATH = r"data"


st.title(" 📄 Dokumentum")

st.header("Töltsd fel a dokumentumot!", divider='blue')

uploaded_files = st.file_uploader(
    "Dokumentáció feltöltése", accept_multiple_files=True, type="pdf"
)

new_file = False

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
                #process(save_path)
                st.success(f"Kész: {uploaded_file.name}")
            new_file = True

if new_file:
    st.rerun()







