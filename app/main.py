from fastapi import FastAPI
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "App Running"}