from fastapi import FastAPI, Header

app = FastAPI()

@app.get("/header")
def get_headers(x_token: str = Header(None, title="토큰", convert_underscores=True)):
    return {"X-Token": x_token}