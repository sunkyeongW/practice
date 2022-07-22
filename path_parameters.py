from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/path/{user_id}")
def path(user_id):
    return {"ID", user_id}


if __name__ == "__main__":
    uvicorn.run(app)