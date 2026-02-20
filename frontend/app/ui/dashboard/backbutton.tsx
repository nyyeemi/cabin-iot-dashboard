'use client';

import { ChevronLeft } from 'lucide-react';
import { useRouter } from 'next/navigation';

export default function BackButton() {
  const router = useRouter();

  return (
    <button
      onClick={() => router.back()}
      className="flex items-center transition-opacity active:opacity-70"
    >
      <ChevronLeft className="mr-1 h-8 w-8" />
      <span>Overview</span>
    </button>
  );
}
