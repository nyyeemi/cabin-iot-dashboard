import { DeviceDetail, OverviewRead, TelemetryRead } from './types';

const BASE_URL = process.env.PUBLIC_API_BASE;

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

export async function fetchTelemetry(
  deviceId: string,
  sensorName: string,
  range: 'day' | 'week' | 'month' | 'year',
) {
  try {
    //sensors/sensor_id/telemetry
    const data = await fetch(
      `${BASE_URL}/devices/${deviceId}/telemetry?sensor_name=${sensorName}&range=${range}`,
    );
    const telemetry: TelemetryRead = await data.json();
    return telemetry.data;
  } catch (error) {
    console.error('Error fetching data', error);
    throw new Error('Failed to fetch telemetry');
  }
}

export async function fetchDeviceOverview(id: string) {
  try {
    const data = await fetch(`${BASE_URL}/devices/${id}/`);
    const deviceDetail: DeviceDetail = await data.json();
    return deviceDetail;
  } catch (error) {
    console.error('Error fetching data', error);
    throw new Error('Failed to fetch telemetry');
  }
}
