def alumne_schema(alumne) -> dict:
    return {
        "nom_alumne": alumne[0],
        "cicle": alumne[1],
        "curs": alumne[2],
        "grup": alumne[3],
        "desc_aula": alumne[4],
    }

def alumnes_schema(alumnes) -> list:
    return [alumne_schema(alumne) for alumne in alumnes]