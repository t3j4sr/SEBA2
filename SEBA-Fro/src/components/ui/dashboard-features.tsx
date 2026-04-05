import React from 'react';
import { motion } from 'framer-motion';
import { cn } from "@/lib/utils";

export function SebaDashboardFeatures() {
  const features = [
    { title: "Financial Coach", desc: "Personalised advice & health score", icon: "🧠", color: "from-pink-500/20 to-rose-500/20" },
    { title: "Predictions", desc: "Future forecasts & calendar alerts", icon: "🔮", color: "from-indigo-500/20 to-purple-500/20", badge: "NEW" },
    { title: "Tax Tips", desc: "Deductions & tax-saving ideas", icon: "📋", color: "from-amber-500/20 to-orange-500/20" },
    { title: "Credit Cards", desc: "Best cards for your habits", icon: "💳", color: "from-blue-500/20 to-cyan-500/20" },
    { title: "Loan Guide", desc: "Eligibility & recommendations", icon: "🏛️", color: "from-slate-500/20 to-zinc-500/20" },
    { title: "Investments", desc: "Grow your surplus wisely", icon: "📈", color: "from-emerald-500/20 to-teal-500/20" },
    { title: "Analytics", desc: "Yearly insights & patterns", icon: "📊", color: "from-violet-500/20 to-fuchsia-500/20" },
  ];

  return (
    <div className="w-full flex flex-col gap-4">
      {/* Features Heading */}
      <div className="flex flex-col gap-2">
        <h2 className="text-[10px] font-bold tracking-[0.2em] text-zinc-500 uppercase">EXPLORE FEATURES</h2>
      </div>

      {/* Features Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {features.map((f, i) => (
          <motion.div
            key={i}
            whileHover={{ y: -5, scale: 1.02 }}
            className={cn(
              "group relative p-6 rounded-2xl border border-zinc-800/50 bg-zinc-900/20 backdrop-blur-sm cursor-pointer overflow-hidden transition-all duration-300",
              "hover:border-zinc-700/50 hover:bg-zinc-800/30"
            )}
          >
            {/* Background Glow */}
            <div className={cn("absolute inset-0 bg-gradient-to-br opacity-0 group-hover:opacity-10 transition-opacity duration-500", f.color)} />
            
            <div className="relative z-10 flex flex-col items-center text-center gap-3">
              <span className="text-3xl mb-1">{f.icon}</span>
              <div className="flex items-center gap-2">
                <h3 className="font-semibold text-white text-sm">{f.title}</h3>
                {f.badge && (
                  <span className="px-1.5 py-0.5 rounded-md bg-emerald-500/10 text-emerald-500 text-[8px] font-bold tracking-wider">
                    {f.badge}
                  </span>
                )}
              </div>
              <p className="text-zinc-500 text-xs leading-relaxed max-w-[150px]">
                {f.desc}
              </p>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
