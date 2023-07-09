from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/produtos")
def get_produtos():
    return {"message": "Hello World"}