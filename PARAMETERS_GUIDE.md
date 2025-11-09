# Video Parameters Guide

## 🎬 Complete Parameter Breakdown

When generating videos via MCP, you have control over 4 main parameters:

---

## 1. 📝 Topic (Required)

**What it is:** The subject matter of your video

**Examples:**
- "The Solar System"
- "How to Make Coffee"
- "History of Ancient Egypt"
- "Top 10 Travel Destinations"
- "Explaining Quantum Physics"

---

## 2. ⏱️ Duration (Optional)

**What it is:** Length of the video in minutes

**Default:** 1 minute

**Range:** 0.5 to 10 minutes

**How to specify:**
```
"30 seconds"     → 0.5 minutes
"1 minute"       → 1 minute
"90 seconds"     → 1.5 minutes
"2 minutes"      → 2 minutes
"2.5 minutes"    → 2.5 minutes
"3 minutes"      → 3 minutes
```

**Scenes generated:**
- ~7-8 scenes per minute
- 1 minute = ~7 scenes
- 2 minutes = ~14 scenes
- 3 minutes = ~21 scenes

**Generation time:**
- 0.5 min video = ~2-4 minutes to generate
- 1 min video = ~3-5 minutes to generate
- 2 min video = ~6-10 minutes to generate
- 3 min video = ~10-15 minutes to generate

**Recommendations:**
- ✅ **0.5-1 min**: Quick tips, simple concepts
- ✅ **1-2 min**: Most topics, good balance
- ✅ **2-3 min**: Complex topics, detailed explanations
- ⚠️ **3-10 min**: Very detailed content (takes long to generate)

---

## 3. 📐 Aspect Ratio (Optional)

**What it is:** Video dimensions / shape

**Default:** 16:9 (horizontal)

### Options with Visual Representation:

#### 16:9 - Horizontal/Widescreen
```
┌──────────────────────┐
│                      │
│     16:9             │
│                      │
└──────────────────────┘
```
**Use for:** YouTube, websites, presentations, TV
**Keywords:** "horizontal", "landscape", "widescreen", "YouTube"

---

#### 9:16 - Vertical/Portrait
```
┌──────────┐
│          │
│          │
│   9:16   │
│          │
│          │
│          │
└──────────┘
```
**Use for:** TikTok, Instagram Reels, Stories, mobile-first
**Keywords:** "vertical", "portrait", "TikTok", "Reels", "9:16"

---

#### 1:1 - Square
```
┌────────────┐
│            │
│    1:1     │
│            │
└────────────┘
```
**Use for:** Instagram posts, Facebook posts
**Keywords:** "square", "Instagram post", "1:1"

---

#### 4:3 - Classic TV
```
┌────────────────┐
│                │
│      4:3       │
│                │
└────────────────┘
```
**Use for:** Old-school TV format, nostalgia
**Keywords:** "4:3", "classic TV", "old TV"

---

#### 3:4 - Tall Portrait
```
┌──────────┐
│          │
│   3:4    │
│          │
│          │
└──────────┘
```
**Use for:** Vertical content, less extreme than 9:16
**Keywords:** "3:4", "tall portrait"

---

## 4. 🎨 Image Style (Optional)

**What it is:** Visual aesthetic for scene images

**Default:** Default (standard AI style)

### Style Options:

#### Default
**Look:** Standard AI-generated imagery
**Use for:** General purpose, any topic
**Example prompt:** "Generate a video about nature"

---

#### Photorealistic
**Look:** Like real photographs, natural, realistic
**Use for:** Nature, documentaries, travel, wildlife, realistic scenes
**Example prompt:** "Create a photorealistic video about African wildlife"

---

#### Cinematic
**Look:** Movie-like, dramatic lighting, epic, high contrast
**Use for:** Storytelling, dramatic topics, epic subjects, history
**Example prompt:** "Generate a cinematic video about ancient Rome"

---

#### Cartoon
**Look:** Illustrated, animated, colorful, fun
**Use for:** Kids content, education, explainers, lighthearted topics
**Example prompt:** "Make a cartoon-style video about the water cycle"

---

#### Anime
**Look:** Japanese animation style, expressive, stylized
**Use for:** Cultural content, storytelling, stylized videos
**Example prompt:** "Create an anime-style video about Japanese history"

---

#### Fantasy Art
**Look:** Magical, mystical, fantastical, imaginative
**Use for:** Fantasy, mythology, magic, dreams, imagination
**Example prompt:** "Generate a fantasy art video about dragons and wizards"

