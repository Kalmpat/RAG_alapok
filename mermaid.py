# kódoláshoz
import base64
import urllib
import zlib

import streamlit as st
# Regex alkalmazása
import re
# HTML belenyúlása
import streamlit.components.v1 as components

import requests

# szövegből --> link
def mermaid(graph):
    # kód tisztítása, helyettesítés és csere
    #clean_code = re.sub(r"```mermaid\n|```", "", graph).strip()

    if not graph:
        st.warning("Nem található Mermaid diagram a válaszban.")
        return

    #match = re.search(r"```[Mm]ermaid\n(.*?)```", graph, re.DOTALL)
    #if not match:
    #    #st.warning("Nem található Mermaid diagram a válaszban.")
    #    return

    #clean_code = match.group(1).strip()
    # Debugra
    # st.code(clean_code, language="text")
    graphbytes = graph.encode("utf8") # kód --> bájt
    base64_bytes = base64.urlsafe_b64encode(graphbytes) # URl alakítás
    base64_string = base64_bytes.decode("ascii") # visszalakaítás (dekódolás)

    url = f"https://mermaid.ink/img/{base64_string}"
    return requests.get(url).content
    #st.image(url, use_container_width=True)

def merm(graph):
    match = re.search(r"```mermaid\n(.*?)```", graph, re.DOTALL)
    if not match:
        st.warning("Nem található Mermaid diagram a válaszban.")
        return

    clean_code = match.group(1).strip()
    return clean_code

def clean_text(text):
   pattern = r"```\s*(graphviz|mermaid).*?```"

   # flags=re.DOTALL és re.IGNORECASE megakályozza a kis, nagy -betűket és a sor emelést
   cleaned = re.sub(pattern, "", text, flags=re.DOTALL | re.IGNORECASE).strip()
   return cleaned


# Mermaid elhelyezése, megjeletése
def render_custom_mermaid(code: str, height: int = 600):
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ 
                startOnLoad: true,
                theme: 'dark'
            }});
        </script>
        <style>
            body {{
                background-color: transparent; 
                margin: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh; 
                overflow: hidden; /* Ezt érdemes visszatenni */
            }}
            .mermaid {{
                width: 100%;
                display: flex;
                justify-content: center;
                align-items: center;
            }}
            .mermaid svg {{
                max-width: 100%;
                max-height: 95vh; 
                width: auto !important;
                height: auto !important;
            }}
        </style>
    </head>
    <body>
        <div class="mermaid">
            {code}
        </div>
    </body>
    </html>
    """
    components.html(html_code, height=height)

def viz(graph):
    match = re.search(r"```[Gg]raphviz\n(.*?)```", graph, re.DOTALL)
    if not match:
        st.warning("Nem található Graphviz diagram a válaszban.")
        return

    clean_code = match.group(1).strip()
    return clean_code

def graphviz(graph):
    #match = re.search(r"```[Gg]raphviz\n(.*?)```", graph, re.DOTALL)
    #if not match:
    #    return
    if not graph:
        st.warning("Nem található Graphviz diagram a válaszban.")
        return
    #clean_code = match.group(1).strip()
    # Hasonló mint a mermaid átalakítás
    #encoded_graph = urllib.parse.quote(clean_code)

    response = requests.post(
        "https://quickchart.io/graphviz",
        json={"graph": graph, "format": "png"}
    )
    return response.content

def echart(graph):
    #match = re.search(r"```[Ee]chart\n(.*?)```", graph, re.DOTALL)
    if not graph:
        st.warning("Nem található Echart diagram a válaszban.")
        return

    #clean_code = match.group(1).strip()
    clean_code = graph.replace('\u00a0', ' ')

    return clean_code

def plantuml(graph):
    if not graph:
        return
    compressed = zlib.compress(graph.encode("utf-8"), 9)
    base64_string = base64.urlsafe_b64encode(compressed).decode("ascii")

    url = f"https://kroki.io/plantuml/png/{base64_string}"
    response = requests.get(url)
    return response.content

def d2lang(graph):
    if not graph:
        return
    compressed = zlib.compress(graph.encode("utf-8"), 9)
    base64_string = base64.urlsafe_b64encode(compressed).decode("ascii")

    url = f"https://kroki.io/d2/png/{base64_string}"
    response = requests.get(url)
    return response.content


