import { DeviceDetail, OverviewRead, TelemetryRead } from './types';

const BASE_URL = process.env.API_URL;
const API_KEY = process.env.API_KEY;

export async function fetchOverview() {
  try {
    //await new Promise((resolve) => setTimeout(resolve, 6000)));
    const data = await fetch(`${BASE_URL}/overview`, {
      headers: {
        'X-API-Key': API_KEY!,
      },
      next: { revalidate: 120 },
    });
    const overview: OverviewRead = await data.json();
    return overview;
  } catch (error) {
    console.error('Error fetching data', error);
    throw new Error('Failed to fetch overview data');
  }
}

export async function fetchTelemetry(sensor_id: string, range: 'day' | 'week' | 'month' | 'year') {
  try {
    const data = await fetch(`${BASE_URL}/sensors/${sensor_id}/telemetry?range=${range}`, {
      headers: {
        'X-API-Key': API_KEY!,
      },
      next: { revalidate: 60 },
    });
    const telemetry: TelemetryRead = await data.json();
    return telemetry.data;
  } catch (error) {
    console.error('Error fetching data', error);
    throw new Error('Failed to fetch telemetry');
  }
}

export async function fetchDeviceOverview(id: string) {
  try {
    const data = await fetch(`${BASE_URL}/devices/${id}`, {
      headers: {
        'X-API-Key': API_KEY!,
      },
      next: { revalidate: 60 },
    });
    const deviceDetail: DeviceDetail = await data.json();
    return deviceDetail;
  } catch (error) {
    console.error('Error fetching data', error);
    throw new Error('Failed to fetch telemetry');
  }
}
