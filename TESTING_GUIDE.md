# Testing Your MCP Server

## ✅ Setup Status

Your MCP server is configured and ready to test!

**Configuration verified:**
- ✅ Python dependencies installed
- ✅ FFmpeg installed
- ✅ Gemini API key configured
- ✅ Claude Desktop config file updated
- ✅ MCP server added to config

---

## 🧪 Testing Steps

### Step 1: Restart Claude Desktop

**Important:** You MUST restart Claude Desktop for the MCP server to load.

1. Quit Claude Desktop completely (Cmd+Q)
2. Reopen Claude Desktop
3. Wait for it to fully load

---

### Step 2: Verify MCP Server is Connected

In Claude Desktop, you should see:
- A small indicator or icon showing MCP servers are connected
- In newer versions, you might see a tool icon or MCP badge

**If you don't see any indication:**
- Check the Claude Desktop logs for errors
- Make sure the server path in config is correct

---

### Step 3: Run Simple Tests

Start with these test commands in Claude Desktop:

#### Test 1: List Videos (Quick Test)
```
"List my generated videos"
```

**Expected result:**
- If no videos exist: "No videos found in the output directory."
- If videos exist: List of videos with details

**This tests:** Basic MCP connectivity

---

#### Test 2: Generate a Short Video
```
"Generate a 30-second video about cats"
```

**Expected result:**
- Claude will show progress messages
- Generation takes 2-4 minutes
- You'll get a file path to the generated video

**This tests:** Full video generation pipeline

---

#### Test 3: Test with Parameters
```
"Create a 1-minute vertical video about coffee in cinematic style"
```

**Expected result:**
- Video generated with 9:16 aspect ratio
- Cinematic-style images
- About 1 minute duration (~7 scenes)

**This tests:** Parameter handling

---

### Step 4: Advanced Tests

Once basic tests work, try these:

```
"Generate a 2-minute horizontal video about space exploration in photorealistic style"
```

```
"Create a 45-second square Instagram video about morning routines in cartoon style"
```

```
"Make a 3-minute YouTube video about AI and machine learning in cyberpunk style"
```

---

## 🔍 Checking Results

### Where to Find Generated Videos

Videos are saved to:
```
/Users/mohammedsalih/Downloads/ai-video-weaver/generated_videos/
```

### Check Video Files

Run this to see generated videos:
```bash
ls -lh /Users/mohammedsalih/Downloads/ai-video-weaver/generated_videos/
```

Or in Claude Desktop:
```
"Show me all my generated videos"
```

---

## 📊 What to Expect

### Generation Timeline

| Phase | Time | What's Happening |
|-------|------|------------------|
| Storyboard | 10-30s | Gemini generates scene scripts |
| Images | 5-30s per scene | Imagen generates images |
| Audio | 3-10s per scene | Gemini TTS generates voiceovers |
| Video Compilation | 30-120s | FFmpeg creates final video |

**Total time examples:**
- 30-second video (~4 scenes): 2-4 minutes
- 1-minute video (~7 scenes): 3-5 minutes
- 2-minute video (~14 scenes): 6-10 minutes
- 3-minute video (~21 scenes): 10-15 minutes

---

## ❌ Troubleshooting

### Issue: "Tool not found" or "No MCP tools available"

**Solution:**
1. Make sure you restarted Claude Desktop
2. Check the config file path is correct
3. Look at Claude Desktop logs for errors

**Check logs:**
```bash
# macOS
tail -f ~/Library/Logs/Claude/mcp*.log
```

---

### Issue: "Module not found" errors in logs

**Solution:**
```bash
cd /Users/mohammedsalih/Downloads/ai-video-weaver
pip install -r requirements.txt
```

Then restart Claude Desktop.

---

### Issue: "GEMINI_API_KEY not found"

**Solution:**
Make sure your `.env.local` file exists and has the API key:
```bash
cat .env.local
```

Should show:
```
GEMINI_API_KEY=AIzaSyB9GKryqS58KBz2lP0yv-rMBR68UuI3rzw
```

---

