#!/usr/bin/env python3
"""
MCP Server for AI Video Weaver
Provides MCP interface for generating AI-powered faceless videos
"""

from __future__ import annotations

import asyncio
import os
import sys
import json
import base64
from pathlib import Path
from typing import Optional, Any
from datetime import datetime
import traceback

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
import mcp.types as types

# Get the script's directory (absolute path)
SCRIPT_DIR = Path(__file__).parent.resolve()

# Add parent directory to path for imports
sys.path.insert(0, str(SCRIPT_DIR))

# Import video generation modules
from video_generator import VideoGenerator

# Import environment variables
from dotenv import load_dotenv
load_dotenv(SCRIPT_DIR / '.env.local')

# Configuration - use absolute paths
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
OUTPUT_DIR = SCRIPT_DIR / "generated_videos"
TEMP_DIR = SCRIPT_DIR / "temp_uploads"

# Create directories if they don't exist
OUTPUT_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)

# Global video generator instance
video_generator = VideoGenerator(output_dir=str(OUTPUT_DIR))

# MCP Server instance
app = Server("ai-video-weaver")


async def generate_storyboard(topic: str, duration: float) -> dict:
    """
    Generate storyboard using Gemini API

    Args:
        topic: Video topic
        duration: Duration in minutes

    Returns:
        Dictionary with scenes and grounding chunks
    """
    try:
        import google.generativeai as genai

        genai.configure(api_key=GEMINI_API_KEY)

        # Calculate parameters
        total_words = round(duration * 150)
        num_scenes = max(3, round(duration * 7))
        words_per_scene = round(total_words / num_scenes)

        prompt = f"""Create a video storyboard about "{topic}" with a total duration of approximately {duration} minute(s).
The total word count for all voice-overs should be around {total_words} words.
Break it down into {num_scenes} short, dynamic scenes. For each scene, provide:
1. A voice-over script of about {words_per_scene} words. This will be displayed as on-screen text.
2. A detailed image prompt for an AI image generator that visually represents the scene.
3. A short caption (this will not be used, but include it for compatibility).
Respond ONLY with a valid JSON object with a "scenes" key. The "scenes" key must contain an array of exactly {num_scenes} scene objects, each with "caption", "voiceOver", and "imagePrompt" properties. Do not wrap the JSON in markdown backticks."""

        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                temperature=0.9,
            )
        )

        # Clean response
        clean_text = response.text.strip().replace('```json', '').replace('```', '').strip()
        parsed = json.loads(clean_text)

        # Add IDs and use voiceOver as caption
        scenes = []
        for index, scene in enumerate(parsed['scenes']):
            scenes.append({
                'id': index + 1,
                'caption': scene['voiceOver'],
                'voiceOver': scene['voiceOver'],
                'imagePrompt': scene['imagePrompt']
            })

        return {'scenes': scenes, 'groundingChunks': []}

    except Exception as e:
        print(f"❌ Error generating storyboard: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        raise


async def generate_image(prompt: str, aspect_ratio: str = "16:9") -> tuple[bytes, str]:
    """
    Generate image using Google Imagen

    Args:
        prompt: Image generation prompt
        aspect_ratio: Aspect ratio (16:9, 9:16, 1:1, etc.)

    Returns:
        Tuple of (image_bytes, mime_type)
    """
    try:
        import google.generativeai as genai
        from PIL import Image
        import io

        genai.configure(api_key=GEMINI_API_KEY)

        # Use Imagen 3 model
        model = genai.ImageGenerationModel('imagen-3.0-generate-001')

        # Generate image
        result = model.generate_images(
            prompt=prompt,
            number_of_images=1,
            aspect_ratio=aspect_ratio,
            safety_filter_level="block_some",
            person_generation="allow_adult"
        )

        # Get the PIL image
        pil_image = result.images[0]._pil_image

        # Convert PIL image to bytes
        img_byte_arr = io.BytesIO()
        pil_image.save(img_byte_arr, format='JPEG', quality=95)
        image_bytes = img_byte_arr.getvalue()

        return image_bytes, 'image/jpeg'

    except Exception as e:
        print(f"❌ Error generating image: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        raise


async def generate_speech(text: str) -> bytes:
    """
    Generate speech using Gemini TTS

    Args:
        text: Text to convert to speech

    Returns:
        Audio bytes (WAV format)
    """
    try:
        import google.generativeai as genai

        genai.configure(api_key=GEMINI_API_KEY)

        model = genai.GenerativeModel('gemini-2.0-flash-exp')

        # Configure for audio output
        generation_config = genai.GenerationConfig(
            response_modalities=["AUDIO"]
        )

        response = model.generate_content(
            f"Say with a clear and engaging tone: {text}",
            generation_config=generation_config
        )

        # Extract audio data
        if response.candidates and len(response.candidates) > 0:
            candidate = response.candidates[0]
            if candidate.content and candidate.content.parts:
                for part in candidate.content.parts:
                    if hasattr(part, 'inline_data') and part.inline_data:
                        audio_b64 = part.inline_data.data
                        audio_bytes = base64.b64decode(audio_b64)
                        return audio_bytes

        raise Exception("No audio data in response")

    except Exception as e:
        print(f"❌ Error generating speech: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        raise


async def save_file_from_bytes(data: bytes, extension: str) -> str:
    """Save bytes to a temp file"""
    import uuid
    filename = f"{uuid.uuid4()}{extension}"
    filepath = TEMP_DIR / filename

    with open(filepath, 'wb') as f:
        f.write(data)

    return str(filepath)


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP tools"""
    return [
        Tool(
            name="generate_video",
            description="""Generate a complete AI video from a topic. This will:
1. Generate a storyboard with multiple scenes
2. Create images for each scene using AI
3. Generate voiceovers for each scene
4. Compile everything into a final video with transitions and captions

The process takes several minutes depending on video length.""",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "The topic or subject for the video (e.g., 'The History of Space Exploration', 'How Photosynthesis Works')"
                    },
                    "duration": {
                        "type": "number",
                        "description": "Duration of the video in minutes (e.g., 1, 2, 3). Recommended: 1-3 minutes",
                        "default": 1,
                        "minimum": 0.5,
                        "maximum": 10
                    },
                    "aspect_ratio": {
                        "type": "string",
                        "description": "Video aspect ratio",
                        "enum": ["16:9", "9:16", "1:1", "4:3", "3:4"],
                        "default": "16:9"
                    },
                    "image_style": {
                        "type": "string",
                        "description": "Visual style for the images",
                        "enum": ["Default", "Photorealistic", "Cinematic", "Cartoon", "Anime", "Fantasy Art", "Watercolor", "Cyberpunk"],
                        "default": "Default"
                    }
                },
                "required": ["topic"]
            }
        ),
        Tool(
            name="list_videos",
            description="List all generated videos in the output directory",
            inputSchema={
                "type": "object",
                "properties": {},
            }
        ),
        Tool(
            name="get_video_info",
            description="Get detailed information about a generated video file",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Name of the video file"
                    }
                },
                "required": ["filename"]
            }
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent | ImageContent | EmbeddedResource]:
    """Handle tool calls"""

    try:
        if name == "generate_video":
            return await handle_generate_video(arguments)
        elif name == "list_videos":
            return await handle_list_videos(arguments)
        elif name == "get_video_info":
            return await handle_get_video_info(arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        error_msg = f"Error executing {name}: {str(e)}\n{traceback.format_exc()}"
        return [TextContent(type="text", text=error_msg)]


async def handle_generate_video(arguments: dict) -> list[TextContent]:
    """Handle video generation request"""

    topic = arguments.get('topic')
    duration = arguments.get('duration', 1)
    aspect_ratio = arguments.get('aspect_ratio', '16:9')
    image_style = arguments.get('image_style', 'Default')

    if not topic:
        return [TextContent(type="text", text="❌ Error: 'topic' parameter is required")]

    output_messages = []
    output_messages.append(f"🎬 Starting video generation for topic: '{topic}'")
    output_messages.append(f"⏱️  Duration: {duration} minute(s)")
    output_messages.append(f"📐 Aspect Ratio: {aspect_ratio}")
    output_messages.append(f"🎨 Image Style: {image_style}")
    output_messages.append("")

    try:
        # Step 1: Generate storyboard
        output_messages.append("📝 Step 1/4: Generating storyboard with Gemini AI...")
        storyboard = await generate_storyboard(topic, duration)
        scenes = storyboard['scenes']
        output_messages.append(f"✅ Generated {len(scenes)} scenes")
        output_messages.append("")

        # Step 2: Generate images
        output_messages.append("🖼️  Step 2/4: Generating images for each scene...")
        processed_scenes = []

        for i, scene in enumerate(scenes):
            output_messages.append(f"   Scene {i+1}/{len(scenes)}: {scene['caption'][:50]}...")

            # Generate image
            final_prompt = scene['imagePrompt']
            if image_style != 'Default':
                final_prompt = f"{scene['imagePrompt']}, in a {image_style.lower()} style"

            image_bytes, mime_type = await generate_image(final_prompt, aspect_ratio)
            image_path = await save_file_from_bytes(image_bytes, '.jpg')

            # Generate audio
            audio_bytes = await generate_speech(scene['voiceOver'])
            audio_path = await save_file_from_bytes(audio_bytes, '.wav')

            processed_scenes.append({
                'image_path': image_path,
                'audio_path': audio_path,
                'caption': scene['caption'],
                'voice_over': scene['voiceOver']
            })

            output_messages.append(f"   ✅ Scene {i+1} assets generated")

        output_messages.append("")
        output_messages.append("✅ All scene assets generated successfully")
        output_messages.append("")

        # Step 3: Generate video
        output_messages.append("🎞️  Step 3/4: Compiling video with FFmpeg...")
        output_messages.append("   (This may take a few minutes...)")

        filename = f"{topic.replace(' ', '_')[:50]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        output_path = video_generator.generate_video(
            scenes=processed_scenes,
            output_filename=filename,
            aspect_ratio=aspect_ratio,
            transition_duration=0.5,
            fps=30
        )

        output_messages.append(f"✅ Video compiled successfully!")
        output_messages.append("")

        # Step 4: Cleanup temp files
        output_messages.append("🧹 Step 4/4: Cleaning up temporary files...")
        for scene in processed_scenes:
            try:
                os.remove(scene['image_path'])
                os.remove(scene['audio_path'])
            except:
                pass

        output_messages.append("✅ Cleanup complete")
        output_messages.append("")
        output_messages.append("=" * 60)
        output_messages.append("🎉 VIDEO GENERATION COMPLETE!")
        output_messages.append("=" * 60)
        output_messages.append(f"📹 Output file: {output_path}")
        output_messages.append(f"📊 Stats:")
        output_messages.append(f"   - Scenes: {len(scenes)}")
        output_messages.append(f"   - Duration: ~{duration} minute(s)")
        output_messages.append(f"   - Aspect Ratio: {aspect_ratio}")
        output_messages.append(f"   - File size: {os.path.getsize(output_path) / (1024*1024):.1f} MB")
        output_messages.append("")
        output_messages.append(f"You can find the video at: {os.path.abspath(output_path)}")

        return [TextContent(type="text", text="\n".join(output_messages))]

    except Exception as e:
        error_msg = f"❌ Error during video generation:\n{str(e)}\n\nTraceback:\n{traceback.format_exc()}"
        output_messages.append("")
        output_messages.append(error_msg)
        return [TextContent(type="text", text="\n".join(output_messages))]


async def handle_list_videos(arguments: dict) -> list[TextContent]:
    """List all generated videos"""

    try:
        video_files = list(OUTPUT_DIR.glob("*.mp4"))

        if not video_files:
            return [TextContent(type="text", text="No videos found in the output directory.")]

        # Sort by modification time (newest first)
        video_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)

        output_lines = [f"📹 Found {len(video_files)} video(s):", ""]

        for i, video_file in enumerate(video_files, 1):
            stat = video_file.stat()
            size_mb = stat.st_size / (1024 * 1024)
            modified = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')

            output_lines.append(f"{i}. {video_file.name}")
            output_lines.append(f"   Size: {size_mb:.1f} MB")
            output_lines.append(f"   Modified: {modified}")
            output_lines.append(f"   Path: {video_file.absolute()}")
            output_lines.append("")

        return [TextContent(type="text", text="\n".join(output_lines))]

    except Exception as e:
        return [TextContent(type="text", text=f"❌ Error listing videos: {str(e)}")]


async def handle_get_video_info(arguments: dict) -> list[TextContent]:
    """Get detailed information about a video"""

    filename = arguments.get('filename')
    if not filename:
        return [TextContent(type="text", text="❌ Error: 'filename' parameter is required")]

    try:
        video_path = OUTPUT_DIR / filename

        if not video_path.exists():
            return [TextContent(type="text", text=f"❌ Video file not found: {filename}")]

        stat = video_path.stat()
        size_mb = stat.st_size / (1024 * 1024)
        created = datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
        modified = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')

        # Get video metadata using ffprobe
        import subprocess
        cmd = [
            'ffprobe',
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_format',
            '-show_streams',
            str(video_path)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        output_lines = [
            f"📹 Video Information: {filename}",
            "=" * 60,
            f"📁 File Details:",
            f"   Path: {video_path.absolute()}",
            f"   Size: {size_mb:.2f} MB ({stat.st_size:,} bytes)",
            f"   Created: {created}",
            f"   Modified: {modified}",
            ""
        ]

        if result.returncode == 0:
            metadata = json.loads(result.stdout)

            # Format information
            fmt = metadata.get('format', {})
            duration = float(fmt.get('duration', 0))
            bitrate = int(fmt.get('bit_rate', 0)) / 1000  # Convert to kbps

            output_lines.append(f"🎬 Video Metadata:")
            output_lines.append(f"   Duration: {duration:.2f} seconds ({duration/60:.2f} minutes)")
            output_lines.append(f"   Bitrate: {bitrate:.0f} kbps")
            output_lines.append(f"   Format: {fmt.get('format_name', 'unknown')}")
            output_lines.append("")

            # Video stream info
            video_streams = [s for s in metadata.get('streams', []) if s.get('codec_type') == 'video']
            if video_streams:
                vs = video_streams[0]
                output_lines.append(f"🎥 Video Stream:")
                output_lines.append(f"   Codec: {vs.get('codec_name', 'unknown')}")
                output_lines.append(f"   Resolution: {vs.get('width')}x{vs.get('height')}")
                output_lines.append(f"   Frame Rate: {vs.get('r_frame_rate', 'unknown')} fps")
                output_lines.append("")

            # Audio stream info
            audio_streams = [s for s in metadata.get('streams', []) if s.get('codec_type') == 'audio']
            if audio_streams:
                aus = audio_streams[0]
                output_lines.append(f"🔊 Audio Stream:")
                output_lines.append(f"   Codec: {aus.get('codec_name', 'unknown')}")
                output_lines.append(f"   Sample Rate: {aus.get('sample_rate', 'unknown')} Hz")
                output_lines.append(f"   Channels: {aus.get('channels', 'unknown')}")
                output_lines.append("")

        return [TextContent(type="text", text="\n".join(output_lines))]

    except Exception as e:
        return [TextContent(type="text", text=f"❌ Error getting video info: {str(e)}")]


async def main():
    """Main entry point for MCP server"""
    print("🎬 AI Video Weaver MCP Server", file=sys.stderr)
    print("=" * 60, file=sys.stderr)
    print(f"Output directory: {OUTPUT_DIR.absolute()}", file=sys.stderr)
    print(f"Temp directory: {TEMP_DIR.absolute()}", file=sys.stderr)
    print("", file=sys.stderr)
    print("Server is ready to accept connections...", file=sys.stderr)
    print("=" * 60, file=sys.stderr)

    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
