from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from redis_client import redis_client
from fastapi.responses import HTMLResponse
import json
import time

app = FastAPI()

# Pydantic model
class User(BaseModel):
    id: int
    name: str

# Fake DB
FAKE_DB = {
    1: {"id": 1, "name": "Netika"},
    2: {"id": 2, "name": "Aryan"}
}

CACHE_EXPIRE = 60  # in seconds

# ✅ ROOT ROUTE — THIS SHOWS HTML
@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
        <head>
            <title>Welcome Netika</title>
        </head>
        <body style="font-family: Arial; padding: 20px;">
            <h2>👋 Welcome Netika!</h2>
            <p><a href="/users" target="_blank">📄 View Cached Users</a></p>
            <p><strong>PUT</strong>: /users/{id} — to update a user</p>
            <p><strong>POST</strong>: /users — to add new user</p>
            <br>
            <a href="/docs" style="
                font-size: 18px;
                color: white;
                background: #4CAF50;
                padding: 10px 15px;
                text-decoration: none;
                border-radius: 5px;
            ">Open Swagger Docs 🚀</a>
        </body>
    </html>
    """

# ✅ GET USERS with Redis cache
@app.get("/users")
def get_users():
    start = time.time()
    cached = redis_client.get("all_users")

    if cached:
        users = json.loads(cached)
        return {"source": "cache", "data": users, "time": time.time() - start}

    users = list(FAKE_DB.values())
    redis_client.setex("all_users", CACHE_EXPIRE, json.dumps(users))
    return {"source": "db", "data": users, "time": time.time() - start}

# ✅ UPDATE USER
@app.put("/users/{user_id}")
def update_user(user_id: int, name: str):
    if user_id not in FAKE_DB:
        raise HTTPException(status_code=404, detail="User not found")

    FAKE_DB[user_id]["name"] = name
    redis_client.delete("all_users")
    return {"msg": "User updated", "user": FAKE_DB[user_id]}

# ✅ ADD USER
@app.post("/users")
def create_user(user: User = Body(...)):
    if user.id in FAKE_DB:
        raise HTTPException(status_code=400, detail="User already exists")

    FAKE_DB[user.id] = {"id": user.id, "name": user.name}
    redis_client.delete("all_users")
    return {"msg": "User added", "user": FAKE_DB[user.id]}

