import React, { useState, useCallback } from 'react';
import { analyzeImage } from '../services/geminiService';
import { blobToBase64 } from '../utils/fileUtils';
import Loader from './Loader';
import SparklesIcon from './icons/SparklesIcon';

const ImageAnalyzer: React.FC = () => {
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [prompt, setPrompt] = useState('');
  const [analysis, setAnalysis] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setImageFile(file);
      setImageUrl(URL.createObjectURL(file));
      setAnalysis('');
      setError('');
    }
  };

  const handleAnalyze = useCallback(async () => {
    if (!imageFile || !prompt) return;
    setIsLoading(true);
    setAnalysis('');
    setError('');
    try {
      const base64Image = await blobToBase64(imageFile);
      const result = await analyzeImage(base64Image, imageFile.type, prompt);
      setAnalysis(result);
    } catch (err) {
      console.error(err);
      setError('Failed to analyze the image. Please try again.');
    } finally {
      setIsLoading(false);
    }
  }, [imageFile, prompt]);

  return (
    <div className="bg-gray-800 rounded-xl p-6">
      <h3 className="text-xl font-bold mb-4 text-transparent bg-clip-text bg-gradient-to-r from-teal-300 to-sky-400">Image Analyzer</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label htmlFor="image-upload" className="block w-full h-48 bg-gray-700 rounded-lg border-2 border-dashed border-gray-600 flex items-center justify-center cursor-pointer hover:border-indigo-400 transition">
            {imageUrl ? (
              <img src={imageUrl} alt="Upload preview" className="max-h-full max-w-full object-contain" />
            ) : (
              <span className="text-gray-400">Click to upload an image</span>
            )}
          </label>
          <input id="image-upload" type="file" accept="image/*" onChange={handleFileChange} className="hidden" />
        </div>
        <div className="flex flex-col gap-4">
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="What do you want to know about the image?"
            className="flex-grow bg-gray-700 border border-gray-600 rounded-md py-2 px-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition"
            rows={3}
            disabled={!imageFile}
          />
          <button onClick={handleAnalyze} disabled={isLoading || !imageFile || !prompt} className="w-full flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-900 text-white font-semibold py-2 px-4 rounded-lg transition">
            <SparklesIcon className="w-5 h-5"/> {isLoading ? 'Analyzing...' : 'Analyze Image'}
          </button>
        </div>
      </div>
      {error && <p className="text-red-400 text-sm mt-4">{error}</p>}
      {isLoading && <div className="mt-4"><Loader text="Analyzing..."/></div>}
      {analysis && (
        <div className="mt-4 bg-gray-700/50 p-4 rounded-lg">
          <h4 className="font-semibold text-indigo-300 mb-2">Analysis Result:</h4>
          <p className="text-gray-300 whitespace-pre-wrap">{analysis}</p>
        </div>
      )}
    </div>
  );
};

export default ImageAnalyzer;
