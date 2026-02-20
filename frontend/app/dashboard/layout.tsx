import Link from 'next/link';

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-screen flex-col md:flex-row md:overflow-hidden">
      <Header />
      <div className="grow pt-18 md:overflow-y-auto md:pt-0 md:pl-64">{children}</div>
    </div>
  );
}

export function Header() {
  return (
    <div className="fixed top-0 right-0 left-0 flex h-18 w-full flex-row items-center gap-8 border-b border-b-zinc-800 bg-zinc-950 px-6 py-6 md:w-64">
      <Link href="/dashboard">Home</Link>
      <Link href="/dashboard/devices">Devices</Link>

      {/* Header / Logo */}
      {/*navlinks*/}
    </div>
  );
}
