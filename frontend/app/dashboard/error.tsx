'use client';

import { useEffect } from 'react';
import { AlertCircle, RotateCcw } from 'lucide-react';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <main className="px-4">
      <div className="my-16 flex flex-col items-center rounded-4xl border border-white/5 bg-zinc-900/50 p-6 shadow-2xl backdrop-blur-2xl">
        <div className="flex flex-row items-center gap-2">
          <div className="rounded-full border border-red-500/10 bg-red-500/5 p-2 text-red-400">
            <AlertCircle className="h-6 w-6" />
          </div>
          <p className="text-2xl font-bold text-zinc-200">Something went wrong</p>
        </div>
        <p className="mt-8 text-center text-zinc-400">
          An error occurred while loading this page. You can try again or come back later.
        </p>
        <button
          onClick={() => reset()}
          className="border-primary/10 bg-primary/5 text-primary hover:bg-primary/10 mt-12 flex items-center gap-2 rounded-full border px-5 py-2 text-sm font-medium transition-colors"
        >
          <RotateCcw className="h-4 w-4" />
          Try again
        </button>
      </div>
    </main>
  );
}
