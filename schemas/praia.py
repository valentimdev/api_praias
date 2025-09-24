from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class PraiaBase(BaseModel):
    nome: str
    estado: str
    municipio: str
    latitude: float = Field(..., ge=-90, le=90)  # validação: -90 <= lat <= 90
    longitude: float = Field(..., ge=-180, le=180)  # validação: -180 <= lon <= 180
    comprimento: Optional[int] = None
    largura: Optional[int] = None
    propria_banho: Optional[bool] = True
    tem_quiosque: Optional[bool] = False
    tem_salvavida: Optional[bool] = False
    rating: Optional[float] = Field(None, ge=0, le=5)  # rating 0–5


class PraiaCreate(PraiaBase):
    pass


class PraiaUpdate(BaseModel):
    nome: Optional[str] = None
    estado: Optional[str] = None
    municipio: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    comprimento: Optional[int] = None
    largura: Optional[int] = None
    propria_banho: Optional[bool] = None
    tem_quiosque: Optional[bool] = None
    tem_salvavida: Optional[bool] = None
    rating: Optional[float] = Field(None, ge=0, le=5)


class PraiaOut(PraiaBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
