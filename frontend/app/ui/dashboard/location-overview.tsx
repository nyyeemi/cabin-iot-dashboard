import { DeviceOverview, Overview, SensorReading } from '@/app/lib/types';
import clsx from 'clsx';
import { Thermometer, Droplets, Plus } from 'lucide-react';
import Link from 'next/link';

export default function LocationOverview({ location }: { location: Overview }) {
  const devices = location.devices;
  const hasDevices = devices.length > 0;
  return (
    <>
      <div className="my-2 flex flex-row items-baseline justify-between">
        <span className="text-xl font-bold">{location.location_name}</span>
        <span className="font-label text-xs font-bold tracking-widest text-zinc-200 uppercase">
          {devices.length} devices
        </span>
      </div>
      {hasDevices ? (
        <div className="flex flex-col gap-4">
          {devices.map((d) => (
            <DeviceCard key={d.device_id} device={d} />
          ))}
        </div>
      ) : (
        <EmptyState />
      )}
    </>
  );
}

function EmptyState() {
  return (
    <Link
      href="/dashboard/devices/new"
      className="hover:border-primary/60 hover:text-primary active:text-primary active:border-primary flex items-center gap-2 rounded-2xl border border-dashed border-zinc-400/60 bg-zinc-900/10 px-4 py-3 text-sm text-zinc-300 transition-colors"
    >
      <Plus className="h-4 w-4" />
      Add first device
    </Link>
  );
}

function DeviceCardHeader({ device }: { device: DeviceOverview }) {
  return (
    <div className="flex flex-row items-center px-4 py-1">
      <h3 className="font-semibold text-zinc-400">{device.device_name}</h3>

      <span
        className={clsx('mx-2 inline-block h-1 w-1 rounded-full ring-2', {
          'bg-green-600 ring-green-400': device.status === 'online',
          'bg-red-800 ring-red-600': device.status === 'offline',
        })}
      />
    </div>
  );
}

function DeviceCard({ device }: { device: DeviceOverview }) {
  return (
    <div className="flex flex-col">
      <DeviceCardHeader device={device} />

      <Link
        className="rounded-3xl bg-zinc-900 px-4 transition-colors duration-200 active:bg-zinc-900/70"
        href={`/dashboard/devices/${device.device_id}`}
        scroll={true}
      >
        <ul className="gap-4 divide-y divide-zinc-800">
          {device.latest_readings.map((r) => (
            <li key={r.sensor_type}>
              <SensorListItem reading={r} />
            </li>
          ))}
        </ul>
      </Link>
    </div>
  );
}

const iconMap = {
  temperature: Thermometer,
  humidity: Droplets,
};

function SensorListItem({ reading }: { reading: SensorReading }) {
  const Icon = iconMap[reading.sensor_type as 'temperature' | 'humidity'];
  const capitalize = (input: string) => input.charAt(0).toUpperCase() + input.slice(1);

  return (
    <div className={'flex w-full flex-row items-center justify-between gap-6 py-4 text-amber-500'}>
      <div className="flex flex-col gap-4 font-semibold">
        <p>{capitalize(reading.sensor_type)}</p>
        <p className="text-3xl font-semibold text-zinc-50">
          {reading.value} {reading.unit}
        </p>
      </div>

      <div className={'rounded-full bg-amber-500/5 p-4'}>
        <Icon className={'h-8 w-8'} />
      </div>
    </div>
  );
}
