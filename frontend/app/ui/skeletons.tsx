const shimmer =
  'relative overflow-hidden before:absolute before:inset-0 before:-translate-x-full before:animate-shimmer before:bg-gradient-to-r before:from-transparent before:via-white/5 before:to-transparent';

export function OverviewSkeleton() {
  return (
    <div className={`flex min-h-screen w-full max-w-3xl flex-col`}>
      <LocationTabsSkeleton />
      <LocationOverviewSkeleton />
    </div>
  );
}

export function LocationTabsSkeleton() {
  return (
    <div className="flex w-full flex-row gap-2 overflow-x-auto py-4">
      {[120, 80, 100].map((w) => (
        <div
          key={w}
          style={{ width: w }}
          className={`${shimmer} relative h-9 shrink-0 overflow-hidden rounded-3xl bg-zinc-900/50`}
        />
      ))}
    </div>
  );
}

export function LocationOverviewSkeleton() {
  return (
    <div className="flex flex-col p-4 opacity-50">
      <div className="my-4 flex items-center gap-2">
        <div className={`${shimmer} h-7 w-48 rounded-lg bg-zinc-800`} />
        <div className={`${shimmer} h-5 w-5 rounded bg-zinc-800`} />
      </div>

      <div className="flex flex-col gap-6">
        {[1, 2].map((i) => (
          <div key={i} className="flex flex-col">
            <div className="flex items-center px-4 py-2">
              <div className={`${shimmer} h-4 w-32 rounded bg-zinc-800`} />
              <div className={`${shimmer} mx-2 h-2 w-2 rounded-full bg-zinc-800`} />
            </div>

            <div className="rounded-3xl bg-zinc-900 px-4">
              <ul className="divide-y divide-zinc-800">
                {[1, 2].map((j) => (
                  <li key={j} className="flex flex-row items-center justify-between py-4">
                    <div className="flex flex-col gap-4">
                      <div className={`${shimmer} h-4 w-20 rounded bg-zinc-800`} />
                      <div className={`${shimmer} h-9 w-28 rounded bg-zinc-800`} />
                    </div>
                    <div className={`${shimmer} h-16 w-16 rounded-full bg-zinc-800/50`} />
                  </li>
                ))}
              </ul>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
