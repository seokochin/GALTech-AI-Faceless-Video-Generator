# MCP Server for GALTech AI Faceless Video Generator

This document explains how to set up and use the MCP (Model Context Protocol) server for the GALTech AI Faceless Video Generator. The MCP server allows you to integrate video generation capabilities with Claude Desktop, n8n, and other MCP-compatible applications.

## What is MCP?

The Model Context Protocol (MCP) is an open standard that enables AI assistants to securely connect to external tools and data sources. It provides a standardized way to expose functionality that AI models can use.

## Features

The MCP server exposes the following tools:

1. **generate_video** - Generate videos from local file paths
2. **generate_video_from_base64** - Generate videos from base64-encoded media
3. **get_video_info** - Get information about generated videos
4. **list_generated_videos** - List all generated videos
5. **cleanup_old_files** - Clean up old temporary and video files

## Prerequisites

Before setting up the MCP server, ensure you have:

- Python 3.8 or higher
- FFmpeg installed on your system
- All project dependencies installed

## Installation

### 1. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt
```

This will install:
- Flask (for the API server)
- flask-cors (for CORS support)
- mcp (MCP Python SDK)

### 2. Verify FFmpeg Installation

The video generator requires FFmpeg. Verify it's installed:

```bash
ffmpeg -version
```

If not installed, follow the instructions in `FFMPEG_SETUP.md`.

## Configuration

### For Claude Desktop

Claude Desktop uses a configuration file to connect to MCP servers.

#### Step 1: Locate Claude Desktop Configuration

The configuration file location varies by operating system:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

#### Step 2: Add MCP Server Configuration

Edit the configuration file and add the MCP server configuration. Replace `/absolute/path/to/GALTech-AI-Faceless-Video-Generator` with the actual path to this project:

```json
{
  "mcpServers": {
    "galtech-video-generator": {
      "command": "python",
      "args": [
        "/absolute/path/to/GALTech-AI-Faceless-Video-Generator/mcp_server.py"
      ],
      "env": {
        "PYTHONPATH": "/absolute/path/to/GALTech-AI-Faceless-Video-Generator"
      }
    }
  }
}
```

**Example (macOS/Linux):**
```json
{
  "mcpServers": {
    "galtech-video-generator": {
      "command": "python3",
      "args": [
        "/Users/yourname/projects/GALTech-AI-Faceless-Video-Generator/mcp_server.py"
      ],
      "env": {
        "PYTHONPATH": "/Users/yourname/projects/GALTech-AI-Faceless-Video-Generator"
      }
    }
  }
}
```

**Example (Windows):**
```json
{
  "mcpServers": {
    "galtech-video-generator": {
      "command": "python",
      "args": [
        "C:\\Users\\YourName\\Projects\\GALTech-AI-Faceless-Video-Generator\\mcp_server.py"
      ],
      "env": {
        "PYTHONPATH": "C:\\Users\\YourName\\Projects\\GALTech-AI-Faceless-Video-Generator"
      }
    }
  }
}
```

#### Step 3: Restart Claude Desktop

After updating the configuration, restart Claude Desktop for the changes to take effect.

#### Step 4: Verify Connection

In Claude Desktop, you should now see the video generation tools available. You can verify by asking Claude:

```
What tools do you have access to?
```

Claude should list the video generation tools provided by this MCP server.

### For n8n

n8n supports MCP servers through custom nodes. Here's how to integrate the MCP server with n8n:

#### Method 1: Using n8n's MCP Node (Recommended)

If n8n has an MCP node available:

1. Add an MCP node to your workflow
2. Configure the MCP server connection:
   - **Server Type**: stdio
   - **Command**: `python`
   - **Args**: `["/path/to/mcp_server.py"]`
   - **Working Directory**: `/path/to/GALTech-AI-Faceless-Video-Generator`

3. Select the tool you want to use (e.g., `generate_video`)
4. Configure the tool parameters
5. Connect it to your workflow

#### Method 2: Using HTTP Wrapper

If n8n doesn't have native MCP support, you can create an HTTP wrapper:

1. Use the existing Flask API server (`api_server.py`) which provides REST endpoints
2. Use n8n's HTTP Request node to call the API:
   - **URL**: `http://localhost:5001/api/generate-video`
   - **Method**: POST
   - **Body**: JSON with scene data

