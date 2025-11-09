# MCP Server Usage Examples

## How to Set Parameters When Generating Videos

When talking to Claude Desktop with the MCP server enabled, you can specify video parameters in natural language. Claude will automatically extract the parameters and call the MCP tool.

## Available Parameters

### 1. **Topic** (Required)
The subject matter for your video.

### 2. **Duration** (Optional, default: 1 minute)
Video length in minutes.
- Range: 0.5 to 10 minutes
- Recommended: 1-3 minutes for best results

### 3. **Aspect Ratio** (Optional, default: 16:9)
Video dimensions:
- `16:9` - Horizontal/landscape (YouTube, TV)
- `9:16` - Vertical/portrait (TikTok, Instagram Reels, Stories)
- `1:1` - Square (Instagram posts)
- `4:3` - Classic TV format
- `3:4` - Vertical, less tall than 9:16

### 4. **Image Style** (Optional, default: Default)
Visual aesthetic for the images:
- `Default` - Standard AI-generated style
- `Photorealistic` - Realistic photography style
- `Cinematic` - Movie-like, dramatic lighting
- `Cartoon` - Animated, illustrated style
- `Anime` - Japanese animation style
- `Fantasy Art` - Magical, fantastical imagery
- `Watercolor` - Painted, artistic style
- `Cyberpunk` - Futuristic, neon, sci-fi style

## Example Prompts

### Basic (Topic Only)
```
"Generate a video about the solar system"
```
**Result:** 1-minute video, 16:9 ratio, default style

---

### Setting Duration
```
"Create a 2-minute video about dinosaurs"
```
**Result:** 2-minute video, 16:9 ratio, default style

```
"Make a 30-second video about coffee"
```
**Result:** 0.5-minute (30-second) video, 16:9 ratio, default style

---

### Setting Aspect Ratio

#### Vertical Video (TikTok/Reels)
```
"Generate a 1-minute vertical video about fitness tips"
```
**Result:** 1-minute video, 9:16 ratio (vertical)

```
"Create a 2-minute video about travel destinations in 9:16 format"
```
**Result:** 2-minute video, 9:16 ratio

#### Square Video (Instagram)
```
"Make a 1-minute square video about healthy recipes"
```
**Result:** 1-minute video, 1:1 ratio (square)

```
"Generate a video about meditation in 1:1 aspect ratio"
```
**Result:** Square format video

---

### Setting Image Style

#### Cinematic Style
```
"Create a 2-minute cinematic video about ancient Egypt"
```
**Result:** 2-minute video with cinematic-style images

```
"Generate a video about space exploration in cinematic style"
```
**Result:** Dramatic, movie-like imagery

#### Cartoon Style
```
"Make a 1-minute cartoon-style video about the water cycle"
```
**Result:** Animated, illustrated imagery

```
"Create a video explaining photosynthesis in cartoon style"
```
**Result:** Cartoon aesthetic

#### Photorealistic Style
```
"Generate a 2-minute photorealistic video about wildlife in Africa"
```
**Result:** Realistic photography-style images

#### Anime Style
```
"Create a 1-minute anime-style video about Japanese culture"
```
**Result:** Japanese animation aesthetic

#### Fantasy Art Style
```
"Make a 2-minute fantasy art video about dragons and castles"
```
**Result:** Magical, fantastical imagery

---

### Combining Multiple Parameters

```
"Generate a 2-minute vertical video about cooking tips in cinematic style"
```
**Parameters:**
- Duration: 2 minutes
- Aspect Ratio: 9:16 (vertical)
- Style: Cinematic

```
"Create a 3-minute square video about art history in photorealistic style"
```
**Parameters:**
- Duration: 3 minutes
- Aspect Ratio: 1:1 (square)
- Style: Photorealistic

```
"Make a 1.5-minute video about cyberpunk cities in 16:9 format with cyberpunk style"
```
**Parameters:**
- Duration: 1.5 minutes
- Aspect Ratio: 16:9
- Style: Cyberpunk

