from fastapi import FastAPI
from server.routes.station import router as StationRouter

app = FastAPI()

app.include_router(StationRouter, tags=["Station"], prefix="/station")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to DroughTracker"}