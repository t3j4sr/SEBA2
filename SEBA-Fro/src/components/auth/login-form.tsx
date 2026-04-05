import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { ChevronLeftIcon, Fingerprint } from 'lucide-react';

export function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const triggerLogin = (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    const savedDataStr = localStorage.getItem('seba_user_data');
    
    if (!savedDataStr) {
      setError("No account registered. Please sign up first.");
      return;
    }

    const savedData = JSON.parse(savedDataStr);
    
    if (savedData.email !== email) {
      setError("Email address not found.");
      return;
    }

    if (savedData.password !== password) {
      setError("Incorrect password. Please try again.");
      return;
    }

    localStorage.setItem('seba_user_name', savedData.name);
    localStorage.setItem('animate_welcome', 'true');
    window.location.href = 'index.html';
  };

  const triggerSocialLogin = (platform: string) => {
    localStorage.setItem('seba_user_name', `${platform} User`);
    localStorage.setItem('animate_welcome', 'true');
    window.location.href = 'index.html';
  };

  return (
    <>
      {error && (
        <div className="fixed top-6 right-6 bg-red-500/90 text-white px-4 py-3 rounded-lg shadow-lg z-50 flex items-center gap-2 animate-in fade-in slide-in-from-top-4">
          <p className="font-medium text-sm">{error}</p>
        </div>
      )}

      {/* Desktop/Mobile Back Button */}
      <Button variant="ghost" className="self-start -ml-3 mb-6 text-zinc-400 hover:text-white" asChild>
        <a href="index.html">
          <ChevronLeftIcon className="me-1 size-4" />
          Dashboard
        </a>
      </Button>

      <div className="w-full space-y-6">
        <div className="flex flex-col space-y-2 mb-8">
          <h1 className="font-heading text-3xl font-bold tracking-wide text-white">
            Sign In to SEBA
          </h1>
          <p className="text-zinc-400 text-base">
            Login to your SEBA account to continue.
          </p>
        </div>
        
        <form onSubmit={triggerLogin} className="space-y-4">
          <div className="space-y-4">
            <input 
              type="email" 
              placeholder="Email Address" 
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full px-4 py-3.5 rounded-xl bg-zinc-900 border border-white/10 text-white placeholder-zinc-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all text-sm"
            />
            <input 
              type="password" 
              placeholder="Password" 
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full px-4 py-3.5 rounded-xl bg-zinc-900 border border-white/10 text-white placeholder-zinc-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all text-sm"
            />
          </div>
          <Button type="submit" size="lg" className="w-full h-12 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold mt-2">
            Sign In
          </Button>
        </form>

        <div className="relative my-8">
          <div className="absolute inset-0 flex items-center">
            <span className="w-full border-t border-white/10" />
          </div>
          <div className="relative flex justify-center text-xs uppercase">
            <span className="bg-[#0a0a0a] px-3 text-zinc-500 font-medium tracking-wider">Or continue with</span>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <Button type="button" variant="outline" className="w-full rounded-xl h-11 bg-zinc-900/50 border-white/10 text-zinc-300 hover:bg-zinc-800 hover:text-white" onClick={() => triggerSocialLogin('Google')}>
            <GoogleIcon className="mr-2 h-4 w-4" />
            Google
          </Button>
          <Button type="button" variant="outline" className="w-full rounded-xl h-11 bg-zinc-900/50 border-white/10 text-zinc-300 hover:bg-zinc-800 hover:text-white" onClick={() => triggerSocialLogin('PhonePe')}>
            <PhonePeIcon className="mr-2 h-4 w-4" />
            PhonePe
          </Button>
          <Button type="button" variant="outline" className="w-full rounded-xl h-11 bg-zinc-900/50 border-white/10 text-zinc-300 hover:bg-zinc-800 hover:text-white" onClick={() => triggerSocialLogin('Google Pay')}>
            <GPayIcon className="mr-2 h-4 w-4" />
            GPay
          </Button>
        </div>

        <p className="text-zinc-400 mt-6 text-center text-sm">
          Don't have an account?{' '}
          <a href="signup.html" className="text-indigo-400 hover:text-indigo-300 font-medium hover:underline underline-offset-4">
            Sign up here
          </a>
        </p>
      </div>
    </>
  );
}

const GoogleIcon = (props: React.ComponentProps<'svg'>) => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" {...props}>
    <path d="M12.479 14.265v-3.279h11.049c.108.571.164 1.247.164 1.979 0 2.46-.672 5.502-2.84 7.669C18.744 22.829 16.051 24 12.483 24 5.869 24 .308 18.613.308 12S5.869 0 12.483 0c3.659 0 6.265 1.436 8.223 3.307L18.392 5.62c-1.404-1.317-3.307-2.341-5.913-2.341-4.83 0-8.606 3.89-8.606 8.721 3.132 0 4.916-1.258 6.059-2.401.927-.927 1.537-2.251 1.777-4.059H12.479z" />
  </svg>
);

const PhonePeIcon = (props: React.ComponentProps<'svg'>) => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" {...props}>
    <rect width="20" height="20" x="2" y="2" rx="5" fill="#5f259f" stroke="none" />
    <text x="12" y="16" fill="white" stroke="none" fontSize="12" fontWeight="bold" textAnchor="middle">पे</text>
  </svg>
);

const GPayIcon = (props: React.ComponentProps<'svg'>) => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" {...props}>
    <rect width="20" height="14" x="2" y="5" rx="3" fill="#ffffff" stroke="none" />
    <path d="M7 10h4M7 14h6" stroke="#4285f4" strokeWidth="2.5" />
    <circle cx="17" cy="12" r="2.5" fill="#34a853" stroke="none" />
  </svg>
);
