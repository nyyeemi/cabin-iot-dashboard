from datetime import datetime
import uuid
from sqlmodel import Field, SQLModel


class TelemetryBase(SQLModel):
    device_id: uuid.UUID
    ts: datetime
    temp: float


class TelemetryCreate(TelemetryBase):
    pass


# db model
class Telemetry(TelemetryBase, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)


# device models
class Device(SQLModel, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(unique=True)
