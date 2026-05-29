import streamlit as st
from streamlit_monaco import st_monaco

from genai_rag import process
from diagrams import mermaid, merm, render_custom_mermaid, clean_text, viz, graphviz
from streamlit_mermaid import st_mermaid


# Képernyő szélesítése
#st.set_page_config(layout="wide")

if not st.session_state.api_key:
    st.warning("⚠️ Kérlek, add meg az API kulcsot az oldalsávon!")
    st.stop()

# Cím
st.title("RAG alapú vizuális jegyzetelő asszisztens")

col1, col2 = st.columns([0.6, 0.4])

if "viz_selection" not in st.session_state:
    st.session_state.viz_selection = "Mermaid"

if "mermaid_code" not in st.session_state:
    st.session_state.mermaid_code = ""

if "graphviz_code" not in st.session_state:
    st.session_state.graphviz_code = ""

if "image" not in st.session_state:
    st.session_state.image = ""

if "edit" not in st.session_state:
    st.session_state.edit = False


with col2:
    st.subheader("📊 Vizualizáció")
    selection_viz = st.pills(
            "Válassz az ábrák közül:",
            options=["Mermaid", "Graphviz", "Editor"],
            selection_mode="single",
            key="viz_selection",
            label_visibility="collapsed"
    )


# Chatbot
with col1:
    st.subheader("💬 Chatbot")
    for i in range(3):
        st.write("")
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
        # Tisztítás
        st.session_state.mermaid_code = ""
        st.session_state.graphviz_code = ""
        st.session_state.image = ""

        # Felhasználó üzenet mentése
        st.session_state.messages.append({"role": "user", "content": query})
        with chat_container:
            with st.chat_message("user"):
                st.write(query)

        with chat_container:
            with st.chat_message("assistant"):
                with st.spinner("Gondolkozom..."):

                    response = process(query, st.session_state.api_key, st.session_state.model, st.session_state.viz_selection)
                    if st.session_state.viz_selection == "Mermaid":
                        st.session_state.mermaid_code = response.text
                        st.session_state.image = mermaid(response.text)
                    if st.session_state.viz_selection == "Graphviz":
                        st.session_state.graphviz_code = response.text
                        st.session_state.image = graphviz(response.text)
                    print(response.text)
                    answer_text = clean_text(response.text)
                    #print(answer_text)
                    st.markdown(answer_text)

                    # Nagy nyelvi modell üzenetének elmentése
                    st.session_state.messages.append({"role": "assistant", "content": answer_text})
                    st.rerun()






# Vizualizáció
with col2:
    viz_container = st.container(height=600)
    with viz_container:
        clean_code = None
        #st.warning("Még nem jó")
        if st.session_state.viz_selection == "Mermaid":
            clean_code = merm(st.session_state.mermaid_code)
            if clean_code:
                render_custom_mermaid(clean_code, height=550)
        elif st.session_state.viz_selection == "Graphviz":
            clean_code = viz(st.session_state.graphviz_code)
            if clean_code:
                st.graphviz_chart(clean_code, use_container_width=True)
        elif st.session_state.viz_selection == "Editor":
            raw_code = st.session_state.mermaid_code or st.session_state.graphviz_code or ""
            content = st_monaco(value=raw_code, height="600px", language="markdown")
            if content and content != raw_code:
                if st.session_state.mermaid_code:
                    st.session_state.mermaid_code = content
                else:
                    st.session_state.graphviz_code = content

    if "image" in st.session_state:
        st.download_button(
                label = "Ábra letöltése",
                data = st.session_state.image,
                file_name = "abra.png",
                mime = "image/png",
                icon=":material/download:",
            )
    #if st.session_state.image == "":
        #st.info("Még nincs ábra")

