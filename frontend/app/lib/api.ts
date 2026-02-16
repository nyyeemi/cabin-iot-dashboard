import { DeviceResponse, OverviewRead, Telemetry } from './types';

const BASE_URL = process.env.PUBLIC_API_BASE;

export async function fetchDevices() {
  try {
    const data = await fetch(`${BASE_URL}/devices`);
    const devices: DeviceResponse = await data.json();
    return devices;
  } catch (error) {
    console.error('Error fetching data', error);
    throw new Error('Failed to fetch card data');
  }
}

export async function fetchTelemetryLatest(device_id: string) {
  try {
    const data = await fetch(`${BASE_URL}/devices/${device_id}/telemetry/latest`);
    const latest_reading: Telemetry = await data.json();
    return latest_reading;
  } catch (error) {
    console.error('Error fetching data', error);
    throw new Error('Failed to fetch telemetry data');
  }
}

export async function fetchOverview() {
  try {
    const data = await fetch(`${BASE_URL}/overview`);
    const overview: OverviewRead = await data.json();
    return overview.data;
  } catch (error) {
    console.error('Error fetching data', error);
    throw new Error('Failed to fetch overview data');
  }
}
