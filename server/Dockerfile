FROM python:3.8.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "server.py" ]

EXPOSE 8000
