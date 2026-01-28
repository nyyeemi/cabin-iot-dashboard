import { Thermometer } from "lucide-react";

export default async function Page() {
  const data = await fetch('http://localhost:8000/devices');
  const devices = await data.json();
  console.log(devices)

  const device_id = devices.data[0].id
  const device_latest = await fetch(`http://localhost:8000/devices/${device_id}/telemetry/latest`)
  const latest_reading = await device_latest.json()
  console.log(latest_reading)

  return (
    <div className="flex min-h-screen items-center justify-center  bg-zinc-50 font-sans dark:bg-black">
      <main className="flex min-h-screen w-full max-w-3xl flex-col p-4  bg-white dark:bg-black">
        <h1 className="text-4xl font-semibold pb-4">Overview</h1>

        <h2 className="px-2 pb-1 font-semibold text-zinc-400">Mäntyranta</h2>
        {/*card*/}
        <div className="flex flex-row items-center gap-2 px-4 py-2 rounded-xl border border-zinc-800 bg-zinc-950">
          <Thermometer className="w-5 h-5 text-amber-600"/>
          <div className="flex flex-col px-4">
            <p className="text-zinc-400 text-sm">Temperature</p>
            <p className="text-2xl font-semibold">21.6°C</p>
          </div>
        </div>
      
      </main>
    </div>
  );
}