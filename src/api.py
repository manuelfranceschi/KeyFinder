from fastapi import FastAPI, requests, HTTPException
from pydantic import BaseModel
import uvicorn
import pymysql
import pandas as pd
from langchain_huggingface import HuggingFaceEndpoint
from langchain.prompts import PromptTemplate, MessagesPlaceholder, ChatPromptTemplate
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from dotenv import load_dotenv
import os
import re
from utils import *

app = FastAPI()
class KBInput(BaseModel):
    kb_usage: str
    budget: int
    switch: str
    kb_size: str
    kb_connection: str
    mk_before: bool
    mk_input: str
class UserPrompt(BaseModel):
    prompt : str

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
    # Prompt para el modelo
    user_input = f'Busco un teclado para {data.kb_usage}, switches {data.switch}, {data.kb_size} y conexion {data.kb_connection}. Tengo un presupuesto de {data.budget} euros. '
    user_prompt = user_input
    if data.mk_before == True:
        mk_input = f"He usado teclados mecanicos antes y {data.mk_input}"
        user_prompt = user_prompt + mk_input
    try:   
        # Ingesta a base de datos
        conn = open_database()
        with conn.cursor() as cursor:
            query = """
                    INSERT INTO kb_input (kb_usage, budget, switch, kb_size, kb_connection, mk_before, mk_input, user_prompt)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """
            cursor.execute(query,(data.kb_usage, data.budget, data.switch, data.kb_size,
                                data.kb_connection, data.mk_before, data.mk_input, user_prompt))
        conn.commit()
        conn.close()
        return {"message": "Datos ingresados correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al insertar datos: {str(e)}")

@app.post("/keyfinder/keyboards")
async def show_keyboards(user_prompt: UserPrompt):   
    # Llamada al LLM 
    chat = load_llm(prompts_variables('prompt_sys'))
    ai_output =chat.invoke({'input': user_prompt.prompt}, config={'configurable': {'session_id': 'abc123'}})
    ai_output_split = ai_output.split("\n\n")
    keyboards = []
    for i, keyboard in enumerate(ai_output_split):
        if '###' in keyboard:
            keyboards.append(extract_keyboard_info_v2(keyboard))
    # Ingesta a base de datos
    try:
        conn = open_database()
        with conn.cursor() as cursor:
            query = """
                    INSERT INTO kb_output (id_kb_input,kb_shown, price, switch, kb_size, mk_output, sys_prompt, kb_name, kb_link)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
            cursor.execute('SELECT id_kb_input from kb_input order by created_at desc limit 1;')
            id_kb_input = cursor.fetchone()
            for keyboard in keyboards:
                i = 1
                cursor.execute(query,(id_kb_input['id_kb_input'],i, keyboard[0]['price'], keyboard[0]['switch'],
                                        keyboard[0]['kb_size'], keyboard[0]['mk_output'],
                                        ai_output, keyboard[0]['name'], keyboard[0]['kb_link']))
                i = i + 1
        conn.commit()
        conn.close()
        return {"message": keyboards}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al insertar datos: {str(e)}")

# Carga de FastAPI
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)