#!/bin/bash

# Stop all servers and clean up processes

echo "🛑 Stopping AI Video Weaver Servers..."
echo "======================================"

# Kill Python API server
echo "Stopping Python API server..."
pkill -f "python3 api_server.py" 2>/dev/null
pkill -f "python api_server.py" 2>/dev/null

# Kill Vite dev server
echo "Stopping Vite dev server..."
pkill -f "vite" 2>/dev/null

# Kill any remaining Node processes on common ports
lsof -ti:3000 | xargs kill -9 2>/dev/null
lsof -ti:3001 | xargs kill -9 2>/dev/null
lsof -ti:5000 | xargs kill -9 2>/dev/null
lsof -ti:5001 | xargs kill -9 2>/dev/null

echo ""
echo "✅ All servers stopped!"
echo ""
echo "To restart, run: ./start_servers.sh"
