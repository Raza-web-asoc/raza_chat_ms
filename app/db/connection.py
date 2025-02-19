import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

MONGO_URI = os.environ.get("MONGODB_URI")  # Obtiene la URI de la variable de entorno
DATABASE_NAME = "chat_app"

try:
    client = AsyncIOMotorClient(MONGO_URI)
    database = client[DATABASE_NAME]
    print("Conexión a MongoDB Atlas establecida.")
except Exception as e:
    print(f"Error al conectar a MongoDB Atlas: {e}")
    # Maneja el error de conexión (por ejemplo, sal del programa)

__all__ = ["database", "client"]