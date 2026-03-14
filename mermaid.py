# kódoláshoz
import base64
import streamlit as st
# Regex alkalmazása
import re
# HTML belenyúlása
import streamlit.components.v1 as components


# szövegből --> link
def mermaid(graph):
    # kód tisztítása, helyettesítés és csere
    # clean_code = re.sub(r"```mermaid\n|```", "", graph).strip()

    match = re.search(r"```mermaid\n(.*?)```", graph, re.DOTALL)
    if not match:
        st.warning("Nem található Mermaid diagram a válaszban.")
        return

    clean_code = match.group(1).strip()
    # Debugra
    # st.code(clean_code, language="text")

    graphbytes = clean_code.encode("utf8")  # kód --> bájt
    base64_bytes = base64.urlsafe_b64encode(graphbytes)  # URl alakítás
    base64_string = base64_bytes.decode("ascii")  # visszalakaítás (dekódolás)

    url = f"https://mermaid.ink/svg/{base64_string}"
    st.image(url, use_container_width=True)


def merm(graph):
    match = re.search(r"```mermaid\n(.*?)```", graph, re.DOTALL)
    if not match:
        st.warning("Nem található Mermaid diagram a válaszban.")
        return

    clean_code = match.group(1).strip()
    return clean_code


def clean_text(text):
    pattern = r"```\s*[Mm]ermaid.*?```"

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
            }}
            .mermaid {{
                width: 100%;
                text-align: center;
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