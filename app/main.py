from fastapi import FastAPI
from app.routers.chat import router_chats

app = FastAPI(title="MongoDB API", version="1.0")

# Incluir el router de consultas
app.include_router(router_chats)

 
