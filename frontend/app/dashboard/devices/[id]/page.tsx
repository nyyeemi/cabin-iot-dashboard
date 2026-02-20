import BackButton from '@/app/ui/dashboard/backbutton';

export default async function Page(props: { params: Promise<{ id: string }> }) {
  const params = await props.params;
  const id = params.id;

  return (
    <div className="flex min-h-screen flex-col bg-zinc-50 dark:bg-black">
      <header className="sticky top-0 z-10 flex items-center border-b border-zinc-800 bg-black/80 p-4 backdrop-blur-md">
        <BackButton />
      </header>

      <main className="mx-auto w-full max-w-3xl p-4">
        <h1 className="mb-6 text-2xl font-bold">Device with id: {id}</h1>
      </main>
    </div>
  );
}
