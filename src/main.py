import json
from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = FastAPI()
app.secret_key = env.get("APP_SECRET_KEY")

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)


@app.post("api/login")
async def login():
    return oauth.auth0.authorize_redirect(redirect_uri="callback/")


@app.get("api/callback")  # POST method should be allowed
async def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    pass


@app.post("api/logout")
async def logout():
    pass


@app.delete("api/delete_account/{user_id}")
async def delete_account(user_id: int):
    pass


@app.get("api/")
def home():
    pass
