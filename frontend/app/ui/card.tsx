import { fetchDevices } from '@/app/lib/api';
import { Device } from '@/app/lib/types';

export default async function CardWrapper() {
  const devices = await fetchDevices();

  return (
    <>
      {devices.data.map((device) => {
        <Card device={device} />;
      })}
    </>
  );
}

export function Card({ device }: { device: Device }) {
  //fetch here
  return <></>;
}
