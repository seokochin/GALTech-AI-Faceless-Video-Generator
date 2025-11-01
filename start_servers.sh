#!/bin/bash

# AI Video Weaver - Start Script
# Starts both Python FFmpeg API and React dev server

echo "🎬 AI Video Weaver - Starting Servers"
echo "======================================"

# Check if FFmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  Warning: FFmpeg is not installed!"
    echo "Install it with: brew install ffmpeg (macOS) or sudo apt install ffmpeg (Linux)"
    echo ""
fi

# Check if Python dependencies are installed
if ! python3 -c "import flask" &> /dev/null; then
    echo "📦 Installing Python dependencies..."
    pip3 install -r requirements.txt
fi

# Check if Node modules are installed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node dependencies..."
    npm install
fi

echo ""
echo "🚀 Starting Python FFmpeg API Server (Port 5001)..."
python3 api_server.py &
PYTHON_PID=$!

# Wait a bit for Python server to start
sleep 2

echo "🚀 Starting React Dev Server (Port 3000)..."
npm run dev &
REACT_PID=$!

echo ""
echo "✅ Servers started successfully!"
echo ""
echo "📱 React App: http://localhost:3000 (or next available port)"
echo "🔧 API Server: http://localhost:5001"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Wait for Ctrl+C
trap "echo ''; echo '🛑 Stopping servers...'; kill $PYTHON_PID $REACT_PID; exit" INT
wait
