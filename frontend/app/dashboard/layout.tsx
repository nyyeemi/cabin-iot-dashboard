import Link from "next/link";

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-screen flex-col md:flex-row md:overflow-hidden">
      <div className="flex w-full flex-row px-4 py-6 gap-8 border-b border-b-zinc-800 bg-black md:w-64">
        <Link href="/dashboard">Home</Link>
        <Link href="/dashboard/devices">Devices</Link>
        {/* Header / Logo */}
        {/*navlinks*/}
      </div>
      <div className="grow p-4 md:overflow-y-auto">{children}</div>
    </div>
  );
}
