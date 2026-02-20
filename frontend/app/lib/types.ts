export type Device = {
  name: string;
  id: string;
};

export type DeviceResponse = {
  data: Device[];
  count: number;
};

export type Telemetry = {
  device_id: string;
  temp: number;
  ts: string;
};

export type SensorReading = {
  sensor_type: string;
  unit?: string | null;
  value: number;
  ts: string;
};

export type DeviceOverview = {
  device_id: string;
  device_name: string;
  status: 'online' | 'offline';
  latest_readings: SensorReading[];
};

export type Overview = {
  location_id: string;
  location_name: string;
  devices: DeviceOverview[];
};

export type OverviewRead = {
  data: Overview[];
};
