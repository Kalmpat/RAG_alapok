from dotenv import load_dotenv
import os
from google import genai
import streamlit as st

# 1. Beállítások betöltése
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("Hiba: Hiányzik az API kulcs a .env fájlból!")
    st.stop()

client = genai.Client(api_key=api_key)


# Képernyő szélesítése
st.set_page_config(layout="wide")


# Cím
st.title("RAG alapú vizuális jegyzetelő asszisztens")

col1, col2 = st.columns([0.6, 0.4])


# Chatbot
with col1:
    st.subheader("💬 Chatbot")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    chat_container = st.container(height=600)

    with chat_container:
        # Előző beszélgetések megjelenítése
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Chatbot
    query = st.chat_input("Kérdezz nyugodtan")

    if query:
        # Felhasználó üzenet mentése
        st.session_state.messages.append({"role": "user", "content": query})
        with chat_container:
            with st.chat_message("user"):
                st.write(query)

        with chat_container:
            with st.chat_message("assistant"):
                with st.spinner("Gondolkozom..."):

                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=query,
                    )

                    answer_text = response.text
                    st.markdown(answer_text)

                    # Nagy nyelvi modell üzenetének elmentése
                    st.session_state.messages.append({"role": "assistant", "content": answer_text})


# Vizualizáció
with col2:
    st.subheader("📊 Vizualizáció")
    viz_container = st.container(height=600)
    with viz_container:
        st.write("Ábrák")