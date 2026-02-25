'use client';
import clsx from 'clsx';
import { useRouter } from 'next/navigation';

export function SensorSelector({
  sensorNames,
  selectedSensor,
  selectedRange,
  deviceId,
}: {
  sensorNames: string[];
  selectedSensor: string;
  selectedRange: string;
  deviceId: string;
}) {
  const router = useRouter();
  return (
    <div className="mb-4 flex w-full flex-row gap-2 overflow-x-auto overflow-y-visible p-0.5">
      {sensorNames.map((sensorName) => {
        const isActive = sensorName === selectedSensor;
        return (
          <button
            key={sensorName}
            onClick={() =>
              router.replace(`${deviceId}?sensor=${sensorName}&range=${selectedRange}`)
            }
            className={clsx(
              'rounded-full px-4 py-1 font-medium ring-1 transition-all duration-200',
              isActive ? 'text-zinc-300 ring-zinc-300' : 'text-zinc-500 ring-zinc-800',
            )}
          >
            {sensorName}
          </button>
        );
      })}
    </div>
  );
}

const dates = ['Day', 'Week', 'Month', 'Year'];

export function DateRangeSelector({
  selectedRange,
  selectedSensor,
  id,
}: {
  selectedRange: string;
  selectedSensor: string;
  id: string;
}) {
  const router = useRouter();
  return (
    <div className="mb-8 flex flex-row items-center justify-between rounded-4xl p-0.5 ring-1 ring-zinc-800 md:max-w-md md:self-center">
      {dates.map((date) => {
        const isActive = selectedRange === date.toLowerCase();
        return (
          <button
            key={date}
            onClick={() =>
              router.replace(`${id}?sensor=${selectedSensor}&range=${date.toLowerCase()}`)
            }
            className={clsx(
              'rounded-4xl px-5 py-0.5 font-medium text-zinc-300 transition-all duration-200',
              isActive ? 'font-medium ring-1 ring-zinc-300' : '',
            )}
          >
            {date}
          </button>
        );
      })}
    </div>
  );
}
