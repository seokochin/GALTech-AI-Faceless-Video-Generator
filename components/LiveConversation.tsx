import React, { useState, useRef, useCallback, useEffect } from 'react';
import { GoogleGenAI, LiveServerMessage, Modality, Blob as GenAI_Blob } from '@google/genai';
// FIX: Correctly import all required audio utility functions.
import { encode, decode, decodeAudioData } from '../utils/audioUtils';
import MicIcon from './icons/MicIcon';
import StopIcon from './icons/StopIcon';

interface LiveConversationProps {
  apiKey: string;
}

const LiveConversation: React.FC<LiveConversationProps> = ({ apiKey }) => {
  const [isActive, setIsActive] = useState(false);
  const [transcripts, setTranscripts] = useState<{ user: string, model: string }[]>([]);
  const [currentInput, setCurrentInput] = useState('');
  const [currentOutput, setCurrentOutput] = useState('');

  const sessionRef = useRef<any>(null); // Use any for session as type not exported
  const inputAudioContextRef = useRef<AudioContext | null>(null);
  const outputAudioContextRef = useRef<AudioContext | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const scriptProcessorRef = useRef<ScriptProcessorNode | null>(null);
  const sourceRef = useRef<MediaStreamAudioSourceNode | null>(null);
  const nextStartTimeRef = useRef<number>(0);
  const sourcesRef = useRef<Set<AudioBufferSourceNode>>(new Set());
  // FIX: Use refs to track current transcriptions to avoid stale closures in callbacks.
  const currentInputRef = useRef('');
  const currentOutputRef = useRef('');

  const stopConversation = useCallback(() => {
    if (sessionRef.current) {
      sessionRef.current.close();
      sessionRef.current = null;
    }
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
    if (scriptProcessorRef.current) {
      scriptProcessorRef.current.disconnect();
      scriptProcessorRef.current = null;
    }
    if (sourceRef.current) {
      sourceRef.current.disconnect();
      sourceRef.current = null;
    }
    if (inputAudioContextRef.current && inputAudioContextRef.current.state !== 'closed') {
      inputAudioContextRef.current.close();
    }
    if (outputAudioContextRef.current && outputAudioContextRef.current.state !== 'closed') {
      outputAudioContextRef.current.close();
    }
    setIsActive(false);
  }, []);

  const startConversation = useCallback(async () => {
    if (isActive) {
      stopConversation();
      return;
    }
    
    setIsActive(true);
    setTranscripts([]);
    setCurrentInput('');
    setCurrentOutput('');
    // FIX: Reset refs when starting a new conversation.
    currentInputRef.current = '';
    currentOutputRef.current = '';
    
    try {
      const ai = new GoogleGenAI({ apiKey });

      inputAudioContextRef.current = new (window.AudioContext || (window as any).webkitAudioContext)({ sampleRate: 16000 });
      outputAudioContextRef.current = new (window.AudioContext || (window as any).webkitAudioContext)({ sampleRate: 24000 });
      nextStartTimeRef.current = 0;
      sourcesRef.current.clear();
      
      const sessionPromise = ai.live.connect({
        model: 'gemini-2.5-flash-native-audio-preview-09-2025',
        callbacks: {
          onopen: async () => {
            console.log("Live session opened.");
            streamRef.current = await navigator.mediaDevices.getUserMedia({ audio: true });
            
            if (!inputAudioContextRef.current || inputAudioContextRef.current.state === 'closed') return;
            
            sourceRef.current = inputAudioContextRef.current.createMediaStreamSource(streamRef.current);
            scriptProcessorRef.current = inputAudioContextRef.current.createScriptProcessor(4096, 1, 1);
            
            scriptProcessorRef.current.onaudioprocess = (audioProcessingEvent) => {
              const inputData = audioProcessingEvent.inputBuffer.getChannelData(0);
              // FIX: Improve efficiency of audio data encoding.
              const l = inputData.length;
              const int16 = new Int16Array(l);
              for (let i = 0; i < l; i++) {
                int16[i] = inputData[i] * 32768;
              }
              const pcmBlob: GenAI_Blob = {
                data: encode(new Uint8Array(int16.buffer)),
                mimeType: 'audio/pcm;rate=16000',
              };
              sessionPromise.then((session) => {
                session.sendRealtimeInput({ media: pcmBlob });
              });
            };
            
            sourceRef.current.connect(scriptProcessorRef.current);
            scriptProcessorRef.current.connect(inputAudioContextRef.current.destination);
          },
          onmessage: async (message: LiveServerMessage) => {
             // FIX: Use refs to update transcription state to avoid stale data.
             if (message.serverContent?.outputTranscription) {
                currentOutputRef.current += message.serverContent.outputTranscription.text;
                setCurrentOutput(currentOutputRef.current);
             }
             if (message.serverContent?.inputTranscription) {
                currentInputRef.current += message.serverContent.inputTranscription.text;
                setCurrentInput(currentInputRef.current);
             }
             if(message.serverContent?.turnComplete) {
                const fullInput = currentInputRef.current;
                const fullOutput = currentOutputRef.current;
                if (fullInput.trim() || fullOutput.trim()) {
                    setTranscripts(prev => [...prev, {user: fullInput, model: fullOutput}]);
                }
                currentInputRef.current = '';
                currentOutputRef.current = '';
                setCurrentInput('');
                setCurrentOutput('');
             }
            
            const base64Audio = message.serverContent?.modelTurn?.parts[0]?.inlineData?.data;
            if (base64Audio && outputAudioContextRef.current) {
              const ctx = outputAudioContextRef.current;
              nextStartTimeRef.current = Math.max(nextStartTimeRef.current, ctx.currentTime);
              const audioBuffer = await decodeAudioData(decode(base64Audio), ctx, 24000, 1);
              const source = ctx.createBufferSource();
              source.buffer = audioBuffer;
              source.connect(ctx.destination);
              source.addEventListener('ended', () => { sourcesRef.current.delete(source); });
              source.start(nextStartTimeRef.current);
              nextStartTimeRef.current += audioBuffer.duration;
              sourcesRef.current.add(source);
            }
          },
          onerror: (e: ErrorEvent) => {
            console.error("Live session error:", e);
            stopConversation();
          },
          onclose: () => {
            console.log("Live session closed.");
            stopConversation();
          },
        },
        config: {
          responseModalities: [Modality.AUDIO],
          inputAudioTranscription: {},
          outputAudioTranscription: {},
          speechConfig: { voiceConfig: { prebuiltVoiceConfig: { voiceName: 'Zephyr' } } },
        },
      });

      sessionRef.current = await sessionPromise;

    } catch (error) {
      console.error("Failed to start conversation:", error);
      setIsActive(false);
    }
    // FIX: Remove state dependencies from useCallback to prevent re-creating the function on every transcription update.
  }, [apiKey, isActive, stopConversation]);

  useEffect(() => {
    return () => {
        stopConversation();
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="fixed bottom-4 right-4 z-50">
        <div className="flex flex-col items-end gap-2">
            <div className={`bg-gray-800/80 backdrop-blur-md rounded-lg p-4 w-80 max-h-96 overflow-y-auto transition-all duration-300 ${isActive ? 'opacity-100' : 'opacity-0 h-0 p-0'}`}>
                <div className="space-y-4 text-sm">
                    {transcripts.map((t, i) => (
                        <div key={i}>
                            <p className="font-bold text-indigo-300">You:</p>
                            <p className="text-gray-300">{t.user}</p>
                            <p className="font-bold text-teal-300 mt-2">AI:</p>
                            <p className="text-gray-300">{t.model}</p>
                        </div>
                    ))}
                    {currentInput && <p><span className="font-bold text-indigo-300">You:</span> {currentInput}...</p>}
                    {currentOutput && <p><span className="font-bold text-teal-300">AI:</span> {currentOutput}...</p>}
                </div>
            </div>
            <button
                onClick={startConversation}
                className="w-16 h-16 rounded-full bg-gradient-to-br from-purple-500 to-indigo-600 text-white flex items-center justify-center shadow-lg hover:scale-105 transition-transform"
            >
                {isActive ? <StopIcon className="w-8 h-8"/> : <MicIcon className="w-8 h-8"/>}
            </button>
        </div>
    </div>
  );
};

export default LiveConversation;
