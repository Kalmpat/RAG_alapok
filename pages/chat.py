import streamlit as st
from genai_rag import processing

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

                    response = processing(query)
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
        st.warning("Még nem jó")