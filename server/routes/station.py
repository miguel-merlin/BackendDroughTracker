from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from requests import Response

from server.database import (
    retrieve_stations,
    add_station,
    delete_station,
    retrieve_station,
    update_station,
)

from server.models.station import (
    ErrorResponseModel,
    ResponseModel,
    StationSchema,
    UpdateStationModel,
)

router = APIRouter()

#Route to add station
@router.post("/", response_description="Station added to the database")
async def add_station_data(station: StationSchema = Body(...)):
    station = jsonable_encoder(station)
    new_station = await add_station(station)
    return ResponseModel(new_station, "Station added succesfuly.")

#Route to get all stations
@router.get("/", response_description="Stations retrieved")
async def get_stations():
    stations = await retrieve_stations()
    if stations:
        return ResponseModel(stations, "Stations retrieved succesfully")
    return ResponseModel(stations, "Empty list returned")

#Route to get a station with id
@router.get("/{id}", response_description="Station data retrieved")
async def get_station_data(id):
    station = await retrieve_station(id)
    if station:
        return ResponseModel(station, "Student data retrieved succesfully")
    return ErrorResponseModel("An error ocurred", 404, "Station does not exist")

#Route to update station
@router.put("/{id}")
async def update_student_data(id: str, req: UpdateStationModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_station = await update_station(id, req)
    if updated_station:
        return ResponseModel(
            "Student with ID: {id} has been updated succesfully".format(id),
            "Student updated succesfully"
        )
    return ErrorResponseModel(
        "An error ocurred",
        404,
        "There was an error updating the station with ID: {id}".format(id)
    )

#Route to delete station
@router.delete("/{id}", response_description="Student deleted from the database")
async def delete_station_data(id: str):
    deleted_student = await delete_station(id)
    if deleted_student:
        return ResponseModel(
            "Student with ID: {id} has been deleted".format(id)
        )
    return ErrorResponseModel(
        "An error has ocurred", 404, "Student with ID: {id} does not exist".format(id)
    )