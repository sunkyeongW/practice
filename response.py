from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
import uvicorn

app = FastAPI()

class Response(BaseModel):
    name : str
    password : str
    url : Optional[HttpUrl] = None

class Response_G(BaseModel):
    name : str
    url : HttpUrl = "http://naver.com"

class Response_C(Response_G):
    password : str

@app.post("/response/me", response_model=Response)
def response(user: Response):
    return user

@app.post("/create", response_model= Response_G, status_code= 201)
def create(user: Response_C):
    return user




if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)