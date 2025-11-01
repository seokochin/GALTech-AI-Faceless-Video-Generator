# FFmpeg Video Generation Setup

This guide explains how to set up and use the Python FFmpeg backend for enhanced video generation with professional transitions and effects.

## Features

### FFmpeg Backend Advantages:
✅ **Better Quality**: Outputs MP4 format with H.264 codec
✅ **Image Transitions**: Smooth fade in/out effects between scenes
✅ **Advanced Text Effects**: Better text rendering with shadows and borders
✅ **Ken Burns Effect**: Smooth zoom animation on images
✅ **Professional Output**: Industry-standard video encoding

### Browser Rendering (Default):
- Quick rendering directly in browser
- Outputs WebM format
- No server setup required
- Good for quick previews

---

## Installation

### 1. Install FFmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
Download from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

Verify installation:
```bash
ffmpeg -version
```

### 2. Install Python Dependencies

```bash
cd ai-video-weaver
pip install -r requirements.txt
```

Or manually:
```bash
pip install Flask==3.0.0 flask-cors==4.0.0
```

---

## Usage

### Start the FFmpeg API Server

In a terminal, run:

```bash
python api_server.py
```

You should see:
```
🎬 AI Video Weaver API Server
============================
Server starting on http://localhost:5001

Available endpoints:
- POST /api/generate-video  : Generate video from scenes
- GET  /api/download/<file> : Download generated video
- POST /api/cleanup         : Cleanup old files
- GET  /api/health          : Health check

Make sure FFmpeg is installed!
 * Running on http://0.0.0.0:5001
```

### Start the React App

In another terminal:

```bash
npm run dev
```

Access at: `http://localhost:3000`

### Use FFmpeg Rendering

1. Generate your storyboard
2. Generate all assets (images + audio)
3. Check the **"Use FFmpeg Rendering"** checkbox (appears when server is running)
4. Click **"Download MP4"**
5. Video will be generated with transitions and effects!

---

## API Endpoints

### Generate Video
**POST** `/api/generate-video`

```json
{
  "scenes": [
    {
      "imageUrl": "data:image/jpeg;base64,...",
      "imageMimeType": "image/jpeg",
      "audioUrl": "data:audio/wav;base64,...",
      "caption": "Scene caption",
      "voiceOver": "Voice over text"
    }
  ],
  "aspectRatio": "16:9",
  "transitionDuration": 0.5,
  "fps": 30,
  "filename": "my_video.mp4"
}
```

**Response:**
```json
{
  "success": true,
  "videoUrl": "/api/download/my_video.mp4",
  "filename": "my_video.mp4",
  "message": "Video generated successfully"
}
```

### Download Video
**GET** `/api/download/{filename}`

Downloads the generated MP4 file.

### Health Check
**GET** `/api/health`

Check if the API server is running.

### Cleanup
**POST** `/api/cleanup`

Remove old temporary files and videos older than 24 hours.

---

## Standalone Python Usage

You can also use the video generator directly in Python:

```python
from video_generator import VideoGenerator

# Scene data
scenes = [
    {
        "image_path": "./scene1.jpg",
        "audio_path": "./scene1.wav",
        "caption": "Welcome to AI Video Weaver",
        "voice_over": "Creating amazing videos with AI"
    },
    {
        "image_path": "./scene2.jpg",
        "audio_path": "./scene2.wav",
        "caption": "Advanced effects and transitions",
        "voice_over": "Professional quality output"
    }
]

# Initialize generator
generator = VideoGenerator(output_dir="./output")

# Generate video
output_video = generator.generate_video(
    scenes=scenes,
    output_filename="my_video.mp4",
    aspect_ratio="16:9",
    transition_duration=0.5,
    fps=30
)

print(f"Video saved to: {output_video}")
```

---

## Video Effects Explained

### 1. **Ken Burns Effect** (Image Animation)
- Images start slightly zoomed in (110%)
- Slowly zoom out to normal size (100%)
- Creates cinematic movement

### 2. **Fade Transitions**
- Each scene fades in (0.5s at start)
- Each scene fades out (0.5s at end)
- Smooth transitions between scenes

### 3. **Text Overlay**
- Captions appear at the bottom
- Black semi-transparent background bar
- White text with black border/shadow
- Typewriter animation effect (first 80% of scene)

### 4. **Audio Sync**
- Each scene duration matches its audio
- Seamless audio transitions
- High-quality AAC audio encoding

---

## Troubleshooting

### FFmpeg not found
```
RuntimeError: FFmpeg is not installed
```
**Solution:** Install FFmpeg (see Installation section)

### Server not connecting
```
⚠️ FFmpeg API server is not available
```
**Solution:** Make sure Python server is running on port 5001

### Port 5000 already in use (macOS AirPlay)
```
Address already in use
```
**Solution:** The API server now uses port 5001 by default. If you need to change it:
- Edit `api_server.py` line 236 and change the port number
- Edit `services/videoApiService.ts` line 3 to match the new port

### Font errors on non-Mac systems
```
Error: Font file not found
```
**Solution:** Edit `video_generator.py` line 235 and change font path:
- **Ubuntu/Debian:** `/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf`
- **Windows:** `C:\\Windows\\Fonts\\arial.ttf`
- Or remove fontfile parameter to use default

### CORS errors
**Solution:** Make sure flask-cors is installed:
```bash
pip install flask-cors
```

---

## Configuration Options

### Aspect Ratios
- `16:9` - Standard widescreen (1920x1080)
- `9:16` - Vertical/Portrait (1080x1920)
- `1:1` - Square (1080x1080)
- `4:3` - Classic (1440x1080)
- `3:4` - Portrait (1080x1440)

### Quality Settings
Edit in `video_generator.py`:
```python
'-crf', '23',  # Lower = better quality (18-28 range)
'-preset', 'medium',  # fast/medium/slow (slow = better quality)
```

### FPS Options
- 24 fps - Cinematic
- 30 fps - Standard (default)
- 60 fps - Smooth (larger file size)

---

## File Structure

```
ai-video-weaver/
├── video_generator.py          # Core FFmpeg video generation
├── api_server.py              # Flask API server
├── requirements.txt           # Python dependencies
├── services/
│   └── videoApiService.ts     # React service to call API
├── temp_uploads/              # Temporary uploaded files (auto-created)
└── generated_videos/          # Output videos (auto-created)
```

---

## Performance Tips

1. **Use SSD**: Store temp files on SSD for faster processing
2. **Adjust Preset**: Use `fast` preset for quicker rendering
3. **Lower Resolution**: Use 720p for faster generation
4. **Cleanup**: Run `/api/cleanup` endpoint regularly
5. **Batch Processing**: Generate multiple scenes before video rendering

---

## Credits

- FFmpeg: [https://ffmpeg.org/](https://ffmpeg.org/)
- Flask: [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
- React: [https://react.dev/](https://react.dev/)

---

## License

This project uses FFmpeg under LGPL/GPL license. See FFmpeg documentation for details.