### Issue: Generation fails with FFmpeg errors

**Solution:**
Verify FFmpeg is working:
```bash
ffmpeg -version
```

If not installed:
```bash
brew install ffmpeg
```

---

### Issue: "Server not responding"

**Solution:**
Test the server directly:
```bash
cd /Users/mohammedsalih/Downloads/ai-video-weaver
python3 mcp_server.py
```

Should show:
```
🎬 AI Video Weaver MCP Server
============================================================
Output directory: ...
Server is ready to accept connections...
```

Press Ctrl+C to stop.

If this works, the server itself is fine - issue is with Claude Desktop connection.

---

## 🎬 Example Test Session

Here's what a successful test looks like in Claude Desktop:

**You:** "Generate a 1-minute video about cats"

**Claude:** "I'll generate a video about cats for you using the ai-video-weaver MCP server.

*[Uses generate_video tool]*

🎬 Starting video generation for topic: 'cats'
⏱️  Duration: 1 minute(s)
📐 Aspect Ratio: 16:9
🎨 Image Style: Default

📝 Step 1/4: Generating storyboard with Gemini AI...
✅ Generated 7 scenes

🖼️  Step 2/4: Generating images for each scene...
   Scene 1/7: Cats are fascinating creatures...
   ✅ Scene 1 assets generated
   [... continues for all scenes ...]

🎞️  Step 3/4: Compiling video with FFmpeg...
   (This may take a few minutes...)
✅ Video compiled successfully!

🧹 Step 4/4: Cleaning up temporary files...
✅ Cleanup complete

============================================================
🎉 VIDEO GENERATION COMPLETE!
============================================================
📹 Output file: /Users/mohammedsalih/Downloads/ai-video-weaver/generated_videos/cats_20250102_143022.mp4
📊 Stats:
   - Scenes: 7
   - Duration: ~1 minute(s)
   - Aspect Ratio: 16:9
   - File size: 12.3 MB

You can find the video at: /Users/mohammedsalih/Downloads/ai-video-weaver/generated_videos/cats_20250102_143022.mp4"

---

## 📹 Viewing Generated Videos

### Option 1: Open in Finder
```bash
open /Users/mohammedsalih/Downloads/ai-video-weaver/generated_videos/
```

### Option 2: Play with VLC/QuickTime
```bash
open -a "QuickTime Player" /Users/mohammedsalih/Downloads/ai-video-weaver/generated_videos/[filename].mp4
```

### Option 3: Use Claude Desktop
```
"Show me my latest video"
```

Claude will list videos and you can click the path to open it.

---

## ✅ Success Criteria

Your MCP server is working correctly if:

1. ✅ Claude recognizes the MCP tools
2. ✅ "List videos" command works
3. ✅ Video generation completes without errors
4. ✅ Generated video file exists in `generated_videos/`
5. ✅ Video plays correctly with image transitions and audio
6. ✅ Parameters (duration, ratio, style) are applied correctly

---

## 🎯 Quick Test Checklist

- [ ] Restart Claude Desktop
- [ ] Run: "List my generated videos"
- [ ] Run: "Generate a 30-second video about cats"
- [ ] Wait 2-4 minutes for generation
- [ ] Check if video file exists
- [ ] Play the video
- [ ] Try with parameters: "Create a 1-minute vertical video about coffee in cinematic style"

---

## 🆘 Getting Help

If you encounter issues:

1. Check this guide's troubleshooting section
2. Review [MCP_SERVER.md](MCP_SERVER.md) for detailed docs
3. Check Claude Desktop logs for specific errors
4. Verify all dependencies with: `python3 test_mcp_setup.py`

---

## 🎉 Next Steps After Successful Testing

Once testing is successful:

1. **Experiment with different parameters** - Try all aspect ratios and styles
2. **Test different durations** - From 30 seconds to 3+ minutes
3. **Try various topics** - Educational, entertainment, marketing content
4. **Share your videos** - Upload to social media, YouTube, etc.
5. **Customize the server** - Modify `mcp_server.py` for your needs

---

**Happy testing!** 🎬
