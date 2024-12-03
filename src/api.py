from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
import pandas as pd
from utils import *
from fastapi.templating import Jinja2Templates
import random
class KBInput(BaseModel):
    kb_usage: str
    budget: int
    switch: str
    kb_size: str
    kb_connection: str
    mk_before: bool
    mk_input: str

app = FastAPI()
chat = load_llm(prompts_variables('prompt_sys'))

app.mount("/data", StaticFiles(directory="./data"), name="data")
templates = Jinja2Templates('./templates')

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})

@app.get("/cuestionario")
async def cuestionario(request: Request):
    return templates.TemplateResponse('cuestionario.html', {'request': request})

@app.get("/teclados")
async def cuestionario(request: Request):
    return templates.TemplateResponse('teclados.html', {'request': request})

# Enviar parametros usuarios a base de datos
@app.post("/keyfinder/send_user_data")
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
        return {"message": "Datos ingresados correctamente en la tabla de kb_input"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al insertar datos: {str(e)}")

# Guardar los datos del output del LLM
@app.post("/keyfinder/send_data_to_llm")
async def show_keyboards():   
    conn = open_database()
    cursor = conn.cursor()
    cursor.execute('select user_prompt from kb_input order by id_kb_input desc limit 1;')
    prompt = cursor.fetchone()

    # Llamada al LLM  
    ai_output =chat.invoke({'input': prompt['user_prompt']}, config={'configurable': {
            'session_id': random.randint(1, 1000000),  # Aleatoriedad en la sesión
            'temperature': 0.4,  # Controla la aleatoriedad
            'top_p': 0.9  # Controla la diversidad
        }})
    ai_output_split = ai_output.split("\n\n")
    keyboards = []
    for i, keyboard in enumerate(ai_output_split):
        if '###' in keyboard:
            keyboards.append(extract_keyboard_info_v2(keyboard))

    # Ingesta a base de datos
    try:
        query = """
                INSERT INTO kb_output (id_kb_input,kb_shown, price, switch, kb_size, mk_output, sys_prompt, kb_name, kb_link)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
        cursor.execute('SELECT id_kb_input from kb_input order by created_at desc limit 1;')
        id_kb_input = cursor.fetchone()
        i = 1
        for keyboard in keyboards:
            if any(isinstance(elemento, dict) for elemento in keyboard):
                cursor.execute(query,(id_kb_input['id_kb_input'],i, keyboard[0]['price'], keyboard[0]['switch'],
                                        keyboard[0]['kb_size'], keyboard[0]['mk_output'],
                                        ai_output, keyboard[0]['name'], keyboard[0]['kb_link']))
                i = i + 1
        conn.commit()
        conn.close()
        return {"message": "Datos ingresados correctamente en la tabla de kb_output"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al insertar datos: {str(e)}")
    
# Enseñar los teclados
@app.get("/keyfinder/show_keyboards")
async def show_keyboards():   
    try:
        conn = open_database()
        with conn.cursor() as cursor:
            cursor.execute('SELECT id_kb_input,kb_name, switch, kb_size, mk_output, price, kb_link from  kb_output order by id_kb_input desc limit 2;')
            keyboards = cursor.fetchall()
            print(type(keyboards))
        conn.close()
        return {"message": keyboards}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al insertar datos: {str(e)}")

# Carga de FastAPI
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)