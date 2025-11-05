#!/usr/bin/env python3
"""
Example MCP Client for GALTech AI Faceless Video Generator

This script demonstrates how to connect to the MCP server and use the video generation tools.
You can use this as a reference for integrating the MCP server with your own applications.
"""

import asyncio
import json
from pathlib import Path


async def example_generate_video():
    """
    Example: Generate a video using the MCP server
    """
    # Note: This example assumes you have the MCP client library installed
    # and the server is running. For production use, you would typically
    # use this with Claude Desktop or another MCP-compatible application.

    try:
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client
    except ImportError:
        print("❌ MCP client library not found.")
        print("   Install it with: pip install mcp")
        return

    # Configure the MCP server connection
    server_params = StdioServerParameters(
        command="python3",
        args=["mcp_server.py"],
        env=None
    )

    print("🔌 Connecting to MCP server...")

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()
            print("✅ Connected to MCP server")

            # List available tools
            print("\n📋 Available tools:")
            tools = await session.list_tools()
            for tool in tools.tools:
                print(f"   - {tool.name}: {tool.description[:80]}...")

            # Example 1: List generated videos
            print("\n📹 Listing generated videos...")
            result = await session.call_tool("list_generated_videos", {})
            print(json.dumps(json.loads(result.content[0].text), indent=2))

            # Example 2: Generate a video (requires scene files)
            # Uncomment and modify the paths to use:
            """
            print("\n🎬 Generating video...")
            result = await session.call_tool(
                "generate_video",
                {
                    "scenes": [
                        {
                            "image_path": "/path/to/your/image1.jpg",
                            "audio_path": "/path/to/your/audio1.wav",
                            "caption": "Welcome to the demo",
                            "voice_over": "This is a demonstration video"
                        },
                        {
                            "image_path": "/path/to/your/image2.jpg",
                            "audio_path": "/path/to/your/audio2.wav",
                            "caption": "Thank you for watching",
                            "voice_over": "We hope you enjoyed this demo"
                        }
                    ],
                    "output_filename": "demo_video.mp4",
                    "aspect_ratio": "16:9",
                    "transition_duration": 0.5,
                    "fps": 30
                }
            )
            print(json.dumps(json.loads(result.content[0].text), indent=2))
            """

            # Example 3: Get video info (if you have a video)
            """
            print("\n📊 Getting video info...")
            result = await session.call_tool(
                "get_video_info",
                {"filename": "demo_video.mp4"}
            )
            print(json.dumps(json.loads(result.content[0].text), indent=2))
            """

            print("\n✅ Examples completed!")


async def example_cleanup():
    """
    Example: Cleanup old files using the MCP server
    """
    try:
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client
    except ImportError:
        print("❌ MCP client library not found.")
        return

    server_params = StdioServerParameters(
        command="python3",
        args=["mcp_server.py"],
        env=None
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            print("🧹 Cleaning up old files...")
            result = await session.call_tool(
                "cleanup_old_files",
                {
                    "max_age_hours": 24,
                    "cleanup_videos": False  # Set to True to also cleanup old videos
                }
            )
            print(json.dumps(json.loads(result.content[0].text), indent=2))


def main():
    """
    Main entry point
    """
    print("""
╔════════════════════════════════════════════════════════════════╗
║  GALTech AI Faceless Video Generator - MCP Client Example     ║
╚════════════════════════════════════════════════════════════════╝

This script demonstrates how to use the MCP server programmatically.

For normal usage, you would typically:
1. Configure the MCP server in Claude Desktop
2. Use Claude to generate videos naturally
3. Or integrate with n8n for workflow automation

This example shows the underlying API for advanced integrations.
    """)

    # Check if we're in the right directory
    if not Path("mcp_server.py").exists():
        print("❌ Error: mcp_server.py not found in current directory")
        print("   Please run this script from the project root directory")
        return

    # Run the example
    print("\n" + "="*60)
    print("Example 1: List videos and explore the API")
    print("="*60)
    asyncio.run(example_generate_video())

    print("\n" + "="*60)
    print("Example 2: Cleanup old files")
    print("="*60)
    asyncio.run(example_cleanup())

    print("\n" + "="*60)
    print("\n✅ All examples completed!")
    print("\nNext steps:")
    print("1. Configure Claude Desktop to use this MCP server")
    print("2. See MCP_SERVER.md for detailed setup instructions")
    print("3. Start generating videos with natural language!")


if __name__ == "__main__":
    main()
