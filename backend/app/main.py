from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .routes.players import router as players_router
from .db.database import create_db_and_tables

# Ready for app startup: creation of db & tables
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

# App startup
app = FastAPI(lifespan=lifespan)

# Serving images
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Providing the api to be accessed
app.include_router(players_router)

# CORS Middleware to allow frontend access to api
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"]
)

