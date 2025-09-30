from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from enum import Enum


class Estado(str, Enum):
    AC = "AC"
    AL = "AL"
    AP = "AP"
    AM = "AM"
    BA = "BA"
    CE = "CE"
    DF = "DF"
    ES = "ES"
    GO = "GO"
    MA = "MA"
    MT = "MT"
    MS = "MS"
    MG = "MG"
    PA = "PA"
    PB = "PB"
    PR = "PR"
    PE = "PE"
    PI = "PI"
    RJ = "RJ"
    RN = "RN"
    RS = "RS"
    RO = "RO"
    RR = "RR"
    SC = "SC"
    SP = "SP"
    SE = "SE"
    TO = "TO"


class PraiaBase(BaseModel):
    nome: str
    estado: Estado
    municipio: str
    latitude: float = Field(..., ge=-90, le=90)  # validação: -90 <= lat <= 90
    longitude: float = Field(..., ge=-180, le=180)  # validação: -180 <= lon <= 180
    comprimento: Optional[int] = None
    largura: Optional[int] = None
    propria_banho: Optional[bool] = True
    tem_salvavida: Optional[bool] = False
    rating: Optional[float] = Field(None, ge=0, le=5)  # rating 0–5


class PraiaCreate(PraiaBase):
    pass


class PraiaPatch(BaseModel):
    nome: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    estado: Optional[Estado] = None
    municipio: Optional[str] = None
    comprimento: Optional[int] = None
    largura: Optional[int] = None
    propria_banho: Optional[bool] = None
    tem_salvavida: Optional[bool] = None
    rating: Optional[float] = None


class PraiaInfo(PraiaBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


from schemas.quiosque import QuiosqueInfo


class PraiaOut(PraiaBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
    quiosques: List[QuiosqueInfo] = []


class PraiaList(BaseModel):
    praias: List[PraiaOut] = []
