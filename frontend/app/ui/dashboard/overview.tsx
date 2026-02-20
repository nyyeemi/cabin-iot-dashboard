'use client';

import { useState } from 'react';
import LocationTabs from './location-tabs';
import { OverviewRead } from '@/app/lib/types';
import LocationSection from '../card';
import { useSearchParams } from 'next/navigation';
import { useRouter } from 'next/router';

export default function Overview({
  overview,
  selectedId,
}: {
  overview: OverviewRead;
  selectedId: string;
}) {
  const locations = overview.data;

  const activeLocation = locations.find((loc) => loc.location_id === selectedId);

  return (
    <>
      <LocationTabs locations={locations} selected={selectedId} />

      {activeLocation && <LocationSection location={activeLocation} />}
    </>
  );
}
