#!/bin/bash
# Manual MCP Server Test Script

echo "🎬 AI Video Weaver - Manual MCP Server Test"
echo "=============================================="
echo ""
echo "This will start the MCP server in test mode."
echo "The server communicates via stdin/stdout (MCP protocol)."
echo ""
echo "To stop: Press Ctrl+C"
echo ""
echo "Starting server..."
echo ""

cd /Users/mohammedsalih/Downloads/ai-video-weaver
python3 mcp_server.py
