import requests
import uvicorn
from fastapi import FastAPI, Security

from config import get_settings
from utils import VerifyToken

app = FastAPI()
auth = VerifyToken()
settings = get_settings()


@app.get("/api/public")
def public():
    """No access token required to access this route"""
    data = requests.get(url="http://127.0.0.1:8000/api/public")
    result = {
        "status": "success",
        "msg": (
            "Hello from a public endpoint! You don't need to be "
            "authenticated to see this."
        ),
    }
    return result, data


@app.get("/api/private")
def private(auth_result: str = Security(auth.verify)):
    """A valid access token is required to access this route"""
    return auth_result


@app.post("/api/login", status_code=201)
async def login():
    return {'id': 1, 'user_type': "admin"}


@app.post("/api/users")
async def create_user():
    pass


@app.get("/api/users")
async def get_users():
    return {"users": [{"id": 1, "user_type": "admin"}]}


@app.get("/api/users/{user_id}")
async def get_user(user_id: int):
    pass


@app.put("/api/users/{user_id}")
async def update_user(user_id: int):
    pass


@app.delete("/api/users/{user_id}")
async def delete_user(user_id: int):
    pass


if __name__ == "__main__":
    uvicorn.run(app, host=settings.SERVICE_HOST, port=settings.SERVICE_PORT)
