FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install fastapi uvicorn httpx jinja2
CMD ["bash", "-c", "uvicorn app:app --host 0.0.0.0 --port $PEER_PORT --reload"]