import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { ChevronLeftIcon, UserPlus } from 'lucide-react';

export function SignupForm() {
  const [error, setError] = useState('');
  
  const triggerSignup = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError('');
    const form = e.currentTarget;
    const formData = new FormData(form);
    
    const pw1 = formData.get('password') as string;
    const pw2 = formData.get('confirmPassword') as string;

    if (pw1 !== pw2) {
      setError("Passwords do not match!");
      return;
    }

    const userData = {
      name: formData.get('name') as string,
      email: formData.get('email') as string,
      mobile: formData.get('mobile') as string,
      dob: formData.get('dob') as string,
      currency: formData.get('currency') as string,
      bank: formData.get('bank') as string,
      password: pw1 
    };

    localStorage.setItem('seba_user_data', JSON.stringify(userData));
    localStorage.setItem('seba_user_name', userData.name);
    localStorage.setItem('animate_welcome', 'true');
    
    window.location.href = 'index.html';
  };

  const triggerSocialSignup = (platform: string) => {
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
        <a href="login.html">
          <ChevronLeftIcon className="me-1 size-4" />
          Login
        </a>
      </Button>

      <div className="w-full space-y-6 pb-12">
        <div className="flex flex-col space-y-2 mb-8 mt-2">
          <h1 className="font-heading text-3xl font-bold tracking-wide text-white">
            Create an Account
          </h1>
          <p className="text-zinc-400 text-base">
            Complete your profile to join SEBA.
          </p>
        </div>
        
        <form onSubmit={triggerSignup} className="space-y-4">
          <input 
            type="text" name="name" placeholder="Full Name" required
            className="w-full px-4 py-3.5 rounded-xl bg-zinc-900 border border-white/10 text-white placeholder-zinc-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all text-sm"
          />
          <input 
            type="email" name="email" placeholder="Email Address" required
            className="w-full px-4 py-3.5 rounded-xl bg-zinc-900 border border-white/10 text-white placeholder-zinc-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all text-sm"
          />
          
          <div className="grid grid-cols-2 gap-4">
            <input 
              type="tel" name="mobile" placeholder="Mobile Number" required
              className="w-full px-4 py-3.5 rounded-xl bg-zinc-900 border border-white/10 text-white placeholder-zinc-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all text-sm"
            />
            <input 
              type="date" name="dob" 
              className="w-full px-4 py-3.5 rounded-xl bg-zinc-900 border border-white/10 text-zinc-400 focus:text-white placeholder-zinc-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all text-sm"
            />
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <select 
              name="currency" required
              className="w-full px-4 py-3.5 rounded-xl bg-zinc-900 border border-white/10 text-white focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all text-sm appearance-none"
            >
              <option value="" disabled selected>Currency</option>
              <option value="₹">₹ INR</option>
              <option value="$">$ USD</option>
              <option value="€">€ EUR</option>
            </select>
            <select 
              name="bank" required
              className="w-full px-4 py-3.5 rounded-xl bg-zinc-900 border border-white/10 text-white focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all text-sm appearance-none"
            >
              <option value="" disabled selected>Select Linked Bank</option>
              <option value="sbi">State Bank of India (SBI)</option>
              <option value="hdfc">HDFC Bank</option>
              <option value="icici">ICICI Bank</option>
              <option value="axis">Axis Bank</option>
              <option value="pnb">Punjab National Bank</option>
              <option value="kotak">Kotak Mahindra Bank</option>
            </select>
          </div>

          <input 
            type="password" name="password" placeholder="Password" required
            className="w-full px-4 py-3.5 rounded-xl bg-zinc-900 border border-white/10 text-white placeholder-zinc-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all text-sm"
          />
          <input 
            type="password" name="confirmPassword" placeholder="Confirm Password" required
            className="w-full px-4 py-3.5 rounded-xl bg-zinc-900 border border-white/10 text-white placeholder-zinc-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all text-sm"
          />

          <Button type="submit" size="lg" className="w-full h-12 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold mt-2">
            Sign Up
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
          <Button type="button" variant="outline" className="w-full rounded-xl h-11 bg-zinc-900/50 border-white/10 text-zinc-300 hover:bg-zinc-800 hover:text-white" onClick={() => triggerSocialSignup('Google')}>
            <GoogleIcon className="mr-2 h-4 w-4" />
            Google
          </Button>
          <Button type="button" variant="outline" className="w-full rounded-xl h-11 bg-zinc-900/50 border-white/10 text-zinc-300 hover:bg-zinc-800 hover:text-white" onClick={() => triggerSocialSignup('PhonePe')}>
            <PhonePeIcon className="mr-2 h-4 w-4" />
            PhonePe
          </Button>
          <Button type="button" variant="outline" className="w-full rounded-xl h-11 bg-zinc-900/50 border-white/10 text-zinc-300 hover:bg-zinc-800 hover:text-white" onClick={() => triggerSocialSignup('Google Pay')}>
            <GPayIcon className="mr-2 h-4 w-4" />
            GPay
          </Button>
        </div>

        <p className="text-zinc-400 mt-8 text-center text-sm">
          Already have an account?{' '}
          <a href="login.html" className="text-indigo-400 hover:text-indigo-300 font-medium hover:underline underline-offset-4">
            Log in here
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
