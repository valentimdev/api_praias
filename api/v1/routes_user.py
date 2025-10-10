from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.session import SessionLocal
from schemas.user import UserCreate, UserOut, Token, UserLogin, RefreshTokenRequest
from models.user import User
from auth.cryptography import verify_password
from auth.deps import get_current_user
from auth.jwt_handler import create_access_and_refresh_tokens, decode_token

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/login", response_model=Token)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    username = user_credentials.username
    user = db.query(User).filter(User.username == username).first()

    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    tokens = create_access_and_refresh_tokens(user.id)

    user.refresh_token_hash = tokens["refresh_token"]
    db.commit()

    token = Token(
        access_token=tokens["access_token"],
        token_type="bearer",
        refresh_token=tokens["refresh_token"],
    )
    return token


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user_credentials: UserCreate, db: Session = Depends(get_db)):
    username = user_credentials.username
    user = db.query(User).filter(User.username == username).first()
    if user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(**user_credentials.model_dump())
    db.add(new_user)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Could not create user")

    db.refresh(new_user)
    return new_user


@router.get("/me", response_model=UserOut)
def read_user(
    current_user: User = Depends(get_current_user),
):
    return current_user


@router.post("/refresh", response_model=Token)
def refresh_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    token_str = request.refresh_token
    try:
        payload = decode_token(token_str)
    except HTTPException:
        raise HTTPException(
            status_code=401, detail="Refresh token inválido ou expirado"
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Payload do token inválido")

    user = db.query(User).filter(User.id == int(user_id)).first()

    if not user or user.refresh_token_hash != token_str:
        raise HTTPException(
            status_code=401, detail="Refresh token revogado ou inválido"
        )

    new_tokens = create_access_and_refresh_tokens(user.id)

    user.refresh_token_hash = new_tokens["refresh_token"]
    db.commit()

    new_token = Token(
        access_token=new_tokens["access_token"],
        token_type="bearer",
        refresh_token=new_tokens["refresh_token"],
    )
    return new_token
