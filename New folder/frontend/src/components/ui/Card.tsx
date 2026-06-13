import React from 'react';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  hover?: boolean;
  gradient?: boolean;
  padding?: 'none' | 'sm' | 'md' | 'lg';
  onClick?: () => void;
  id?: string;
}

const paddingClasses = {
  none: '',
  sm: 'p-4',
  md: 'p-6',
  lg: 'p-8',
};

const Card: React.FC<CardProps> = ({
  children,
  className = '',
  hover = true,
  gradient = false,
  padding = 'md',
  onClick,
  id,
}) => {
  return (
    <div
      id={id}
      onClick={onClick}
      className={`
        ${hover ? 'glass-card' : 'glass-card-static'}
        ${gradient ? 'gradient-border' : ''}
        ${paddingClasses[padding]}
        ${onClick ? 'cursor-pointer' : ''}
        ${className}
      `}
    >
      {children}
    </div>
  );
};

export default Card;

interface CardHeaderProps {
  children: React.ReactNode;
  className?: string;
}

export const CardHeader: React.FC<CardHeaderProps> = ({ children, className = '' }) => (
  <div className={`mb-4 ${className}`}>{children}</div>
);

export const CardTitle: React.FC<CardHeaderProps> = ({ children, className = '' }) => (
  <h3 className={`text-lg font-semibold text-slate-100 ${className}`}>{children}</h3>
);

export const CardDescription: React.FC<CardHeaderProps> = ({ children, className = '' }) => (
  <p className={`text-sm text-slate-400 mt-1 ${className}`}>{children}</p>
);

export const CardContent: React.FC<CardHeaderProps> = ({ children, className = '' }) => (
  <div className={className}>{children}</div>
);
