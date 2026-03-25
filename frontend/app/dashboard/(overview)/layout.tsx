import Image from 'next/image';
import backdropWinter from '@/public/backdrop_winter.jpeg';
import { Ellipsis, HousePlus } from 'lucide-react';

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="bg-background relative w-full items-center font-sans">
      {/*
      <Image src={backdropWinter} alt="" fill sizes="100vw" className="-z-10 object-cover" />
      <div className="absolute inset-0 -z-10 bg-slate-900/50 backdrop-blur-2xl" />
      */}
      <div className="mx-auto min-h-screen w-full max-w-3xl">
        <header className="flex justify-end p-4">
          <div className="flex flex-row gap-6 rounded-4xl bg-zinc-950/50 px-4 py-2 ring-1 ring-zinc-700">
            <HousePlus className="h-6 w-6" />
            <Ellipsis className="h-6 w-6" />
          </div>
        </header>
        {children}
      </div>
    </div>
  );
}
