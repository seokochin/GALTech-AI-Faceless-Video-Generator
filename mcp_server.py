#!/usr/bin/env python3
"""
MCP Server for GALTech AI Faceless Video Generator

This MCP server exposes video generation capabilities through the Model Context Protocol,
allowing integration with Claude Desktop, n8n, and other MCP-compatible clients.
"""

import asyncio
import base64
import json
import os
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional
from contextlib import asynccontextmanager

from mcp.server import Server
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)
import mcp.server.stdio

from video_generator import VideoGenerator

# Initialize paths
UPLOAD_FOLDER = Path("./temp_uploads")
OUTPUT_FOLDER = Path("./generated_videos")
UPLOAD_FOLDER.mkdir(exist_ok=True)
OUTPUT_FOLDER.mkdir(exist_ok=True)

# Initialize video generator
video_generator = VideoGenerator(output_dir=str(OUTPUT_FOLDER))

# Create MCP server
app = Server("galtech-video-generator")


def save_base64_file(base64_data: str, file_extension: str) -> str:
    """
    Save base64 encoded file to disk

    Args:
        base64_data: Base64 encoded file data (with or without data URI prefix)
        file_extension: File extension (.jpg, .wav, etc.)

    Returns:
        Path to saved file
    """
    # Remove data URI prefix if present
    if ',' in base64_data and base64_data.startswith('data:'):
        base64_data = base64_data.split(',')[1]

    # Decode base64
    file_data = base64.b64decode(base64_data)

    # Generate unique filename
    filename = f"{uuid.uuid4()}{file_extension}"
    file_path = UPLOAD_FOLDER / filename

    # Save file
    with open(file_path, 'wb') as f:
        f.write(file_data)

    return str(file_path)


