#!/usr/bin/env python3
"""
Test script to validate MCP server setup
"""

import sys
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.8+"""
    print("Checking Python version...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True


def check_dependencies():
    """Check if required dependencies are installed"""
    print("\nChecking dependencies...")
    required = [
        'mcp',
        'google.generativeai',
        'dotenv',
        'aiohttp',
        'flask',
    ]

    missing = []
    for module in required:
        try:
            # Try to import the module
            parts = module.split('.')
            __import__(parts[0])
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module} not found")
            missing.append(module)

    if missing:
        print("\n⚠️  Missing dependencies. Install them with:")
        print("   pip install -r requirements.txt")
        return False

    return True


def check_ffmpeg():
    """Check if FFmpeg is installed"""
    print("\nChecking FFmpeg...")
    import subprocess
    try:
        result = subprocess.run(['ffmpeg', '-version'],
                              capture_output=True,
                              text=True)
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            print(f"✅ {version}")
            return True
    except FileNotFoundError:
        pass

    print("❌ FFmpeg not found")
    print("   Install FFmpeg:")
    print("   - macOS: brew install ffmpeg")
    print("   - Linux: sudo apt-get install ffmpeg")
    print("   - Windows: Download from https://ffmpeg.org/download.html")
    return False


def check_env_file():
    """Check if .env.local exists and has API key"""
    print("\nChecking environment configuration...")
    env_file = Path(".env.local")

    if not env_file.exists():
        print("❌ .env.local file not found")
        print("   Create it with:")
        print("   echo 'GEMINI_API_KEY=your_api_key_here' > .env.local")
        return False

    content = env_file.read_text()
    if 'GEMINI_API_KEY' not in content:
        print("❌ GEMINI_API_KEY not found in .env.local")
        return False

    # Check if it's not just a placeholder
    if 'your_api_key' in content.lower() or 'your_gemini_api_key' in content.lower():
        print("⚠️  .env.local exists but API key looks like a placeholder")
        print("   Update it with your actual Gemini API key")
        return False

    print("✅ .env.local file exists with API key")
    return True


def check_directories():
    """Check if required directories exist"""
    print("\nChecking directories...")
    dirs = ['generated_videos', 'temp_uploads']

    for dirname in dirs:
        dirpath = Path(dirname)
        if not dirpath.exists():
            print(f"ℹ️  Creating {dirname}/")
            dirpath.mkdir(exist_ok=True)
        print(f"✅ {dirname}/")

    return True


def check_mcp_server():
    """Check if MCP server file exists and is executable"""
    print("\nChecking MCP server...")
    server_file = Path("mcp_server.py")

    if not server_file.exists():
        print("❌ mcp_server.py not found")
        return False

    print("✅ mcp_server.py exists")

    # Check if executable (Unix-like systems)
    if os.name != 'nt':  # Not Windows
        if not os.access(server_file, os.X_OK):
            print("ℹ️  Making mcp_server.py executable...")
            os.chmod(server_file, 0o755)
        print("✅ mcp_server.py is executable")

    return True


def print_next_steps():
    """Print next steps for user"""
    print("\n" + "="*60)
    print("NEXT STEPS")
    print("="*60)
    print("\n1. Configure Claude Desktop:")
    print("   Edit your claude_desktop_config.json:")

    # Detect OS and show appropriate path
    if sys.platform == 'darwin':
        config_path = "~/Library/Application Support/Claude/claude_desktop_config.json"
    elif sys.platform == 'win32':
        config_path = "%APPDATA%\\Claude\\claude_desktop_config.json"
    else:
        config_path = "~/.config/Claude/claude_desktop_config.json"

    print(f"   {config_path}")
    print("\n2. Add this configuration:")
    print("   See mcp_config_example.json for template")
    print("\n3. Restart Claude Desktop")
    print("\n4. Test by asking Claude:")
    print('   "Generate a 1-minute video about space exploration"')
    print("\n5. For detailed documentation, see MCP_SERVER.md")


def main():
    """Run all checks"""
    print("🎬 AI Video Weaver - MCP Server Setup Validator")
    print("="*60)

    checks = [
        check_python_version(),
        check_dependencies(),
        check_ffmpeg(),
        check_env_file(),
        check_directories(),
        check_mcp_server(),
    ]

    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)

    passed = sum(checks)
    total = len(checks)

    if passed == total:
        print(f"✅ All checks passed ({passed}/{total})")
        print("\nYour MCP server is ready to use!")
        print_next_steps()
        return 0
    else:
        print(f"⚠️  {total - passed} check(s) failed ({passed}/{total} passed)")
        print("\nPlease fix the issues above before proceeding.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
