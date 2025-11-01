# Scene Updates - Shorter Scenes with Full Text Display

## 🎯 What Changed

### 1. **More Scenes Per Video** (Shorter, Dynamic Scenes)
- **Before**: ~3.5 scenes per minute
- **Now**: ~7 scenes per minute (doubled!)

This creates:
- More frequent image changes
- More dynamic, engaging content
- Better visual variety with animation effects

### 2. **Full Voice Over as Caption**
- **Before**: Short caption + separate voice over
- **Now**: Full voice over text displayed on screen

Benefits:
- Better accessibility (viewers can read along)
- Clearer message delivery
- Professional subtitle-like experience

---

## 📊 Scene Count Examples

| Duration | Old Scene Count | New Scene Count | Seconds/Scene |
|----------|----------------|-----------------|---------------|
| Shorts (1 min) | 3-4 scenes | 7 scenes | ~8-9s each |
| Medium (2 min) | 7-8 scenes | 14 scenes | ~8-9s each |
| Long (5 min) | 17-18 scenes | 35 scenes | ~8-9s each |

---

## 🎨 Text Display Improvements

### Adaptive Font Sizing
Text size automatically adjusts based on length:
- **Short text** (<100 chars): Larger font (28-36px)
- **Medium text** (100-200 chars): Medium font (24-32px)
- **Long text** (>200 chars): Smaller font (20-28px)

### Visual Features
- ✨ **Semi-transparent black background** for readability
- ✨ **Text border** (black outline) for contrast
- ✨ **Automatic centering** horizontally
- ✨ **Fixed bottom position** (lower 25% of screen)
- ✨ **Line spacing** for multi-line text
- ✨ **Fade-in animation** (0.5s)

---

## 🎬 Example Video Structure

**1-Minute "Shorts" Video:**
```
Scene 1 (8s): [Image with Ken Burns effect]
              Full voice over text displayed at bottom
              ↓ [0.5s crossfade]
Scene 2 (8s): [Image with Zoom Out effect]
              Full voice over text displayed at bottom
              ↓ [0.5s crossfade]
Scene 3 (8s): [Image with Pan Right effect]
              Full voice over text displayed at bottom
              ... (continues for 7 scenes total)
```

---

## 🔧 Technical Details

### File Modified: `services/geminiService.ts`
```typescript
// Old: 3.5 scenes per minute
const numScenes = Math.max(2, Math.round(duration * 3.5));

// New: 7 scenes per minute
const numScenes = Math.max(3, Math.round(duration * 7));

// Caption now equals voice over
const scenesWithIds = parsed.scenes.map((scene, index) => ({
  ...scene,
  caption: scene.voiceOver, // Use full voice over text
  id: index + 1,
}));
```

### File Modified: `video_generator.py`
```python
# Adaptive font sizing based on text length
if text_length > 200:
    font_size = max(20, int(height * 0.03))
elif text_length > 100:
    font_size = max(24, int(height * 0.035))
else:
    font_size = max(28, int(height * 0.04))

# Text display with background box
drawtext=text='...'
  :fontcolor=white
  :box=1
  :boxcolor=black@0.6
  :x=(w-tw)/2
  :y=height-25%
  :alpha='if(lt(t,0.5),t/0.5,1)'  # Fade in
```

---

## 💡 Benefits

### For Creators:
- ✅ More images per video = more visual variety
- ✅ Shorter scenes = easier to generate
- ✅ Full text display = better message delivery

### For Viewers:
- ✅ More engaging with frequent scene changes
- ✅ Can read along with voice over
- ✅ Better accessibility
- ✅ Professional look with text overlay

### For Animation Effects:
Each of the 5 effects cycles through more frequently:
```
Scene 1: Ken Burns
Scene 2: Zoom Out
Scene 3: Pan Right
Scene 4: Pan Left
Scene 5: Dynamic
Scene 6: Ken Burns (repeats)
Scene 7: Zoom Out
...
```

---

## 🚀 Usage

No changes needed to your workflow! Just:

1. Start servers: `./start_servers.sh`
2. Generate storyboard (you'll see MORE scenes now)
3. Generate all assets
4. Download video

**Your videos will automatically have:**
- More scenes (shorter duration each)
- Full voice over text displayed
- Better text formatting with background box
- Smooth transitions between all scenes

---

## 🎯 Perfect For:

- **Social Media Content** - Short, punchy scenes
- **Educational Videos** - Read along while listening
- **Explainer Videos** - Clear text + visuals
- **Marketing Videos** - Frequent visual changes maintain attention
- **Accessibility** - Text display helps viewers with hearing impairment

---

Enjoy your more dynamic, text-rich AI videos! 🎬✨
