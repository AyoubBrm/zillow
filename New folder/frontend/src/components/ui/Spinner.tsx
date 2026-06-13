import React from 'react';
import { Loader2 } from 'lucide-react';

interface SpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

const sizeClasses = {
  sm: 'w-4 h-4',
  md: 'w-6 h-6',
  lg: 'w-10 h-10',
};

const Spinner: React.FC<SpinnerProps> = ({ size = 'md', className = '' }) => {
  return (
    <Loader2 className={`animate-spin text-violet-400 ${sizeClasses[size]} ${className}`} />
  );
};

export default Spinner;

export const FullPageSpinner: React.FC = () => (
  <div className="flex items-center justify-center min-h-screen bg-[#0a0e1a]">
    <div className="flex flex-col items-center gap-4">
      <div className="relative">
        <div className="w-12 h-12 rounded-full border-2 border-violet-500/20 border-t-violet-500 animate-spin" />
        <div className="absolute inset-0 w-12 h-12 rounded-full border-2 border-transparent border-b-indigo-500/50 animate-spin" style={{ animationDirection: 'reverse', animationDuration: '1.5s' }} />
      </div>
      <p className="text-sm text-slate-400 animate-pulse">Loading LedgerAI...</p>
    </div>
  </div>
);
