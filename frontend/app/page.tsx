import Image from 'next/image';
import Link from 'next/link';
import backdropWinter from '@/public/backdrop_winter.jpeg';

export default function Home() {
  return (
    <div className="relative flex min-h-dvh overflow-y-visible font-sans">
      <div className="-z-10">
        <Image src={backdropWinter} alt="" preload fill sizes="50vw" />
        <div className="absolute inset-0 bg-slate-900/50 backdrop-blur-2xl" />
      </div>

      <main className="relative z-10 flex w-full max-w-3xl flex-col items-center justify-between px-16 py-32">
        <div className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-full bg-white">
            <div className="h-3 w-3 bg-black" />
          </div>

          <span className="text-sm font-semibold tracking-wide text-white">Placeholder</span>
        </div>

        <div className="flex flex-col items-center gap-6 text-center sm:items-start sm:text-left">
          <h1 className="max-w-xs text-3xl leading-10 font-semibold tracking-tight text-white">
            Welcome
          </h1>
          <p className="max-w-md text-lg leading-8 text-white/70">Boilerplate text.</p>
        </div>

        <div className="flex flex-col gap-4 text-base font-medium sm:flex-row">
          <Link
            className="flex h-12 w-full items-center justify-center gap-2 rounded-full bg-white px-5 text-black transition-colors hover:bg-white/90 md:w-[158px]"
            href="/dashboard"
          >
            To Dashboard
          </Link>
        </div>
      </main>
    </div>
  );
}
