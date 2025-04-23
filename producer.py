import pika, random, json, time, threading

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI()

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

def generateRandomLog():
    logLevels = ['INFO', 'ERROR', 'WARNING', 'CRITICAL']
    logMessages = [
        "User logged in successfully.",
        "File not found.",
        "Database connection failed.",
        "Request processed successfully.",
        "Memory usage is high.",
        "Unexpected input received.",
        "Permission denied for the requested operation."
    ]
    level = random.choice(logLevels)
    message = random.choice(logMessages)
    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    logEvent = {
        "level": level,
        "message": message,
        "timestamp": timestamp
    }
    return logEvent

logGenerationActive = False

def generateLog():
    while logGenerationActive:
        log = generateRandomLog()
        channel.basic_publish(
            exchange='',
            routing_key='logs',
            body=json.dumps(log),
            properties=pika.BasicProperties(delivery_mode=2),
        )  
        time_to_sleep = random.uniform(0.05, 0.1) 
        time.sleep(time_to_sleep)


@app.post("/startLogGeneration/")
async def startLogGeneration():
    global logGenerationActive, logThread
    if logGenerationActive:
        print('Log Generation is already Active.')
        return
    logGenerationActive = True
    threading.Thread(target=generateLog, daemon=True).start()
    print('Log Generation started.')


@app.post("/stopLogGeneration/")
async def stopLogGeneration():
    global logGenerationActive
    if not logGenerationActive:
        print('Log Generation is not active.')
        return
    logGenerationActive = False
    print('Log Generation stopped.')
