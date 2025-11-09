import React, { useState } from 'react';
import SparklesIcon from './icons/SparklesIcon';
import { VoiceName, VoiceOption } from '../types';

interface TopicInputProps {
  onGenerate: (topic: string, duration: number, voice: VoiceName) => void;
  isLoading: boolean;
}

type VideoDurationType = 'shorts' | 'medium' | 'long';

interface DurationOption {
  label: string;
  value: VideoDurationType;
  minutes: number;
  description: string;
}

const durationOptions: DurationOption[] = [
  { label: 'Shorts', value: 'shorts', minutes: 1, description: '~1 min (2-4 scenes)' },
  { label: 'Medium', value: 'medium', minutes: 2, description: '~2 min (7-8 scenes)' },
  { label: 'Long', value: 'long', minutes: 5, description: '~5 min (17-18 scenes)' },
];

const voiceOptions: VoiceOption[] = [
  // Female voices
  { name: "Aoede", gender: "Female", description: "Breezy and natural" },
  { name: "Kore", gender: "Female", description: "Firm and confident" },
  { name: "Leda", gender: "Female", description: "Youthful and energetic" },
  { name: "Zephyr", gender: "Female", description: "Bright and cheerful" },
  // Male voices
  { name: "Puck", gender: "Male", description: "Upbeat and energetic" },
  { name: "Charon", gender: "Male", description: "Informative and clear" },
  { name: "Fenrir", gender: "Male", description: "Excitable and dynamic" },
  { name: "Orus", gender: "Male", description: "Deep and resonant" },
];

const TopicInput: React.FC<TopicInputProps> = ({ onGenerate, isLoading }) => {
  const [topic, setTopic] = useState('');
  const [durationType, setDurationType] = useState<VideoDurationType>('shorts');
  const [selectedVoice, setSelectedVoice] = useState<VoiceName>('Kore');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (topic.trim() && !isLoading) {
      const selectedOption = durationOptions.find(opt => opt.value === durationType);
      onGenerate(topic, selectedOption?.minutes || 1, selectedVoice);
    }
  };

  return (
    <div className="w-full max-w-3xl mx-auto">
      <h2 className="text-3xl font-bold text-center text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-indigo-600 mb-4">
        AI Video Weaver
      </h2>
      <p className="text-center text-gray-400 mb-8">Enter a topic and desired duration, and we'll weave a video storyboard for you.</p>
      <form onSubmit={handleSubmit} className="flex flex-col items-center gap-6">
        <div className="flex flex-col w-full gap-4">
          <input
            type="text"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="e.g., The last day of the dinosaurs, a science story"
            className="w-full bg-gray-800 border border-gray-700 rounded-lg py-3 px-4 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-300"
            disabled={isLoading}
          />

          <div className="w-full">
            <label className="text-gray-300 font-medium mb-3 block">Video Duration:</label>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              {durationOptions.map((option) => (
                <button
                  key={option.value}
                  type="button"
                  onClick={() => setDurationType(option.value)}
                  disabled={isLoading}
                  className={`relative p-4 rounded-lg border-2 transition-all duration-200 text-left ${
                    durationType === option.value
                      ? 'border-indigo-500 bg-indigo-600/20 shadow-lg shadow-indigo-500/20'
                      : 'border-gray-700 bg-gray-800 hover:border-gray-600 hover:bg-gray-750'
                  } ${isLoading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
                >
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-bold text-lg text-white">{option.label}</span>
                    {durationType === option.value && (
                      <div className="w-5 h-5 bg-indigo-500 rounded-full flex items-center justify-center">
                        <svg className="w-3 h-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                        </svg>
                      </div>
                    )}
                  </div>
                  <p className="text-sm text-gray-400">{option.description}</p>
                </button>
              ))}
            </div>
          </div>

          <div className="w-full">
            <label className="text-gray-300 font-medium mb-3 block">Voice Narrator:</label>
            <div className="grid grid-cols-1 gap-3">
              {/* Female Voices */}
              <div>
                <p className="text-sm text-gray-400 mb-2 font-semibold">Female Voices</p>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                  {voiceOptions.filter(v => v.gender === "Female").map((voice) => (
                    <button
                      key={voice.name}
                      type="button"
                      onClick={() => setSelectedVoice(voice.name)}
                      disabled={isLoading}
                      className={`relative p-3 rounded-lg border-2 transition-all duration-200 text-left ${
                        selectedVoice === voice.name
                          ? 'border-pink-500 bg-pink-600/20 shadow-lg shadow-pink-500/20'
                          : 'border-gray-700 bg-gray-800 hover:border-gray-600 hover:bg-gray-750'
                      } ${isLoading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
                    >
                      <div className="flex items-center justify-between mb-1">
                        <span className="font-semibold text-sm text-white">{voice.name}</span>
                        {selectedVoice === voice.name && (
                          <div className="w-4 h-4 bg-pink-500 rounded-full flex items-center justify-center">
                            <svg className="w-2.5 h-2.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                            </svg>
                          </div>
                        )}
                      </div>
                      <p className="text-xs text-gray-400">{voice.description}</p>
                    </button>
                  ))}
                </div>
              </div>

              {/* Male Voices */}
              <div>
                <p className="text-sm text-gray-400 mb-2 font-semibold">Male Voices</p>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                  {voiceOptions.filter(v => v.gender === "Male").map((voice) => (
                    <button
                      key={voice.name}
                      type="button"
                      onClick={() => setSelectedVoice(voice.name)}
                      disabled={isLoading}
                      className={`relative p-3 rounded-lg border-2 transition-all duration-200 text-left ${
                        selectedVoice === voice.name
                          ? 'border-blue-500 bg-blue-600/20 shadow-lg shadow-blue-500/20'
                          : 'border-gray-700 bg-gray-800 hover:border-gray-600 hover:bg-gray-750'
                      } ${isLoading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
                    >
                      <div className="flex items-center justify-between mb-1">
                        <span className="font-semibold text-sm text-white">{voice.name}</span>
                        {selectedVoice === voice.name && (
                          <div className="w-4 h-4 bg-blue-500 rounded-full flex items-center justify-center">
                            <svg className="w-2.5 h-2.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                            </svg>
                          </div>
                        )}
                      </div>
                      <p className="text-xs text-gray-400">{voice.description}</p>
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>

        <button
          type="submit"
          disabled={isLoading || !topic.trim()}
          className="flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-900 disabled:text-gray-400 disabled:cursor-not-allowed text-white font-bold py-3 px-6 rounded-lg transition duration-300 w-full sm:w-auto"
        >
          <SparklesIcon className="w-5 h-5" />
          {isLoading ? 'Weaving...' : 'Generate Storyboard'}
        </button>
      </form>
    </div>
  );
};

export default TopicInput;