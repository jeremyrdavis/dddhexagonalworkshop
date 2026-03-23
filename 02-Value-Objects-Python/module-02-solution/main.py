from contextlib import asynccontextmanager

from fastapi import FastAPI

from conference.attendees.infrastructure.endpoint import router
from conference.attendees.persistence.address_entity import AddressEntity  # noqa: F401
from conference.attendees.persistence.entity import AttendeeEntity  # noqa: F401
from database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup (equivalent to Quarkus drop-and-create)
    target_engine = getattr(app.state, "engine", engine)
    Base.metadata.create_all(bind=target_engine)
    yield


app = FastAPI(title="DDD Hexagonal Workshop - Attendees", lifespan=lifespan)
app.include_router(router)
