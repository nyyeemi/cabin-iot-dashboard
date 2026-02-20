'use client';

import LocationTabs from './location-tabs';
import { OverviewRead } from '@/app/lib/types';
import LocationSection from '../card';
import { useSearchParams } from 'next/navigation';

export default function Overview({ overview }: { overview: OverviewRead }) {
  const searchParams = useSearchParams();

  const selectedId = searchParams.get('location') || 'all';
  const locations = overview.data;

  const visibleLocations =
    selectedId === 'all' ? locations : locations.filter((loc) => loc.location_id === selectedId);

  return (
    <>
      <LocationTabs locations={locations} selected={selectedId} />

      <div className="flex flex-col pb-10">
        {visibleLocations.map((loc) => (
          <LocationSection key={loc.location_id} location={loc} />
        ))}
      </div>
    </>
  );
}
