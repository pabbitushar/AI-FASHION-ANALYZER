import React from 'react';
import { AnimatePresence } from 'framer-motion';
import { DemoBanner } from './DemoBanner';

interface LayoutProps {
  children: React.ReactNode;
  isDemo?: boolean;
}

export const Layout: React.FC<LayoutProps> = ({ children, isDemo = false }) => {
  return (
    <div className="min-h-screen bg-[var(--color-background)] flex flex-col relative">
      {isDemo && <DemoBanner />}
      
      <header className="w-full max-w-7xl mx-auto px-6 py-6 flex items-center justify-between z-10 relative">
        <div className="flex items-center gap-2 cursor-pointer select-none" onClick={() => window.location.reload()}>
          <h1 className="text-2xl font-bold tracking-tight text-[var(--color-primary)]">
            StyleSense
          </h1>
          <span className="bg-[var(--color-accent)] text-white text-xs font-semibold px-2 py-0.5 rounded-full uppercase tracking-wider">
            AI
          </span>
        </div>
      </header>

      <main className="flex-1 w-full max-w-7xl mx-auto px-6 pb-12 flex flex-col items-center">
        <AnimatePresence mode="wait">
          {children}
        </AnimatePresence>
      </main>
    </div>
  );
};
