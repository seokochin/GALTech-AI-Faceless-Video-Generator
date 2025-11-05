#!/bin/bash

# Run the MCP Server for GALTech AI Faceless Video Generator
# This script starts the MCP server which can be used with Claude Desktop, n8n, and other MCP clients

echo "🚀 Starting GALTech AI Faceless Video Generator MCP Server..."
echo ""
echo "This server exposes video generation tools through the Model Context Protocol (MCP)"
echo "Configure your MCP client to connect to this server."
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the script directory
cd "$SCRIPT_DIR"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "❌ Error: Python is not installed or not in PATH"
        exit 1
    fi
    PYTHON_CMD="python"
else
    PYTHON_CMD="python3"
fi

# Check if FFmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  Warning: FFmpeg is not installed or not in PATH"
    echo "   Video generation will not work without FFmpeg"
    echo "   Please install FFmpeg and try again"
    echo ""
fi

# Check if dependencies are installed
$PYTHON_CMD -c "import mcp" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  MCP Python package not found. Installing dependencies..."
    $PYTHON_CMD -m pip install -r requirements.txt
    echo ""
fi

# Run the MCP server
echo "✅ Starting MCP server..."
$PYTHON_CMD mcp_server.py
