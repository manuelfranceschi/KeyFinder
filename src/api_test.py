import requests

def test_send_data():
    url = 'http://localhost:8000/keyfinder/send_user_data'  
    data =   {
                "kb_usage": "Gaming",
                "budget": 150,
                "switch": "lineal",
                "kb_size": "60%",
                "kb_connection": "inalambrico",
                "mk_before": 'true',
                "mk_input": "Me gusta que tengan buen recorrido"
                }
    response = requests.post(url, json=data)
    assert response.status_code == 200
    assert response.json() == {"message": "Datos ingresados correctamente en la tabla de kb_input"}

def test_send_data_to_llm():
    url = 'http://localhost:8000/keyfinder/send_data_to_llm'  
    data = {} 
    
    response = requests.post(url, json=data)
    assert response.status_code == 200
    assert response.json() == {"message": "Datos ingresados correctamente en la tabla de kb_output"}

def test_show_keyboards():
    url = 'http://localhost:8000/keyfinder/show_keyboards'  
    response = requests.get(url)
    
    # Verificamos que el código de estado sea 200
    assert response.status_code == 200
    
    # Obtenemos los datos de la respuesta
    data = response.json()
    
    # Verificamos que la respuesta tenga la clave 'message' que contenga una lista
    assert "message" in data
    assert isinstance(data["message"], list)
    
    # Verificamos que cada teclado tenga el formato correcto
    if data["message"]:
        for keyboard in data["message"]:
            assert "id_kb_input" in keyboard
            assert "kb_name" in keyboard
            assert "switch" in keyboard
            assert "kb_size" in keyboard
            assert "mk_output" in keyboard
            assert "price" in keyboard
            assert "kb_link" in keyboard
