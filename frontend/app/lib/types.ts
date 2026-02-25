export type Device = {
  name: string;
  id: string;
};

export type DeviceResponse = {
  data: Device[];
  count: number;
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

export type TelemetryRead = {
  sensor_type: string;
  unit: string;
  mean: number;
  range: {
    min: number;
    max: number;
  };
  data: [{ ts: string; value: number }];
};

type SensorOverview = {
  id: number;
  sensor_type: string;
  unit: string;
};

export type DeviceDetail = {
  id: string;
  device_name: string;
  location_name: string;
  room: string;
  status: string;
  last_seen: string;
  created_at: string;
  uptime: number;
  sensors: SensorOverview[];
};
