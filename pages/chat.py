import json

import streamlit as st

from streamlit_echarts import st_echarts

#from chat_monaco import answer_text
from genai_rag import process
from diagrams import mermaid, merm, render_custom_mermaid, clean_text, viz, graphviz, echart, plantuml, d2lang
from streamlit_mermaid import st_mermaid

# Képernyő szélesítése
#st.set_page_config(layout="wide")




if not st.session_state.api_key:
    st.warning("⚠️ Kérlek, add meg az API kulcsot az oldalsávon!")
    st.stop()

# Cím
st.markdown("""
    <style>
    h1 {
        color: #c8a96e !important; 
    }
    </style>
    """, unsafe_allow_html=True)

st.title("RAG alapú vizuális jegyzetelő asszisztens")

col1, col2 = st.columns([0.5, 0.5])

if "viz_selection" not in st.session_state:
    st.session_state.viz_selection = "Mermaid"

if "mermaid_code" not in st.session_state:
    st.session_state.mermaid_code = ""

if "graphviz_code" not in st.session_state:
    st.session_state.graphviz_code = ""

if "echart_code" not in st.session_state:
    st.session_state.echart_code = ""

if "plantuml_code" not in st.session_state:
    st.session_state.plantuml_code = ""

if "image" not in st.session_state:
    st.session_state.image = ""

with col2:
    st.subheader("📊 Vizualizáció")
    selection_viz = st.pills(
        "Válassz az ábrák közül:",
        options=["Mermaid", "Graphviz", "Echart", "Plantuml"],
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
            if message["role"] == "user":
                current_avatar = "avatar/user.png"
            else:
                current_avatar = "avatar/bot.png"
            with st.chat_message(message["role"], avatar=current_avatar):
                st.markdown(message["content"])

    # Chatbot
    query = st.chat_input("Kérdezz nyugodtan")

    if query:
        # Tisztítás
        st.session_state.mermaid_code = ""
        st.session_state.graphviz_code = ""
        st.session_state.echart_code = ""
        st.session_state.plantuml_code = ""
        st.session_state.image = ""


        # Felhasználó üzenet mentése
        st.session_state.messages.append({"role": "user", "content": query})
        with chat_container:
            with st.chat_message("user", avatar = "avatar/user.png"):
                st.write(query)

        with chat_container:
            with st.chat_message("assistant", avatar = "avatar/bot.png"):
                with st.spinner("Gondolkozom..."):
                    try:
                        process(query, st.session_state.api_key, st.session_state.model, st.session_state.viz_selection)
                        with open("chatviz.json", "r", encoding="UTF-8") as f:
                            adatok = json.load(f)
                        if st.session_state.viz_selection == "Mermaid":
                            st.session_state.mermaid_code = adatok["mermaid_code"]
                            st.session_state.image = mermaid(adatok["mermaid_code"])
                        elif st.session_state.viz_selection == "Graphviz":
                            st.session_state.graphviz_code = adatok["graphviz_code"]
                            st.session_state.image = graphviz(adatok["graphviz_code"])
                        elif st.session_state.viz_selection == "Echart":
                            st.session_state.echart_code = echart(adatok["echart_code"])
                        elif st.session_state.viz_selection == "Plantuml":
                            st.session_state.plantuml_code = adatok["plantuml_code"]
                            st.session_state.image = plantuml(adatok["plantuml_code"])
                        #print(response.text)
                        #answer_text = clean_text(response.text)
                        answer_text = adatok["answer"]
                        print(answer_text)
                        st.markdown(answer_text)


                        # Nagy nyelvi modell üzenetének elmentése
                        st.session_state.messages.append({"role": "assistant", "content": answer_text})
                        st.rerun()
                    except Exception as e:
                        st.error(f"**Alkalmazás hiba:** {e}")


# Vizualizáció
with col2:
    viz_container = st.container(height=600)
    with viz_container:
        #clean_code = None
        #st.warning("Még nem jó")

        if st.session_state.viz_selection == "Mermaid" and st.session_state.mermaid_code:
            #clean_code = merm(st.session_state.mermaid_code)
            #if clean_code:
            render_custom_mermaid(st.session_state.mermaid_code, height=550)
        elif st.session_state.viz_selection == "Graphviz" and st.session_state.graphviz_code:
            #clean_code = viz(st.session_state.graphviz_code)
            #if clean_code:
            st.graphviz_chart(st.session_state.graphviz_code, use_container_width=True)
        elif st.session_state.viz_selection == "Echart" and st.session_state.echart_code:
            try:
                code = json.loads(st.session_state.echart_code)
                st_echarts(code, height="500px")
            except Exception as e:
                st.error(f"Echart megjelenítési hiba: {e}")
        elif st.session_state.viz_selection == "Plantuml" and st.session_state.plantuml_code:
            st.image(st.session_state.image, use_container_width=True)
        else:
            st.warning("Nincs megjeleníthető ábra")

    if "image" in st.session_state and st.session_state.viz_selection != "Echart":
        st.download_button(
                label = "Ábra letöltése",
                data = st.session_state.image,
                file_name = "abra.png",
                mime = "image/png",
                icon=":material/download:",
            )
    #if st.session_state.image == "":
        #st.info("Még nincs ábra")

