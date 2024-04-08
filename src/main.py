import requests
import uvicorn
from fastapi import FastAPI, Header, HTTPException, Request, Response, Security, status

from auth import get_password_hash, verify_password
from config import get_settings
from database import Base, SessionLocal, engine
from models import User
from schemas import UserForm, UsernamePasswordForm
from utils import VerifyToken

app = FastAPI()
auth = VerifyToken()
settings = get_settings()
db = SessionLocal()


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


@app.post("/api/login", status_code=status.HTTP_201_CREATED)
async def login(form_data: UsernamePasswordForm):
    user = db.query(User).filter(User.id).first()  # POBRAĆ USERA
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    verify = verify_password(form_data.password, user.hashed_password)
    if not verify:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong password"
        )

    return user


@app.post("/api/users", status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserForm,
    request: Request,
    response: Response,
    request_user_id: str = Header(None),
):
    hashed_password = get_password_hash(user.password)
    data = user.dict()
    db.add(data, hashed_password, request_user_id)
    db.commit()
    db.refresh(data, hashed_password, request_user_id)
    return user


@app.get("/api/users")
async def get_users():
    return {
        "users": [
            {
                "id": 1,
                "user_type": "admin",
                "username": "username",
                "hashed_password": "password",
                "created_by": 2,
            }
        ]
    }


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
    User.metadata.create_all(bind=engine)
    uvicorn.run(app, host=settings.SERVICE_HOST, port=settings.SERVICE_PORT)
