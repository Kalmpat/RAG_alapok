import os.path

import streamlit as st
import json
import random

from mermaid import mermaid
from zh_generator import zh_base, zh_generator, zh_javitokulcs_generator, mermaid_zh

st.title("📚 Jegyzetek")
st.subheader("Összefoglalók:")

SUMMARY_PATH = "summaries"
PDFS_PATH = "pdfs"

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
                        st.pdf(pdf_path, height=400, key=f"pdf_{base_name}")

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
                    label="📥 Diák Feladatlap Letöltése (PDF)",
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
                    label="🔑 Tanári Javítókulcs Letöltése (PDF)",
                    data=f,
                    file_name="Zarthelyi_Javitokulcs.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
