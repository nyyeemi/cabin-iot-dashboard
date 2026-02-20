import { DeviceOverview, Overview, SensorReading } from '@/app/lib/types';
import clsx from 'clsx';
import { Thermometer, Droplets } from 'lucide-react';
import Link from 'next/link';

//section list type secction, renders cards for each device in location
export default function LocationSection({ location }: { location: Overview }) {
  const devices = location.devices;
  return (
    <>
      <h2 className="mt-4 mb-4 text-3xl font-semibold">{location.location_name}</h2>
      <div className="flex flex-col gap-6">
        {devices.map((d) => (
          <DeviceCard key={d.device_id} device={d} />
        ))}
      </div>
    </>
  );
}

//outer card (border) wrapping the inner senssor cards
function DeviceCard({ device }: { device: DeviceOverview }) {
  return (
    <Link
      key={device.device_id}
      className="rounded-2xl border border-zinc-700 transition delay-75 duration-200 hover:border-zinc-600 hover:bg-zinc-950/50"
      href={`/dashboard/devices/${device.device_id}`}
    >
      <div className="flex flex-row items-center justify-between px-4 py-4">
        <h3 className="font-semibold text-zinc-200">{device.device_name}</h3>
        <p className="font-mono text-xs text-zinc-500">
          {device.status}
          <span
            className={clsx('mx-2 inline-block h-1.5 w-1.5 rounded-full ring-2', {
              'bg-green-600 ring-green-400': device.status === 'online',
              'bg-red-800 ring-red-600': device.status === 'offline',
            })}
          />
        </p>
      </div>

      <div className="grid grid-cols-2 gap-4 px-4 pb-4">
        {device.latest_readings.map((r) => (
          <SensorCard key={r.sensor_type} reading={r} />
        ))}
      </div>

      <p className="px-4 pb-2 font-mono text-xs text-zinc-700">Device id: {device.device_id}</p>
    </Link>
  );
}

const iconMap = {
  temperature: Thermometer,
  humidity: Droplets,
};

function SensorCard({ reading }: { reading: SensorReading }) {
  const Icon = iconMap[reading.sensor_type as 'temperature' | 'humidity'];
  const tsFormatted = new Date(reading.ts).toLocaleString('en-GB', {
    day: '2-digit',
    month: '2-digit',
    year: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  });

  const capitalize = (input: string) => input.charAt(0).toUpperCase() + input.slice(1);

  return (
    <div className="flex w-full flex-col gap-6 rounded-2xl border border-zinc-900 bg-zinc-950 p-4">
      <div className="flex flex-row items-center gap-2">
        <Icon
          className={clsx('h-6 w-6', {
            'text-red-500': reading.sensor_type === 'temperature',
            'text-blue-500': reading.sensor_type === 'humidity',
          })}
        />
        <p className="text-zinc-200">{capitalize(reading.sensor_type)}</p>
      </div>

      <p className="text-3xl font-semibold">
        {reading.value} {reading.unit}
      </p>
      <p className="text-xs leading-tight text-zinc-400">{tsFormatted}</p>
    </div>
  );
}
