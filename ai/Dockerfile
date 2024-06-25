FROM python:3.12.4-slim-bookworm

RUN apt update -y && apt upgrade -y

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
