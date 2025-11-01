import React, { useState, useRef, useCallback } from 'react';
import { transcribeAudio } from '../services/geminiService';
import Loader from './Loader';
import MicIcon from './icons/MicIcon';
import StopIcon from './icons/StopIcon';

const AudioTranscriber: React.FC = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [transcription, setTranscription] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  const handleStartRecording = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      audioChunksRef.current = [];

      mediaRecorderRef.current.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };

      mediaRecorderRef.current.onstop = async () => {
        setIsLoading(true);
        setError('');
        setTranscription('');
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm;codecs=opus' });
        try {
          const result = await transcribeAudio(audioBlob);
          setTranscription(result);
        } catch (err) {
          console.error(err);
          setError('Failed to transcribe audio. Please try again.');
        } finally {
          setIsLoading(false);
          stream.getTracks().forEach(track => track.stop());
        }
      };

      mediaRecorderRef.current.start();
      setIsRecording(true);
    } catch (err) {
      console.error('Microphone access denied:', err);
      setError('Microphone access is required for transcription.');
    }
  }, []);

  const handleStopRecording = useCallback(() => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  }, []);

  return (
    <div className="bg-gray-800 rounded-xl p-6">
      <h3 className="text-xl font-bold mb-4 text-transparent bg-clip-text bg-gradient-to-r from-pink-400 to-orange-400">Audio Transcriber</h3>
      <div className="flex flex-col items-center gap-4">
        <button
          onClick={isRecording ? handleStopRecording : handleStartRecording}
          className={`w-20 h-20 rounded-full flex items-center justify-center transition-colors ${isRecording ? 'bg-red-600 hover:bg-red-700' : 'bg-indigo-600 hover:bg-indigo-700'}`}
        >
          {isRecording ? <StopIcon className="w-10 h-10 text-white" /> : <MicIcon className="w-10 h-10 text-white" />}
        </button>
        <p className="text-gray-400 text-sm">{isRecording ? 'Recording...' : 'Click to start recording'}</p>
      </div>
      
      {error && <p className="text-red-400 text-sm mt-4 text-center">{error}</p>}
      {isLoading && <div className="mt-4"><Loader text="Transcribing..." /></div>}
      
      {transcription && (
        <div className="mt-4 bg-gray-700/50 p-4 rounded-lg">
          <h4 className="font-semibold text-indigo-300 mb-2">Transcription:</h4>
          <p className="text-gray-300 whitespace-pre-wrap">{transcription}</p>
        </div>
      )}
    </div>
  );
};

export default AudioTranscriber;
