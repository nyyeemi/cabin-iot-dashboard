import LocationTabs from '@/app/ui/dashboard/location-tabs';

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-screen flex-col md:flex-row md:overflow-hidden">
      <h1 className="p-8 text-4xl font-bold">Locations</h1>
      <LocationTabs />
      <div className="grow pt-18 md:overflow-y-auto md:pt-0 md:pl-64">{children}</div>
    </div>
  );
}
