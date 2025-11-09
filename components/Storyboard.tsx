import React, { useState, useEffect } from 'react';
import { Scene, AspectRatio, GroundingChunk, VoiceName } from '../types';
import SceneCard from './SceneCard';
import { generateImage, generateSpeech } from '../services/geminiService';
import { decode, createWavBlob } from '../utils/audioUtils';
import { generateVideoWithFFmpeg, downloadVideoFile, checkApiHealth } from '../services/videoApiService';

interface StoryboardProps {
  scenes: Scene[];
  updateScene: (sceneId: number, updatedScene: Partial<Scene>) => void;
  deleteScene: (sceneId: number) => void;
  onReset: () => void;
  groundingSources: GroundingChunk[];
  selectedVoice: VoiceName;
}

const imageStyles = ['Default', 'Photorealistic', 'Cinematic', 'Cartoon', 'Anime', 'Fantasy Art', 'Watercolor', 'Cyberpunk'];

const Storyboard: React.FC<StoryboardProps> = ({ scenes, updateScene, deleteScene, onReset, groundingSources, selectedVoice }) => {
  const [aspectRatio, setAspectRatio] = useState<AspectRatio>('16:9');
  const [imageStyle, setImageStyle] = useState<string>('Default');
  const [isRendering, setIsRendering] = useState(false);
  const [renderProgress, setRenderProgress] = useState(0);
  const [isGeneratingAll, setIsGeneratingAll] = useState(false);
  const [generationProgress, setGenerationProgress] = useState({ current: 0, total: 0, type: '' });
  const [ffmpegAvailable, setFfmpegAvailable] = useState(false);
  const [currentGeneratingScene, setCurrentGeneratingScene] = useState<{ sceneId: number, type: 'image' | 'audio' } | null>(null);
  const [enableCaptions, setEnableCaptions] = useState(true);

  const allAssetsGenerated = scenes.every(s => s.imageUrl && s.audioUrl);

  // Check if FFmpeg API is available on mount
  useEffect(() => {
    const checkFFmpeg = async () => {
      const available = await checkApiHealth();
      setFfmpegAvailable(available);
      if (available) {
        console.log('✅ FFmpeg API server is available');
      } else {
        console.error('❌ FFmpeg API server is not available. Please start the Python server.');
      }
    };
    checkFFmpeg();
  }, []);

  const handleGenerateAll = async () => {
    setIsGeneratingAll(true);
    const totalAssets = scenes.length * 2; // Each scene needs image + audio
    let completed = 0;

    try {
      for (const scene of scenes) {
        // Generate image if not exists
        if (!scene.imageUrl) {
          setCurrentGeneratingScene({ sceneId: scene.id, type: 'image' });
          setGenerationProgress({ current: completed, total: totalAssets, type: `Generating image for Scene ${scene.id}...` });
          try {
            const finalPrompt = imageStyle !== 'Default'
              ? `${scene.imagePrompt}, in a ${imageStyle.toLowerCase()} style`
              : scene.imagePrompt;
            const { base64Image, mimeType } = await generateImage(finalPrompt, aspectRatio);
            const imageUrl = `data:${mimeType};base64,${base64Image}`;
            updateScene(scene.id, { imageUrl, imageMimeType: mimeType });
          } catch (error) {
            console.error(`Failed to generate image for scene ${scene.id}:`, error);
          }
          completed++;
        } else {
          completed++;
        }

        // Generate audio if not exists
        if (!scene.audioUrl) {
          setCurrentGeneratingScene({ sceneId: scene.id, type: 'audio' });
          setGenerationProgress({ current: completed, total: totalAssets, type: `Generating audio for Scene ${scene.id}...` });
          try {
            const base64Audio = await generateSpeech(scene.voiceOver, selectedVoice);
            const audioBytes = decode(base64Audio);
            const blob = createWavBlob(audioBytes, 24000);
            const audioUrl = URL.createObjectURL(blob);

            // Also convert blob to base64 for server upload
            const reader = new FileReader();
            await new Promise<void>((resolve) => {
              reader.onloadend = () => {
                const audioBase64 = reader.result as string;
                updateScene(scene.id, { audioUrl, audioBase64 });
                resolve();
              };
              reader.readAsDataURL(blob);
            });
          } catch (error) {
            console.error(`Failed to generate audio for scene ${scene.id}:`, error);
          }
          completed++;
        } else {
          completed++;
        }
      }
      setGenerationProgress({ current: totalAssets, total: totalAssets, type: 'All assets generated!' });
      setCurrentGeneratingScene(null);
    } catch (error) {
      console.error("Error generating assets:", error);
      alert("An error occurred while generating assets. Please check the console for details.");
    } finally {
      setIsGeneratingAll(false);
      setCurrentGeneratingScene(null);
    }
  };

  const handleDownload = async () => {
    if (!allAssetsGenerated) {
      alert('Please generate all assets first!');
      return;
    }

    if (!ffmpegAvailable) {
      alert('FFmpeg server is not available. Please start the Python server with: python3 api_server.py');
      return;
    }

    setIsRendering(true);
    setRenderProgress(0);

    try {
      console.log('🎬 Generating video with FFmpeg...');
      setRenderProgress(10);

      const videoUrl = await generateVideoWithFFmpeg(
        scenes,
        aspectRatio,
        0.5, // transition duration
        30,  // fps
        `ai-video-${Date.now()}.mp4`,
        enableCaptions
      );

      setRenderProgress(90);

      // Download the video
      await downloadVideoFile(videoUrl, 'ai-video.mp4');
      setRenderProgress(100);

      console.log('✅ Video downloaded successfully!');

    } catch (error: any) {
      console.error("Failed to render video", error);
      alert(`Error generating video: ${error.message || error}\n\nPlease check:\n1. Python server is running\n2. FFmpeg is installed\n3. All assets are generated`);
    } finally {
      setIsRendering(false);
    }
  };

  return (
    <div className="w-full max-w-7xl mx-auto">
      <div className="flex flex-col sm:flex-row justify-between items-center mb-6 gap-4">
        <h2 className="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-indigo-600">Storyboard</h2>
        <div className="flex items-center gap-4 flex-wrap justify-center">
           <div className="flex items-center gap-2">
            <label htmlFor="aspectRatio" className="text-sm font-medium text-gray-300">Aspect Ratio:</label>
            <select
              id="aspectRatio"
              value={aspectRatio}
              onChange={(e) => setAspectRatio(e.target.value as AspectRatio)}
              className="bg-gray-700 border border-gray-600 rounded-md py-1 px-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            >
              <option value="16:9">16:9</option>
              <option value="9:16">9:16</option>
              <option value="1:1">1:1</option>
              <option value="4:3">4:3</option>
              <option value="3:4">3:4</option>
            </select>
          </div>
          <div className="flex items-center gap-2">
            <label htmlFor="imageStyle" className="text-sm font-medium text-gray-300">Image Style:</label>
            <select
              id="imageStyle"
              value={imageStyle}
              onChange={(e) => setImageStyle(e.target.value)}
              className="bg-gray-700 border border-gray-600 rounded-md py-1 px-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            >
              {imageStyles.map(style => <option key={style} value={style}>{style}</option>)}
            </select>
          </div>
          <div className="flex items-center gap-2">
            <label htmlFor="enableCaptions" className="text-sm font-medium text-gray-300">Captions:</label>
            <input
              type="checkbox"
              id="enableCaptions"
              checked={enableCaptions}
              onChange={(e) => setEnableCaptions(e.target.checked)}
              className="w-4 h-4 text-indigo-600 bg-gray-700 border-gray-600 rounded focus:ring-indigo-500 focus:ring-2"
            />
          </div>
          <button onClick={onReset} className="text-gray-400 hover:text-white transition">New Story</button>
        </div>
      </div>
      
      <div className="space-y-6 mb-8">
        {scenes.map(scene => (
          <SceneCard
            key={scene.id}
            scene={scene}
            updateScene={updateScene}
            deleteScene={deleteScene}
            aspectRatio={aspectRatio}
            imageStyle={imageStyle}
            selectedVoice={selectedVoice}
            isGeneratingImage={currentGeneratingScene?.sceneId === scene.id && currentGeneratingScene?.type === 'image'}
            isGeneratingAudio={currentGeneratingScene?.sceneId === scene.id && currentGeneratingScene?.type === 'audio'}
            canDelete={scenes.length > 1}
          />
        ))}
      </div>

      {groundingSources.length > 0 && (
        <div className="my-6 p-4 bg-gray-800 rounded-lg">
          <h4 className="font-semibold text-lg text-indigo-300 mb-2">Sources</h4>
          <ul className="list-disc list-inside text-sm space-y-1">
            {groundingSources.map((chunk, index) => chunk.web && (
              <li key={index}>
                <a href={chunk.web.uri} target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:underline">
                  {chunk.web.title}
                </a>
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="text-center mt-8 flex flex-col items-center gap-4">
        {!allAssetsGenerated && (
          <button
            onClick={handleGenerateAll}
            disabled={isGeneratingAll}
            className="bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-900 disabled:text-gray-400 disabled:cursor-not-allowed text-white font-bold py-3 px-8 rounded-lg transition text-lg flex items-center gap-2"
          >
            <svg className={`w-5 h-5 ${isGeneratingAll ? 'animate-spin' : ''}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            {isGeneratingAll ? 'Generating...' : 'Generate All Assets'}
          </button>
        )}

        {isGeneratingAll && (
          <div className="w-full max-w-md">
            <div className="bg-gray-800 rounded-lg p-4">
              <p className="text-sm text-gray-300 mb-2">{generationProgress.type}</p>
              <div className="w-full bg-gray-700 rounded-full h-2.5">
                <div
                  className="bg-indigo-500 h-2.5 rounded-full transition-all duration-300"
                  style={{ width: `${(generationProgress.current / generationProgress.total) * 100}%` }}
                ></div>
              </div>
              <p className="text-xs text-gray-400 mt-2 text-center">
                {generationProgress.current} / {generationProgress.total} assets
              </p>
            </div>
          </div>
        )}

        <div className="flex flex-col items-center gap-4 w-full max-w-2xl">
          <button
            onClick={handleDownload}
            disabled={!allAssetsGenerated || isRendering || !ffmpegAvailable}
            className="bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-900 disabled:text-gray-400 disabled:cursor-not-allowed text-white font-bold py-4 px-12 rounded-lg transition text-xl shadow-lg w-full sm:w-auto flex items-center justify-center gap-3"
          >
            {isRendering ? (
              <>
                <svg className="animate-spin h-6 w-6" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Rendering {renderProgress.toFixed(0)}%
              </>
            ) : (
              <>
                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3V10" />
                </svg>
                Generate & Download Video (MP4)
              </>
            )}
          </button>

          {!ffmpegAvailable && (
            <div className="bg-red-900/30 border border-red-700 text-red-300 px-4 py-3 rounded-lg text-center max-w-md">
              <p className="font-semibold mb-1">⚠️ FFmpeg Server Not Available</p>
              <p className="text-sm">Please start the Python server:</p>
              <code className="text-xs bg-black/30 px-2 py-1 rounded mt-2 inline-block">python3 api_server.py</code>
            </div>
          )}

          {!allAssetsGenerated && !isGeneratingAll && (
            <p className="text-center text-gray-400 text-sm mt-2">
              Click "Generate All Assets" above to create all images and audio, or generate them individually for each scene.
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default Storyboard;