from datetime import datetime
from fastapi import HTTPException
from app.db import database  # Importar la conexión desde el módulo `db`
from app.models import MessageRequest

# Obtener la colección "chats"
collection = database["chats"]

# Función para obtener todos los chats (esto posiblemente nunca se use pero aja)
async def get_all_chats():
    try:
        cursor = collection.find({}, {"_id": 0}) 
        results = await cursor.to_list(length=100) 
        return {"data": results, "count": len(results)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


# Función para obtener un chat específico
async def get_chat(pets: list[int]):
    if len(pets) != 2:
        raise HTTPException(status_code=400, detail="El campo 'pets' debe contener exactamente 2 IDs")
    
    if pets[0] < 0 or pets[1] < 0:
        raise HTTPException(status_code=400, detail="Las ids de las mascotas son positivas")

    try:
        chat = await collection.find_one({"pets": {"$all": pets}})
        if chat:
            return chat["messages"]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# Función para agregar un mensaje a un chat
async def save_message(request: MessageRequest):
    pets = request.pets
    pet_id = request.pet_id
    message = request.message

    if len(pets) != 2:
        raise HTTPException(status_code=400, detail="El campo 'pets' debe contener exactamente 2 IDs")
    
    if pets[0] < 0 or pets[1] < 0:
        raise HTTPException(status_code=400, detail="Las ids de las mascotas son positivas")
    
    if pet_id not in pets:
        raise HTTPException(status_code=400, detail="La id de la mascota que envio el mensaje no hace parte del chat")

    try:
        chat = await collection.find_one({"pets": {"$all": pets}})
        message_id = await last_id(pets)

        new_message = {
            "message_id": message_id,
            "pet_id": pet_id,
            "message": message,
            "timestamp": datetime.utcnow()
        }

        if chat:
            await collection.update_one(
                {"_id": chat["_id"]},
                {"$push": {"messages": new_message}}
            )
            return {"message": "Mensaje guardado exitosamente"}
        else:
            raise HTTPException(status_code=400, detail="El chat entre estas dos mascotas aún no existe")     

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# Función para crear un nuevo chat entre dos mascotas
async def new_chat(pets: list[int]):
    if len(pets) != 2:
        raise HTTPException(status_code=400, detail="El campo 'pets' debe contener exactamente 2 IDs")
    
    if pets[0] < 0 or pets[1] < 0:
        raise HTTPException(status_code=400, detail="Las ids de las mascotas son positivas")
    
    try:
        chat = await collection.find_one({"pets": {"$all": pets}})
        if chat:
            raise HTTPException(status_code=400, detail="Ya existe un chat entre estas dos mascotas")
        
        pets_chat = {"pets": pets, "messages": []}
        await collection.insert_one(pets_chat)
        return {"message": "Chat creado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


# Función que retorna la última id de mensaje enviado para un chat
async def last_id(pets: list[int]):
    if len(pets) != 2:
        raise HTTPException(status_code=400, detail="El campo 'pets' debe contener exactamente 2 IDs")
    
    if pets[0] < 0 or pets[1] < 0:
        raise HTTPException(status_code=400, detail="Las ids de las mascotas son positivas")
    
    try:
        chat = await collection.find_one({"pets": {"$all": pets}})
        if chat:
            if len(chat["messages"]) > 0:
                max_message_id = max(message["message_id"] for message in chat["messages"])
                return max_message_id + 1
            else:
                return 0
        else:
            raise HTTPException(status_code=400, detail="El chat entre estas dos mascotas aún no existe")
    except:
        raise HTTPException(status_code=500, detail=str(e))




# Funcion para obtener todas las ids de mascotas con las que una mascota tiene chats disponibles
async def chats_available(pet_id: int):
    if pet_id < 0:
        raise HTTPException(status_code=400, detail="Las ids de las mascotas son positivas")
    
    try:
        cursor = collection.find({"pets": {"$all": [pet_id]}})
        chats = await cursor.to_list()
        if len(chats) > 0:
            pets_ids = []
            for chat in chats:
                if chat["pets"][0] == pet_id:
                    pets_ids.append(chat["pets"][1])
                else:
                    pets_ids.append(chat["pets"][0])
            return pets_ids
        
        else:
            return chats
    except:
        raise HTTPException(status_code=500, detail=str(e))    
    