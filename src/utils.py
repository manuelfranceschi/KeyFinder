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

# Funciones 

def open_database():
    load_dotenv()
    db = pymysql.connect(host = os.getenv("HOST_BBDD"),
                     user = os.getenv("USERNAME_BBDD"),
                     password = os.getenv("PASSWORD_BBDD"),
                     database=os.getenv("DB_NAME"),
                     cursorclass = pymysql.cursors.DictCursor
    )   
    return db

def load_llm(prompt):
    llm = HuggingFaceEndpoint(endpoint_url='https://api-inference.huggingface.co/models/Qwen/Qwen2.5-72B-Instruct',
                          huggingfacehub_api_token=os.getenv('API_KEY_MODEL'),
                          temperature=0.3, max_lenght=2000)
    prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            prompt,
         ),
         MessagesPlaceholder(variable_name='history'),
         ('human', '{input}')
    ]
    )
    
    runnable = prompt_template | llm
    store = {}
    def get_session_history(session_id: str) -> BaseChatMessageHistory:
        if session_id not in store:
            store[session_id] = ChatMessageHistory()
        return store[session_id]

    with_message_history = RunnableWithMessageHistory(
    runnable,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
    )

    return with_message_history

def extract_keyboard_info_v2(text):
    # Regex para extraer cada bloque de teclado
    keyboard_blocks = re.findall(
        r"### \d+\.\s\*\*(.*?)\*\*\n- \*\*Precio:\*\* (.*?)\n- \*\*Modelo de switches:\*\* (.*?)\n- \*\*Formato del teclado y número de teclas:\*\* (.*?)\n- \*\*Justificación:\*\* (.*?)\n- \*\*Enlace para comprar:\*\* \[(.*?)\]\((.*?)\)",
        text,
        re.DOTALL
    )

    keyboards = []
    for block in keyboard_blocks:
        keyboard_info = {
            "name": block[0].strip(),
            "price": block[1].strip(),
            "switch": block[2].strip(),
            "kb_size": block[3].strip(),
            "mk_output": block[4].strip(),
            "kb_link": block[6].strip()
        }
        keyboards.append(keyboard_info)

    return keyboards

#Prompts

def prompts_variables(which_one:str):
    if which_one == 'prompt_sys':
        output = """
            Eres un experto en teclados mecánicos y tu tarea es recomendar los 2 mejores teclados mecánicos al usuario según sus necesidades específicas. 
            El usuario ha proporcionado la siguiente información: {input}

            Responde estrictamente en el siguiente formato. Proporciona la información para los dos teclados en un solo bloque. Asegúrate de que cada teclado tenga todos los campos completos y que la justificación sea breve pero específica:

            ### 1. **[Nombre del teclado]**
            - **Precio:** [Precio en euros]
            - **Modelo de switches:** [Modelo exacto de los switches, por ejemplo, Cherry MX Brown o Gateron Red]
            - **Formato del teclado y número de teclas:** [Formato, por ejemplo, 60%, 65%, TKL o completo, seguido del número exacto de teclas]
            - **Justificación:** [Una breve opinión de por qué este teclado es una buena opción considerando las preferencias del usuario, pero sobretodo si ha usado teclados mecánicos antes, lo que más le gusta]
            - **Enlace para comprar:** [Texto visible del enlace](URL exacta del enlace)
            
            Recuerda: responde en un solo bloque de texto y asegúrate de completar todos los campos para los tres teclados sin omitir ningún detalle.
            """
    return output