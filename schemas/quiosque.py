from pydantic import BaseModel, Field
from typing import Optional, List


class QuiosqueBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    nota: Optional[float] = Field(None, ge=-180, le=180)
    latitude: float = Field(..., ge=-90, le=90)  # validação: -90 <= lat <= 90
    longitude: float = Field(..., ge=-180, le=180)  # validação: -180 <= lon <= 180
    tem_acessibilidade: Optional[bool] = None
    tem_banheiro: Optional[bool] = None
    valor: Optional[int] = Field(None, ge=0, le=5)
    ocupacao_maxima: Optional[int] = None
    praia_id: int


class QuiosqueCreate(QuiosqueBase):
    pass


class QuiosqueUpdate(BaseModel):
    nome: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    descricao: Optional[str] = None
    nota: Optional[float] = Field(None, ge=-180, le=180)
    tem_acessibilidade: Optional[bool] = None
    tem_banheiro: Optional[bool] = None
    valor: Optional[int] = Field(None, ge=0, le=5)
    ocupacao_maxima: Optional[int] = None
    praia_id: Optional[int] = None


class QuiosquePatch(BaseModel):
    nome: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    descricao: Optional[str] = None
    nota: Optional[float] = None
    tem_acessibilidade: Optional[bool] = None
    tem_banheiro: Optional[bool] = None
    valor: Optional[int] = None
    ocupacao_maxima: Optional[int] = None
    praia_id: Optional[int] = None


class QuiosqueInfo(QuiosqueBase):
    id: int

    class Config:
        orm_mode = True


from schemas.praia import PraiaInfo


class QuiosqueOut(QuiosqueBase):
    id: int
    praia: PraiaInfo

    class Config:
        orm_mode = True


class QuiosqueList(BaseModel):
    quiosques: List[QuiosqueOut] = []
