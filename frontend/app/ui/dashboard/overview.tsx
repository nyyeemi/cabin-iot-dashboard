import LocationTabs from './location-tabs';
import LocationOverview from './location-overview';
import { fetchOverview } from '@/app/lib/api';
import Link from 'next/link';
import { InfoIcon, Plus } from 'lucide-react';

type Props = {
  selectedLocationId: string;
};

export default async function Overview({ selectedLocationId }: Props) {
  const overview = await fetchOverview();
  const locations = overview.data;

  const visibleLocations =
    selectedLocationId === 'all'
      ? locations
      : locations.filter((loc) => loc.location_id === selectedLocationId);

  const hasLocations = locations.length > 0;
  return (
    <>
      {hasLocations ? (
        <>
          <LocationTabs locations={locations} selected={selectedLocationId} />
          <div className="flex flex-col pb-10">
            {visibleLocations.map((loc) => (
              <LocationOverview key={loc.location_id} location={loc} />
            ))}
          </div>
        </>
      ) : (
        <EmptyState />
      )}
    </>
  );
}

function EmptyState() {
  return (
    <div className="my-16 flex flex-col justify-center rounded-4xl border border-white/5 bg-zinc-900/50 p-6 text-start shadow-2xl backdrop-blur-2xl transition-all">
      <>
        <div className="flex flex-row items-center gap-2">
          <div className="text-primary border-primary/10 bg-primary/5 rounded-full border p-2">
            <InfoIcon className="h-6 w-6" />
          </div>
          <p className="text-2xl font-bold text-zinc-200">No locations found</p>
        </div>
        <p className="mt-8 self-center text-center text-zinc-400">
          Get started by creating your first location. Come back to this page to see a summary of
          device readings when you have added a location and its first device.
        </p>
        <Link
          href="/dashboard/locations/new"
          className="bg-primary-container/10 border-primary/10 hover:bg-primary-container/20 text-primary mt-12 flex max-w-sm items-center gap-2 self-center rounded-full border px-5 py-2 text-sm font-medium transition-colors"
        >
          <Plus className="h-4 w-4" />
          Create Location
        </Link>
      </>
    </div>
  );
}
