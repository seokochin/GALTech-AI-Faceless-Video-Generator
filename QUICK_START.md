# Quick Start Guide - AI Video Weaver

## ✅ What I Fixed

### 1. FFmpeg Audio Error
- Added audio validation and automatic re-encoding
- Fixed duration detection with fallback methods
- WAV files are now automatically converted to FFmpeg-compatible format

### 2. Simplified UI - FFmpeg Only
- ✅ **Removed**: WebM browser rendering
- ✅ **Removed**: Preview modal
- ✅ **Kept**: FFmpeg rendering only (professional quality MP4)

---

## 🚀 How to Use (3 Steps)

### Step 1: Start Servers
```bash
./start_servers.sh
```

**You should see:**
```
✅ Servers started successfully!

📱 React App: http://localhost:3000
🔧 API Server: http://localhost:5001
```

### Step 2: Create Your Video
1. Open `http://localhost:3000` in browser
2. Enter your topic (e.g., "The history of space exploration")
3. Choose duration: Shorts (1 min), Medium (2 min), or Long (5 min)
4. Click **"Generate Storyboard"**
   - **Shorts**: Creates ~7 short, dynamic scenes
   - **Medium**: Creates ~14 scenes
   - **Long**: Creates ~35 scenes

### Step 3: Generate & Download
1. Click **"Generate All Assets"** (generates all images + audio)
2. Wait for progress to complete
3. Click **"Generate & Download Video (MP4)"**
4. Your video downloads automatically! 🎉

---

## 🎬 What You Get

**Video Features:**
- ✨ **Shorter, Dynamic Scenes** (~7 scenes per minute for engaging content)
- ✨ **Live Caption Style** - 3-4 words at a time, like TV/streaming captions!
- ✨ **BIG Text** (40-60px fonts) for maximum visibility
- ✨ **Smooth fade in/out** transitions for each caption chunk
- ✨ **Perfect voice sync** - captions timed to match speech
- ✨ **4 Cinematic Effects** (Pan Right, Pan Left, Dynamic Zoom, Zoom Out)
- ✨ **Automatic effect cycling** for visual variety
- ✨ **Smooth crossfade transitions** (0.5s between scenes)
- ✨ **Aspect Ratio Support** - Perfect text display for 16:9, 9:16, 1:1, 4:3, 3:4
- ✨ **Image sharpening** for crisp output
- ✨ **Professional MP4 format** with H.264 codec
- ✨ **Perfect audio sync** with visuals

**Quality:**
- 1920x1080 resolution (or custom aspect ratio)
- 30 FPS
- High-quality AAC audio
- Scene duration matches audio perfectly

---

## 🔧 Troubleshooting

### Error: "FFmpeg Server Not Available"
**Solution:** Make sure Python server is running
```bash
# In a separate terminal:
python3 api_server.py
```

### Error: "could not convert string to float"
**Solution:** This is now automatically fixed! The server will:
1. Detect invalid audio files
2. Re-encode them automatically to proper format
3. Continue with video generation

### Port 5001 in use
**Solution:** Change port in both files:
```bash
# In api_server.py (line 236):
app.run(debug=True, host='0.0.0.0', port=5002)

# In services/videoApiService.ts (line 3):
const API_BASE_URL = 'http://localhost:5002/api';
```

---

## 📁 Output

**Videos are saved to:**
- `./generated_videos/ai-video-[timestamp].mp4`

**Temporary files:**
- Automatically cleaned up after generation
- Run `/api/cleanup` endpoint to manually clean old files

---

## 🎨 Customization

### Change Aspect Ratio
In the UI, select from dropdown:
- **16:9** - Widescreen (YouTube, landscape)
- **9:16** - Vertical (TikTok, Instagram Stories)
- **1:1** - Square (Instagram feed)
- **4:3** - Classic TV
- **3:4** - Portrait

### Change Image Style
Select from dropdown:
- Default
- Photorealistic
- Cinematic
- Cartoon
- Anime
- Fantasy Art
- Watercolor
- Cyberpunk

### Edit Video Effects
Edit `video_generator.py`:
- **Line 131-132**: Change zoom amount
- **Line 136-147**: Adjust text animation timing
- **Line 154-162**: Modify text styling

---

## 📊 Performance

**Typical Generation Times:**
- Shorts (1 min, ~7 scenes): ~45 seconds
- Medium (2 min, ~14 scenes): ~1.5 minutes
- Long (5 min, ~35 scenes): ~3-4 minutes

*Times vary based on system specs and FFmpeg performance. More scenes = slightly longer generation time, but still very fast!*

---

## 🆘 Need Help?

**Check logs:**
- Python server shows detailed FFmpeg output
- Browser console shows client-side errors

**Common issues:**
1. ✅ FFmpeg not installed → `brew install ffmpeg`
2. ✅ Python server not running → `python3 api_server.py`
3. ✅ Port conflicts → Change ports in config files
4. ✅ Audio issues → Now auto-fixed with re-encoding!

---

## 🎯 What's Different Now

### Before:
- Preview button ❌ (removed)
- WebM rendering ❌ (removed)
- FFmpeg toggle switch ❌ (removed)
- Multiple rendering options ❌ (removed)

### Now:
- ✅ **One button:** "Generate & Download Video (MP4)"
- ✅ **One format:** Professional MP4 only
- ✅ **One method:** FFmpeg with transitions
- ✅ **Simpler UI:** Less confusion, better results

---

## 📝 Tips

1. **Generate all assets first** before downloading video
2. **Edit individual scenes** if needed before final render
3. **Use "New Story"** to start over with different topic
4. **Keep server running** for multiple videos
5. **Check aspect ratio** before generating assets

---

Enjoy creating amazing AI-powered videos! 🎬✨
