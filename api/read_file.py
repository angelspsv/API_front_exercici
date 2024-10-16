from conn_file import db_connexio

def read_alumnes():
    try:
        conn = db_connexio()

        # Si 'conn' es un diccionario, es que ocurrió un error en la conexión
        if isinstance(conn, dict) and conn.get("status") == -1:
            return conn  # Devuelve el error

        cur = conn.cursor()
        cur.execute("SELECT * FROM Alumne")
        alumnes = cur.fetchall()
        
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    
    finally:
        if conn and not isinstance(conn, dict):
            conn.close()
    
    return alumnes


def read_alumne_id(id_alumne):
    try:
        conn = db_connexio()
        cur = conn.cursor()
        
        # s'executa la query d'alumne amb l'id agafat des de navegador
        cur.execute("SELECT * FROM Alumne WHERE id_alumne = %s", (id_alumne,))

        #el resultat es desa en la variable
        alumne = cur.fetchone()
        #si l'id de l'alumne no existeix
        if alumne is None:
            return None

    except Exception as e:
        return {"status": -1, "message": f"Error de connexió: {e}"}
    finally:
        if conn and not isinstance(conn, dict):
            conn.close()
    
    return alumne



# funcio per veure si existeix l'id_aula a la taula Aula
def read_aula_id(id_aula):
    try:
        conn = db_connexio()
        cur = conn.cursor()

        #fem la consulta sql per veure si existeix el id_aula
        cur.execute("SELECT * FROM aula WHERE id_aula = %s", (id_aula,))
        aula = cur.fetchone()

        # retorna True o False de la consulta sql
        return aula

    #en cas d'error: no existeix l'id d'aula
    except Exception as e:
        print(f"Error al verificar el id_aula: {e}")
        return None

    #si o si tanquem la connexio a la bbdd al final
    finally:
        if conn and not isinstance(conn, dict):
            cur.close()
            conn.close()