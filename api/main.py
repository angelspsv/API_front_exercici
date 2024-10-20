from typing import List, Dict
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from read_file import read_alumnes
from read_file import read_alumne_id
from read_file import read_aula_id
from conn_file import db_connexio
import alumne
from fastapi.middleware.cors import CORSMiddleware
import csv

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
    nom_alumne: str
    cicle: str
    curs: int
    grup: str
    desc_aula: str


#endpoint
#raiz de la api
@app.get("/")
def read_root():
    return {"Hola Toni!"}


#endpoint
#exercici de prova
@app.get("/prueba", response_model=List[TablaAlumne])
def muestrame_los_alumnos():
    conn = db_connexio()
    cur = conn.cursor()
    try:
        query_sql = "SELECT alumne.nom_alumne, alumne.cicle, alumne.curs, alumne.grup, aula.desc_aula FROM alumne JOIN aula ON alumne.id_aula = aula.id_aula"
        cur.execute(query_sql)
        alumnes = cur.fetchall()
        #pasem els resultats a diccionari
        alumnes_list = []
        for alumne in alumnes:
            alumne_dict = {
                "nom_alumne": alumne[0],
                "cicle": alumne[1],
                "curs": alumne[2],
                "grup": alumne[3],
                "desc_aula": alumne[4]
            }
            alumnes_list.append(alumne_dict)
        #retornem els resultats en json
        return alumnes_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtenir els alumnes: {str(e)}")
    finally:
        cur.close()
        conn.close()

# Aquest exercici (Ex1 Prac1) s'ha modificat per l'Apartat 2 de la segona pràctica 
#Ara es poden fer consultes mes complexes amb order by, contain(LIKE),
# skip & limit (skip per treure resultats del principi i limit, limita la quantitat de resultats)
# EXERCICI 1
#endpoint
#funcio per veure tots els alumnes de la taula
@app.get("/alumnes/list", response_model=List[TablaAlumne])
def read_alumnes(orderby: str | None = None, contain: str | None = None,
                 skip: int = 0, limit: int | None = None):
    #connexió a la bbdd
    conn = db_connexio()
    cur = conn.cursor()

    try:
        #consultes sql_query per cada cas
        #combinació 1 amb orderby ASC i DESC
        if orderby in ["asc", "desc"]:
            query = f"""
            SELECT alumne.nom_alumne, alumne.cicle, alumne.curs, alumne.grup, aula.desc_aula
            FROM alumne
            JOIN aula ON alumne.id_aula = aula.id_aula
            ORDER BY alumne.nom_alumne {orderby.upper()}
            """

        #combinació 2 de contain
        elif contain:
            query = f"""
            SELECT alumne.nom_alumne, alumne.cicle, alumne.curs, alumne.grup, aula.desc_aula
            FROM alumne
            JOIN aula ON alumne.id_aula = aula.id_aula
            WHERE alumne.nom_alumne LIKE '%{contain}%'
            """

        #combinació 3 de skip & limit
        elif limit is not None:
            query = f"""
            SELECT alumne.nom_alumne, alumne.cicle, alumne.curs, alumne.grup, aula.desc_aula
            FROM alumne
            JOIN aula ON alumne.id_aula = aula.id_aula
            LIMIT {limit} OFFSET {skip}
            """

        #executem la consulta sql
        cur.execute(query)
        alumnes = cur.fetchall()

        #pasem els resultats a diccionari
        alumnes_list = []
        for alumne in alumnes:
            alumne_dict = {
                "nom_alumne": alumne[0],
                "cicle": alumne[1],
                "curs": alumne[2],
                "grup": alumne[3],
                "desc_aula": alumne[4]
            }
            alumnes_list.append(alumne_dict)

        #retornem els alumnes en format json
        return alumnes_list

    #llançem excepcio
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtenir els alumnes: " + str(e))

    finally:
        #tanquem les connexions
        cur.close()
        conn.close()



#practica 2, apartat 3: carrega massiva de dades
#endpoint
# s'ha de desenvolupar una funció per fer un POST
#  carregant dades des d'un fitxer csv a la bbdd ja existent 
# IMPORTANT: abans de fer un insert a AULA no es pot repetir desc_aula
# si ja existeix aquesta aula no es fara l'insert a la taula
# l'alumne NO POT estar matriculat mes d'un cop a: cicle, curs, grup
@app.post("/alumne/loadalumnes")
def importarDadesCSV():
    # connexió a la bbdd
    conn = db_connexio()
    cur = conn.cursor()
    
    with open("alumnes_aules.csv","r") as csvfile:
    #fem servir next() per saltar la 1a linia
    # desc_aula, edifici, pis, nom_alumne, cicle, curs, grup
        next(csvfile)
        #resta de linies amb dades per insert 
        linies = csvfile.readlines()
        
        for linia in linies:
        #començem a tractar les dades linia x linia
        #transformem cada linia en una llista
        #dividim manualment i separem per ','
            #amb cada linia fem una llista amb valors
            valors = linia.strip().split(',')
            
            #valors[0] es desc_aula
            cur.execute("SELECT desc_aula FROM aula WHERE desc_aula = %s", (valors[0],))

            #el resultat es desa en la variable existeix
            existeix = cur.fetchone()
            #si desc_aula no existeix es pot fer l'insert a la taula aula
            if not existeix:
                try:
                #fem l'insert query per entrar les dades de la nova aula
                    cur.execute("""INSERT INTO aula (desc_aula, edifici, pis) VALUES (%s, %s, %s)""", (valors[0], valors[1], valors[2]))
                    print("Nova aula " + valors[0] + " inserida correctamt")
                
                except Exception as e:
                    print("Aula " + valors[0] + " ja existeix. " + str(e))
        
        #desem els canvis en la bbdd
        conn.commit()

        

        cur.close()
        conn.close()









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
                "nom_alumne": alumne[0],
                "cicle": alumne[1],
                "curs": alumne[2],
                "grup": alumne[3],
                "desc_aula": alumne[4]
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