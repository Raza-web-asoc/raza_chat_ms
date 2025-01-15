# chat
This module is focused on chat functionality

# clone
git clone ...
pip install -r requirements.txt

# commands for docker
docker network create autenticador_network

docker-compose up --build
docker-compose down
docker volume rm raza_chat_ms_mongo_data

docker-compose logs

docker-compose logs raza-chats-ms
docker-compose logs raza-chats-db