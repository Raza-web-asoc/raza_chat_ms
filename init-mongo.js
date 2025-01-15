db = db.getSiblingDB("chat_app");

db.createUser({
    user: "root",
    pwd: "root",
    roles: [{ role: "readWrite", db: "chat_app" }]
});

db.test_collection.insertOne({ message: "Base de datos inicializada correctamente." });
