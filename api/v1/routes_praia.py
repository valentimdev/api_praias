from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.exc import IntegrityError
from typing import List, Optional

from auth.deps import get_current_user
from models.user import User


from db.session import SessionLocal
from models.praia import Praia
from schemas.praia import PraiaCreate, PraiaOut, PraiaPatch, PraiaList
from models.quiosque import Quiosque

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# GET GERAL
@router.get("/", response_model=PraiaList)
def get_todas_as_praias(
    skip: int = 0,
    limit: int = 50,
    municipio: Optional[str] = None,
    estado: Optional[str] = None,
    min_rating: Optional[float] = None,
    max_rating: Optional[float] = None,
    tem_quiosque: Optional[bool] = None,
    quiosque: Optional[int] = None,
    tem_salvavida: Optional[bool] = None,
    min_latitude: Optional[float] = None,
    max_latitude: Optional[float] = None,
    min_longitude: Optional[float] = None,
    max_longitude: Optional[float] = None,
    min_comprimento: Optional[int] = None,
    max_comprimento: Optional[int] = None,
    min_largura: Optional[int] = None,
    max_largura: Optional[int] = None,
    propria_banho: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Praia).options(selectinload(Praia.quiosques))

    filtros_igualdade = {
        "municipio": municipio,
        "estado": estado,
        "tem_salvavida": tem_salvavida,
        "propria_banho": propria_banho,
    }
    for attr, value in filtros_igualdade.items():
        if value is not None:
            query = query.filter(getattr(Praia, attr) == value)

    filtros_range = [
        (min_rating, Praia.rating, ">="),
        (max_rating, Praia.rating, "<="),
        (min_latitude, Praia.latitude, ">="),
        (max_latitude, Praia.latitude, "<="),
        (min_longitude, Praia.longitude, ">="),
        (max_longitude, Praia.longitude, "<="),
        (min_comprimento, Praia.comprimento, ">="),
        (max_comprimento, Praia.comprimento, "<="),
        (min_largura, Praia.largura, ">="),
        (max_largura, Praia.largura, "<="),
    ]
    for value, column, op in filtros_range:
        if value is not None:
            if op == ">=":
                query = query.filter(column >= value)
            else:
                query = query.filter(column <= value)

    if tem_quiosque is True:
        query = query.filter(Praia.quiosques.any())
    elif tem_quiosque is False:
        query = query.filter(~Praia.quiosques.any())

    if quiosque:
        query = query.filter(Praia.quiosques.any(Quiosque.id == quiosque))

    praias = query.offset(skip).limit(limit).all()
    return {"praias": praias}


# GET POR ID
@router.get("/{praia_id}", response_model=PraiaOut)
def get_praia_por_id(praia_id: int, db: Session = Depends(get_db)):
    praia_encontrada = (
        db.query(Praia)
        .options(selectinload(Praia.quiosques))
        .filter(Praia.id == praia_id)
        .first()
    )
    if praia_encontrada is None:
        raise HTTPException(status_code=404, detail="Praia nao registrada")
    return praia_encontrada


# POST
@router.post("/", response_model=PraiaOut, status_code=status.HTTP_201_CREATED)
def create_praia(
    praia: PraiaCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        db_praia = Praia(**praia.model_dump())
        db.add(db_praia)
        db.commit()
        db.refresh(db_praia)
        return db_praia
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao criar a praia. Verifique se os dados estão corretos e se o nome não está duplicado.",
        )


# DELETE
@router.delete("/{praia_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_praia(
    praia_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    praia_encontrada = (
        db.query(Praia)
        .options(selectinload(Praia.quiosques))
        .filter(Praia.id == praia_id)
        .first()
    )
    if praia_encontrada is None:
        raise HTTPException(status_code=404, detail="Praia nao registrada")
    db.delete(praia_encontrada)
    db.commit()
    return {"message": "Praia deletada com sucesso!"}


# PUT
@router.put("/{praia_id}", response_model=PraiaOut)
def update_praia(
    praia_id: int,
    praia: PraiaPatch,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    praia_db = db.query(Praia).filter(Praia.id == praia_id).first()
    if not praia_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Praia com id {praia_id} não encontrada.",
        )
    update_data = praia.model_dump()
    for key, value in update_data.items():
        setattr(praia_db, key, value)

    try:
        db.commit()
        db.refresh(praia_db)
        return praia_db
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao atualizar a praia. O nome pode já estar em uso por outra praia.",
        )


# PATCH
@router.patch("/{praia_id}", response_model=PraiaOut)
def partial_update_praia(
    praia_id: int,
    praia: PraiaPatch,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    praia_db = db.query(Praia).filter(Praia.id == praia_id).first()

    if not praia_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Praia com id {praia_id} não encontrada.",
        )

    update_data = praia.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nenhum campo fornecido para atualização.",
        )

    for key, value in update_data.items():
        setattr(praia_db, key, value)

    try:
        db.add(praia_db)
        db.commit()
        db.refresh(praia_db)
        return praia_db
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao atualizar a praia. O nome pode já estar em uso por outra praia.",
        )
