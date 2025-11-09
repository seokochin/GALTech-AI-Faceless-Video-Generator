# AI Video Weaver MCP Server

This MCP (Model Context Protocol) server allows MCP clients (like Claude Desktop, Claude Code, etc.) to generate AI-powered videos by simply providing a topic.

## Features

The MCP server exposes the following tools:

### 1. `generate_video`
Generate a complete AI video from a topic description.

**Parameters:**
- `topic` (required): The subject for the video (e.g., "The History of Space Exploration")
- `duration` (optional): Duration in minutes (default: 1, range: 0.5-10)
- `aspect_ratio` (optional): Video aspect ratio (default: "16:9", options: "16:9", "9:16", "1:1", "4:3", "3:4")
- `image_style` (optional): Visual style (default: "Default", options: "Photorealistic", "Cinematic", "Cartoon", "Anime", etc.)

**What it does:**
1. Generates a storyboard with multiple scenes using Gemini AI
2. Creates images for each scene using Imagen
3. Generates voiceovers using Gemini TTS
4. Compiles everything into a final video with transitions and captions

### 2. `list_videos`
List all generated videos in the output directory.

### 3. `get_video_info`
Get detailed metadata about a specific video file.

**Parameters:**
- `filename` (required): Name of the video file

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `mcp` - MCP SDK for Python
- `python-dotenv` - Environment variable management
- `google-generativeai` - Google Gemini API client
- `Flask` and `flask-cors` - For the web API
- `Pillow` - Image processing

### 2. Set up Environment Variables

Make sure your `.env.local` file contains your Gemini API key:

```
GEMINI_API_KEY=your_api_key_here
```

### 3. Ensure FFmpeg is Installed

The video generation requires FFmpeg. Install it if you haven't:

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install ffmpeg
```

**Windows:**
Download from https://ffmpeg.org/download.html

## Usage with Claude Desktop

### Configure Claude Desktop

1. Open your Claude Desktop configuration file:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - Linux: `~/.config/Claude/claude_desktop_config.json`

2. Add the AI Video Weaver MCP server to the configuration:

```json
{
  "mcpServers": {
    "ai-video-weaver": {
      "command": "python3",
      "args": ["/absolute/path/to/ai-video-weaver/mcp_server.py"],
      "env": {
        "GEMINI_API_KEY": "your_gemini_api_key_here"
      }
    }
  }
}
```

**Important:** Replace `/absolute/path/to/ai-video-weaver/` with the actual absolute path to your project directory.

3. Restart Claude Desktop

### Using the MCP Server in Claude Desktop

Once configured, you can ask Claude to generate videos using natural language:

**Quick Examples:**

```
"Generate a 2-minute video about the solar system in cinematic style"

"Create a 1-minute video explaining how photosynthesis works, in a cartoon style, vertical format"

"Make a 3-minute video about the history of the internet with photorealistic images"

"Generate a 30-second TikTok video about quick life hacks"

"List all my generated videos"
```

**Available Parameters:**
- **Duration**: 0.5 to 10 minutes (e.g., "2 minutes", "30 seconds")
- **Aspect Ratio**: 16:9 (horizontal), 9:16 (vertical), 1:1 (square), 4:3, 3:4
- **Image Style**: Default, Photorealistic, Cinematic, Cartoon, Anime, Fantasy Art, Watercolor, Cyberpunk
- **Topic**: Any subject you want the video about

**📚 See detailed usage examples:**
- **[MCP_USAGE_EXAMPLES.md](MCP_USAGE_EXAMPLES.md)** - Comprehensive examples with all parameters
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Quick cheat sheet

Claude will automatically:
1. Extract parameters from your request
2. Generate the storyboard
3. Create all images and audio
4. Compile the final video
5. Provide you with the output file path

## Usage with Claude Code

If you're using Claude Code with MCP support, you can invoke the tools directly:

```python
# Example: Ask Claude Code to generate a video
"Use the ai-video-weaver MCP server to generate a 2-minute video about dinosaurs"
```

## Manual Testing

You can test the MCP server manually:

```bash
# Run the server directly (for testing)
python3 mcp_server.py
```

The server will start and wait for MCP protocol messages on stdin/stdout.

## Output Directory

Generated videos are saved to:
```
./generated_videos/
```

Videos are automatically named with the topic and timestamp:
```
The_Solar_System_20250102_143022.mp4
```

## Troubleshooting

### Server Not Connecting

1. Check that the path in `claude_desktop_config.json` is absolute and correct
2. Ensure Python 3 is installed and accessible as `python3`
3. Verify all dependencies are installed: `pip install -r requirements.txt`

### Video Generation Fails

1. Check that FFmpeg is installed: `ffmpeg -version`
2. Verify your Gemini API key is valid
3. Ensure you have enough disk space (videos can be large)
4. Check the Claude Desktop logs for error messages

### "Module not found" errors

Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### API Key Issues

1. Check that `GEMINI_API_KEY` is set in your environment or `.env.local` file
2. Verify the API key is valid and has access to Gemini, Imagen, and TTS APIs
3. Ensure the environment variable is properly set in the MCP server configuration

## Example Configuration (Complete)

Here's a complete example configuration for Claude Desktop:

```json
{
  "mcpServers": {
    "ai-video-weaver": {
      "command": "python3",
      "args": [
        "/Users/yourname/Downloads/ai-video-weaver/mcp_server.py"
      ],
      "env": {
        "GEMINI_API_KEY": "XXXXXX"
      }
    }
  }
}
```

## Advanced Usage

### Custom Output Directory

By default, videos are saved to `./generated_videos/`. You can modify this in the MCP server code by changing the `OUTPUT_DIR` variable in `mcp_server.py`.

### Customizing Generation Parameters

You can customize default parameters by modifying the tool definitions in `mcp_server.py`:

- Default duration
- Default aspect ratio
- Default image style
- FPS (frames per second)
- Transition duration

## API Limits

Be aware of Google Gemini API limits:
- **Imagen**: Image generation may have rate limits
- **Gemini TTS**: Voice generation rate limits
- **Gemini Pro**: Text generation rate limits

For long videos with many scenes, generation may take several minutes.

## Performance

Typical generation times:
- **1-minute video** (~7 scenes): 3-5 minutes
- **2-minute video** (~14 scenes): 6-10 minutes
- **3-minute video** (~21 scenes): 10-15 minutes

Time varies based on:
- Number of scenes
- Image generation time
- Audio generation time
- FFmpeg rendering time
- Internet connection speed

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the main project README.md
3. Check FFmpeg setup guide: FFMPEG_SETUP.md
4. Submit an issue on GitHub

## Credits

Developed by [GALTech Learning](https://www.galtechlearning.com/)
