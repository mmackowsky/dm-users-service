import requests
import uvicorn
from fastapi import FastAPI, Security

from utils import VerifyToken

app = FastAPI()
auth = VerifyToken()


@app.get("/api/public")
def public():
    """No access token required to access this route"""
    data = requests.get(url="http://127.0.0.1:8001/api/public")
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


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8002)
