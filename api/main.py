from typing import Union
from typing import List, Dict
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from read_file import read_alumnes
from read_file import read_alumne_id
from read_file import read_aula_id
from conn_file import db_connexio
import alumne
from fastapi.middleware.cors import CORSMiddleware


#fem la api
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Alumne(BaseModel):
    id_aula: int
    nom_alumne: str
    cicle: str
    curs: int
    grup: str


#introduit per la pràctica 2
class TablaAlumne(BaseModel):
    nombre: str
    cicle: str
    curs: int
    grup: str
    desc_aula: str


#endpoint
#raiz de la api
@app.get("/")
def read_root():
    return {"Hola Toni!"}


# EXERCICI 1
#endpoint
#funcio per veure tots els alumnes de la taula
@app.get("/alumne/list/", response_model=List[Dict])
def get_alumnes():
    alumnes = read_alumnes()

    # Si hi ha error en la connexió a la bbdd, retorna excepció
    if isinstance(alumnes, dict) and "status" in alumnes and alumnes["status"] == -1:
        raise HTTPException(status_code=500, detail=alumnes["message"])
    
    alumnes_sch = alumne.alumnes_schema(alumnes)
    return alumnes_sch


# EXERCICI 2
#endpoint
#per veure un alumne en concret
@app.get("/alumne/show/{id_alumne}")
def read_alumne(id_alumne):
    alumne_data = read_alumne_id(id_alumne)

    #si l'id no existeix
    if alumne_data is None:
        raise HTTPException(status_code=404, detail="Alumne no trobat amb aquesta id")

    alumne_sch = alumne.alumne_schema(alumne_data)
    return alumne_sch


# EXERCICI 3
#endpoint
# afegit un alumne nou a la taula alumne
# l'operació d'inserció acabarà bé si l'id_aula existeix
@app.post("/alumne/add/")
def create_alumne(alumne_data: Alumne):
    # connexió a la bbdd
    conn = db_connexio()
    cur = conn.cursor()

    try:
        #verifiquem que el id_aula existeix
        aula = read_aula_id(alumne_data.id_aula)

        #si False, id_aula no existeix
        if not aula:
            raise HTTPException(status_code=404, detail="El id_aula no existeix")

        # si el id_aula existeix, fem el INSERT del nou alumne
        cur.execute("""
            INSERT INTO Alumne (id_aula, nom_alumne, cicle, curs, grup) 
            VALUES (%s, %s, %s, %s, %s)
        """, (alumne_data.id_aula, alumne_data.nom_alumne, alumne_data.cicle, alumne_data.curs, alumne_data.grup))

        #desem els canvis en la bbdd
        conn.commit()

        #mostrem sms d'èxit en format JSON
        return {"message": "Se ha afegit correctament!"}

    except Exception as e:
        #en cas d'error mostrem un sms
        raise HTTPException(status_code=500, detail=f"Error afegint el nou alumne: {str(e)}")

    finally:
        #es tanca la connexió a la bbdd
        cur.close()
        conn.close()


