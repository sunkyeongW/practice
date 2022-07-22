from fastapi import FastAPI
from enum import Enum
import uvicorn

class UserLevel(str, Enum):
    a = "a"
    b = "b"
    c = "c"


app = FastAPI()

@app.get("/enum")
def enum(grade: UserLevel= UserLevel.a):
    return {"grade": grade}




@app.get("/query")
def query_users(limit: int):
    return {"limit": limit}



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
