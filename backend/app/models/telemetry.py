from datetime import datetime
import uuid
from sqlmodel import Field, SQLModel


class Telemetry(SQLModel, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
    device_id: uuid.UUID
    ts: datetime
    temp: float
