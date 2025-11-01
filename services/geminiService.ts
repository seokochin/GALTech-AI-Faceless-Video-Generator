import { GoogleGenAI, Type, Modality } from "@google/genai";
import { Scene, AspectRatio } from "../types";
import { blobToBase64 } from "../utils/fileUtils";

const API_KEY = process.env.API_KEY;
if (!API_KEY) {
  throw new Error("API_KEY environment variable is not set");
}

const ai = new GoogleGenAI({ apiKey: API_KEY });

export const generateStoryboard = async (topic: string, duration: number): Promise<{ scenes: Scene[], groundingChunks: any[] }> => {
  try {
    // Speaking rate: ~150 words per minute.
    const totalWords = Math.round(duration * 150);
    // Scene count: ~7-8 scenes per minute for shorter, more dynamic scenes
    const numScenes = Math.max(3, Math.round(duration * 7));
    const wordsPerScene = Math.round(totalWords / numScenes);

    const prompt = `Create a video storyboard about "${topic}" with a total duration of approximately ${duration} minute(s).
The total word count for all voice-overs should be around ${totalWords} words.
Break it down into ${numScenes} short, dynamic scenes. For each scene, provide:
1. A voice-over script of about ${wordsPerScene} words. This will be displayed as on-screen text.
2. A detailed image prompt for an AI image generator that visually represents the scene.
3. A short caption (this will not be used, but include it for compatibility).
Respond ONLY with a valid JSON object with a "scenes" key. The "scenes" key must contain an array of exactly ${numScenes} scene objects, each with "caption", "voiceOver", and "imagePrompt" properties. Do not wrap the JSON in markdown backticks.`;

    const response = await ai.models.generateContent({
      model: "gemini-2.5-pro",
      contents: prompt,
      config: {
        thinkingConfig: { thinkingBudget: 32768 },
        tools: [{ googleSearch: {} }],
      },
    });

    // The model might still wrap the response in markdown, so we clean it up.
    const cleanResponseText = response.text.trim().replace(/^```json/, '').replace(/```$/, '').trim();
    const parsed = JSON.parse(cleanResponseText);

    // Use voiceOver as caption for all scenes
    const scenesWithIds = parsed.scenes.map((scene: Omit<Scene, 'id'>, index: number) => ({
      ...scene,
      caption: scene.voiceOver, // Use full voice over text as caption
      id: index + 1,
    }));

    const groundingChunks = response.candidates?.[0]?.groundingMetadata?.groundingChunks || [];

    return { scenes: scenesWithIds, groundingChunks };
  } catch (error) {
    console.error("Error generating storyboard:", error);
    throw new Error("Failed to generate storyboard. The AI returned an unexpected format. Please try again.");
  }
};

export const generateImage = async (prompt: string, aspectRatio: AspectRatio): Promise<{ base64Image: string, mimeType: string }> => {
  const response = await ai.models.generateImages({
    model: 'imagen-4.0-generate-001',
    prompt: prompt,
    config: {
      numberOfImages: 1,
      outputMimeType: 'image/jpeg',
      aspectRatio,
    },
  });

  const base64Image = response.generatedImages[0].image.imageBytes;
  return { base64Image, mimeType: 'image/jpeg' };
};

export const editImage = async (base64Image: string, mimeType: string, prompt: string): Promise<{ base64Image: string, mimeType: string }> => {
  const response = await ai.models.generateContent({
    model: 'gemini-2.5-flash-image',
    contents: {
      parts: [
        {
          inlineData: {
            data: base64Image,
            mimeType: mimeType,
          },
        },
        {
          text: prompt,
        },
      ],
    },
    config: {
      responseModalities: [Modality.IMAGE],
    },
  });

  const part = response.candidates?.[0]?.content?.parts?.[0];
  if (part?.inlineData) {
    return { base64Image: part.inlineData.data, mimeType: part.inlineData.mimeType };
  }
  throw new Error("Image editing failed to produce an image.");
};

export const generateSpeech = async (text: string): Promise<string> => {
  const response = await ai.models.generateContent({
    model: "gemini-2.5-flash-preview-tts",
    contents: [{ parts: [{ text: `Say with a clear and engaging tone: ${text}` }] }],
    config: {
      responseModalities: [Modality.AUDIO],
      speechConfig: {
        voiceConfig: {
          prebuiltVoiceConfig: { voiceName: 'Kore' },
        },
      },
    },
  });

  const base64Audio = response.candidates?.[0]?.content?.parts?.[0]?.inlineData?.data;
  if (!base64Audio) {
    throw new Error("Failed to generate audio.");
  }
  return base64Audio;
};

// FIX: Add analyzeImage function for ImageAnalyzer component.
export const analyzeImage = async (base64Image: string, mimeType: string, prompt: string): Promise<string> => {
  const imagePart = {
    inlineData: {
      data: base64Image,
      mimeType: mimeType,
    },
  };
  const textPart = {
    text: prompt,
  };

  const response = await ai.models.generateContent({
    model: 'gemini-2.5-flash',
    contents: { parts: [imagePart, textPart] },
  });

  return response.text;
};

// FIX: Add transcribeAudio function for AudioTranscriber component.
export const transcribeAudio = async (audioBlob: Blob): Promise<string> => {
  const base64Audio = await blobToBase64(audioBlob);
  const audioPart = {
    inlineData: {
      data: base64Audio,
      mimeType: audioBlob.type,
    },
  };
  const textPart = {
    text: "Transcribe this audio.",
  };

  const response = await ai.models.generateContent({
    model: 'gemini-2.5-pro',
    contents: { parts: [audioPart, textPart] },
  });

  return response.text;
};