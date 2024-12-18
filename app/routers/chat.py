from fastapi import APIRouter, HTTPException
from app.db.connection import db
from datetime import datetime

router_chats = APIRouter(prefix="/chats")

@router_chats.get("/") 
def read_root(): 
    return {"message": "Hello, FastAPI with Docker!"}



@router_chats.get("/all")
async def get_chats():
    if db is None:
        raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")

    try:
        collection = db["chats"]
        
        query = {}

        results = list(collection.find(query, {"_id": 0}))
        return {"data": results, "count": len(results)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


@router_chats.get("/{pet1}/{pet2}")
async def get_chat_by_value_in_array(pet1: int, pet2: int):
    if db is None:
        raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")

    try:
        collection = db["chats"] 

        query_filter = {"pets": {"$all": [pet1, pet2]}}

        # Realizar la consulta
        results = list(collection.find(query_filter, {"_id": 0}))

        if not results:
            raise HTTPException(status_code=404, detail="No se encontraron resultados")

        return {"data": results, "count": len(results)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router_chats.post("/save-message")
async def save_message(pets: list[int], pet_id: int, message: str):
    if db is None:
        raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")

    if len(pets) != 2:
        raise HTTPException(status_code=400, detail="El campo 'pets' debe contener exactamente 2 IDs")

    try:
        # Nombre de la colección
        collection = db["chats"]

        # Buscar el documento correspondiente al par de `pets`
        chat = collection.find_one({"pets": {"$all": pets}})

        # Crear un nuevo mensaje
        new_message = {
            "pet_id": pet_id,
            "message": message,
            "timestamp": datetime.utcnow()
        }

        if chat:
            # Si el documento ya existe, actualizar el arreglo de mensajes
            collection.update_one(
                {"_id": chat["_id"]},
                {"$push": {"messages": new_message}}
            )
        else:
            # Si no existe, crear un nuevo documento
            new_chat = {
                "pets": pets,
                "messages": [new_message]
            }
            collection.insert_one(new_chat)

        return {"message": "Mensaje guardado exitosamente"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
