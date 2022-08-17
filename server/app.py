from fastapi import FastAPI
from server.routes.station import router as StationRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(StationRouter, tags=["Station"], prefix="/station")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to DroughTracker"}