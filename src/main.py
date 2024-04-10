import uvicorn
from fastapi import FastAPI, HTTPException, Request, Response, status

from auth import get_password_hash, verify_password
from config import get_settings
from database import SessionLocal, engine
from models import User
from schemas import UserForm, UsernamePasswordForm, UserUpdateForm
from utils import VerifyToken, set_new_id

app = FastAPI()
auth = VerifyToken()
settings = get_settings()
db = SessionLocal()


@app.post("/api/login", status_code=status.HTTP_201_CREATED)
async def login(form_data: UsernamePasswordForm):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user:
        raise HTTPException(
            detail="User with given username not found",
            status_code=status.HTTP_404_NOT_FOUND,
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
    username = db.query(User).filter(User.username == user_form.username).first()
    email = db.query(User).filter(User.email == user_form.email).first()
    if username or email:
        raise HTTPException(
            detail="User for given data already exists",
            status_code=status.HTTP_409_CONFLICT,
        )

    user = User(
        id=set_new_id(db),
        username=user_form.username,
        email=user_form.email,
        user_type=user_form.user_type,
        hashed_password=get_password_hash(user_form.password),
    )

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
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            detail="User with given id not found", status_code=status.HTTP_404_NOT_FOUND
        )

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
    if not user:
        raise HTTPException(
            detail="User with given id not found", status_code=status.HTTP_404_NOT_FOUND
        )

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully."}


if __name__ == "__main__":
    User.metadata.create_all(bind=engine)
    uvicorn.run(app, host=settings.SERVICE_HOST, port=settings.SERVICE_PORT)
