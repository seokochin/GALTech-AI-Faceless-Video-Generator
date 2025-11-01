import React, { useState, useEffect, useRef } from 'react';
import { Scene } from '../types';

interface VideoPreviewerProps {
  scenes: Scene[];
  onClose: () => void;
}

const VideoPreviewer: React.FC<VideoPreviewerProps> = ({ scenes, onClose }) => {
  const [currentSceneIndex, setCurrentSceneIndex] = useState(0);
  const audioRef = useRef<HTMLAudioElement>(null);

  const currentScene = scenes[currentSceneIndex];

  useEffect(() => {
    const audioEl = audioRef.current;
    
    if (audioEl && currentScene.audioUrl) {
      audioEl.src = currentScene.audioUrl;
      audioEl.play().catch(e => console.error("Audio playback failed", e));
    }
    
    const handleAudioEnd = () => {
      if (currentSceneIndex < scenes.length - 1) {
        setCurrentSceneIndex(prev => prev + 1);
      }
    };
    
    audioEl?.addEventListener('ended', handleAudioEnd);
    
    return () => {
      audioEl?.removeEventListener('ended', handleAudioEnd);
    };
  }, [currentSceneIndex, scenes, currentScene.audioUrl]);

  if (!currentScene) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-80 flex items-center justify-center z-50" onClick={onClose}>
      <div className="bg-gray-900 rounded-lg shadow-2xl w-full max-w-4xl aspect-video relative flex flex-col overflow-hidden" onClick={e => e.stopPropagation()}>
        <div className="absolute top-4 right-4 z-10">
          <button onClick={onClose} className="bg-white/10 hover:bg-white/20 text-white rounded-full p-2 focus:outline-none">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {currentScene.imageUrl && (
          <img src={currentScene.imageUrl} alt={currentScene.caption} className="absolute inset-0 w-full h-full object-cover animate-fade-in" />
        )}
        
        <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/30 to-transparent"></div>
        
        <div className="relative mt-auto p-8 text-white">
           <p className="text-2xl md:text-4xl font-bold drop-shadow-lg animate-slide-up">{currentScene.caption}</p>
        </div>
        
        <div className="absolute bottom-4 left-4 right-4 flex items-center gap-4">
            <div className="w-full bg-white/20 rounded-full h-1.5">
                <div className="bg-indigo-400 h-1.5 rounded-full" style={{ width: `${((currentSceneIndex + 1) / scenes.length) * 100}%` }}></div>
            </div>
        </div>
        
        <audio ref={audioRef} hidden />
      </div>
       <style>{`
        @keyframes fade-in {
          from { opacity: 0; transform: scale(1.05); }
          to { opacity: 1; transform: scale(1); }
        }
        .animate-fade-in { animation: fade-in 1s ease-out forwards; }
        
        @keyframes slide-up {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .animate-slide-up { animation: slide-up 0.5s ease-out forwards; }
      `}</style>
    </div>
  );
};

export default VideoPreviewer;
