import Link from 'next/link';

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-screen flex-col md:flex-row md:overflow-hidden">
      <div className="flex w-full flex-row gap-8 border-b border-b-zinc-800 bg-black px-4 py-6 md:w-64">
        <Link href="/dashboard">Home</Link>
        <Link href="/dashboard/devices">Devices</Link>
        {/* Header / Logo */}
        {/*navlinks*/}
      </div>
      <div className="grow md:overflow-y-auto">{children}</div>
    </div>
  );
}
