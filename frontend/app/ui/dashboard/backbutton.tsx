import { ChevronLeft } from 'lucide-react';
import Link from 'next/link';

export default function BackButton() {
  return (
    <Link
      href="/dashboard"
      className="flex items-center rounded-full bg-zinc-800/50 p-1 ring-1 ring-zinc-800 backdrop-blur-sm transition duration-200 active:scale-125 active:bg-zinc-200/20"
    >
      <ChevronLeft className="my-0.5 mr-1 h-8 w-8" />
    </Link>
  );
}
