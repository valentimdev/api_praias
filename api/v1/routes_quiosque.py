from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from typing import List, Optional

from db.session import SessionLocal
from models.quiosque import Quiosque
from schemas.quiosque import QuiosqueCreate, QuiosqueUpdate, QuiosqueOut, QuiosquePatch
from models.praia import Praia


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# GET GERAL
@router.get("/", response_model=List[QuiosqueOut])
def get_todos_os_quiosques(
    skip: int = 0,
    limit: int = 50,
    nome: Optional[str] = None,
    min_nota: Optional[float] = None,
    max_nota: Optional[float] = None,
    tem_acessibilidade: Optional[bool] = None,
    tem_banheiro: Optional[bool] = None,
    praia_id: Optional[int] = None,
    min_valor: Optional[float] = None,
    max_valor: Optional[float] = None,
    min_latitude: Optional[float] = None,
    max_latitude: Optional[float] = None,
    min_longitude: Optional[float] = None,
    max_longitude: Optional[float] = None,
    estado: Optional[str] = None,
    municipio: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Quiosque).join(Praia).options(joinedload(Quiosque.praia))

    eq_filters = {
        "nome": nome,
        "tem_acessibilidade": tem_acessibilidade,
        "tem_banheiro": tem_banheiro,
        "praia_id": praia_id,
    }
    for attr, value in eq_filters.items():
        if value is not None:
            query = query.filter(getattr(Quiosque, attr) == value)

    range_filters = [
        (min_nota, Quiosque.nota, ">="),
        (max_nota, Quiosque.nota, "<="),
        (min_valor, Quiosque.valor, ">="),
        (max_valor, Quiosque.valor, "<="),
        (min_latitude, Quiosque.latitude, ">="),
        (max_latitude, Quiosque.latitude, "<="),
        (min_longitude, Quiosque.longitude, ">="),
        (max_longitude, Quiosque.longitude, "<="),
    ]
    for value, column, op in range_filters:
        if value is not None:
            if op == ">=":
                query = query.filter(column >= value)
            else:
                query = query.filter(column <= value)

    if estado:
        query = query.filter(Praia.estado == estado)
    if municipio:
        query = query.filter(Praia.municipio == municipio)

    quiosques = query.offset(skip).limit(limit).all()
    return quiosques


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


# DELETE
@router.delete("/{quiosque_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quiosque(quiosque_id: int, db: Session = Depends(get_db)):
    quiosque_encontrado = (
        db.query(Quiosque)
        .options(joinedload(Quiosque.praia))
        .filter(Quiosque.id == quiosque_id)
        .first()
    )
    if quiosque_encontrado is None:
        raise HTTPException(status_code=404, detail="Quiosque nao registrado")
    db.delete(quiosque_encontrado)
    db.commit()
    return


# PUT
@router.put("/{quiosque_id}", response_model=QuiosqueOut)
def update_quiosque(
    quiosque_id: int, quiosque: QuiosqueUpdate, db: Session = Depends(get_db)
):
    quiosque_db = db.query(Quiosque).filter(Quiosque.id == quiosque_id).first()
    if not quiosque_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Quiosque com id {quiosque_id} não encontrado.",
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
def partial_update_quiosque(
    quiosque_id: int, quiosque: QuiosquePatch, db: Session = Depends(get_db)
):
    quiosque_db = db.query(Quiosque).filter(Quiosque.id == quiosque_id).first()

    if not quiosque_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Quiosque com id {quiosque_id} não encontrado.",
        )

    update_data = quiosque.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nenhum campo fornecido para atualização.",
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
