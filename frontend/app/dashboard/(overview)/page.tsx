import Overview from '@/app/ui/dashboard/overview';
import { Suspense } from 'react';
import { OverviewSkeleton } from '../../ui/skeletons';

export default async function Page(props: { searchParams?: Promise<{ location?: string }> }) {
  const searchParams = await props.searchParams;
  const selectedId = searchParams?.location ?? 'all';

  return (
    <main className="flex w-full max-w-3xl flex-col p-4">
      <h1 className="pb-2 text-4xl font-bold tracking-tight">Overview</h1>
      <Suspense fallback={<OverviewSkeleton />}>
        <Overview selectedLocationId={selectedId} />
      </Suspense>
    </main>
  );
}
