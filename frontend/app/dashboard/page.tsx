import { Thermometer, Droplets } from 'lucide-react';

import { DeviceOverview, Overview, OverviewRead, SensorReading } from '@/app/lib/types';

const overviewMock: OverviewRead = {
  data: [
    {
      location_id: 'c0041f6c-bfa5-4b8d-9ff4-e701ea8212ed',
      location_name: 'Mäntyranta',
      devices: [
        {
          device_id: '38965dc3-b0fc-4444-8185-5d611b6aaed6',
          device_name: 'Living room',
          latest_readings: [
            { sensor_type: 'temperature', unit: 'C', value: 22.3, ts: new Date().toISOString() },
            { sensor_type: 'humidity', unit: '%', value: 55, ts: new Date().toISOString() },
          ],
        },
        {
          device_id: 'd9845ece-402d-465b-8e90-33ba3718575d',
          device_name: 'Upstairs',
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
          device_id: '38965dc3-b0fc-4444-8185-5d611b6aaed6',
          device_name: 'Living room',
          latest_readings: [
            { sensor_type: 'temperature', unit: 'C', value: 22.3, ts: new Date().toISOString() },
            { sensor_type: 'humidity', unit: '%', value: 55, ts: new Date().toISOString() },
          ],
        },
        {
          device_id: 'd9845ece-402d-465b-8e90-33ba3718575d',
          device_name: 'Upstairs',
          latest_readings: [
            { sensor_type: 'humidity', unit: '%', value: 55, ts: new Date().toISOString() },
          ],
        },
      ],
    },
  ],
};

export default async function Page() {
  //const overview = await fetchOverview();
  const overview = overviewMock;

  /*const dateFormatted = new Date(device_latest.ts).toLocaleString('fi-FI', {
    day: '2-digit',
    month: '2-digit',
    year: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  });*/

  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
      <main className="flex min-h-screen w-full max-w-3xl flex-col bg-white p-4 dark:bg-black">
        <h1 className="pb-4 text-4xl font-semibold">Overview</h1>
        <div>
          {overview.data.map((loc) => (
            <LocationSection key={loc.location_id} location={loc} />
          ))}
        </div>
      </main>
    </div>
  );
}

function LocationSection({ location }: { location: Overview }) {
  return (
    <div>
      <h2 className="my-2 text-2xl font-medium text-zinc-300">{location.location_name}</h2>
      <div className="rounded-2xl border border-zinc-900">
        <SectionWrapper devices={location.devices} />
      </div>
    </div>
  );
}

function SectionWrapper({ devices }: { devices: DeviceOverview[] }) {
  return (
    <>
      {devices.map((d) => (
        <DeviceSection key={d.device_id} device={d} />
      ))}
    </>
  );
}

function DeviceSection({ device }: { device: DeviceOverview }) {
  return (
    <div key={device.device_id}>
      <h3 className="border-b border-b-zinc-900 px-4 py-2 text-zinc-400">{device.device_name}</h3>
      <div className="mt-4 grid grid-cols-2 gap-4 px-4 pt-4 pb-6">
        {device.latest_readings.map((r) => (
          <Card key={r.sensor_type} reading={r} />
        ))}
      </div>
    </div>
  );
}

const iconMap = {
  temperature: Thermometer,
  humidity: Droplets,
};

function Card({ reading }: { reading: SensorReading }) {
  const Icon = iconMap[reading.sensor_type as 'temperature' | 'humidity'];
  const tsFormatted = new Date(reading.ts).toLocaleString(undefined, {
    day: '2-digit',
    month: '2-digit',
    year: '2-digit',
  });

  const capitalize = (input: string) => input.charAt(0).toUpperCase() + input.slice(1);

  return (
    <div className="flex flex-row items-center gap-0 rounded-3xl border border-zinc-900 bg-zinc-950/60">
      <Icon className="m-4 h-6 w-6 text-amber-600" />

      <div className="flex flex-col py-4">
        <p className="text-sm font-semibold text-zinc-300">{capitalize(reading.sensor_type)}</p>
        <p className="text-2xl font-semibold">
          {reading.value} {reading.unit}
        </p>
        <p className="text-xs leading-tight text-zinc-500">{tsFormatted}</p>
      </div>
    </div>
  );
}
