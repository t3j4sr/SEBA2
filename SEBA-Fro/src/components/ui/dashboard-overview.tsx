import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { cn } from "@/lib/utils";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowDown, ArrowUp, Minus, Activity, DollarSign, Wallet, CreditCard } from 'lucide-react';

type IconType = React.ElementType | React.FunctionComponent<React.SVGProps<SVGSVGElement>>;
export type TrendType = 'up' | 'down' | 'neutral';

export interface DashboardMetricCardProps {
  value: string;
  title: string;
  icon?: IconType;
  trendChange?: string;
  trendType?: TrendType;
  className?: string;
}

const DashboardMetricCard: React.FC<DashboardMetricCardProps> = ({
  value,
  title,
  icon: IconComponent,
  trendChange,
  trendType = 'neutral',
  className,
}) => {
  const TrendIcon = trendType === 'up' ? ArrowUp : trendType === 'down' ? ArrowDown : Minus;
  const trendColorClass =
    trendType === 'up'
      ? "text-emerald-500"
      : trendType === 'down'
      ? "text-rose-500"
      : "text-zinc-500";

  return (
    <motion.div
      whileHover={{ y: -4, boxShadow: "0 10px 15px -3px rgb(0 0 0 / 0.2), 0 4px 6px -4px rgb(0 0 0 / 0.1)" }}
      transition={{ type: "spring", stiffness: 400, damping: 20 }}
      className={cn("cursor-pointer rounded-lg", className)}
    >
      <Card className="h-full transition-colors duration-200">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium text-zinc-400">
            {title}
          </CardTitle>
          {IconComponent && (
            <IconComponent className="h-4 w-4 text-zinc-500" aria-hidden="true" />
          )}
        </CardHeader>
        <CardContent>
          <div className="text-3xl font-bold text-white mb-2 tracking-tight">{value}</div>
          {trendChange && (
            <p className={cn("flex items-center text-xs font-medium", trendColorClass)}>
              <TrendIcon className="h-3 w-3 mr-1" aria-hidden="true" />
              {trendChange} {trendType === 'up' ? "increase" : trendType === 'down' ? "decrease" : "change"}
            </p>
          )}
        </CardContent>
      </Card>
    </motion.div>
  );
};

export function SebaDashboardOverview() {
  const [stats, setStats] = useState({
    transactions: 0,
    balance: 0,
    income: 0,
    spent: 0,
    currency: '₹'
  });

  const loadData = () => {
    const savedTx = localStorage.getItem('seba_transactions');
    const userData = localStorage.getItem('seba_user_data');
    let currency = '₹';
    if(userData) {
      currency = JSON.parse(userData).currency || '₹';
    }

    if (savedTx) {
      const txData = JSON.parse(savedTx);
      let income = 0;
      let spent = 0;
      txData.forEach((tx: any) => {
        if (tx.type === 'income') { income += tx.amount; }
        else { spent += tx.amount; }
      });
      setStats({
        transactions: txData.length,
        balance: income - spent,
        income,
        spent,
        currency
      });
    } else {
      setStats({ transactions: 0, balance: 0, income: 0, spent: 0, currency });
    }
  };

  useEffect(() => {
    loadData();
    window.addEventListener('seba-transactions-updated', loadData);
    return () => window.removeEventListener('seba-transactions-updated', loadData);
  }, []);

  return (
    <div className="w-full flex flex-col gap-6">
      {/* Metrics Section */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4 w-full relative">
        <DashboardMetricCard
          title="TOTAL SPENT"
          value={`${stats.currency}${stats.spent.toLocaleString()}`}
          icon={CreditCard}
          trendType="neutral"
          className="bg-zinc-900/40 border-zinc-800"
        />
        <DashboardMetricCard
          title="THIS MONTH"
          value={`${stats.currency}${(stats.spent * 0.4).toLocaleString()}`} // Mocked month value for demo
          icon={Wallet}
          className="bg-zinc-900/40 border-zinc-800"
        />
        <DashboardMetricCard
          title="TRANSACTIONS"
          value={stats.transactions.toString()}
          icon={Activity}
          className="bg-zinc-900/40 border-zinc-800"
        />
        <DashboardMetricCard
          title="IMPULSIVE"
          value="0"
          icon={Activity}
          trendType="down"
          className="bg-zinc-900/40 border-zinc-800"
        />
      </div>
    </div>
  );
}
