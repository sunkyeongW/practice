from fastapi import FastAPI
from typing import Optional, List
from pydantic import BaseModel, HttpUrl
import uvicorn

from main import Request

app = FastAPI()

class Item(BaseModel):
    name : str
    price : str
    amount : int = 0

class Request(BaseModel):
    name : str
    password : str
    url : Optional[HttpUrl] = None
    inventory : List[Item] = []

@app.post ("/request")
def request_user(user:Request):
    return user

@app.get ("/request/me")
def me():
    fake_user = Request(
        name = "fast",
        password = "123",
        inventory =[
            Item(name="전설 무기", price=1_000_000),
            Item(name="전설 방어구", price=900_000),
        ]
    )
    return fake_user