def encode_file_to_base64(file_path: str) -> str:
    """
    Encode file to base64 string

    Args:
        file_path: Path to file

    Returns:
        Base64 encoded string
    """
    with open(file_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')


@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    List available tools for video generation
    """
    return [
        Tool(
            name="generate_video",
            description=(
                "Generate a complete faceless video from scenes. Each scene should contain an image, "
                "audio narration, and caption text. The tool will create a professional video with "
                "transitions, text overlays, and synchronized audio. Perfect for creating educational "
                "videos, social media content, or AI-generated stories."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "scenes": {
                        "type": "array",
                        "description": "List of scenes for the video",
                        "items": {
                            "type": "object",
                            "properties": {
                                "image_path": {
                                    "type": "string",
                                    "description": "Path to the scene image file (local path)"
                                },
                                "audio_path": {
                                    "type": "string",
                                    "description": "Path to the scene audio file (local path)"
                                },
                                "caption": {
                                    "type": "string",
                                    "description": "Text caption to overlay on the video"
                                },
                                "voice_over": {
                                    "type": "string",
                                    "description": "Voice over script (optional, for reference)",
                                    "default": ""
                                }
                            },
                            "required": ["image_path", "audio_path", "caption"]
                        },
                        "minItems": 1
                    },
                    "output_filename": {
                        "type": "string",
                        "description": "Output video filename (e.g., 'my_video.mp4')",
                        "default": "output.mp4"
                    },
                    "aspect_ratio": {
                        "type": "string",
                        "description": "Video aspect ratio",
                        "enum": ["16:9", "9:16", "1:1", "4:3", "3:4"],
                        "default": "16:9"
                    },
                    "transition_duration": {
                        "type": "number",
                        "description": "Duration of transitions between scenes in seconds",
                        "default": 0.5,
                        "minimum": 0.1,
                        "maximum": 2.0
                    },
                    "fps": {
                        "type": "integer",
                        "description": "Frames per second",
                        "default": 30,
                        "minimum": 24,
                        "maximum": 60
                    }
                },
                "required": ["scenes"]
            }
        ),
        Tool(
            name="generate_video_from_base64",
            description=(
                "Generate a video from base64-encoded images and audio. This is useful when you have "
                "media content in base64 format (e.g., from API responses). The tool will decode the "
                "base64 data, create a video with transitions and text overlays, and return the path "
                "to the generated video file."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "scenes": {
                        "type": "array",
                        "description": "List of scenes with base64-encoded media",
                        "items": {
                            "type": "object",
                            "properties": {
                                "image_base64": {
                                    "type": "string",
                                    "description": "Base64-encoded image data (with or without data URI prefix)"
                                },
                                "image_format": {
                                    "type": "string",
                                    "description": "Image format",
                                    "enum": ["jpg", "jpeg", "png"],
                                    "default": "jpg"
                                },
                                "audio_base64": {
                                    "type": "string",
                                    "description": "Base64-encoded audio data (with or without data URI prefix)"
                                },
                                "audio_format": {
                                    "type": "string",
                                    "description": "Audio format",
                                    "enum": ["wav", "mp3"],
                                    "default": "wav"
                                },
                                "caption": {
                                    "type": "string",
                                    "description": "Text caption to overlay on the video"
                                },
                                "voice_over": {
                                    "type": "string",
                                    "description": "Voice over script (optional)",
                                    "default": ""
                                }
                            },
                            "required": ["image_base64", "audio_base64", "caption"]
                        },
                        "minItems": 1
                    },
                    "output_filename": {
                        "type": "string",
                        "description": "Output video filename",
                        "default": "output.mp4"
                    },
                    "aspect_ratio": {
                        "type": "string",
                        "description": "Video aspect ratio",
                        "enum": ["16:9", "9:16", "1:1", "4:3", "3:4"],
                        "default": "16:9"
                    },
                    "transition_duration": {
                        "type": "number",
                        "description": "Duration of transitions between scenes in seconds",
                        "default": 0.5
                    },
                    "fps": {
                        "type": "integer",
                        "description": "Frames per second",
                        "default": 30
                    }
                },
                "required": ["scenes"]
            }
        ),
        Tool(
            name="get_video_info",
            description=(
                "Get information about a generated video file including its path, size, "
                "duration, and other metadata. Useful for checking video generation results."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Name of the video file to get info about"
                    }
                },
                "required": ["filename"]
            }
        ),
        Tool(
            name="list_generated_videos",
            description=(
                "List all generated videos in the output folder. Returns filenames, "
                "file sizes, and creation timestamps."
            ),
            inputSchema={
                "type": "object",
                "properties": {},
            }
        ),
        Tool(
            name="cleanup_old_files",
            description=(
                "Clean up old temporary files and optionally old generated videos. "
                "Helps manage disk space by removing files older than specified age."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "max_age_hours": {
                        "type": "number",
                        "description": "Maximum age of files to keep in hours",
                        "default": 24,
                        "minimum": 1
                    },
                    "cleanup_videos": {
                        "type": "boolean",
                        "description": "Whether to also cleanup old generated videos",
                        "default": False
                    }
                }
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent | ImageContent | EmbeddedResource]:
    """
    Handle tool calls
    """
    try:
        if name == "generate_video":
            return await handle_generate_video(arguments)

        elif name == "generate_video_from_base64":
            return await handle_generate_video_from_base64(arguments)

        elif name == "get_video_info":
            return await handle_get_video_info(arguments)

        elif name == "list_generated_videos":
            return await handle_list_generated_videos(arguments)

        elif name == "cleanup_old_files":
            return await handle_cleanup_old_files(arguments)

        else:
            return [TextContent(
                type="text",
                text=f"Unknown tool: {name}"
            )]

    except Exception as e:
        import traceback
        error_msg = f"Error executing tool '{name}': {str(e)}\n\n{traceback.format_exc()}"
        return [TextContent(type="text", text=error_msg)]


async def handle_generate_video(arguments: Dict[str, Any]) -> list[TextContent]:
    """
    Handle video generation from local file paths
    """
    scenes = arguments.get("scenes", [])
    output_filename = arguments.get("output_filename", "output.mp4")
    aspect_ratio = arguments.get("aspect_ratio", "16:9")
    transition_duration = arguments.get("transition_duration", 0.5)
    fps = arguments.get("fps", 30)

    # Validate scenes
    if not scenes:
        return [TextContent(type="text", text="Error: No scenes provided")]

    # Generate video
    output_path = video_generator.generate_video(
        scenes=scenes,
        output_filename=output_filename,
        aspect_ratio=aspect_ratio,
        transition_duration=transition_duration,
        fps=fps
    )

    # Get video info
    file_size = os.path.getsize(output_path)
    file_size_mb = file_size / (1024 * 1024)

    result = {
        "success": True,
        "message": "Video generated successfully",
        "output_path": output_path,
        "filename": os.path.basename(output_path),
        "file_size_mb": round(file_size_mb, 2),
        "num_scenes": len(scenes),
        "aspect_ratio": aspect_ratio,
        "fps": fps
    }

    return [TextContent(
        type="text",
        text=json.dumps(result, indent=2)
    )]


async def handle_generate_video_from_base64(arguments: Dict[str, Any]) -> list[TextContent]:
    """
    Handle video generation from base64-encoded media
    """
    scenes_data = arguments.get("scenes", [])
    output_filename = arguments.get("output_filename", "output.mp4")
    aspect_ratio = arguments.get("aspect_ratio", "16:9")
    transition_duration = arguments.get("transition_duration", 0.5)
    fps = arguments.get("fps", 30)

    if not scenes_data:
        return [TextContent(type="text", text="Error: No scenes provided")]

    # Process scenes and save files
    processed_scenes = []
    temp_files = []

    for i, scene in enumerate(scenes_data):
        # Save image
        image_format = scene.get("image_format", "jpg")
        image_ext = f".{image_format}"
        image_path = save_base64_file(scene["image_base64"], image_ext)
        temp_files.append(image_path)

        # Save audio
        audio_format = scene.get("audio_format", "wav")
        audio_ext = f".{audio_format}"
        audio_path = save_base64_file(scene["audio_base64"], audio_ext)
        temp_files.append(audio_path)

        processed_scenes.append({
            "image_path": image_path,
            "audio_path": audio_path,
            "caption": scene.get("caption", ""),
            "voice_over": scene.get("voice_over", "")
        })

    try:
        # Generate video
        output_path = video_generator.generate_video(
            scenes=processed_scenes,
            output_filename=output_filename,
            aspect_ratio=aspect_ratio,
            transition_duration=transition_duration,
            fps=fps
        )

        # Get video info
        file_size = os.path.getsize(output_path)
        file_size_mb = file_size / (1024 * 1024)

        result = {
            "success": True,
            "message": "Video generated successfully from base64 data",
            "output_path": output_path,
            "filename": os.path.basename(output_path),
            "file_size_mb": round(file_size_mb, 2),
            "num_scenes": len(scenes_data),
            "aspect_ratio": aspect_ratio,
            "fps": fps
        }

        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]

    finally:
        # Cleanup temp files
        for temp_file in temp_files:
            try:
                os.remove(temp_file)
            except:
                pass


async def handle_get_video_info(arguments: Dict[str, Any]) -> list[TextContent]:
    """
    Get information about a generated video
    """
    filename = arguments.get("filename")

    if not filename:
        return [TextContent(type="text", text="Error: No filename provided")]

    file_path = OUTPUT_FOLDER / filename

    if not file_path.exists():
        return [TextContent(type="text", text=f"Error: Video file '{filename}' not found")]

    # Get file info
    file_size = os.path.getsize(file_path)
    file_size_mb = file_size / (1024 * 1024)
    creation_time = os.path.getctime(file_path)

    import subprocess

    # Get video duration using ffprobe
    try:
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            str(file_path)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        duration = float(result.stdout.strip()) if result.returncode == 0 else None
    except:
        duration = None

    from datetime import datetime

    info = {
        "filename": filename,
        "path": str(file_path),
        "file_size_mb": round(file_size_mb, 2),
        "file_size_bytes": file_size,
        "created_at": datetime.fromtimestamp(creation_time).isoformat(),
        "duration_seconds": round(duration, 2) if duration else None
    }

    return [TextContent(
        type="text",
        text=json.dumps(info, indent=2)
    )]


async def handle_list_generated_videos(arguments: Dict[str, Any]) -> list[TextContent]:
    """
    List all generated videos
    """
    from datetime import datetime

    videos = []

    for video_file in OUTPUT_FOLDER.glob("*.mp4"):
        file_size = os.path.getsize(video_file)
        file_size_mb = file_size / (1024 * 1024)
        creation_time = os.path.getctime(video_file)

        videos.append({
            "filename": video_file.name,
            "file_size_mb": round(file_size_mb, 2),
            "created_at": datetime.fromtimestamp(creation_time).isoformat()
        })

    # Sort by creation time (newest first)
    videos.sort(key=lambda x: x["created_at"], reverse=True)

    result = {
        "total_videos": len(videos),
        "videos": videos
    }

    return [TextContent(
        type="text",
        text=json.dumps(result, indent=2)
    )]


async def handle_cleanup_old_files(arguments: Dict[str, Any]) -> list[TextContent]:
    """
    Cleanup old temporary and optionally video files
    """
    import time

    max_age_hours = arguments.get("max_age_hours", 24)
    cleanup_videos = arguments.get("cleanup_videos", False)

    max_age_seconds = max_age_hours * 3600
    current_time = time.time()

    cleaned_files = []

    # Cleanup temp uploads
    for temp_file in UPLOAD_FOLDER.glob("*"):
        try:
            file_age = current_time - os.path.getmtime(temp_file)
            if file_age > max_age_seconds:
                os.remove(temp_file)
                cleaned_files.append(f"temp/{temp_file.name}")
        except Exception as e:
            pass

    # Optionally cleanup old videos
    if cleanup_videos:
        for video_file in OUTPUT_FOLDER.glob("*.mp4"):
            try:
                file_age = current_time - os.path.getmtime(video_file)
                if file_age > max_age_seconds:
                    os.remove(video_file)
                    cleaned_files.append(f"videos/{video_file.name}")
            except Exception as e:
                pass

    result = {
        "success": True,
        "message": f"Cleanup completed. Removed {len(cleaned_files)} files.",
        "cleaned_files": cleaned_files,
        "max_age_hours": max_age_hours
    }

    return [TextContent(
        type="text",
        text=json.dumps(result, indent=2)
    )]


async def main():
    """
    Main entry point for the MCP server
    """
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
