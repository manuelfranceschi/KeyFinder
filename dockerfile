FROM python:3.12.7-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0"]