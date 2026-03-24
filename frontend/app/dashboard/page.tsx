import Image from 'next/image';
import Overview from '@/app/ui/dashboard/overview';
import { Ellipsis, HousePlus } from 'lucide-react';
import backdropWinter from '@/public/backdrop_winter.jpeg';
import { Suspense } from 'react';
import { OverviewSkeleton } from '../ui/skeletons';

export default async function Page(props: { searchParams?: Promise<{ location?: string }> }) {
  const searchParams = await props.searchParams;
  const selectedId = searchParams?.location ?? 'all';

  return (
    <div className="relative flex min-h-screen items-center justify-center font-sans">
      <div className="-z-10">
        <Image src={backdropWinter} alt="" preload fill sizes="50vw" />
        <div className="absolute inset-0 bg-slate-900/50 backdrop-blur-2xl" />
      </div>

      <main className="flex min-h-screen w-full max-w-3xl flex-col p-4">
        <header className="flex justify-end">
          <div className="bg-blur-lg flex flex-row gap-6 rounded-4xl bg-zinc-950/50 px-4 py-2 ring-1 ring-zinc-700">
            <HousePlus className="h-6 w-6" />
            <Ellipsis className="h-6 w-6" />
          </div>
        </header>
        <h1 className="pb-2 text-4xl font-bold tracking-tight">Overview</h1>
        <Suspense fallback={<OverviewSkeleton />}>
          <Overview selectedLocationId={selectedId} />
        </Suspense>
      </main>
    </div>
  );
}
