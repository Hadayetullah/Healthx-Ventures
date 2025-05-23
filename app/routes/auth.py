from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials 

from app.database import SessionLocal
from app.crud import get_user_by_username
from app.auth.jwt_handler import verify_password, create_access_token, create_refresh_token, decode_access_token, decode_refresh_token, get_password_hash
from app.models import User
from app.schemas.user import UserCreate, RefreshTokenRequest

oauth2_scheme = HTTPBearer()

router = APIRouter(prefix="/auth", tags=["auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}

@router.post("/login")
def login(form_data: UserCreate, db: Session = Depends(get_db)):
    user = get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    return {
        "access_token": access_token, 
        "refresh_token": refresh_token, 
        # "token_type": "bearer"
    }

@router.post("/get-new-access-token")
def refresh_token(data: RefreshTokenRequest, db: Session = Depends(get_db)):
    payload = decode_refresh_token(data.refresh_token)

    user_id = payload.get("sub")
    # print("user_id : ", user_id)
    user = db.query(User).get(int(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_access_token = create_access_token({"sub": str(user.id)})

    return {
        "access_token": new_access_token,
        # "token_type": "bearer"
    }

def get_current_user(token: HTTPAuthorizationCredentials = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # print("payload : ", token)
    payload = decode_access_token(token.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(get_user_by_username.__globals__['models'].User).get(int(payload["sub"]))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user