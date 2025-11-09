# MCP Server Quick Reference

## Basic Command Format

When talking to Claude Desktop:

```
"Generate a [DURATION] [ASPECT_RATIO] video about [TOPIC] in [STYLE] style"
```

## Parameters Cheat Sheet

### Duration Options
| You Say | Actual Value |
|---------|--------------|
| 30 seconds / 0.5 minutes | 0.5 |
| 1 minute | 1 |
| 90 seconds / 1.5 minutes | 1.5 |
| 2 minutes | 2 |
| 3 minutes | 3 |

### Aspect Ratio Options
| You Say | Value | Use For |
|---------|-------|---------|
| vertical / portrait / TikTok / Reels | 9:16 | TikTok, Instagram Reels, Stories |
| horizontal / landscape / YouTube | 16:9 | YouTube, websites, presentations |
| square / Instagram post | 1:1 | Instagram feed posts |
| classic TV | 4:3 | Old-school TV format |
| tall portrait | 3:4 | Vertical, less extreme than 9:16 |

### Image Style Options
| Style | Description | Best For |
|-------|-------------|----------|
| Default | Standard AI style | General purpose |
| Photorealistic | Like real photos | Nature, documentaries, realism |
| Cinematic | Movie-like, dramatic | Storytelling, drama, epic topics |
| Cartoon | Illustrated, animated | Kids content, explainers |
| Anime | Japanese animation | Cultural content, stylized videos |
| Fantasy Art | Magical, fantastical | Fantasy, mythology, imagination |
| Watercolor | Painted, artistic | Artistic content, soft topics |
| Cyberpunk | Futuristic, neon, sci-fi | Tech, future, sci-fi topics |

## Example Commands

### Quick Examples
```
"Generate a video about cats"
→ 1 min, 16:9, default style

"Create a 2-minute video about space"
→ 2 min, 16:9, default style

"Make a vertical video about cooking tips"
→ 1 min, 9:16, default style

"Generate a cinematic video about ancient Rome"
→ 1 min, 16:9, cinematic style
```

### Complete Examples
```
"Create a 2-minute vertical video about fitness in cinematic style"
→ 2 min, 9:16, cinematic

"Generate a 30-second square video about coffee in photorealistic style"
→ 0.5 min, 1:1, photorealistic

"Make a 3-minute YouTube video about AI in cyberpunk style"
→ 3 min, 16:9, cyberpunk
```

## Other Commands

```
"List my videos"
→ Shows all generated videos

"Show video info for [filename]"
→ Details about specific video

"What videos have I created?"
→ Lists videos with details
```

## Tips

✅ **DO:**
- Be specific about your topic
- Mention duration if not 1 minute
- Say "vertical" for TikTok/Reels (9:16)
- Say "square" for Instagram posts (1:1)
- Specify style for better aesthetics

❌ **DON'T:**
- Ask for videos longer than 10 minutes (too long)
- Expect instant results (takes 3-15 minutes)
- Use custom style names (stick to the list)

## Generation Time

| Duration | Typical Time |
|----------|--------------|
| 0.5 min (30s) | 2-4 minutes |
| 1 minute | 3-5 minutes |
| 2 minutes | 6-10 minutes |
| 3 minutes | 10-15 minutes |

## Output Location

Videos are saved to:
```
./generated_videos/[Topic_Name]_[Timestamp].mp4
```

Example:
```
./generated_videos/The_Solar_System_20250102_143022.mp4
```

---

For detailed examples, see: **MCP_USAGE_EXAMPLES.md**
