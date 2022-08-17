from array import array
import motor.motor_asyncio
import os
from dotenv import load_dotenv
from bson.objectid import ObjectId

load_dotenv()

MONGO_DETAILS = os.getenv('MONGO_URI')
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client.DroughTracker
station_collection = database.get_collection("stations")


# helpers

def station_helper(station) -> dict:
    return {
        "id": str(station["_id"]),
        "name": str(station["name"]),
        "lat": float(station["lat"]),
        "lng": float(station["lng"]),
        "stationNumber": int(station["stationNumber"]),
        "state" : str(station["state"]),
        "beginning" : str(station["beginning"]),
        "dataSet" : list(station["dataSet"]),
    }

# Retrieve all stations
async def retrieve_stations():
    stations = []
    async for station in station_collection.find():
        stations.append(station_helper(station))
    return stations

#Retrieve all stations by state
async def retrieve_stations_state(state: str) -> dict:
    stations = []
    async for station in station_collection.find({"state": state}):
        stations.append(station_helper(station))
    return stations

#Get states
async def retrieve_states():
    states = []
    async for station in station_collection.find():
        states.append(station_helper(station)["state"])
    states = list(dict.fromkeys(states))
    return states

# Add a station
async def add_station(station_data: dict) -> dict:
    station = await station_collection.insert_one(station_data)
    new_station = await station_collection.find_one({"_id": station.inserted_id})
    return station_helper(new_station)

# Retrieve a station by ID
async def retrieve_station(id: str) -> dict:
    station = await station_collection.find_one({"_id": ObjectId(id)})
    if station:
        return station_helper(station)

# Update a station with ID
async def update_station(id: str, data: dict) -> dict:
    if len(data) < 1:
        return False
    station = await station_collection.find_one({"_id": ObjectId(id)})
    if station:
        updated_station = await station_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data},
        )
        if updated_station:
            return True
        return False

# Delete station with ID
async def delete_station(id: str):
    station = await station_collection.find_one({"_id": ObjectId(id)})
    if station:
        await station_collection.delete_one({"_id": ObjectId(id)})
        return True