---

#### Watercolor
**Look:** Painted, soft, artistic, gentle
**Use for:** Artistic content, soft topics, poetic subjects, nature
**Example prompt:** "Make a watercolor-style video about the four seasons"

---

#### Cyberpunk
**Look:** Futuristic, neon, dark, high-tech, sci-fi
**Use for:** Technology, future, AI, science fiction
**Example prompt:** "Create a cyberpunk video about AI and the future"

---

## 🎯 Putting It All Together

### Basic Formula:
```
"Generate a [DURATION] [ASPECT_RATIO] video about [TOPIC] in [STYLE] style"
```

### Real Examples:

**Example 1: YouTube Educational Video**
```
"Generate a 2-minute horizontal video about photosynthesis in photorealistic style"
```
- Duration: 2 minutes
- Aspect Ratio: 16:9 (horizontal)
- Topic: Photosynthesis
- Style: Photorealistic

**Example 2: TikTok Content**
```
"Create a 30-second vertical video about quick cooking tips in cartoon style"
```
- Duration: 0.5 minutes (30 seconds)
- Aspect Ratio: 9:16 (vertical)
- Topic: Quick cooking tips
- Style: Cartoon

**Example 3: Instagram Post**
```
"Make a 1-minute square video about meditation in watercolor style"
```
- Duration: 1 minute
- Aspect Ratio: 1:1 (square)
- Topic: Meditation
- Style: Watercolor

**Example 4: Epic Story Video**
```
"Generate a 3-minute cinematic video about the rise and fall of ancient civilizations"
```
- Duration: 3 minutes
- Aspect Ratio: 16:9 (default)
- Topic: Ancient civilizations
- Style: Cinematic

---

## 💡 Pro Tips

### Matching Style to Topic

| Topic Type | Recommended Style |
|------------|-------------------|
| Nature/Wildlife | Photorealistic, Watercolor |
| History | Cinematic, Photorealistic |
| Science/Education | Photorealistic, Default, Cartoon |
| Technology/AI | Cyberpunk, Cinematic |
| Kids Content | Cartoon, Anime |
| Fantasy/Mythology | Fantasy Art, Cinematic |
| Art/Culture | Watercolor, Fantasy Art |
| Travel | Photorealistic, Cinematic |

### Matching Aspect Ratio to Platform

| Platform | Aspect Ratio |
|----------|--------------|
| YouTube | 16:9 |
| TikTok | 9:16 |
| Instagram Reels | 9:16 |
| Instagram Stories | 9:16 |
| Instagram Posts | 1:1 |
| Facebook | 16:9 or 1:1 |
| Twitter | 16:9 |
| Website/Blog | 16:9 |
| Presentations | 16:9 |

### Duration Best Practices

| Platform | Recommended Duration |
|----------|---------------------|
| TikTok | 0.5-1 minute |
| Instagram Reels | 0.5-1.5 minutes |
| YouTube Shorts | 0.5-1 minute |
| YouTube (main) | 2-10 minutes |
| Educational | 2-5 minutes |
| Marketing | 0.5-2 minutes |

---

## 🚀 Quick Start Examples

Copy and paste these into Claude Desktop:

```
"Generate a 1-minute video about space exploration"

"Create a 2-minute vertical video about fitness tips in cartoon style"

"Make a 30-second square video about coffee in photorealistic style"

"Generate a 3-minute cinematic video about ancient Egypt"

"Create a 1-minute TikTok video about life hacks in anime style"

"Make a 2-minute YouTube video about AI in cyberpunk style"

"Generate a 45-second Instagram Reels video about travel in watercolor style"
```

---

## 📊 Parameter Matrix

Quick lookup table:

| Parameter | Options | Default |
|-----------|---------|---------|
| **Duration** | 0.5, 1, 1.5, 2, 2.5, 3... 10 minutes | 1 minute |
| **Aspect Ratio** | 16:9, 9:16, 1:1, 4:3, 3:4 | 16:9 |
| **Style** | Default, Photorealistic, Cinematic, Cartoon, Anime, Fantasy Art, Watercolor, Cyberpunk | Default |
| **Topic** | Any text | Required |

---

**Need more help?** See:
- [MCP_USAGE_EXAMPLES.md](MCP_USAGE_EXAMPLES.md) for detailed examples
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for a quick cheat sheet
- [MCP_SERVER.md](MCP_SERVER.md) for full documentation
