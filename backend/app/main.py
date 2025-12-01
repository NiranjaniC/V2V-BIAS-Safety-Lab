from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "V2V Bias Safety Lab API is running "}
