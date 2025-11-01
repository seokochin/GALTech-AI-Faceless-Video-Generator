# Text Animation & Aspect Ratio Support

## 🎨 Animated Text Captions

Your AI Video Weaver now includes **professional typewriter-style text animations** that make captions appear dynamically throughout each scene!

---

## ✨ Typewriter Effect

### How It Works
Text appears **progressively** in chunks, creating a smooth typing animation:

```
Time 0.0s:  "Welcome to the world of..."
Time 0.5s:  "Welcome to the world of artificial intelligence. Today we'll explore..."
Time 1.0s:  "Welcome to the world of artificial intelligence. Today we'll explore how AI is transforming..."
Time 1.5s:  [Full text displayed]
```

### Animation Features
- 📝 **Progressive reveal** - Text appears in 3-10 chunks based on length
- ⚡ **Smart pacing** - Longer text = more chunks for smoother animation
- 🎭 **Fade-in effect** - Each chunk smoothly fades in (0.1s)
- ⏱️ **Adaptive duration** - Animation lasts up to 60% of scene duration (max 3s)
- 🎯 **Seamless transition** - After animation, text stays visible for entire scene

### Animation Timing

| Text Length | Chunks | Animation Time | Effect |
|-------------|--------|---------------|---------|
| < 60 chars | 3 chunks | ~1.5s | Quick reveal |
| 60-100 chars | 5 chunks | ~2.0s | Smooth typing |
| 100-200 chars | 7 chunks | ~2.5s | Steady flow |
| > 200 chars | 10 chunks | ~3.0s | Gentle reveal |

---

## 📱 Aspect Ratio Support

Text automatically adapts to **all aspect ratios** for perfect display on any platform!

### Supported Aspect Ratios

#### 1. **16:9 (Widescreen)** - YouTube, Landscape
- **Dimensions**: 1920x1080
- **Font sizing**: Standard (height-based)
- **Text position**: Bottom 28% of screen
- **Best for**: YouTube, TV displays, horizontal viewing

#### 2. **9:16 (Vertical)** - TikTok, Instagram Stories, Reels
- **Dimensions**: 1080x1920
- **Font sizing**: Larger (width is limited)
- **Text position**: Lower 22% of screen (more visible)
- **Best for**: Mobile-first content, social media stories

#### 3. **1:1 (Square)** - Instagram Feed
- **Dimensions**: 1080x1080
- **Font sizing**: Balanced
- **Text position**: Bottom 25% of screen
- **Best for**: Instagram posts, Facebook

#### 4. **4:3 (Classic TV)** - Traditional Format
- **Dimensions**: 1440x1080
- **Font sizing**: Standard
- **Text position**: Bottom 28% of screen
- **Best for**: Classic presentations, older displays

#### 5. **3:4 (Portrait)** - Vertical Alternative
- **Dimensions**: 1080x1440
- **Font sizing**: Larger (vertical orientation)
- **Text position**: Lower 22% of screen
- **Best for**: Mobile content, vertical displays

---

## 🎯 Adaptive Font Sizing

Font size automatically adjusts based on:

### 1. Text Length
- **Short (<100 chars)**: Larger, bold text
- **Medium (100-200 chars)**: Standard size
- **Long (>200 chars)**: Smaller to fit comfortably

### 2. Aspect Ratio
- **Vertical (9:16, 3:4)**: Larger fonts (limited width)
- **Square (1:1)**: Balanced fonts
- **Horizontal (16:9, 4:3)**: Standard fonts

### 3. Video Dimensions
Font scales proportionally with video resolution for consistency.

---

## 📐 Font Size Chart

### Horizontal Videos (16:9, 4:3)
| Text Length | Font Size | Visual Impact |
|-------------|-----------|---------------|
| < 100 chars | 28-36px | Large, prominent |
| 100-200 chars | 24-32px | Comfortable reading |
| > 200 chars | 20-28px | Dense but readable |

### Vertical Videos (9:16, 3:4)
| Text Length | Font Size | Visual Impact |
|-------------|-----------|---------------|
| < 100 chars | 32-40px | Bold, eye-catching |
| 100-200 chars | 28-36px | Clear, readable |
| > 200 chars | 24-32px | Balanced density |

### Square Videos (1:1)
| Text Length | Font Size | Visual Impact |
|-------------|-----------|---------------|
| < 100 chars | 30-38px | Prominent |
| 100-200 chars | 26-34px | Balanced |
| > 200 chars | 22-30px | Comfortable |

---

## 🎨 Visual Styling

### Text Appearance
- **Color**: White text for maximum contrast
- **Border**: 2px black outline for readability
- **Background**: Semi-transparent black box (60% opacity)
- **Box padding**: 10px for comfortable spacing
- **Line spacing**: 8px for multi-line text

### Position
- **Horizontal**: Always centered
- **Vertical**: Bottom area (adapts to aspect ratio)
- **Safe zones**: Positioned to avoid screen cutoffs

