from lib2to3.pgen2.token import OP
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class StationSchema(BaseModel):
    name: str = Field(...)
    fileName: str = Field('default.csv')

    class Config:
        schema_extra = {
            "example": {
                "name": "Cierro Prieto",
                "fileName": "cierroPrieto.csv"
            }
        }


class UpdateStationModel(BaseModel):
    name: Optional[str]
    fileName: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "name": "Cierro Dorado",
                "fileName" : "cierroDorado.csv"
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