import React from 'react';

const SparklesIcon: React.FC<{ className?: string }> = ({ className }) => (
  <svg xmlns="http://www.w3.org/2000/svg" className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l-1.5 1.5M19.5 4.5L18 6m-12 6l-1.5 1.5M10.5 19.5L9 18m12-6h-4m2 2l-1.5-1.5M13.5 4.5L12 6m-5 13.5l1.5-1.5M18 13.5l1.5 1.5m-15-5a3 3 0 116 0 3 3 0 01-6 0zm12 0a3 3 0 116 0 3 3 0 01-6 0z" />
  </svg>
);

export default SparklesIcon;
