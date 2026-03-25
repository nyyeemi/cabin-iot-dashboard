import { fetchDeviceOverview, fetchTelemetry } from '@/app/lib/api';
import { DeviceDetail } from '@/app/lib/types';
import BackButton from '@/app/ui/dashboard/backbutton';
import { DateRangeSelector, SensorSelector } from '@/app/ui/dashboard/devices/selectors';
import TimeSeriesChart from '@/app/ui/dashboard/timeseries-chart';
import { ThermometerSun } from 'lucide-react';

const mockData = {
  id: 'mock-id-001',
  device_name: 'A-101',
  location_name: 'Mäntyranta',
  room: 'Upstairs',
  status: 'online',
  last_seen: new Date().toISOString(),
  created_at: new Date().toISOString(),
  uptime: 12, //in seconds maybe or formatted here to hours
  sensors: [
    {
      id: 'd9845ece-402d-465b-8e90-33ba3718575d',
      sensor_type: 'temperature',
      unit: '°C',
      latest_reading: {
        value: 21.4,
        ts: new Date().toISOString(),
      },

      range: {
        min: 16,
        max: 25,
      },

      mean: 21.3,

      telemetry: generateTemperatureTelemetry(24), // 24h hourly
    },
    {
      id: 'd9845ece-402d-465b-8e90-33ba3718575c',
      sensor_type: 'humidity',
      unit: '%',
      latest_reading: {
        value: 21.4,
        ts: new Date().toISOString(),
      },

      range: {
        min: 16,
        max: 25,
      },

      mean: 22.3,

      telemetry: generateTemperatureTelemetry(24), // 24h hourly
    },
  ],
};

function generateTemperatureTelemetry(hours: number) {
  const now = Date.now();
  const data = [];

  for (let i = hours; i >= 0; i--) {
    const ts = new Date(now - i * 60 * 60 * 1000);
    const base = 21;
    const variation = Math.sin(i / 3) * 1.5;
    const noise = (Math.random() - 0.5) * 0.3;

    data.push({
      ts: ts.toISOString(),
      value: Number((base + variation + noise).toFixed(2)),
    });
  }

  return data;
}

type SensorOverview = {
  id: string;
  sensor_type: string;
  unit: string;
};

type DeviceOverview = {
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

type Telemetry = {
  sensor_type: string;
  unit: string;
  mean: number;
  range: {
    min: number;
    max: number;
  };
  data: [{ ts: string; value: number }];
};

export default async function Page(props: {
  params: Promise<{ id: string }>;
  searchParams?: Promise<{ range?: 'day' | 'month' | 'week' | 'year'; sensor?: string }>;
}) {
  const params = await props.params;
  const id = params.id;

  const deviceData = await fetchDeviceOverview(id);
  console.log(deviceData);
  //const deviceData = mockData;
  //const telemetry = mockData.sensors[0].telemetry;
  const sensors = deviceData.sensors;

  const searchParams = await props.searchParams;
  const selectedRange = searchParams?.range ?? 'day';
  const selectedSensor = searchParams?.sensor ?? sensors[0].sensor_type;

  const selectedSensorObj = sensors.find((s) => s.sensor_type === selectedSensor);
  const telemetry = await fetchTelemetry(selectedSensorObj?.id ?? 'skip', selectedRange);

  /*const telemetryData = await fetchTelemetry(
      id,
      selectedSensor,
      selectedRange
    );*/

  return (
    <div className="bg-background flex min-h-screen items-center justify-center font-sans">
      <main className="relative flex min-h-screen w-full max-w-3xl flex-col">
        {/*<h1 className="mt-2 text-3xl font-bold">{deviceData.location_name}</h1>
        <h2 className="mb-4 font-semibold text-zinc-500">{deviceData.room}</h2>*/}
        <header className="sticky top-0 z-10 my-2 flex items-center justify-center bg-linear-to-t to-black px-4 py-4">
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

          {/*
          <div className="mt-8 flex flex-row justify-between rounded-3xl px-8 py-2 ring-1 ring-zinc-900">
            <Summary
              header={'AVERAGE'}
              value={deviceData.sensors[0].mean}
              unit={mockData.sensors[0].unit}
              footer={dateRangeMap[selectedRange as 'day' | 'month' | 'week' | 'year']}
            />
            <Summary
              header={'MIN'}
              value={deviceData.sensors[0].range.min}
              unit={mockData.sensors[0].unit}
              footer={'+0.5'}
            />
            <Summary
              header={'MAX'}
              value={deviceData.sensors[0].range.max}
              unit={mockData.sensors[0].unit}
              footer={'+0.9'}
            />
            </div>
            */}
        </div>
        <DeviceDetails deviceData={deviceData} />
      </main>
    </div>
  );
}

const dateRangeMap = {
  day: 'Today',
  month: 'Last month',
  week: 'Last week',
  year: 'Year to date',
};

type Props = {
  header: string;
  value: number;
  unit?: string;
  footer?: string;
};

function Summary(props: Props) {
  return (
    <div className="flex flex-col">
      <p className="text-sm font-medium tracking-wide text-zinc-500">{props.header}</p>
      <p className="text-2xl font-bold">
        {props.value}
        <span className="text-xl font-semibold text-zinc-500"> {props.unit}</span>
      </p>
      <p className="text-sm font-medium tracking-wide text-zinc-500">{props.footer}</p>
    </div>
  );
}

function DeviceDetails({ deviceData }: { deviceData: DeviceDetail }) {
  return (
    <div className="mt-8 flex flex-col gap-4 rounded-t-3xl bg-zinc-900 p-4">
      {/**Card title */}
      <div className="flex flex-row items-center gap-4">
        <div className="rounded-full border border-sky-400/10 bg-sky-500/10 p-2">
          <ThermometerSun className="h-8 w-8 text-sky-500" />
        </div>
        <div>
          <h2 className="mt-2 flex text-2xl font-bold">{deviceData.device_name}</h2>
          <span className="font-semibold text-zinc-500">{deviceData.status}</span>
        </div>
      </div>

      <p className="px-8 py-4 text-center font-semibold">
        Device available and functioning normally.
      </p>

      {/**List sections */}
      <div className="flex flex-col divide-y divide-zinc-700 rounded-3xl bg-zinc-800 px-4 py-2">
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
      <div className="flex flex-col divide-y divide-zinc-700 rounded-3xl bg-zinc-800 px-4 py-2">
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
