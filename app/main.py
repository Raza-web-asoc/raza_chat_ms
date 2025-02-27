from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.routers.chat import router_chats
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

connections = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=[""],
    allow_headers=[""],
)

Instrumentator().instrument(app).expose(app, endpoint="/metrics")

@app.websocket("/ws")
async def  websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            for connection in connections:
                await connection.send_text(data)
    
    except WebSocketDisconnect:
        connections.remove(websocket)

        

# Registrar el router
app.include_router(router_chats, prefix="/chats", tags=["Chats"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Chat API"}

@app.get("/error")
def error():
    return {"message": "Internal Server Error"}, 500