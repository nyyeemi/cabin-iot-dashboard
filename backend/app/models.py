from datetime import datetime
import uuid
from sqlmodel import DateTime, Field, Relationship, SQLModel

from app.utils import utc_now


# ------locations-------
class LocationBase(SQLModel):
    name: str = Field(unique=True)


class Location(LocationBase, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)

    devices: list["Device"] = Relationship(back_populates="location")


# ------devices-------
class DeviceBase(SQLModel):
    name: str


class Device(DeviceBase, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
    location_id: uuid.UUID = Field(foreign_key="location.id")
    room: str | None = None
    last_reboot_ts: datetime | None = Field(
        default=None, sa_type=DateTime(timezone=True)
    )
    created_at: datetime = Field(
        default_factory=utc_now, sa_type=DateTime(timezone=True)
    )

    sensors: list["Sensor"] = Relationship(back_populates="device")
    location: "Location" = Relationship(back_populates="devices")


class DeviceCreate(SQLModel):
    name: str
    location_name: str
    sensors: list["SensorCreate"]


class DeviceRead(DeviceBase):
    id: uuid.UUID
    location_name: str
    sensors: list["Sensor"]


class DevicePublic(DeviceBase):
    id: uuid.UUID


class DevicesPublic(SQLModel):
    data: list[DevicePublic]
    count: int


class UptimeDetail(SQLModel):
    days: int
    hours: int
    minutes: int
    seconds: int
    total_seconds: int


class DeviceDetail(SQLModel):
    id: uuid.UUID
    device_name: str
    location_name: str
    room: str | None
    status: str
    last_seen: datetime | None
    created_at: datetime
    uptime: UptimeDetail | None
    sensors: list["SensorPublic"]


# ------sensors-------
class SensorBase(SQLModel):
    sensor_type: str
    unit: str | None = None


class Sensor(SensorBase, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
    device_id: uuid.UUID = Field(foreign_key="device.id")

    device: Device = Relationship(back_populates="sensors")
    telemetry: list["Telemetry"] = Relationship(back_populates="sensor")


class SensorCreate(SensorBase):
    pass


class SensorPublic(SensorBase):
    id: uuid.UUID


# ------telemetry-------
class TelemetryBase(SQLModel):
    ts: datetime = Field(sa_type=DateTime(timezone=True))
    value: float
    sensor_id: uuid.UUID = Field(index=True, foreign_key="sensor.id")


class TelemetryCreate(TelemetryBase):
    pass


class TelemetryPublic(TelemetryBase):
    pass


class TelemetryRead(SQLModel):
    sensor_type: str
    unit: str
    mean: float
    minimum: float
    maximum: float
    data: list["SensorData"]


class SensorData(SQLModel):
    ts: datetime
    value: float


class Telemetry(TelemetryBase, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
    sensor: Sensor = Relationship(back_populates="telemetry")


# Pydantic models for overview read
class SensorReading(SQLModel):
    sensor_type: str
    unit: str | None
    value: float
    ts: datetime


class DeviceOverview(SQLModel):
    device_id: uuid.UUID
    device_name: str
    status: str
    latest_readings: list[SensorReading]


class Overview(SQLModel):
    location_id: uuid.UUID
    location_name: str
    devices: list[DeviceOverview]


class OverviewRead(SQLModel):
    data: list[Overview]
