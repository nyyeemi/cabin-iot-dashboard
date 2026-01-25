import uuid
from sqlmodel import Field, SQLModel


class Device(SQLModel, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
