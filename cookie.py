from fastapi import FastAPI, Cookie

app= FastAPI()

@app.get("/cookie")
def get_cookie(ga: str = Cookie(None)):
    return {"ga": ga}

