from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from typing import List

from db.session import SessionLocal
from models.quiosque import Quiosque
from schemas.quiosque import QuiosqueCreate, QuiosqueUpdate, QuiosqueOut

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# GET GERAL
@router.get("/", response_model=List[QuiosqueOut])
def get_todos_os_quiosque(
    skip: int = 0, limit: int = 50, db: Session = Depends(get_db)
):
    quiosque = (
        db.query(Quiosque)
        .offset(skip)
        .options(joinedload(Quiosque.praia))
        .limit(limit)
        .all()
    )
    return quiosque


# GET POR ID
@router.get("/{quiosque_id}", response_model=QuiosqueOut)
def get_quiosque_por_id(quiosque_id: int, db: Session = Depends(get_db)):
    quiosque_encontrada = (
        db.query(Quiosque)
        .filter(Quiosque.id == quiosque_id)
        .options(joinedload(Quiosque.praia))
        .first()
    )
    if quiosque_encontrada is None:
        raise HTTPException(status_code=404, detail="Quiosque nao registrado")
    return quiosque_encontrada


# POST
@router.post("/", response_model=QuiosqueOut, status_code=status.HTTP_201_CREATED)
def create_quiosque(quiosque: QuiosqueCreate, db: Session = Depends(get_db)):
    try:
        db_quiosque = Quiosque(**quiosque.model_dump())
        db.add(db_quiosque)
        db.commit()
        db.refresh(db_quiosque)
        return db_quiosque
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao criar o quiosque. Verifique se os dados estão corretos e se o nome não está duplicado.",
        )