See the API server documentation for endpoint details.

#### Method 3: Using Python Script Node

If you have the n8n Python node:

1. Add a Python node to your workflow
2. Install the MCP client library in n8n's Python environment
3. Write a script that connects to the MCP server
4. Call the desired tools

Example n8n Python script:

```python
from mcp import ClientSession
from mcp.client.stdio import stdio_client
import asyncio

async def generate_video():
    server_params = {
        "command": "python",
        "args": ["/path/to/mcp_server.py"]
    }

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool(
                "generate_video",
                {
                    "scenes": [
                        {
                            "image_path": "/path/to/image1.jpg",
                            "audio_path": "/path/to/audio1.wav",
                            "caption": "Scene 1 caption"
                        }
                    ],
                    "output_filename": "my_video.mp4"
                }
            )

            return result

# Run the async function
result = asyncio.run(generate_video())
return result
```

### For Other MCP Clients

Any MCP-compatible client can connect to this server using the stdio transport:

**Command**: `python` or `python3`
**Args**: `["/path/to/GALTech-AI-Faceless-Video-Generator/mcp_server.py"]`
**Working Directory**: `/path/to/GALTech-AI-Faceless-Video-Generator`

## Usage Examples

### Example 1: Generate Video from Local Files

Using Claude Desktop with the MCP server:

```
Please generate a video with these scenes:
- Scene 1: Image at /path/to/scene1.jpg, audio at /path/to/scene1.wav, caption "Welcome to our story"
- Scene 2: Image at /path/to/scene2.jpg, audio at /path/to/scene2.wav, caption "The journey begins"

Use 16:9 aspect ratio and save as "my_story.mp4"
```

### Example 2: Generate Video from Base64 Data

If you have base64-encoded images and audio:

```
Generate a video from these base64-encoded scenes:
Scene 1:
- Image: [base64 data here]
- Audio: [base64 data here]
- Caption: "Introduction"

Save as "presentation.mp4" in 9:16 format (vertical video)
```

### Example 3: List Generated Videos

```
Show me all the videos I've generated
```

### Example 4: Get Video Information

```
Get information about the video "my_story.mp4"
```

### Example 5: Cleanup Old Files

```
Clean up temporary files older than 12 hours
```

## Tool Reference

### 1. generate_video

Generate a video from local file paths.

**Parameters:**
- `scenes` (required): Array of scene objects
  - `image_path` (required): Path to image file
  - `audio_path` (required): Path to audio file
  - `caption` (required): Text caption for overlay
  - `voice_over` (optional): Voice over script
- `output_filename` (optional): Output filename (default: "output.mp4")
- `aspect_ratio` (optional): Video aspect ratio (default: "16:9")
  - Options: "16:9", "9:16", "1:1", "4:3", "3:4"
- `transition_duration` (optional): Transition duration in seconds (default: 0.5)
- `fps` (optional): Frames per second (default: 30)

**Returns:**
- Success status
- Output path
- File size
- Video metadata

### 2. generate_video_from_base64

Generate a video from base64-encoded media.

**Parameters:**
- `scenes` (required): Array of scene objects
  - `image_base64` (required): Base64-encoded image
  - `image_format` (optional): Image format (default: "jpg")
  - `audio_base64` (required): Base64-encoded audio
  - `audio_format` (optional): Audio format (default: "wav")
  - `caption` (required): Text caption
  - `voice_over` (optional): Voice over script
- `output_filename` (optional): Output filename
- `aspect_ratio` (optional): Video aspect ratio
- `transition_duration` (optional): Transition duration
- `fps` (optional): Frames per second

**Returns:**
- Success status
- Output path
- File size
- Video metadata