```
"Generate a 30-second vertical TikTok video about quick life hacks in cartoon style"
```
**Parameters:**
- Duration: 0.5 minutes (30 seconds)
- Aspect Ratio: 9:16 (vertical)
- Style: Cartoon

---

## Advanced Examples

### Educational Content
```
"Create a 2-minute educational video about the human heart in photorealistic style with 16:9 ratio"
```

### Social Media Content
```
"Generate a 45-second Instagram Reels video about morning routines in a clean, cinematic style"
```
(Claude will understand "Instagram Reels" → 9:16 ratio)

```
"Make a 1-minute TikTok video about dance moves in anime style"
```
(Claude will understand "TikTok" → 9:16 ratio)

### Artistic Content
```
"Create a 3-minute watercolor-style video about the four seasons in square format"
```

### Tech Content
```
"Generate a 2-minute cyberpunk-style video about AI and the future in widescreen"
```
(Claude will understand "widescreen" → 16:9 ratio)

---

## Natural Language Flexibility

Claude understands various ways to express the same thing:

### Duration
- "1 minute video"
- "60-second video"
- "a minute-long video"
- "one minute"

### Aspect Ratio
- "vertical video" = 9:16
- "portrait mode" = 9:16
- "TikTok format" = 9:16
- "Instagram Reels" = 9:16
- "horizontal video" = 16:9
- "landscape" = 16:9
- "widescreen" = 16:9
- "YouTube format" = 16:9
- "square video" = 1:1
- "Instagram post" = 1:1

### Style
- "realistic" = Photorealistic
- "movie-like" = Cinematic
- "animated" = Cartoon
- "illustrated" = Cartoon
- "artistic" = Fantasy Art or Watercolor

---

## Other MCP Tools

### List Generated Videos
```
"Show me all my generated videos"
```
or
```
"List my videos"
```

### Get Video Information
```
"Get information about the video file 'The_Solar_System_20250102_143022.mp4'"
```
or
```
"Tell me about my latest video"
```
(Claude will list videos first, then get info on the newest one)

---

## Tips for Best Results

1. **Be Specific**: More details = better results
   ```
   ❌ "Make a video about space"
   ✅ "Create a 2-minute cinematic video about black holes and space exploration in 16:9 format"
   ```

2. **Choose Appropriate Duration**:
   - Short topics: 0.5-1 minute
   - Medium topics: 1-2 minutes
   - Complex topics: 2-3 minutes
   - Longer videos take more time to generate!

3. **Match Style to Content**:
   - Educational: Photorealistic or Default
   - Kids content: Cartoon or Anime
   - Sci-fi: Cyberpunk or Cinematic
   - Nature: Photorealistic or Watercolor
   - Fantasy: Fantasy Art or Cinematic

4. **Match Aspect Ratio to Platform**:
   - YouTube/Website: 16:9
   - TikTok/Reels: 9:16
   - Instagram Posts: 1:1

5. **Generation Time**:
   - 1-minute video: ~3-5 minutes
   - 2-minute video: ~6-10 minutes
   - 3-minute video: ~10-15 minutes

---

## Troubleshooting

### "I asked for a vertical video but got horizontal"
Try being more explicit:
```
"Generate a video in 9:16 aspect ratio"
```

### "The style doesn't look right"
The style names must match exactly:
- ✅ "Cinematic"
- ❌ "Cinema" or "Movie style"

Valid styles: Default, Photorealistic, Cinematic, Cartoon, Anime, Fantasy Art, Watercolor, Cyberpunk

### "How do I know what parameters were used?"
Ask Claude:
```
"What parameters did you use for that last video?"
```
Claude will show you the exact tool call it made.

---

## JSON Format (Advanced)

If you want to see the exact JSON that gets sent to the MCP tool:

```json
{
  "topic": "The Solar System",
  "duration": 2,
  "aspect_ratio": "16:9",
  "image_style": "Cinematic"
}
```

But you don't need to use JSON - just talk naturally to Claude!
