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