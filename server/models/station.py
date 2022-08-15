from lib2to3.pgen2.token import OP
from optparse import Option
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class StationSchema(BaseModel):
    name: str = Field(...)
    fileName: str = Field('default.csv')
    lat: float = Field(37.0902)
    lng: float = Field(95.7129)

    class Config:
        schema_extra = {
            "example": {
                "name": "Cierro Prieto",
                "fileName": "cierroPrieto.csv",
                "lat" : 37.0902,
                "lng" : 95.7129,
            }
        }


class UpdateStationModel(BaseModel):
    name: Optional[str]
    fileName: Optional[str]
    lat: Optional[float]
    lng: Optional[float]

    class Config:
        schema_extra = {
            "example": {
                "name": "Cierro Dorado",
                "fileName" : "cierroDorado.csv",
                "lat" : 37.0902,
                "lng" : 95.7129,
            }
        }


def ResponseModel(data, message): 
    return{
        "data": data,
        "code": 201,
        "message": message,
    }

def ErrorResponseModel(error, code, message):
    return {"error":error, "code":code, "message": message}