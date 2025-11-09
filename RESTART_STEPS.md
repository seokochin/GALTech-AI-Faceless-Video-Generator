# How to Properly Restart Claude Desktop

## The Issue
Claude Desktop caches the MCP server. You're seeing **old logs** from before the fix.

**Old log timestamp:** 15:48-15:49
**Fix applied:** After that

You need a **complete restart** to pick up the changes.

---

## ✅ Proper Restart Steps

### 1. Completely Quit Claude Desktop

**Don't just close the window!** You must fully quit:

```
Cmd + Q
```

Or:
- Click "Claude" in the menu bar
- Click "Quit Claude"

**Make sure** Claude Desktop is completely closed:
```bash
# Check if Claude is still running
ps aux | grep -i claude | grep -v grep
```

Should return **nothing**. If you see Claude processes, force quit them.

### 2. Wait 3-5 Seconds

Give macOS time to clean up processes.

### 3. Clear the Old Log (Optional but Recommended)

```bash
# Delete the old log so you see only new entries
rm ~/Library/Logs/Claude/mcp-server-ai-video-weaver.log
```

### 4. Reopen Claude Desktop

Open Claude Desktop fresh.

### 5. Check the New Log

```bash
cat ~/Library/Logs/Claude/mcp-server-ai-video-weaver.log
```

**You should see:**
```
🎬 AI Video Weaver MCP Server
============================================================
Output directory: /Users/mohammedsalih/Downloads/ai-video-weaver/generated_videos
Temp directory: /Users/mohammedsalih/Downloads/ai-video-weaver/temp_uploads

Server is ready to accept connections...
============================================================
```

**And NO errors after that!**

---

## 🔍 Verification Checklist

Before testing in Claude Desktop, verify:

- [ ] Claude Desktop is completely quit (not just window closed)
- [ ] No Claude processes running: `ps aux | grep -i claude | grep -v grep`
- [ ] Fix is in file: `head -10 mcp_server.py | grep "from __future__"`
- [ ] Old log cleared (optional)
- [ ] Waited 3-5 seconds
- [ ] Reopened Claude Desktop fresh
- [ ] New log shows no errors

---

## 🧪 Test After Restart

Once restarted, in Claude Desktop:

**Test 1:**
```
"List my generated videos"
```

**Test 2:**
```
"Generate a 30-second video about cats"
```

---

## 🆘 If Still Not Working

### Check if the fix is really there:
```bash
head -10 /Users/mohammedsalih/Downloads/ai-video-weaver/mcp_server.py
```

Should show on line 7:
```python
from __future__ import annotations
```

### Force kill Claude if it won't quit:
```bash
pkill -9 Claude
```

Then wait 5 seconds and reopen.

### Check MCP server path in config:
```bash
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json | grep -A3 "ai-video-weaver"
```

Should show:
```json
"ai-video-weaver": {
  "command": "python3",
  "args": ["/Users/mohammedsalih/Downloads/ai-video-weaver/mcp_server.py"],
```

---

## 📊 What Should Happen

### Old Log (Before Fix):
```
Traceback (most recent call last):
  ...
TypeError: 'function' object is not subscriptable
```

### New Log (After Fix):
```
🎬 AI Video Weaver MCP Server
============================================================
Output directory: /Users/mohammedsalih/Downloads/ai-video-weaver/generated_videos
...
Server is ready to accept connections...
============================================================
```

**NO ERRORS** - just waits for commands!

---

**Try the restart steps above, then check the new log!**
