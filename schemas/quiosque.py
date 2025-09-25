from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class QuiosqueBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    praia: Optional[float] = Field(None, ge=-90, le=90)
    nota: Optional[float] = Field(None, ge=-180, le=180)
    tem_acessibilidade: Optional[bool] = None
    tem_banheiro: Optional[bool] = None
    valor: Optional[int] = Field(None, ge=0, le=5)
    ocupacao_maxima: Optional[int] = None


class QuiosqueCreate(QuiosqueBase):
    pass


class QuiosqueUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    praia: Optional[float] = Field(None, ge=-90, le=90)
    nota: Optional[float] = Field(None, ge=-180, le=180)
    tem_acessibilidade: Optional[bool] = None
    tem_banheiro: Optional[bool] = None
    valor: Optional[int] = Field(None, ge=0, le=5)
    ocupacao_maxima: Optional[int] = None


class QuiosqueOut(QuiosqueBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
