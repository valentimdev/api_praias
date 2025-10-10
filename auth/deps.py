from fastapi import Depends, HTTPException, status, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from .jwt_handler import decode_token
from db.session import SessionLocal
from models.user import User


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = HTTPBearer(auto_error=False)


def token_extractor(
    security_data: HTTPAuthorizationCredentials = Security(oauth2_scheme),
) -> str:
    if security_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais de autenticação não fornecidas.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return security_data.credentials


def get_current_user(
    token: str = Depends(token_extractor), db: Session = Depends(get_db)
) -> User:
    payload = decode_token(token)

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido: ID de usuário ausente (sub).",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(User).filter(User.id == int(user_id)).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário do token não encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
