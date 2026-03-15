import streamlit as st

#st.set_page_config(layout="wide")


col1, col2 = st.columns([1, 3])


with col1:
    st.image("images/home_ai.png")
with col2:
    st.title("🏠 Kezdőlap")
    st.header("Üdvözöllek a tanulóalkalmazásban!", divider="gray")
    st.write(""" Ez az alkalmazás segít megérteni feltöltött dokumentumaid tartalmát 
    mesterséges intelligencia segítségével, nemcsak szöveges magyarázattal,
    hanem vizuális ábrákkal is. """)

    st.write("""Sokszor eszedbe jutott már, hogyan lehetne a tanulásodat hatékonyabbá tenni, különösen vizsgaidőszakban? Épp ezért jött létre ez az alkalmazás: hogy könnyebbé tegye a tanulási folyamatodat.  
    Csak tölts fel egy PDF-et, és az AI segít összefoglalni a lényeget, válaszol a kérdéseidre, és ha a téma megkívánja, vizuális diagramokkal ábrázolja a folyamatokat, így gyorsabban és jobban megértheted a komplex anyagot.""")

    st.write("""Kezdéshez lépj a **Dokumentum** menüpontra, tölts fel egy PDF-et, és máris elkezdheted a tanulást!""")

    st.badge("New")