# EXERCICI 4
#endpoint
# cal fer un update d'un alumne des del seu id (parametre)
# si modifiquem el camp de id_aula s'ha de fer com en el POST
# retorna objecte json amb sms "S'ha modificat correctament"
@app.put("/alumne/update/{id_alumne}")
def update_alumne(id_alumne: int, alumne_update: Alumne):
    conn = db_connexio()  
    cur = conn.cursor()

    try:
        #mirem si l'alumne existeix a la bbdd
        alumne_existent = read_alumne_id(id_alumne) 
        if not alumne_existent:
            raise HTTPException(status_code=404, detail="Alumne no trobat amb aquest id")

        #agafem les dades de l'alumne des del seu id_alumne
        alumne_data = read_alumne_id(id_alumne)

        #de tupla a diccionari
        alumne_dicc = {
            "id_alumne": alumne_data[0],
            "id_aula": alumne_data[1],
            "nom_alumne": alumne_data[2],
            "cicle": alumne_data[3],
            "curs": alumne_data[4],
            "grup": alumne_data[5],
        }

        id_aula_actual = alumne_data[1]

        #verificar si l'id_aula existeix a la bbdd
        if alumne_update.id_aula is not None and alumne_update.id_aula != id_aula_actual:
            if not read_aula_id(alumne_update.id_aula):
                raise HTTPException(status_code=404, detail="El nou id_aula no existeix")

        #Actualizar los campos solo si se proporcionan valores nuevos
        if alumne_update.id_aula is not None:
            alumne_dicc["id_aula"] = alumne_update.id_aula
        if alumne_update.nom_alumne is not None:
            alumne_dicc["nom_alumne"] = alumne_update.nom_alumne
        if alumne_update.cicle is not None:
            alumne_dicc["cicle"] = alumne_update.cicle
        if alumne_update.curs is not None:
            alumne_dicc["curs"] = alumne_update.curs
        if alumne_update.grup is not None:
            alumne_dicc["grup"] = alumne_update.grup

        #s'executa la sql i s'actualitza la bbdd
        cur.execute("""
            UPDATE Alumne
            SET id_aula = %s, nom_alumne = %s, cicle = %s, curs = %s, grup = %s
            WHERE id_alumne = %s
        """, (
            alumne_dicc["id_aula"],
            alumne_dicc["nom_alumne"],
            alumne_dicc["cicle"],
            alumne_dicc["curs"],
            alumne_dicc["grup"],
            id_alumne
        ))

        #desem els canvis a la bbdd
        conn.commit()

        #sms per indicar que tot ha anat bé
        return {"message": "S'ha modificat correctament", "data": alumne_dicc}

    #sms d'error si algun camp nno es correcte
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al modificar l'alumne: {str(e)}")

    #tanquem la connexió a la bbdd
    finally:
        cur.close()
        conn.close()


# EXERCICI 5
#endpoint
#esborrar un alumne de la bbdd pel seu id_alumne(parametre)
#s'ha de retornar un sms objecte "S'ha esborrat correctament"
@app.delete("/alumne/delete/{id_alumne}")
def delete_alumne(id_alumne):
    conn = db_connexio()
    cur = conn.cursor()

    try:
        #mirar si esta el alumne
        alumne_data = read_alumne_id(id_alumne)
        if alumne_data is None:
            raise HTTPException(status_code=404, detail="Alumne no trobat amb aquesta id")

        #esborrem l'alumne de la bbdd pel seu id_alumne
        cur.execute("DELETE FROM alumne WHERE id_alumne = %s", (id_alumne,))

        #desem els canvis
        conn.commit()

        #sms d'operació finalitzada amb èxit
        return {"message": "S'ha esborrat correctament"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar l'alumne: {str(e)}")

    finally:
        cur.close()
        conn.close()


# EXERCICI 6
# endpoint
# fer una funció per fer una query_join de alumne i aula
# retornar els resultats en formar json
@app.get("/alumne/listall", response_model=List[TablaAlumne])
def alumneJoinAula():
    #connexio a la bbdd
    conn = db_connexio()
    cur = conn.cursor()

    try:
        #fem la sql join query
        join_query = "SELECT alumne.nom_alumne, alumne.cicle, alumne.curs, alumne.grup, aula.desc_aula FROM alumne JOIN aula ON alumne.id_aula = aula.id_aula;"
        cur.execute(join_query)

        #agafem tots els resultats
        alumnes = cur.fetchall()

        #fem un diccionari amb els resultats
        alumnes_list = []
        for alumne in alumnes:
            alumne_dict = {
                "id_alumne": alumne[0],
                "nom_alumne": alumne[1],
                "cicle": alumne[2],
                "curs": alumne[3],
                "grup": alumne[4],
                "desc_aula": alumne[5],
                "edifici": alumne[6],
                "pis": alumne[7]
            }
            alumnes_list.append(alumne_dict)

        #retornem la llista d'objectes json d'alumnes i aula
        return alumnes_list

    #avís en cas d'error
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtenir els alumnes: {str(e)}")

    #tanquem els recursos/connexions
    finally:
        cur.close()
        conn.close()