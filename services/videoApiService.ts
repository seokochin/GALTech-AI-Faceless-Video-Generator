import { Scene, AspectRatio } from '../types';

const API_BASE_URL = 'http://localhost:5001/api';

interface VideoGenerationResponse {
  success: boolean;
  videoUrl: string;
  filename: string;
  message: string;
}

interface VideoGenerationError {
  error: string;
  details?: string;
}

/**
 * Generate video using Python FFmpeg backend
 * @param scenes Array of scenes with images and audio
 * @param aspectRatio Video aspect ratio
 * @param transitionDuration Duration of transitions in seconds
 * @param fps Frames per second
 * @param filename Output filename
 * @returns Promise with video URL
 */
export const generateVideoWithFFmpeg = async (
  scenes: Scene[],
  aspectRatio: AspectRatio,
  transitionDuration: number = 0.5,
  fps: number = 30,
  filename: string = 'ai-video.mp4'
): Promise<string> => {
  try {
    const response = await fetch(`${API_BASE_URL}/generate-video`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        scenes: scenes.map(scene => ({
          imageUrl: scene.imageUrl,
          imageMimeType: scene.imageMimeType,
          audioUrl: scene.audioBase64 || scene.audioUrl, // Use base64 WAV if available
          caption: scene.caption,
          voiceOver: scene.voiceOver,
        })),
        aspectRatio,
        transitionDuration,
        fps,
        filename,
      }),
    });

    if (!response.ok) {
      const errorData: VideoGenerationError = await response.json();
      throw new Error(errorData.error || 'Failed to generate video');
    }

    const data: VideoGenerationResponse = await response.json();

    // Return full download URL
    return `${API_BASE_URL.replace('/api', '')}${data.videoUrl}`;
  } catch (error) {
    console.error('Error generating video with FFmpeg:', error);
    throw error;
  }
};

/**
 * Download video file from the server
 * @param videoUrl URL to the video file
 * @param filename Desired filename for download
 */
export const downloadVideoFile = async (videoUrl: string, filename: string) => {
  try {
    const response = await fetch(videoUrl);
    const blob = await response.blob();

    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  } catch (error) {
    console.error('Error downloading video:', error);
    throw error;
  }
};

/**
 * Check if the Python API server is running
 */
export const checkApiHealth = async (): Promise<boolean> => {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    return response.ok;
  } catch (error) {
    return false;
  }
};
