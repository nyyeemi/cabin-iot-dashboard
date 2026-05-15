import LoginForm from '@/app/ui/login-form';
import { Suspense } from 'react';

export default function LoginPage() {
  return (
    <main className="bg-background flex items-center justify-center">
      <div className="relative mx-auto flex w-full max-w-100 flex-col space-y-2.5 p-4">
        <div>
          <p>Login</p>
        </div>
        <Suspense>
          <LoginForm />
        </Suspense>
      </div>
    </main>
  );
}
