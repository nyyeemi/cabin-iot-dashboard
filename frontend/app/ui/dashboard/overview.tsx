import LocationTabs from './location-tabs';
import { OverviewRead } from '@/app/lib/types';
import LocationOverview from './location-overview';

type Props = {
  overview: OverviewRead;
  selectedLocationId: string;
};

export default function Overview({ overview, selectedLocationId }: Props) {
  const locations = overview.data;

  const visibleLocations =
    selectedLocationId === 'all'
      ? locations
      : locations.filter((loc) => loc.location_id === selectedLocationId);

  return (
    <>
      <LocationTabs locations={locations} selected={selectedLocationId} />

      <div className="flex flex-col pb-10">
        {visibleLocations.map((loc) => (
          <LocationOverview key={loc.location_id} location={loc} />
        ))}
      </div>
    </>
  );
}