### 3. get_video_info

Get information about a generated video.

**Parameters:**
- `filename` (required): Video filename

**Returns:**
- Filename
- Full path
- File size (bytes and MB)
- Creation timestamp
- Duration (seconds)

### 4. list_generated_videos

List all generated videos.

**Parameters:** None

**Returns:**
- Total count
- Array of videos with:
  - Filename
  - File size (MB)
  - Creation timestamp

### 5. cleanup_old_files

Clean up old temporary and video files.

**Parameters:**
- `max_age_hours` (optional): Maximum file age in hours (default: 24)
- `cleanup_videos` (optional): Whether to cleanup videos (default: false)

**Returns:**
- Success status
- Number of files cleaned
- List of cleaned files

## Troubleshooting

### MCP Server Not Connecting

1. **Check Python Path**: Ensure the Python command in your configuration is correct
   - Try `python3` instead of `python` on macOS/Linux
   - Use `which python` or `which python3` to find the correct path

2. **Check File Paths**: Ensure all paths in the configuration are absolute paths

3. **Check Permissions**: Ensure the MCP server script is executable:
   ```bash
   chmod +x mcp_server.py
   ```

4. **Check Dependencies**: Ensure all Python dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

5. **Check FFmpeg**: Ensure FFmpeg is installed and accessible:
   ```bash
   ffmpeg -version
   ```

### Video Generation Fails

1. **Check FFmpeg**: The most common issue is FFmpeg not being installed or not in PATH

2. **Check File Permissions**: Ensure the server has write permissions to the output directory

3. **Check Input Files**: Ensure image and audio files exist and are valid

4. **Check Logs**: Look at the console output for error messages

### Claude Desktop Not Showing Tools

1. **Restart Claude Desktop**: After configuration changes, always restart
2. **Check Configuration Syntax**: Ensure the JSON configuration is valid
3. **Check Logs**: Look at Claude Desktop logs for connection errors
4. **Verify Server Runs**: Try running the MCP server manually:
   ```bash
   python mcp_server.py
   ```

## Advanced Configuration

### Custom Output Directory

You can modify the output directory by editing `mcp_server.py`:

```python
OUTPUT_FOLDER = Path("./my_custom_output")
```

### Environment Variables

You can configure the server using environment variables:

```json
{
  "mcpServers": {
    "galtech-video-generator": {
      "command": "python",
      "args": ["/path/to/mcp_server.py"],
      "env": {
        "PYTHONPATH": "/path/to/project",
        "OUTPUT_DIR": "/custom/output/path",
        "TEMP_DIR": "/custom/temp/path"
      }
    }
  }
}
```

Then modify `mcp_server.py` to read these environment variables:

```python
OUTPUT_FOLDER = Path(os.getenv("OUTPUT_DIR", "./generated_videos"))
UPLOAD_FOLDER = Path(os.getenv("TEMP_DIR", "./temp_uploads"))
```

## Security Considerations

1. **File Access**: The MCP server can access any files on the system that the user running it can access
2. **Output Directory**: Generated videos are stored in `./generated_videos` by default
3. **Temporary Files**: Temporary files are stored in `./temp_uploads` and should be cleaned regularly
4. **Network**: The MCP server uses stdio (standard input/output) and doesn't open network ports

## Performance Tips

1. **Use SSD**: Store temporary files and output on an SSD for better performance
2. **Adjust FFmpeg Settings**: Modify the FFmpeg preset in `video_generator.py` for speed vs quality tradeoff
3. **Clean Up Regularly**: Use the `cleanup_old_files` tool to remove old files
4. **Monitor Disk Space**: Video generation can use significant disk space

## Support

For issues, questions, or contributions:

1. Check the main README.md for project documentation
2. Review the QUICK_START.md for setup instructions
3. Check FFMPEG_SETUP.md for FFmpeg installation help
4. Open an issue on the project repository

## License

This MCP server is part of the GALTech AI Faceless Video Generator project and is licensed under the MIT License.
