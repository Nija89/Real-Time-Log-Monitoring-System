from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import pika
import json
import asyncio
from threading import Thread

app = FastAPI()
websocket_clients = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='logs', durable=True, arguments={'x-max-length': 1000})

def callback(ch, method, properties, body):
    log_message = body.decode()
    logLevel = json.loads(body.decode())
    if logLevel["level"] == 'ERROR' or logLevel['level'] == 'CRITICAL':
        for websocket in websocket_clients.copy():
            try:
                asyncio.run(websocket.send_text(log_message))
            except Exception as e:
                print("Error sending to WebSocket:", e)
                websocket_clients.remove(websocket)

def startConsumer():
    channel.basic_consume(queue='logs', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

Thread(target=startConsumer, daemon=True).start()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    websocket_clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        print("WebSocket disconnected")
        websocket_clients.remove(websocket)
