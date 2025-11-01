import { Scene, AspectRatio } from '../types';

const loadImage = (src: string): Promise<HTMLImageElement> => new Promise((resolve, reject) => {
    const img = new Image();
    img.crossOrigin = 'anonymous'; // Required for drawing images from object URLs to a canvas
    img.onload = () => resolve(img);
    img.onerror = (err) => reject(err);
    img.src = src;
});

const getAudioBuffer = async (audioContext: AudioContext, url: string): Promise<AudioBuffer> => {
    const response = await fetch(url);
    const arrayBuffer = await response.arrayBuffer();
    return audioContext.decodeAudioData(arrayBuffer);
};

const getCanvasDimensions = (aspectRatio: AspectRatio): [number, number] => {
    // Use a resolution based on 720p height for quality
    const baseHeight = 720;
    switch (aspectRatio) {
        case '16:9': return [baseHeight * 16 / 9, baseHeight];
        case '9:16': return [baseHeight * 9 / 16, baseHeight];
        case '1:1': return [baseHeight, baseHeight];
        case '4:3': return [baseHeight * 4 / 3, baseHeight];
        case '3:4': return [baseHeight * 3 / 4, baseHeight];
        default: return [1280, 720]; // Default to 16:9
    }
}

export const createVideo = async (
  scenes: Scene[],
  aspectRatio: AspectRatio,
  onProgress: (progress: number) => void
): Promise<Blob> => {
  onProgress(0);

  // 1. Setup Canvas
  const [width, height] = getCanvasDimensions(aspectRatio);
  const canvas = document.createElement('canvas');
  canvas.width = width;
  canvas.height = height;
  const ctx = canvas.getContext('2d');
  if (!ctx) throw new Error("Could not get canvas context");

  // 2. Prepare assets
  onProgress(5);
  const audioContext = new AudioContext();
  const loadedImages = await Promise.all(scenes.map(scene => loadImage(scene.imageUrl!)));
  onProgress(15);
  const audioBuffers = await Promise.all(scenes.map(scene => getAudioBuffer(audioContext, scene.audioUrl!)));
  onProgress(25);

  const sceneDurations = audioBuffers.map(b => b.duration);
  const sceneEndTimes = sceneDurations.reduce((acc, duration, i) => {
    acc.push((acc[i - 1] || 0) + duration);
    return acc;
  }, [] as number[]);
  const totalDuration = sceneEndTimes[sceneEndTimes.length - 1];

  // 3. Combine Audio into a single track
  const combinedBuffer = audioContext.createBuffer(1, audioContext.sampleRate * totalDuration, audioContext.sampleRate);
  let offset = 0;
  for (const buffer of audioBuffers) {
      combinedBuffer.copyToChannel(buffer.getChannelData(0), 0, offset);
      offset += buffer.length;
  }

  const audioSource = audioContext.createBufferSource();
  audioSource.buffer = combinedBuffer;
  const audioDestination = audioContext.createMediaStreamDestination();
  audioSource.connect(audioDestination);
  const audioTrack = audioDestination.stream.getAudioTracks()[0];
  
  // 4. Setup MediaRecorder
  const frameRate = 30;
  const videoStream = canvas.captureStream(frameRate);
  const combinedStream = new MediaStream([videoStream.getVideoTracks()[0], audioTrack]);
  const recorder = new MediaRecorder(combinedStream, { mimeType: 'video/webm;codecs=vp9,opus' });
  const chunks: Blob[] = [];
  recorder.ondataavailable = e => chunks.push(e.data);
  const recordPromise = new Promise<Blob>(resolve => {
    recorder.onstop = () => resolve(new Blob(chunks, { type: 'video/webm' }));
  });

  // 5. Start recording and rendering frames
  recorder.start();
  audioSource.start();

  const drawFrame = () => {
    const elapsedTime = audioContext.currentTime;
    
    if (elapsedTime >= totalDuration) {
        if(recorder.state === 'recording') {
            recorder.stop();
        }
        audioContext.close();
        onProgress(100);
        return;
    }
    
    // Find current scene index and calculate progress within the scene
    let sceneIdx = sceneEndTimes.findIndex(endTime => elapsedTime < endTime);
    if(sceneIdx === -1) sceneIdx = scenes.length - 1;

    const sceneStartTime = sceneIdx === 0 ? 0 : sceneEndTimes[sceneIdx - 1];
    const sceneDuration = sceneDurations[sceneIdx];
    const timeInScene = elapsedTime - sceneStartTime;
    const sceneProgress = Math.max(0, Math.min(1, timeInScene / sceneDuration));

    // FIX: Wrap all drawing in a save/restore block to prevent state leakage between frames.
    ctx.save();

    // Clear canvas for each new frame
    ctx.clearRect(0, 0, width, height);

    // 1. Draw Image with Zoom Out effect (Ken Burns effect)
    const startScale = 1.1; // Zoomed in at the start
    const endScale = 1.0;   // Normal size at the end
    const currentScale = startScale - (startScale - endScale) * sceneProgress;

    const scaledWidth = width * currentScale;
    const scaledHeight = height * currentScale;
    const x = (width - scaledWidth) / 2;
    const y = (height - scaledHeight) / 2;
    ctx.drawImage(loadedImages[sceneIdx], x, y, scaledWidth, scaledHeight);
    
    // 2. Draw Caption with Typing effect
    const caption = scenes[sceneIdx].caption;
    const fontSize = Math.max(24, height * 0.05);
    // Use a monospaced font for a classic typing effect
    ctx.font = `bold ${fontSize}px "Courier New", monospace`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    // Typing effect logic
    const typingDurationRatio = 0.8; // Caption finishes typing at 80% of scene duration
    const typingProgress = Math.min(1, sceneProgress / typingDurationRatio);
    const charsToShow = Math.floor(typingProgress * caption.length);
    let visibleCaption = caption.substring(0, charsToShow);

    let textToDraw = visibleCaption;
    if (typingProgress < 1) {
        // Blinking cursor
        if (Math.floor(elapsedTime * 2) % 2 === 0) {
            textToDraw += '_';
        }
    }
    
    // Rendering logic for text
    const barHeight = fontSize * 1.5;
    const barY = height - barHeight * 1.5; // Position the bar a bit up from the bottom

    // Draw background bar for text
    ctx.fillStyle = 'rgba(0, 0, 0, 0.6)';
    ctx.fillRect(0, barY, width, barHeight);

    // Draw text itself
    // FIX: Add a shadow for better visibility.
    ctx.shadowColor = 'black';
    ctx.shadowBlur = 7;
    ctx.fillStyle = 'white';
    ctx.fillText(textToDraw, width / 2, barY + barHeight / 2);
    
    ctx.restore(); // Restore context state

    const progress = 25 + (elapsedTime / totalDuration) * 75;
    onProgress(progress);
    requestAnimationFrame(drawFrame);
  };
  
  requestAnimationFrame(drawFrame);
  
  return recordPromise;
};