import { fetchDeviceOverview, fetchTelemetry } from '@/app/lib/api';
import { DeviceDetail } from '@/app/lib/types';
import BackButton from '@/app/ui/dashboard/backbutton';
import { DateRangeSelector, SensorSelector } from '@/app/ui/dashboard/devices/selectors';
import TimeSeriesChart from '@/app/ui/dashboard/timeseries-chart';
import { ThermometerSun } from 'lucide-react';

export default async function Page(props: {
  params: Promise<{ id: string }>;
  searchParams?: Promise<{ range?: 'day' | 'month' | 'week' | 'year'; sensor?: string }>;
}) {
  const params = await props.params;
  const id = params.id;

  const deviceData = await fetchDeviceOverview(id);

  const sensors = deviceData.sensors;

  const searchParams = await props.searchParams;
  const selectedRange = searchParams?.range ?? 'day';
  const selectedSensor = searchParams?.sensor ?? sensors[0].sensor_type;

  const selectedSensorObj = sensors.find((s) => s.sensor_type === selectedSensor);
  const telemetry = await fetchTelemetry(selectedSensorObj?.id ?? 'skip', selectedRange);

  // maybe have api return
  const values = telemetry.map((d) => d.value);
  const mean = values.reduce((a, b) => a + b, 0) / values.length;
  const min = Math.min(...values);
  const max = Math.max(...values);
  const unit = selectedSensorObj?.unit;

  return (
    <div className="bg-background flex min-h-screen items-center justify-center font-sans">
      <main className="relative flex min-h-screen w-full max-w-3xl flex-col">
        <header className="to-background sticky top-0 z-10 flex items-center justify-center bg-linear-to-t px-4 py-4">
          <span className="text-lg font-semibold">{deviceData.device_name}</span>
          <div className="absolute left-4">
            <BackButton />
          </div>
        </header>

        <div className="p-4">
          <SensorSelector
            sensorNames={sensors.map((s) => s.sensor_type)}
            selectedRange={selectedRange}
            selectedSensor={selectedSensor}
            deviceId={id}
          />

          <DateRangeSelector
            selectedRange={selectedRange}
            selectedSensor={selectedSensor}
            id={id}
          />

          <TimeSeriesChart data={telemetry} range={selectedRange} />

          <div className="mt-8 grid grid-cols-3 justify-items-center gap-4">
            <Summary header={'AVERAGE'} value={mean} unit={unit} />
            <Summary header={'MIN'} value={min} unit={unit} />
            <Summary header={'MAX'} value={max} unit={unit} />
          </div>
        </div>
        <DeviceDetails deviceData={deviceData} />
      </main>
    </div>
  );
}

type Props = {
  header: string;
  value: number;
  unit?: string;
  footer?: string;
};

function Summary(props: Props) {
  return (
    <div className="flex flex-col gap-1">
      <p className="text-sm font-medium tracking-widest text-zinc-500 uppercase">{props.header}</p>
      <p className="text-2xl font-bold">
        {props.value.toFixed(1)}
        <span className="text-xl font-semibold text-zinc-500"> {props.unit}</span>
      </p>
      <p className="text-sm font-medium tracking-wide text-zinc-500">{props.footer}</p>
    </div>
  );
}

function DeviceDetails({ deviceData }: { deviceData: DeviceDetail }) {
  return (
    <div className="mt-8 mb-20 flex flex-col gap-4 rounded-4xl border-t border-white/5 bg-zinc-900/60 p-4 shadow-2xl shadow-black/40">
      {/**Card title */}
      <div className="flex flex-row items-center gap-4">
        <div className="bg-primary-container/40 flex h-14 w-14 items-center justify-center rounded-full">
          <ThermometerSun className="text-primary h-6 w-6" />
        </div>
        <div className="flex flex-col gap-1">
          <h2 className="flex text-xl leading-tight font-bold">{deviceData.device_name}</h2>
          <span className="text-xs font-medium text-zinc-400">{deviceData.status}</span>
        </div>
      </div>

      {/**List sections */}
      <div className="flex flex-col divide-y divide-zinc-800 py-2">
        <div className="flex w-full flex-row justify-between py-2">
          <p>Location</p>
          <p className="text-zinc-400">{deviceData.location_name}</p>
        </div>

        <div className="flex w-full flex-row justify-between py-2">
          <p>Room</p>
          <p className="text-zinc-400">{deviceData.room}</p>
        </div>

        <div className="flex w-full flex-row justify-between py-2">
          <p>Sensors</p>
          <p className="text-zinc-400">{deviceData.sensors.map((s) => s.sensor_type).join(', ')}</p>
        </div>

        <div className="flex w-full flex-row justify-between py-2">
          <p>Last Seen</p>
          <p className="text-zinc-400">{deviceData.last_seen}</p>
        </div>

        <div className="flex w-full flex-row justify-between py-2">
          <p>Register date</p>
          <p className="text-zinc-400">{deviceData.created_at}</p>
        </div>
      </div>

      {/**Techincal details, add battery, ip, signal strength etc */}
      <div className="flex flex-col divide-y divide-zinc-800 py-2">
        <div className="flex w-full flex-row justify-between py-2">
          <p>Device ID</p>
          <p className="text-zinc-400">{deviceData.id}</p>
        </div>

        <div className="flex w-full flex-row justify-between py-2">
          <p>Uptime</p>
          <p className="text-zinc-400">
            {deviceData.uptime
              ? `${deviceData.uptime.days}d ${deviceData.uptime.hours}h ${deviceData.uptime.minutes}m`
              : '—'}
          </p>
        </div>
      </div>
    </div>
  );
}