---

## 🔄 How Aspect Ratio Detection Works

```python
aspect = width / height

if aspect < 0.8:
    # Vertical video (9:16, 3:4)
    - Larger fonts
    - Lower text position
    - More space for text box

elif 0.8 <= aspect <= 1.2:
    # Square video (1:1)
    - Balanced settings
    - Centered approach

else:
    # Horizontal video (16:9, 4:3)
    - Standard settings
    - Optimized for wide screens
```

---

## 📊 Text Layout Examples

### 16:9 Widescreen
```
┌─────────────────────────────────────┐
│                                     │
│     [Image with Animation]          │
│                                     │
│                                     │
├─────────────────────────────────────┤
│  ┌─────────────────────────────┐   │  ← 28% from bottom
│  │  Your animated text here... │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

### 9:16 Vertical
```
┌───────────────┐
│               │
│   [Image]     │
│     with      │
│  Animation    │
│               │
│               │
├───────────────┤
│ ┌───────────┐ │  ← 22% from bottom
│ │  Larger   │ │
│ │   text    │ │
│ │  appears  │ │
│ └───────────┘ │
└───────────────┘
```

### 1:1 Square
```
┌──────────────────┐
│                  │
│    [Image]       │
│      with        │
│   Animation      │
│                  │
├──────────────────┤
│ ┌──────────────┐ │  ← 25% from bottom
│ │ Balanced text│ │
│ └──────────────┘ │
└──────────────────┘
```

---

## 🎬 Typewriter Effect Details

### Chunk-Based Animation
Instead of character-by-character (which would be slow for long text), we use **intelligent chunking**:

1. Text is divided into 3-10 chunks
2. Each chunk contains 10-50+ characters
3. Chunks fade in progressively
4. Creates smooth, readable typing effect

### Why Chunking?
- ✅ **Faster animation** - No lag for long captions
- ✅ **Smoother rendering** - FFmpeg handles chunks efficiently
- ✅ **Better readability** - Viewers can read words, not just letters
- ✅ **Professional look** - Similar to broadcast subtitles

### Example Animation Sequence:
```
Chunk 1 (0.0-0.3s): "Welcome to the world of artificial"
Chunk 2 (0.3-0.6s): " intelligence. Today we'll explore"
Chunk 3 (0.6-0.9s): " how AI is transforming industries"
Chunk 4 (0.9-1.2s): " and creating new opportunities"
Chunk 5 (1.2-1.5s): " for innovation and growth."
Complete (1.5s+):   [Full text remains visible]
```

---

## 🎯 Platform Optimization

### YouTube (16:9)
- Wide text box for comfortable reading
- Standard font sizes
- Bottom position doesn't interfere with player controls

### TikTok/Instagram Stories (9:16)
- Larger fonts for mobile viewing
- Text positioned to avoid UI elements
- Maximum readability on small screens

### Instagram Feed (1:1)
- Balanced layout for square format
- Centered text positioning
- Works well in grid view

---

## 💡 Best Practices

### For Creators:
1. **Keep voice over concise** - Even with adaptive sizing, shorter text looks better
2. **Test different aspect ratios** - Generate samples to see text layout
3. **Consider platform** - Choose aspect ratio based on where you'll share

### For Viewers:
- Text automatically adapts to any device
- Animations make content more engaging
- Can read along even with sound off

---

## 🔧 Technical Implementation

### Typewriter Animation Code:
```python
# Divide text into chunks
num_chunks = min(10, max(3, int(text_length / 20)))
time_per_chunk = typing_duration / num_chunks

# Create progressive reveal
for i in range(num_chunks):
    cumulative_text = caption[:end_idx]
    # Fade in this chunk
    alpha='if(lt(t,{start}),0,if(lt(t,{start+0.1}),(t-{start})/0.1,1))'
```

### Aspect Ratio Detection:
```python
aspect = width / height
is_vertical = aspect < 0.8    # 9:16, 3:4
is_square = 0.8 <= aspect <= 1.2  # 1:1
is_horizontal = aspect > 1.2  # 16:9, 4:3
```

---

## 🎨 Example Output

**Your generated video will have:**

✨ Text that types on progressively
✨ Perfect sizing for any aspect ratio
✨ Smooth fade-in animations
✨ Professional background box
✨ Clear, readable captions throughout

---

## 📱 Cross-Platform Compatibility

| Platform | Aspect Ratio | Text Size | Animation Speed |
|----------|--------------|-----------|-----------------|
| YouTube | 16:9 | Standard | ~2s |
| TikTok | 9:16 | Large | ~2.5s |
| Instagram Stories | 9:16 | Large | ~2.5s |
| Instagram Feed | 1:1 | Balanced | ~2s |
| Facebook | 1:1 or 16:9 | Adaptive | ~2s |
| Twitter | 16:9 | Standard | ~2s |

---

Enjoy your professionally animated, multi-platform videos! 🎬✨
