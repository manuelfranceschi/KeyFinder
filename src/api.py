from fastapi import FastAPI, requests, HTTPException
from pydantic import BaseModel
import uvicorn
import pymysql
import pandas as pd
from dotenv import load_dotenv
import os

app = FastAPI()

class KBInput(BaseModel):
    kb_usage: str
    budget: int
    switch: str
    kb_size: str
    kb_connection: str
    mk_before: bool
    mk_input: str

def open_database():
    load_dotenv()
    username = os.getenv("API_KEY_MODEL")
    password = os.getenv("PASSWORD")
    host = os.getenv("HOST")
    port = os.getenv("PORT")
    db_name = os.getenv("DB_NAME")
    db = pymysql.connect(host = host,
                     user = username,
                     password = password,
                     database=db_name,
                     cursorclass = pymysql.cursors.DictCursor
    )   
    return db

# Home de la app, se muestra el landing page
@app.get("/home")
async def hello():
    return "Bienvenido a mi API :)"

# Mostrar datos en database
@app.get("/database")
async def show_database():
    try:
        conn = open_database()
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM kb_input')
            results = cursor.fetchall()
        conn.close()
        return dict({"results": results})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Enviar parametros usuarios
@app.post("/keyfinder/send")
async def send_data(data: KBInput):
    if not data:
        raise HTTPException(status_code=400, detail='No se han proporcionado datos')
    try:
        conn = open_database()
        cursor = conn.cursor()
        with conn.cursor() as cursor:
            query = """
                    INSERT INTO kb_input (kb_usage, budget, switch, kb_size, kb_connection, mk_before, mk_input)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
            cursor.execute(query,(data.kb_usage, data.budget, data.switch, data.kb_size,
                                data.kb_connection, data.mk_before, data.mk_input))
        conn.commit()
        conn.close()
        return {"message": "Datos ingresados correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al insertar datos: {str(e)}")


# Carga de FastAPI
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)