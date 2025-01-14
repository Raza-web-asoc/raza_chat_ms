from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.chat import router_chats

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=[""],
    allow_headers=[""],
)

# Registrar el router
app.include_router(router_chats, prefix="/chats", tags=["Chats"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Chat API"}
