import { Thermometer, Droplets } from 'lucide-react';
import clsx from 'clsx';
import { DeviceOverview, OverviewRead, SensorReading } from '@/app/lib/types';
import Link from 'next/link';
import Overview from '../ui/dashboard/overview';

const locations = [
  { location_name: 'Mäntyranta' },
  { location_name: 'Koti' },
  { location_name: 'Office' },
  { location_name: 'Mökki' },
  { location_name: 'Harjumänty' },
];

export const overviewMock: OverviewRead = {
  data: [
    {
      location_id: 'c0041f6c-bfa5-4b8d-9ff4-e701ea8212ed',
      location_name: 'Mäntyranta',
      devices: [
        {
          device_id: '38965dc3-b0fc-4444-8185-5d611b6aaed6',
          device_name: 'Living room',
          status: 'online',
          latest_readings: [
            { sensor_type: 'temperature', unit: '°C', value: 22.3, ts: new Date().toISOString() },
            { sensor_type: 'humidity', unit: '%', value: 55, ts: new Date().toISOString() },
          ],
        },
        {
          device_id: 'd9845ece-402d-465b-8e90-33ba3718575d',
          device_name: 'Upstairs',
          status: 'online',
          latest_readings: [
            { sensor_type: 'humidity', unit: '%', value: 55, ts: new Date().toISOString() },
          ],
        },
      ],
    },
    {
      location_id: 'c0041f6c-bfa5-4b8d-9ff4-e701ea8212as',
      location_name: 'Home',
      devices: [
        {
          device_id: '38965dc3-b0fc-4444-8185-5d611b6aaed0',
          device_name: 'Office',
          status: 'online',
          latest_readings: [
            { sensor_type: 'temperature', unit: '°C', value: 19.3, ts: new Date().toISOString() },
            { sensor_type: 'humidity', unit: '%', value: 51.9, ts: new Date().toISOString() },
          ],
        },
      ],
    },
  ],
};

export default async function Page() {
  //const overview = await fetchOverview();
  const overview = overviewMock;

  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
      <main className="flex min-h-screen w-full max-w-4xl flex-col bg-white p-4 dark:bg-black">
        <h1 className="pt-6 pb-2 text-4xl font-bold tracking-tight">Overview</h1>
        <Overview overview={overview} />
      </main>
    </div>
  );
}
