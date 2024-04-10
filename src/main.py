import requests
import uvicorn
from fastapi import FastAPI, Header, HTTPException, Request, Response, Security, status

from auth import get_password_hash, verify_password
from config import get_settings
from database import SessionLocal, engine
from models import User
from schemas import UserForm, UsernamePasswordForm, UserUpdateForm
from utils import VerifyToken, check_user_exists

app = FastAPI()
auth = VerifyToken()
settings = get_settings()
db = SessionLocal()


@app.post("/api/login", status_code=status.HTTP_201_CREATED)
async def login(form_data: UsernamePasswordForm):
    user = check_user_exists(
        db=db, db_value=User.username, input_value=form_data.username
    )
    # user = db.query(User).filter(User.username == form_data.username).first()
    # if not user:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    verify = verify_password(form_data.password, user.hashed_password)
    if not verify:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong password"
        )

    return user


@app.post("/api/users", status_code=status.HTTP_201_CREATED)
async def create_user(
    user_form: UserForm,
    request: Request,
    response: Response,
    request_user_id: str = Header(None),
):
    check_user_exists(db=db, db_value=User.username, input_value=user_form.username)

    user = User(
        id=request_user_id,
        username=user_form.username,
        email=user_form.email,
        user_type=user_form.user_type,
        hashed_password=get_password_hash(user_form.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.get("/api/users")
async def get_users():
    return db.query(User).all()


@app.get("/api/users/{user_id}")
async def get_user_by_id(user_id: int):
    check_user_exists(db=db, db_value=User.id, input_value=user_id)
    return db.query(User).filter(User.id == user_id).first()


@app.put("/api/users/{user_id}")
async def update_user(user_id: int, update_form: UserUpdateForm):
    user = check_user_exists(db=db, db_value=User.id, input_value=user_id)

    user.username = update_form.username
    user.email = update_form.email
    user.user_type = update_form.user_type
    user.hashed_password = get_password_hash(update_form.password)

    db.commit()
    db.refresh(user)
    return user


@app.delete("/api/users/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: int):
    user = check_user_exists(db=db, db_value=User, input_value=user_id)
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully."}


if __name__ == "__main__":
    User.metadata.create_all(bind=engine)
    uvicorn.run(app, host=settings.SERVICE_HOST, port=settings.SERVICE_PORT)
