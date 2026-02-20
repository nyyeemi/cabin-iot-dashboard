'use client';

import { Overview } from '@/app/lib/types';
import clsx from 'clsx';
import Link from 'next/link';
import { usePathname, useSearchParams, useRouter } from 'next/navigation';

type Props = {
  locations: Overview[];
  selected: string;
};

export default function LocationTabs({ locations, selected }: Props) {
  const searchParams = useSearchParams();
  const pathname = usePathname();
  const { replace } = useRouter();

  function onSelect(id: string) {
    const params = new URLSearchParams(searchParams);
    params.set('location', id);
    replace(`${pathname}?${params.toString()}`);
  }

  return (
    <div className="flex w-full flex-row gap-2 overflow-x-auto px-2 py-4">
      {locations.map((loc) => (
        <button
          onClick={() => onSelect(loc.location_id)}
          key={loc.location_id}
          className={clsx(
            'rounded-2xl px-3 transition-all duration-200',
            selected === loc.location_id ? 'font-semibold ring-2' : 'ring-1 ring-zinc-700',
          )}
        >
          {loc.location_name}
        </button>
      ))}
    </div>
  );
}
