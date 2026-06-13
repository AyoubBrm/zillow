import React from 'react';
import { Search } from 'lucide-react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
  icon?: React.ReactNode;
  variant?: 'default' | 'search';
  containerClassName?: string;
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, helperText, icon, variant = 'default', containerClassName = '', className = '', id, ...props }, ref) => {
    const inputId = id || label?.toLowerCase().replace(/\s+/g, '-');
    const isSearch = variant === 'search';

    return (
      <div className={`space-y-1.5 ${containerClassName}`}>
        {label && (
          <label htmlFor={inputId} className="block text-sm font-medium text-slate-300">
            {label}
          </label>
        )}
        <div className="relative">
          {(icon || isSearch) && (
            <div className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none">
              {isSearch ? <Search className="w-4 h-4" /> : icon}
            </div>
          )}
          <input
            ref={ref}
            id={inputId}
            className={`
              w-full bg-slate-800/50 border border-slate-700/50 rounded-xl
              text-slate-100 placeholder-slate-500
              transition-all duration-200
              focus:outline-none focus:border-violet-500/50 focus:ring-2 focus:ring-violet-500/20 focus:bg-slate-800/80
              hover:border-slate-600/50
              disabled:opacity-50 disabled:cursor-not-allowed
              ${icon || isSearch ? 'pl-10' : 'pl-4'}
              pr-4 py-2.5 text-sm
              ${error ? 'border-rose-500/50 focus:border-rose-500/50 focus:ring-rose-500/20' : ''}
              ${className}
            `}
            {...props}
          />
        </div>
        {error && (
          <p className="text-xs text-rose-400 flex items-center gap-1 mt-1">
            <span className="inline-block w-1 h-1 bg-rose-400 rounded-full" />
            {error}
          </p>
        )}
        {helperText && !error && (
          <p className="text-xs text-slate-500 mt-1">{helperText}</p>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';

export default Input;
