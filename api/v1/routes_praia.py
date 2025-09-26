from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.exc import IntegrityError
from typing import List

from db.session import SessionLocal
from models.praia import Praia
from schemas.praia import PraiaCreate, PraiaUpdate, PraiaOut, PraiaPatch

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# GET GERAL
@router.get("/", response_model=List[PraiaOut])
def get_todas_as_praias(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    praias = (
        db.query(Praia)
        .offset(skip)
        .options(selectinload(Praia.quiosques))
        .limit(limit)
        .all()
    )
    return praias


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
def create_praia(praia: PraiaCreate, db: Session = Depends(get_db)):
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

#DELETE
@router.delete("/{praia_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_praia(praia_id: int, db: Session = Depends(get_db)):
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
def update_praia(praia_id: int, praia: PraiaUpdate, db: Session = Depends(get_db)):
    praia_db = db.query(Praia).filter(Praia.id == praia_id).first()
    if not praia_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Praia com id {praia_id} não encontrada."
        )
    update_data = praia.model_dump(exclude_unset=True)
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

# PATCH
@router.patch("/{praia_id}", response_model=PraiaOut)
def partial_update_praia(praia_id: int, praia: PraiaPatch, db: Session = Depends(get_db)):
    praia_db = db.query(Praia).filter(Praia.id == praia_id).first()

    if not praia_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Praia com id {praia_id} não encontrada."
        )

    update_data = praia.model_dump(exclude_unset=True)
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nenhum campo fornecido para atualização."
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