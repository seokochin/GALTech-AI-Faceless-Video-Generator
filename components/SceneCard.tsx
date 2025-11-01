import React, { useState, useCallback, useRef, useEffect } from 'react';
import { Scene, AspectRatio } from '../types';
import { generateImage, editImage, generateSpeech } from '../services/geminiService';
// FIX: Import createWavBlob to correctly format audio for playback.
import { decode, createWavBlob } from '../utils/audioUtils';
import Loader from './Loader';
import ImageIcon from './icons/ImageIcon';
import MicIcon from './icons/MicIcon';
import SparklesIcon from './icons/SparklesIcon';

interface SceneCardProps {
  scene: Scene;
  updateScene: (sceneId: number, updatedScene: Partial<Scene>) => void;
  aspectRatio: AspectRatio;
  imageStyle: string;
  isGeneratingImage?: boolean;
  isGeneratingAudio?: boolean;
}

const SceneCard: React.FC<SceneCardProps> = ({ scene, updateScene, aspectRatio, imageStyle, isGeneratingImage: externalGeneratingImage, isGeneratingAudio: externalGeneratingAudio }) => {
  const [isGeneratingImage, setIsGeneratingImage] = useState(false);
  const [isGeneratingAudio, setIsGeneratingAudio] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [editPrompt, setEditPrompt] = useState("");
  const [error, setError] = useState<string | null>(null);
  const cardRef = useRef<HTMLDivElement>(null);

  // Combine external and internal loading states
  const showImageLoading = isGeneratingImage || externalGeneratingImage;
  const showAudioLoading = isGeneratingAudio || externalGeneratingAudio;

  // Scroll to this card when it starts generating
  useEffect(() => {
    if (showImageLoading || showAudioLoading) {
      cardRef.current?.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }, [showImageLoading, showAudioLoading]);

  const handleGenerateImage = useCallback(async () => {
    setIsGeneratingImage(true);
    setError(null);
    try {
      const finalPrompt = imageStyle !== 'Default'
        ? `${scene.imagePrompt}, in a ${imageStyle.toLowerCase()} style`
        : scene.imagePrompt;
      const { base64Image, mimeType } = await generateImage(finalPrompt, aspectRatio);
      const imageUrl = `data:${mimeType};base64,${base64Image}`;
      updateScene(scene.id, { imageUrl, imageMimeType: mimeType });
    } catch (err) {
      setError("Failed to generate image. Please try again.");
      console.error(err);
    } finally {
      setIsGeneratingImage(false);
    }
  }, [scene.id, scene.imagePrompt, updateScene, aspectRatio, imageStyle]);

  const handleEditImage = useCallback(async () => {
    if (!scene.imageUrl || !scene.imageMimeType || !editPrompt) return;
    setIsEditing(true);
    setError(null);
    try {
      const originalBase64 = scene.imageUrl.split(',')[1];
      const { base64Image, mimeType } = await editImage(originalBase64, scene.imageMimeType, editPrompt);
      const newImageUrl = `data:${mimeType};base64,${base64Image}`;
      updateScene(scene.id, { imageUrl: newImageUrl, imageMimeType: mimeType });
      setEditPrompt("");
    } catch (err) {
      setError("Failed to edit image. Please try again.");
      console.error(err);
    } finally {
      setIsEditing(false);
    }
  }, [scene.id, scene.imageUrl, scene.imageMimeType, editPrompt, updateScene]);

  const handleGenerateAudio = useCallback(async () => {
    setIsGeneratingAudio(true);
    setError(null);
    try {
      const base64Audio = await generateSpeech(scene.voiceOver);
      const audioBytes = decode(base64Audio);
      // FIX: Use createWavBlob to create a playable WAV file from raw PCM data. The sample rate for TTS is 24000.
      const blob = createWavBlob(audioBytes, 24000);
      const audioUrl = URL.createObjectURL(blob);

      // Also store the base64 WAV data for server upload
      const reader = new FileReader();
      reader.onloadend = () => {
        const base64Wav = reader.result as string;
        updateScene(scene.id, { audioUrl, audioBase64: base64Wav });
      };
      reader.readAsDataURL(blob);
    } catch (err) {
      setError("Failed to generate audio. Please try again.");
      console.error(err);
    } finally {
      setIsGeneratingAudio(false);
    }
  }, [scene.id, scene.voiceOver, updateScene]);

  // Determine if this card should have animation
  const isActivelyGenerating = showImageLoading || showAudioLoading;

  return (
    <div
      ref={cardRef}
      className={`bg-gray-800 rounded-xl overflow-hidden shadow-lg transition-all duration-300 ${
        isActivelyGenerating
          ? 'ring-4 ring-indigo-500 ring-offset-2 ring-offset-gray-900 animate-pulse shadow-indigo-500/50'
          : 'hover:shadow-indigo-500/20'
      }`}
    >
      <div className="p-6">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-lg font-bold text-indigo-400">Scene {scene.id}</h3>
          {isActivelyGenerating && (
            <div className="flex items-center gap-2 text-sm text-indigo-300">
              <svg className="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span>{showImageLoading ? 'Generating Image...' : 'Generating Audio...'}</span>
            </div>
          )}
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Left Column: Image and Actions */}
          <div className="flex flex-col gap-4">
            <div className={`aspect-video bg-gray-700 rounded-lg flex items-center justify-center relative ${
              showImageLoading ? 'ring-2 ring-indigo-400 animate-pulse' : ''
            }`}>
              {showImageLoading ? (
                <div className="flex flex-col items-center gap-2">
                  <Loader text="Generating image..." />
                  <div className="text-xs text-indigo-300 animate-pulse">✨ AI creating visuals...</div>
                </div>
              ) : scene.imageUrl ? (
                <img src={scene.imageUrl} alt={`Scene ${scene.id}`} className="w-full h-full object-cover rounded-lg" />
              ) : (
                <div className="text-center text-gray-400">
                  <ImageIcon className="w-12 h-12 mx-auto mb-2"/>
                  <p>Generate an image</p>
                </div>
              )}
            </div>
            {!scene.imageUrl && (
              <button onClick={handleGenerateImage} disabled={isGeneratingImage} className="w-full flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-900 text-white font-semibold py-2 px-4 rounded-lg transition">
                <ImageIcon className="w-5 h-5"/> Generate Image
              </button>
            )}
            {scene.imageUrl && (
              <div className="flex flex-col gap-2">
                <input
                  type="text"
                  value={editPrompt}
                  onChange={(e) => setEditPrompt(e.target.value)}
                  placeholder="e.g., add a retro filter"
                  className="w-full bg-gray-700 border border-gray-600 rounded-md py-2 px-3 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  disabled={isEditing}
                />
                <button onClick={handleEditImage} disabled={!editPrompt || isEditing} className="w-full flex items-center justify-center gap-2 bg-purple-600 hover:bg-purple-700 disabled:bg-purple-900 text-white font-semibold py-2 px-4 rounded-lg transition">
                  <SparklesIcon className="w-5 h-5" /> {isEditing ? "Editing..." : "Edit Image"}
                </button>
              </div>
            )}
          </div>
          {/* Right Column: Text and Audio */}
          <div className="flex flex-col gap-4">
            <div>
              <label className="text-sm font-semibold text-gray-400">Caption:</label>
              <p className="text-gray-300 bg-gray-700/50 p-2 rounded-md mt-1">{scene.caption}</p>
            </div>
            <div>
              <label className="text-sm font-semibold text-gray-400">Voice-over:</label>
              <p className="text-gray-300 bg-gray-700/50 p-2 rounded-md mt-1 text-sm">{scene.voiceOver}</p>
            </div>
             <div className={`mt-auto ${showAudioLoading ? 'ring-2 ring-teal-400 rounded-lg p-3 animate-pulse' : ''}`}>
              {showAudioLoading ? (
                <div className="flex flex-col items-center gap-2 py-4">
                  <Loader text="Generating audio..."/>
                  <div className="text-xs text-teal-300 animate-pulse">🎙️ AI synthesizing voice...</div>
                </div>
              ) : scene.audioUrl ? (
                <div className="flex flex-col gap-2">
                  <audio controls src={scene.audioUrl} className="w-full" />
                  <div className="text-xs text-green-400 text-center">✓ Audio ready</div>
                </div>
              ) : (
                <button onClick={handleGenerateAudio} disabled={showAudioLoading} className="w-full flex items-center justify-center gap-2 bg-teal-600 hover:bg-teal-700 disabled:bg-teal-900 text-white font-semibold py-2 px-4 rounded-lg transition">
                  <MicIcon className="w-5 h-5" /> Generate Voice
                </button>
              )}
            </div>
          </div>
        </div>
        {error && <p className="text-red-400 text-sm mt-4 text-center">{error}</p>}
      </div>
    </div>
  );
};

export default SceneCard;