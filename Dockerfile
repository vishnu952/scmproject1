FROM python:3.8.10-slim

WORKDIR /app

COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD [ "uvicorn", "python.main:app", "--reload" ,"--host", "0.0.0.0" ]