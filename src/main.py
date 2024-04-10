import requests
import uvicorn
from fastapi import FastAPI, Header, HTTPException, Request, Response, Security, status

from auth import get_password_hash, verify_password
from config import get_settings
from database import SessionLocal, engine
from models import User
from schemas import UserForm, UsernamePasswordForm, UserUpdateForm
from utils import VerifyToken, check_user_exists, set_new_id

app = FastAPI()
auth = VerifyToken()
settings = get_settings()
db = SessionLocal()


@app.post("/api/login", status_code=status.HTTP_201_CREATED)
async def login(form_data: UsernamePasswordForm):
    user = check_user_exists(
        db=db, db_value=User.username, input_value=form_data.username
    )

    verify = verify_password(form_data.password, user.hashed_password)
    if not verify:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong password"
        )

    return user


@app.post("/api/users", status_code=status.HTTP_201_CREATED)
async def register(
    user_form: UserForm,
    request: Request,
    response: Response,
):
    check_user_exists(db=db, db_value=User.username, input_value=user_form.username)
    user = User(
        id=set_new_id(db),
        username=user_form.username,
        email=user_form.email,
        user_type=user_form.user_type,
        hashed_password=get_password_hash(user_form.password),
    )
    print(user)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user_form


@app.get("/api/users", status_code=status.HTTP_200_OK)
async def get_users():
    return db.query(User).all()


@app.get("/api/users/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: int):
    return db.query(User).filter(User.id == user_id).first()


@app.put("/api/users/{user_id}", status_code=status.HTTP_201_CREATED)
async def update_user(user_id: int, update_form: UserUpdateForm):
    user = check_user_exists(db=db, db_value=User.id, input_value=user_id)

    user.username = update_form.username
    user.email = update_form.email
    user.user_type = update_form.user_type
    user.full_name = update_form.full_name

    db.commit()
    db.refresh(user)
    return user


@app.delete("/api/users/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully."}


if __name__ == "__main__":
    User.metadata.create_all(bind=engine)
    uvicorn.run(app, host=settings.SERVICE_HOST, port=settings.SERVICE_PORT)
