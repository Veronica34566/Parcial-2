from pydantic import BaseModel, Field
from typing import Optional, List

class VaccinationRecord(BaseModel):
    country: str = Field(example="PAN")
    indicator: str = Field(example="SH.IMM.MEAS")
    year: int = Field(example=2001)
    value: Optional[float] = Field(None, ge=0, le=100, description="% cobertura")

class VaccinationList(BaseModel):
    count: int
    data: List[VaccinationRecord]

class ProvinceRecord(BaseModel):
    province: str
    year: int
    value: Optional[float] = Field(None, ge=0, le=100)
    simulated: bool = True
    base_country_value: Optional[float] = Field(None, ge=0, le=100)
