from datetime import datetime
import uuid
from sqlmodel import Field, Relationship, SQLModel


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

    sensors: list["Sensor"] = Relationship(back_populates="device")
    location: "Location" = Relationship(back_populates="devices")


class DeviceCreate(SQLModel):
    name: str
    location_name: str
    sensors: list["SensorPublic"]


class DeviceRead(DeviceBase):
    id: uuid.UUID
    location_name: str
    sensors: list["Sensor"]


class DevicePublic(DeviceBase):
    id: uuid.UUID


class DevicesPublic(SQLModel):
    data: list[DevicePublic]
    count: int


# ------sensors-------
class SensorBase(SQLModel):
    sensor_type: str
    unit: str | None = None


class Sensor(SensorBase, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
    device_id: uuid.UUID = Field(foreign_key="device.id")

    device: Device = Relationship(back_populates="sensors")
    telemetry: list["Telemetry"] = Relationship(back_populates="sensor")


class SensorPublic(SensorBase):
    pass


# ------telemetry-------
class TelemetryBase(SQLModel):
    ts: datetime
    value: float
    sensor_id: uuid.UUID = Field(index=True, foreign_key="sensor.id")


class TelemetryCreate(TelemetryBase):
    pass


class TelemetryPublic(TelemetryBase):
    pass


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
    latest_readings: list[SensorReading]


class Overview(SQLModel):
    location_id: uuid.UUID
    location_name: str
    devices: list[DeviceOverview]


class OverviewRead(SQLModel):
    data: list[Overview]
