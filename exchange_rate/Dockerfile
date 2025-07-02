# exchange_rate/Dockerfile
FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY exchange_rate/ ./exchange_rate/

EXPOSE 8001

CMD ["uvicorn", "exchange_rate.app:app", "--host", "0.0.0.0", "--port", "8001"]