# KeyFinder

Enlace al contenedor de Docker: https://hub.docker.com/repository/docker/manuelfranceschi/keyfinder/general

KeyFinder es un asistente para la busqueda de teclados mecánicos. Si eres un usuario que todavía no ha dado el paso a probar este tipo de teclados, ¿Puede ser por la inmensa variedad de switches que existen actualmente en el mercado? ¿La gran cantidad de modelos que guarden similitudes? Esto puede llegar a ser un problema sobretodo si queremos traer más gente al mundillo

Puntos clave:

1. Muestra teclados concretos en base a las características que le pases. 
2. Permite generar estos tantas veces queramos.
3. Nos deja un enlace de amazon para su compra (no afiliado).

Nota: KeyFinder aún esta en proceso de desarrollo.

Requisitos:
fastapi==0.115.5
pydantic==2.10.2
uvicorn==0.32.1
PyYAML==6.0.2
PyMySQL==1.1.1
langchain==0.3.9
langsmith==0.1.147
pandas==2.2.3
numpy==1.26.4
Jinja2==3.1.4
langchain-huggingface==0.1.2
langchain-community==0.3.8

Para el funcionamiento de este modelo en local hace falta un API KEY de HuggingFace.

Toda la documentación con respecto a endpoints puedes conseguirlo en /docs gracias a la documentación autogenerada por FastAPI:
localhost:8000/docs

Tambien existe un test para comprobar el funcionamiento de estos mismos, lo puedes conseguir en el repo como api_test.py

Contacto

Si te ha parecido interesante o quieres dejarme algo de feedback:
https://www.linkedin.com/in/manuelfranceschi/