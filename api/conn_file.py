import mysql.connector

def db_connexio():
    #establim la connexió amb la base de dades
    try:
        dbname = "alumnat_db"
        user = "root"
        password = "1234"
        host = "localhost"
        port = "3309"
        
        return mysql.connector.connect(
            host = host,
            port = port,
            user = user,
            password = password,
            database = dbname,
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci' 
        )
           
    # excepció per si hi ha algun error       
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }