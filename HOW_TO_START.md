# How to Start & Use the MCP Server

## 🎯 TL;DR (Quick Answer)

**You don't need to manually start the MCP server!**

Just:
1. Restart Claude Desktop
2. Talk to Claude: "Generate a video about cats"
3. Done! ✅

The server starts automatically when Claude Desktop opens.

---

## 📖 Detailed Explanation

### Understanding MCP Servers

MCP (Model Context Protocol) servers are different from traditional web servers:

- **Traditional Web Server**: You start it, it runs on a port (like :5001), you connect to it
- **MCP Server**: Claude Desktop starts it automatically, it communicates via stdin/stdout, it runs only when needed

---

## ✅ Method 1: Claude Desktop (Recommended)

### Step 1: Configuration is Already Done ✅

Your config file already has:
```json
{
  "mcpServers": {
    "ai-video-weaver": {
      "command": "python3",
      "args": ["/Users/mohammedsalih/Downloads/ai-video-weaver/mcp_server.py"],
      "env": {
        "GEMINI_API_KEY": "XXXXXXX"
      }
    }
  }
}
```

### Step 2: Restart Claude Desktop

```bash
# Quit Claude Desktop completely (Cmd+Q)
# Then reopen it
```

**What happens behind the scenes:**
1. Claude Desktop reads the config file
2. It automatically runs: `python3 /path/to/mcp_server.py`
3. The server starts in the background
4. Claude Desktop connects to it
5. You can now use MCP tools!

### Step 3: Use It!

Just talk to Claude:

```
"Generate a video about cats"
```

Claude will automatically:
- Detect you want to use the MCP tool
- Call the `generate_video` tool
- Show you progress messages
- Give you the video file path

---

## 🔍 Method 2: Manual Testing (For Debugging)

If you want to test the server manually outside of Claude Desktop:

### Option A: Simple Test

```bash
cd /Users/mohammedsalih/Downloads/ai-video-weaver
python3 mcp_server.py
```

**You should see:**
```
🎬 AI Video Weaver MCP Server
============================
Output directory: /Users/mohammedsalih/Downloads/ai-video-weaver/generated_videos
Temp directory: /Users/mohammedsalih/Downloads/ai-video-weaver/temp_uploads

Server is ready to accept connections...
============================
```

**What this means:**
- ✅ Server can start successfully
- ✅ Dependencies are working
- ✅ Paths are correct

Press **Ctrl+C** to stop.

### Option B: Use the Test Script

```bash
cd /Users/mohammedsalih/Downloads/ai-video-weaver
./test_mcp_manual.sh
```

---

## 🚫 Common Misunderstandings

### ❌ WRONG: Starting like a web server

```bash
# DON'T do this - it won't work the way you expect
python3 mcp_server.py &
```

MCP servers don't run as background daemons. They're started by MCP clients.

### ✅ CORRECT: Let Claude Desktop manage it

- Claude Desktop starts it when needed
- Claude Desktop stops it when done
- You just use it through Claude Desktop

---

## 🔧 How to Verify MCP Server is Running

### Option 1: Check Claude Desktop UI

In Claude Desktop, look for:
- Tool icons or MCP indicators
- When you type a message, Claude might suggest MCP tools
- In the conversation, Claude will show when it uses tools

### Option 2: Check System Processes

```bash
# Check if the MCP server process is running
ps aux | grep mcp_server.py
```

If Claude Desktop is open and using it, you'll see:
```
python3 /Users/mohammedsalih/Downloads/ai-video-weaver/mcp_server.py
```

### Option 3: Check Claude Desktop Logs

```bash
# View Claude Desktop logs
tail -f ~/Library/Logs/Claude/mcp*.log
```

Look for:
- "ai-video-weaver" server starting
- Any error messages
- Tool initialization messages

---

## 🎬 Complete Testing Workflow

### 1. First Time Setup

```bash
# Verify everything is installed
cd /Users/mohammedsalih/Downloads/ai-video-weaver
python3 test_mcp_setup.py
```

Should show all ✅ checks passed.

### 2. Restart Claude Desktop

```
Quit Claude Desktop (Cmd+Q)
Reopen Claude Desktop
Wait for it to fully load
```

### 3. Test Basic Connectivity

In Claude Desktop:
```
"List my generated videos"
```

**Expected response:**
- If it works: Claude will use the MCP tool and show results
- If it doesn't work: Claude will say it doesn't have access to that information

### 4. Generate a Test Video

In Claude Desktop:
```
"Generate a 30-second video about cats"
```

**Expected response:**
- Claude starts using the `generate_video` tool
- Shows progress messages (generating storyboard, images, etc.)
- Takes 2-4 minutes
- Gives you a file path to the video

---

## 🆘 Troubleshooting "Server Not Starting"

### Issue: Claude Desktop doesn't recognize MCP tools

**Check 1: Config file location**
```bash
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

Should show your `ai-video-weaver` configuration.

**Check 2: Config file syntax**
Make sure JSON is valid (no missing commas, brackets, etc.)

**Check 3: Restart Claude Desktop**
Make sure you fully quit and reopened it.

### Issue: Server starts but fails immediately

**Check 1: Dependencies**
```bash
cd /Users/mohammedsalih/Downloads/ai-video-weaver
pip install -r requirements.txt
```

**Check 2: Test manually**
```bash
python3 mcp_server.py
```

If it shows errors, fix those first.

**Check 3: API Key**
```bash
cat .env.local
```

Make sure `GEMINI_API_KEY` is set.

### Issue: Can't find generated videos

Videos are saved to:
```bash
ls -la /Users/mohammedsalih/Downloads/ai-video-weaver/generated_videos/
```

---

## 📊 Server Lifecycle

Here's what happens during a typical session:

```
1. You open Claude Desktop
   ↓
2. Claude Desktop reads config
   ↓
3. Claude Desktop starts: python3 mcp_server.py
   ↓
4. MCP server initializes and waits
   ↓
5. You ask Claude to generate a video
   ↓
6. Claude sends MCP command to server
   ↓
7. Server generates video
   ↓
8. Server returns result to Claude
   ↓
9. Claude shows you the result
   ↓
10. You close Claude Desktop
   ↓
11. Server automatically stops
```

---

## 🎯 Quick Reference

| Scenario | Command |
|----------|---------|
| **Use with Claude Desktop** | Just talk to Claude (server auto-starts) |
| **Test if server can start** | `python3 mcp_server.py` |
| **Check all dependencies** | `python3 test_mcp_setup.py` |
| **View config file** | `cat ~/Library/Application\ Support/Claude/claude_desktop_config.json` |
| **Find generated videos** | `ls -la generated_videos/` |
| **Check if running** | `ps aux \| grep mcp_server.py` |

---

## 🎉 Next Steps

Once you understand this, try:

1. **Test the basic setup**
   ```
   "List my generated videos"
   ```

2. **Generate your first video**
   ```
   "Generate a 30-second video about space"
   ```

3. **Try different parameters**
   ```
   "Create a 1-minute vertical video about coffee in cinematic style"
   ```

4. **Check your videos**
   ```bash
   open generated_videos/
   ```

---

## 📚 Related Documentation

- [TESTING_GUIDE.md](TESTING_GUIDE.md) - Complete testing instructions
- [MCP_SERVER.md](MCP_SERVER.md) - Full MCP server documentation
- [PARAMETERS_GUIDE.md](PARAMETERS_GUIDE.md) - All video parameters explained
- [MCP_USAGE_EXAMPLES.md](MCP_USAGE_EXAMPLES.md) - Example commands

---

**Remember:** The MCP server is designed to be invisible. You configure it once, then just use it through Claude Desktop. No manual starting required! 🎬
