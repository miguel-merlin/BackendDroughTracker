import csv
from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from requests import Response

from server.database import (
    retrieve_stations,
    add_station,
    delete_station,
    retrieve_station,
    retrieve_stations_state,
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

#Route to get station by state
@router.get("/stations/{state}")
async def get_stations_state(state):
    stations = await retrieve_stations_state(state)
    if stations:
        return ResponseModel(stations, "Stations by state retrieved succesfully")

#Route to get states



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
        return ResponseModel(station, "Station data retrieved succesfully")
    return ErrorResponseModel("An error ocurred", 404, "Station does not exist")

#Route to get predictions for a station with id
@router.get("/prediction/{id}", response_description="Predictions for station")
async def get_prediction(id: str):
    station = await retrieve_station(id)
    if station:
        dataSet = []
        #Code to read .csv and invoke ANN
        return #Here return prediction
    return ErrorResponseModel("An error ocurred", 404, "Station does not exist")


#Route to update station
@router.put("/{id}")
async def update_station_data(id: str, req: UpdateStationModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_station = await update_station(id, req)
    if updated_station:
        return ResponseModel(
            "Station with ID: {id} has been updated succesfully".format(id),
            "Station updated succesfully"
        )
    return ErrorResponseModel(
        "An error ocurred",
        404,
        "There was an error updating the station with ID: {id}".format(id)
    )

#Route to delete station
@router.delete("/{id}", response_description="Station deleted from the database")
async def delete_station_data(id: str):
    deleted_station = await delete_station(id)
    if deleted_station:
        return ResponseModel(
            "Station with ID: {id} has been deleted".format(id)
        )
    return ErrorResponseModel(
        "An error has ocurred", 404, "Station with ID: {id} does not exist".format(id)
    )