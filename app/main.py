from fastapi import FastAPI
from app.database import Base, engine
from app.routes import auth
from app.models.user import User

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "App is Running"}