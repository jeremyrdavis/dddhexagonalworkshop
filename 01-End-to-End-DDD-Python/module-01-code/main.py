from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup (equivalent to Quarkus drop-and-create)
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="DDD Hexagonal Workshop - Attendees", lifespan=lifespan)

# TODO: Include the attendee router once implemented
# from conference.attendees.infrastructure.endpoint import router
# app.include_router(router)
