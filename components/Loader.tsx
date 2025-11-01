import React from 'react';

const Loader: React.FC<{ text?: string }> = ({ text = "Loading..." }) => (
  <div className="flex flex-col items-center justify-center space-y-2">
    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-400"></div>
    {text && <p className="text-sm text-gray-400">{text}</p>}
  </div>
);

export default Loader;
