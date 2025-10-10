import time
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer
from typing import Dict

bearer_scheme = HTTPBearer()

SECRET_KEY = "SEGREDO_SUPER_SECRETO_TROQUE_ISSO"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


def create_token(data: dict, token_type: str) -> str:
    to_encode = data.copy()

    if token_type == "access":
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    elif token_type == "refresh":
        expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    else:
        raise ValueError("Invalid token type")

    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_access_and_refresh_tokens(user_id: int) -> Dict[str, str]:
    data = {"sub": str(user_id)}

    access_token = create_token(data, "access")
    refresh_token = create_token(data, "refresh")

    return {"access_token": access_token, "refresh_token": refresh_token}


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        )

