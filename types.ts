export interface Scene {
  id: number;
  caption: string;
  voiceOver: string;
  imagePrompt: string;
  imageUrl?: string;
  imageMimeType?: string;
  audioUrl?: string;
  audioBase64?: string; // Base64 WAV data for server upload
}

export type AspectRatio = "1:1" | "16:9" | "9:16" | "4:3" | "3:4";

export interface GroundingChunk {
  web?: {
    uri: string;
    title: string;
  };
}
