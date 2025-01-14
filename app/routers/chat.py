from fastapi import APIRouter, HTTPException
from app.controllers.chat_controller import get_all_chats, save_message, get_chat, new_chat, chats_available  # Importar las funciones del controlador
from app.models import MessageRequest

router_chats = APIRouter()

@router_chats.get("/all")
async def read_all_chats():
    return await get_all_chats()

@router_chats.post("/save-message")
async def create_message(request: MessageRequest):
    return await save_message(request)

@router_chats.get("/get-chat/{pet_id1}/{pet_id2}")
async def read_chat(pet_id1: int, pet_id2: int):    
    pets = [pet_id1, pet_id2]
    return await get_chat(pets)

@router_chats.post("/create-chat/{pet_id1}/{pet_id2}")
async def create_chat(pet_id1: int, pet_id2: int):
    pets = [pet_id1, pet_id2]
    return await new_chat(pets)

@router_chats.get("/get-available-chats/{pet_id}")
async def read_all_pet_chats(pet_id: int):
    return await chats_available(pet_id)