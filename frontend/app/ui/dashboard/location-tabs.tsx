import { Overview } from '@/app/lib/types';
import clsx from 'clsx';
import { Url } from 'next/dist/shared/lib/router/router';
import Link from 'next/link';

type Props = {
  locations: Overview[];
  selected: string;
};

export default function LocationTabs({ locations, selected }: Props) {
  return (
    <div className="flex w-full flex-row gap-2 overflow-x-auto py-4">
      <TabPill isActive={selected === 'all'} href={'/dashboard'} title={'All Locations'} />

      {locations.map((loc) => (
        <TabPill
          key={loc.location_id}
          isActive={selected === loc.location_id}
          href={`/dashboard?location=${encodeURIComponent(loc.location_id)}`}
          title={loc.location_name}
        />
      ))}
    </div>
  );
}

function TabPill({ isActive, href, title }: { isActive: boolean; href: Url; title: string }) {
  return (
    <Link
      href={href}
      className={clsx(
        'rounded-3xl px-4 py-2 transition-all duration-200',
        isActive ? 'bg-zinc-200 font-medium text-black' : 'bg-zinc-900',
      )}
    >
      {title}
    </Link>
  );
}
