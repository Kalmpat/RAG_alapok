import streamlit as st

st.set_page_config(layout="wide")

# CSS
st.markdown("""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Outfit:wght@300;400;500;600&display=swap');



    .main .block-container {
        display: flex;
        flex-direction: column;
        justify-content: flex-start; 
        align-items: center;
        padding-top: 10vh !important; 
        min-height: 90vh;
    }

    /* Robot csillogás és lüktetés */
    @keyframes pulseGlow {
        0% { filter: drop-shadow(0 0 15px rgba(200, 169, 110, 0.25)); }
        50% { filter: drop-shadow(0 0 45px rgba(200, 169, 110, 0.5)); }
        100% { filter: drop-shadow(0 0 15px rgba(200, 169, 110, 0.25)); }
    }

    .stImage img {
        animation: pulseGlow 4s infinite ease-in-out;
        border-radius: 30px;
        max-width: 450px;
    }

    /* Szöveg stílusok */
    .hero-eyebrow {
        font-family: 'Outfit', sans-serif;
        color: #c8a96e;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        font-size: 11px;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }

    .hero-title {
        font-family: 'DM Serif Display', serif;
        font-size: 3.8rem;
        color: #f0ede8;
        line-height: 1.1;
        text-align: center;
        margin-bottom: 1rem;
    }

    .hero-title em {
        color: #c8a96e;
        font-style: italic;
        text-shadow: 0 0 15px rgba(200, 169, 110, 0.3);
        border: 1px solid rgba(200, 169, 110, 0.1);
    }

    .hero-sub {
        font-family: 'Outfit', sans-serif;
        color: #7a7880;
        font-size: 16px;
        text-align: center;
        max-width: 500px;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

center_header = st.columns([1, 4, 1])

with center_header[1]:
    st.markdown(
        "<p style='text-align: center; color: #c8a96e; font-weight: bold; letter-spacing: 1.5px; margin-bottom: 0;'>OKTATÁSI RAG RENDSZER</p>",
        unsafe_allow_html=True)
    st.markdown(
        "<h1 style='text-align: center; margin-top: 10px; font-family: serif; font-size: 3.5rem; line-height: 1.1;'>"
        "Tanulj <i style='color: #c8a96e;'>okosabban</i><br>vizualizációval</h1>",
        unsafe_allow_html=True)

    st.markdown(
        "<p style='text-align: center; color: #aaa; margin-bottom: 40px;'>Töltsd fel tananyagaidat és várd a vizuális válaszokat.</p>",
        unsafe_allow_html=True)

center_header = st.columns([1, 0.8, 1])
with center_header[1]:
    st.image("images/home_ai.png")
