from motor.motor_asyncio import AsyncIOMotorClient

# Configuración de la conexión
MONGO_URI = "mongodb://root:root@raza-chats-db:27017/chat_app"
# MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "chat_app"

# Crear cliente MongoDB (Motor)
client = AsyncIOMotorClient(MONGO_URI)

# Seleccionar la base de datos
database = client[DATABASE_NAME]

# Exportar las variables
__all__ = ["database", "client"]

