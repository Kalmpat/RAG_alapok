import streamlit as st

st.set_page_config(layout="wide")

pages = {
   "Navigáció":[ st.Page("pages/home.py", title="🏠 Kezdőlap"),
    st.Page("pages/document.py", title="📄 Dokumentum"),
    st.Page("pages/chat.py", title="💬 Chat + Vizualizáció"),
    st.Page("pages/notes.py", title="📚 Jegyzetek"),
    st.Page("pages/guide.py", title="ℹ️ Útmutató"),

    ]
}

if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "model" not in st.session_state:
    st.session_state.model = "gemini-2.5-flash"


with st.sidebar:
    st.logo("https://www.bme.hu/assets/bme_logo.png", icon_image="https://www.bme.hu/assets/bme_logo.png")
    st.markdown("# 🚀 Tanulást segítő alkalmazásban")
    st.write("Üdvözöllek a rendszerben!")
    st.divider()
    with st.expander("⚙️ Beállítások"):
        st.selectbox("Modellek", ["gemini-2.5-flash", "gemini-2.5-flash-lite", "gemini-3-flash-preview","gemini-3.1-flash-lite-preview"], key="model")
        st.text_input("OPENAPI-KEY", type="password", key="api_key")

pg = st.navigation(pages)
pg.run()


