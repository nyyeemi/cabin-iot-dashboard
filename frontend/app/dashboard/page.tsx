import Image from 'next/image';
import { OverviewRead } from '@/app/lib/types';
import Overview from '../ui/dashboard/overview';
import { Ellipsis, HousePlus } from 'lucide-react';
import backdropWinter from '@/public/backdrop_winter.jpeg';

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

export default async function Page(props: { searchParams?: Promise<{ location?: string }> }) {
  //const overview = await fetchOverview();
  const overview = overviewMock;
  const searchParams = await props.searchParams;
  const selectedId = searchParams?.location ?? 'all';

  return (
    <div className="relative flex min-h-screen items-center justify-center font-sans">
      <div className="-z-10">
        <Image src={backdropWinter} alt="" preload fill sizes="50vw" />
        <div className="absolute inset-0 bg-slate-900/50 backdrop-blur-2xl" />
      </div>

      <main className="flex min-h-screen w-full max-w-3xl flex-col p-4">
        <header className="flex justify-end">
          <div className="bg-blur-lg flex flex-row gap-6 rounded-4xl bg-zinc-950/50 px-4 py-2 ring-1 ring-zinc-700">
            <HousePlus className="h-6 w-6" />
            <Ellipsis className="h-6 w-6" />
          </div>
        </header>
        <h1 className="pb-2 text-4xl font-bold tracking-tight">Overview</h1>
        <Overview overview={overview} selectedLocationId={selectedId} />
      </main>
    </div>
  );
}
