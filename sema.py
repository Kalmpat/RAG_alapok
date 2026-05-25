tananyag_sema = {
    "type": "OBJECT",
    "properties": {
        "cim": {"type": "STRING"},
        "leiras": {"type": "STRING"},
        "szakkifejezesek": {
            "type": "OBJECT",
            "properties": {
                "definiciok": {
                    "type": "ARRAY",
                    "items": {
                        "type": "OBJECT",
                        "properties": {
                            "kifejezes": {"type": "STRING"},
                            "magyarazat": {"type": "STRING"}
                        },
                        "required": ["kifejezes", "magyarazat"]
                    }
                },
                "tetelek": {
                    "type": "ARRAY",
                    "items": {
                        "type": "OBJECT",
                        "properties": {
                            "nev": {"type": "STRING"},
                            "leiras": {"type": "STRING"}
                        },
                        "required": ["nev", "leiras"]
                    }
                }
            },
            "required": ["definiciok", "tetelek"]
        },
        "osszefuggesek": {"type": "STRING"},
        "didaktikai_tipp": {"type": "STRING"}
    },
    "required": ["cim", "leiras", "szakkifejezesek", "osszefuggesek", "didaktikai_tipp"]
}

# mermaid_sema
mermaid_sema = {
    "title": "MermaidResponse",
    "type": "object",
    "properties": {
        "answer": {"type": "string"},
        "mermaid_code": {"type": "string"}
    },
    "required": ["answer", "mermaid_code"]
}

# graphviz_sema
graphviz_sema = {
    "type": "OBJECT",
    "properties": {
        "answer": {"type": "STRING"},
        "graphviz_code": {"type": "STRING"}
    },
    "required": ["answer", "graphviz_code"]
}
# echart_sema
echart_sema = {
    "type": "OBJECT",
    "properties": {
        "answer": {"type": "STRING"},
        "echart_code": {"type": "STRING"}
    },
    "required": ["answer", "echart_code"]
}

# plantuml_sema
plantuml_sema = {
    "type": "OBJECT",
    "properties": {
        "answer": {"type": "STRING"},
        "plantuml_code": {"type": "STRING"}
    },
    "required": ["answer", "plantuml_code"]
}

# d2lang_sema
d2lang_sema = {
    "type": "OBJECT",
    "properties": {
        "answer": {"type": "STRING"},
        "d2lang_code": {"type": "STRING"}
    },
    "required": ["answer", "d2lang_code"]
}

# ZH séma

zh_sema = {
    "type": "OBJECT",
    "properties": {
        "igaz_hamis_kerdesek": {
            "type": "ARRAY",
            "description": "Pontosan 5 darab Igaz-Hamis kérdés.",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "allitas": {"type": "STRING", "description": "Az állítás szövege a tananyag alapján."},
                    "helyes_valasz": {"type": "BOOLEAN", "description": "True ha igaz, False ha hamis."},
                    "indoklas": {"type": "STRING", "description": "Rövid magyarázat a javítókulcsba, hogy miért ez a válasz."}
                },
                "required": ["allitas", "helyes_valasz", "indoklas"]
            }
        },
        "feleletvalaszto_kerdesek": {
            "type": "ARRAY",
            "description": "Feleletválasztós kérdések (A, B, C, D opciókkal).",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "kerdes": {"type": "STRING", "description": "A feltett kérdés."},
                    "opcio_A": {"type": "STRING"},
                    "opcio_B": {"type": "STRING"},
                    "opcio_C": {"type": "STRING"},
                    "opcio_D": {"type": "STRING"},
                    "helyes_opcio": {"type": "STRING", "description": "A helyes opció betűjele: A, B, C vagy D."},
                    "indoklas": {"type": "STRING", "description": "Magyarázat a javítókulcsba."}
                },
                "required": ["kerdes", "opcio_A", "opcio_B", "opcio_C", "opcio_D", "helyes_opcio", "indoklas"]
            }
        },
        "kifejtos_kerdesek": {
            "type": "ARRAY",
            "description": "Pontosan 3 darab kifejtős kérdés.",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "kerdes": {"type": "STRING", "description": "A kifejtendő kérdés."},
                    "elvart_kulcsszavak": {
                        "type": "ARRAY",
                        "items": {"type": "STRING"},
                        "description": "A legfontosabb szavak, amiket a diáknak le kell írnia."
                    },
                    "mintavalasz": {"type": "STRING", "description": "Az ideális válasz a javítókulcsba."}
                },
                "required": ["kerdes", "elvart_kulcsszavak", "mintavalasz"]
            }
        },

    },
    "required": ["igaz_hamis_kerdesek", "feleletvalaszto_kerdesek", "kifejtos_kerdesek"]
}