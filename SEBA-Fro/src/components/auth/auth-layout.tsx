import React from 'react';
import { Particles } from '@/components/ui/particles';
import { LayoutGridIcon } from 'lucide-react';

interface AuthLayoutProps {
  children: React.ReactNode;
}

export function AuthLayout({ children }: AuthLayoutProps) {
  return (
    <div className="relative min-h-screen w-full bg-[#0a0a0a] text-zinc-50 flex overflow-hidden">
      
      {/* Left Column (Graphic & Testimonial) */}
      <div className="hidden lg:flex lg:flex-col lg:w-1/2 relative bg-[#0a0a0a] border-r border-white/5 p-12 justify-between">
        <Particles
          color="#818cf8"
          quantity={120}
          ease={20}
          className="absolute inset-0 z-0"
        />
        
        {/* Background Graphic Overlay (Dark minimal waves) */}
        <div 
          className="absolute inset-0 z-0 opacity-30 bg-cover bg-center pointer-events-none mix-blend-screen"
          style={{ backgroundImage: "url('https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=2564&auto=format&fit=crop')" }}
        />
        <div className="absolute inset-0 bg-gradient-to-t from-[#0a0a0a] via-[#0a0a0a]/40 to-transparent z-0 pointer-events-none" />

        {/* Logo Section */}
        <div className="relative z-10 flex items-center gap-3">
          <LayoutGridIcon className="size-8 text-white" />
          <p className="text-2xl font-semibold tracking-wide">SEBA</p>
        </div>

        {/* Testimonial Section */}
        <div className="relative z-10 max-w-lg mb-8">
          <blockquote className="space-y-4">
            <p className="text-xl font-medium text-white leading-relaxed">
              "Decode Your Spending. Master Your Behaviour"
            </p>
            <footer className="text-base text-zinc-400 font-semibold tracking-wide">
              ~ Team SEBA
            </footer>
          </blockquote>
        </div>
      </div>

      {/* Right Column (Form Box) */}
      <div className="relative flex-1 flex flex-col h-screen overflow-hidden">
        <div
          aria-hidden
          className="absolute inset-0 isolate z-0 contain-strict pointer-events-none opacity-40 mix-blend-screen hidden lg:block"
        >
          <div className="bg-[radial-gradient(68.54%_68.72%_at_55.02%_31.46%,rgba(99,102,241,0.15)_0,rgba(79,70,229,0.05)_50%,transparent_80%)] absolute top-0 left-0 h-[320px] w-[140%] -translate-y-[87.5px] -rotate-45 rounded-full" />
          <div className="bg-[radial-gradient(50%_50%_at_50%_50%,rgba(99,102,241,0.1)_0,rgba(79,70,229,0.02)_80%,transparent_100%)] absolute top-0 left-0 h-[320px] w-[60%] [translate:5%_-50%] -rotate-45 rounded-full" />
        </div>
        
        {/* Full-width scrollable container */}
        <div className="relative z-10 w-full h-full overflow-y-auto overflow-x-hidden flex flex-col justify-center px-6 sm:px-12 custom-scrollbar">
          <div className="w-full max-w-[420px] mx-auto py-12 lg:py-16">
            {children}
          </div>
        </div>
      </div>
    </div>
  );
}
