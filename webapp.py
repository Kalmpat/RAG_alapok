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
    st.markdown("""
               <div style="background: rgba(200, 169, 110, 0.05); padding: 15px; border-radius: 10px; border-left: 3px solid #c8a96e; margin: 10px 0;">
                   <p style="color: #c8a96e; font-family: 'Outfit', sans-serif; font-size: 14px; font-weight: 600; margin: 0;">
                       Üdvözlünk a tanuló alkalmazásban!
                   </p>
                   <p style="color: #7a7880; font-family: 'Outfit', sans-serif; font-size: 12px; margin-top: 5px;">
                       Az AI asszisztensed készen áll. Kezdjük el a közös munkát! Kérlek állítsd be a modelt és az API kulcsot!
                   </p>
               </div>
       """, unsafe_allow_html=True)
    st.divider()
    with st.expander("⚙️ Beállítások"):
        st.selectbox("Modellek", ["gemini-2.5-flash", "gemini-2.5-flash-lite", "gemini-3-flash-preview","gemini-3.1-flash-lite"], key="model")
        st.text_input("OPENAPI-KEY", type="password", key="api_key")

pg = st.navigation(pages)
pg.run()


