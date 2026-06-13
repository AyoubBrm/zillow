import React, { useState, useRef, useEffect } from 'react';

interface DropdownItem {
  id: string;
  label: string;
  icon?: React.ReactNode;
  danger?: boolean;
  divider?: boolean;
  onClick?: () => void;
}

interface DropdownProps {
  trigger: React.ReactNode;
  items: DropdownItem[];
  align?: 'left' | 'right';
  className?: string;
  id?: string;
}

const Dropdown: React.FC<DropdownProps> = ({ trigger, items, align = 'right', className = '', id }) => {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <div className={`relative ${className}`} ref={dropdownRef} id={id}>
      <div onClick={() => setIsOpen(!isOpen)} className="cursor-pointer">
        {trigger}
      </div>

      {isOpen && (
        <div
          className={`
            absolute top-full mt-2 z-50
            ${align === 'right' ? 'right-0' : 'left-0'}
            min-w-[200px]
            bg-slate-900/95 backdrop-blur-xl
            border border-white/10 rounded-xl
            shadow-2xl shadow-black/50
            animate-scaleIn origin-top-right
            py-1.5
          `}
        >
          {items.map((item) => {
            if (item.divider) {
              return <div key={item.id} className="my-1.5 border-t border-slate-700/50" />;
            }
            return (
              <button
                key={item.id}
                onClick={() => {
                  item.onClick?.();
                  setIsOpen(false);
                }}
                className={`
                  w-full flex items-center gap-3 px-4 py-2 text-sm
                  transition-colors duration-150
                  ${
                    item.danger
                      ? 'text-rose-400 hover:bg-rose-500/10'
                      : 'text-slate-300 hover:bg-white/5 hover:text-slate-100'
                  }
                `}
                id={`${id}-${item.id}`}
              >
                {item.icon && <span className="flex-shrink-0">{item.icon}</span>}
                {item.label}
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default Dropdown;
