import streamlit as st



pages = {
   "Navigáció":[ st.Page("pages/home.py", title="🏠 Kezdőlap"),
    st.Page("pages/document.py", title="📄 Dokumentum"),
    st.Page("pages/chat.py", title="💬 Chat + Vizualizáció"),
    st.Page("pages/notes.py", title="📚 Jegyzetek"),
    st.Page("pages/guide.py", title="ℹ️ Útmutató"),

    ]
}

with st.sidebar:
    st.logo("https://www.bme.hu/assets/bme_logo.png", icon_image="https://www.bme.hu/assets/bme_logo.png")
    st.markdown("# 🚀 Tanulást segítő alkalmazásban")
    st.write("Üdvözöllek a rendszerben!")
    st.divider()
    with st.expander("⚙️ Beállítások"):
        st.selectbox("Modellek", ["Gemini-1.5-flash", "Gemini-1.5-pro"], key="model_select")
        st.text_input("OPENAPI-KEY", type="password", key="api_key_input")

pg = st.navigation(pages)
pg.run()


