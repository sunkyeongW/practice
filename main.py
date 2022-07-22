from dataclasses import Field
from importlib.resources import path
from tkinter import N
from fastapi import FastAPI, status, Query, Path, Cookie, Header
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, HttpUrl, parse_obj_as, Field
import uvicorn

from requests import request

app = FastAPI()

Inventory = (
    {
        "id": 1,
        "user_id" : 1,
        "name" : "레전드포션",
        "price" : 2500.0,
        "amount" : 100,
    },
    {
        "id": 2,
        "user_id" : 1,
        "name" : "포션",
        "price" : 300.0,
        "amount" : 50,
    },
)

class UserLevel(str, Enum):
    a = "a"
    b = "b"
    c = "c"


class Item(BaseModel):
    name : str
    price : float
    amount : int = 0

class Item2(BaseModel):
    name : str = Field(..., min_length=1, max_length=100, title="이름")
    price : float = Field(None, ge=0)
    amount : int = Field(
        default= 1,
        gt = 0,
        le= 100,
        title="수량",
        description="아이템 갯수. 1~100개 까지 소지 가능"
    )


class Request(BaseModel):
    name : str
    password : str
    url : Optional[HttpUrl] = None
    inventory : List[Item] = []

class Response(BaseModel):
    name : str
    password : str
    url : Optional[HttpUrl] = None


class Response_G(BaseModel):
    name : str
    url : HttpUrl = "http://naver.com"

class Response_C(Response_G):
    password : str


@app.get("/")
def hello():
    return "Hello, Python!"

@app.get("/path/{user_id}")
def get_user(user_id):
    return {"Id": user_id}

@app.get("/query")
def query_users(admin: bool, limit: int = None):   #optional[int] = None 같은 의미.
    return {"admin": admin ,"limit": limit}

@app.get("/enum")
def enum(grade: UserLevel = UserLevel.a):  #a를 기본값으로 지정.
    return {"grade": grade}

@app.post("/request")
def request_user(user: Request):
    return user

@app.get("/request/me")
def me():
    fake_user = Request(
        name = "fast",
        password = 123,
        inventory=[
            Item(name="전설 무기", price=1_000_000),
            Item(name="전설 방어구", price=900_000),
        ]
    )
    return fake_user

@app.post("/create", response_model= Response_G, status_code= 201)
def response_c(user: Response_C):
    return user

@app.post("/response/me", response_model=Response)
def response(user: Response):
    return user


@app.get("/data/{user_id}/inventory", response_model=List[Item])
def get_item(
    user_id:int = Path(..., gt=0, title="사용자 ID", description="DB의 User_ID"),
    name:str = Query(None, min_length=1, max_length=2, title="아이템 이름"),
):
    user_items = []
    for item in Inventory:
        if item["user_id"] == user_id:
            user_items.append(item)

    response = []
    for item in user_items:
        if name is None:
            response = user_items
            break
        if item["name"] == name:
            response.append(item)

    return response

@app.post("/field/{user_id}/item")
def create_item(item: Item2):
    return item

@app.get("/cookie")
def get_cookie(ga : str = Cookie(None)):
    return {"ga": ga}

@app.get("/header")
def get_header(x_token: str = Header(None, title="토큰", convert_underscores=True)):
    return { "X-Token": x_token}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)


