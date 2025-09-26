from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from typing import List

from db.session import SessionLocal
from models.quiosque import Quiosque
from schemas.quiosque import QuiosqueCreate, QuiosqueUpdate, QuiosqueOut, QuiosquePatch


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
        .options(joinedload(Quiosque.quiosque))
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
        .options(joinedload(Quiosque.quiosque))
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

#DELETE
@router.delete("/{quiosque_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quiosque(quiosque_id: int, db: Session = Depends(get_db)):
    quiosque_encontrado = (
        db.query(Quiosque)
        .options(selectinload(Quiosque.quiosques))
        .filter(Quiosque.id == quiosque_id)
        .first()
    )
    if quiosque_encontrado is None:
        raise HTTPException(status_code=404, detail="Quiosque nao registrada")
    db.delete(quiosque_encontrado)
    db.commit()
    return {"message": "Quiosque deletado com sucesso!"}

# PUT
@router.put("/{quiosque_id}", response_model=QuiosqueOut)
def update_quiosque(quiosque_id: int, quiosque: QuiosqueUpdate, db: Session = Depends(get_db)):
    quiosque_db = db.query(Quiosque).filter(Quiosque.id == quiosque_id).first()
    if not quiosque_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Quiosque com id {quiosque_id} não encontrado."
        )
    update_data = quiosque.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(quiosque_db, key, value)

    try:
        db.add(quiosque_db)
        db.commit()
        db.refresh(quiosque_db)
        return quiosque_db
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao atualizar o quiosque. O nome pode já estar em uso por outro quiosque.",
        )

# PATCH
@router.patch("/{quiosque_id}", response_model=QuiosqueOut)
def partial_update_quiosque(quiosque_id: int, quiosque: QuiosquePatch, db: Session = Depends(get_db)):
    quiosque_db = db.query(Quiosque).filter(Quiosque.id == quiosque_id).first()

    if not quiosque_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Quiosque com id {quiosque_id} não encontrado."
        )

    update_data = quiosque.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nenhum campo fornecido para atualização."
        )

    for key, value in update_data.items():
        setattr(quiosque_db, key, value)

    try:
        db.add(quiosque_db)
        db.commit()
        db.refresh(quiosque_db)
        return quiosque_db
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao atualizar o quiosque. O nome pode já estar em uso por outro quiosque.",
        )