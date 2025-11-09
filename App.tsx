import React, { useState, useCallback } from 'react';
import { Scene, GroundingChunk, VoiceName } from './types';
import { generateStoryboard } from './services/geminiService';
import TopicInput from './components/TopicInput';
import Storyboard from './components/Storyboard';
import Loader from './components/Loader';

type View = 'TOPIC_INPUT' | 'STORYBOARD';

const App: React.FC = () => {
  const [view, setView] = useState<View>('TOPIC_INPUT');
  const [scenes, setScenes] = useState<Scene[]>([]);
  const [groundingSources, setGroundingSources] = useState<GroundingChunk[]>([]);
  const [selectedVoice, setSelectedVoice] = useState<VoiceName>('Kore');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleGenerate = useCallback(async (topic: string, duration: number, voice: VoiceName) => {
    setIsLoading(true);
    setError(null);
    setSelectedVoice(voice);
    try {
      const { scenes: newScenes, groundingChunks } = await generateStoryboard(topic, duration);
      setScenes(newScenes);
      setGroundingSources(groundingChunks);
      setView('STORYBOARD');
    } catch (err: any) {
      setError(err.message || 'An unknown error occurred.');
      setView('TOPIC_INPUT');
    } finally {
      setIsLoading(false);
    }
  }, []);

  const handleUpdateScene = useCallback((sceneId: number, updatedScene: Partial<Scene>) => {
    setScenes(prevScenes =>
      prevScenes.map(scene =>
        scene.id === sceneId ? { ...scene, ...updatedScene } : scene
      )
    );
  }, []);

  const handleDeleteScene = useCallback((sceneId: number) => {
    setScenes(prevScenes => {
      const filtered = prevScenes.filter(scene => scene.id !== sceneId);
      // Re-number the scenes to maintain sequential IDs
      return filtered.map((scene, index) => ({ ...scene, id: index + 1 }));
    });
  }, []);

  const handleReset = () => {
    setView('TOPIC_INPUT');
    setScenes([]);
    setGroundingSources([]);
    setError(null);
  };

  const renderContent = () => {
    if (isLoading && view === 'TOPIC_INPUT') {
      return <Loader text="Generating your storyboard... This may take a moment." />;
    }

    switch (view) {
      case 'STORYBOARD':
        return (
          <Storyboard
            scenes={scenes}
            updateScene={handleUpdateScene}
            deleteScene={handleDeleteScene}
            onReset={handleReset}
            groundingSources={groundingSources}
            selectedVoice={selectedVoice}
          />
        );
      case 'TOPIC_INPUT':
      default:
        return <TopicInput onGenerate={handleGenerate} isLoading={isLoading} />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-4 sm:p-8 font-sans">
      <main className="container mx-auto">
        <div className="flex flex-col items-center justify-center">
          {error && (
            <div className="bg-red-900/50 border border-red-700 text-red-300 px-4 py-3 rounded-lg relative mb-6 max-w-2xl w-full" role="alert">
              <strong className="font-bold">Error: </strong>
              <span className="block sm:inline">{error}</span>
            </div>
          )}
          {renderContent()}
        </div>
      </main>
    </div>
  );
};

export default App;