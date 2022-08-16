from array import array
from lib2to3.pgen2.token import OP
from optparse import Option
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class StationSchema(BaseModel):
    name: str = Field(...)
    lat: float = Field(37.0902)
    lng: float = Field(95.7129)
    dataSet: list = Field([])
    numStation: int = Field(1000)

    class Config:
        schema_extra = {
            "example": {
                "name": "Cierro Prieto",
                "lat" : 37.0902,
                "lng" : 95.7129,
                "dataSet" : [1,2,3,4],
                "numStation" : 1000
            }
        }


class UpdateStationModel(BaseModel):
    name: Optional[str]
    lat: Optional[float]
    lng: Optional[float]
    dataSet: Optional[list]
    numStation: Optional[int]  

    class Config:
        schema_extra = {
            "example": {
                "name": "Cierro Dorado",
                "lat" : 37.0902,
                "lng" : 95.7129,
                "dataSet" : [1,2,3,4],
                "numStation" : 1000,
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