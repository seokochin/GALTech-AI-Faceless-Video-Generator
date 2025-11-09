# GALTech AI Faceless Video Generator



This project is an AI-powered video generator that creates "faceless" videos based on a given topic. It automatically generates a storyboard, scripts, images, and voice-overs, and then combines them into a final video.

## About GALTech

This project is an initiative of [GALTech Learning](https://www.galtechlearning.com/), an educational venture by GALTech Technologies Pvt Ltd. GALTech is a leading IT training institute in Kerala, India, specializing in AI-powered education and next-generation technology courses. They are recognized by Startup India and the Kerala Startup Mission.

## Features

-   **Automated Video Creation**: Generate complete videos from a single topic.
-   **Storyboard Generation**: Automatically creates a scene-by-scene storyboard.
-   **AI-Generated Content**: Uses AI to generate scripts, images, and voice-overs.
-   **Customizable Output**: Supports different aspect ratios and image styles.
-   **Web-Based Interface**: Easy-to-use interface for generating and previewing videos.
-   **MCP Server Integration**: Connect via Model Context Protocol to generate videos from Claude Desktop or other MCP clients.

## Tech Stack

**Frontend:**

-   React
-   Vite
-   TypeScript
-   Google Gemini API

**Backend:**

-   Python
-   Flask

## Getting Started

### Prerequisites

-   Node.js and npm
-   Python 3.x and pip
-   A Google Gemini API Key

### Installation & Setup

1.  **Clone the repository:**

    ```bash
    git clone <your-repository-url>
    cd ai-video-weaver
    ```

2.  **Setup the Frontend:**

    -   Install the dependencies:
        ```bash
        npm install
        ```
    -   Create a `.env.local` file in the root directory and add your Gemini API key:
        ```
        GEMINI_API_KEY=your_gemini_api_key
        ```

3.  **Setup the Backend:**

    -   Install the Python dependencies:
        ```bash
        pip install -r requirements.txt
        ```

### Running the Application

You need to start both the frontend development server and the backend Flask server.

1.  **Start the backend server:**

    ```bash
    python api_server.py
    ```

2.  **Start the frontend server (in a new terminal):**

    ```bash
    npm run dev
    ```

The application should now be running on your local machine.

## MCP Server (Model Context Protocol)

This project includes an MCP server that allows you to generate videos directly from Claude Desktop or other MCP-compatible clients.

### Quick Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure Claude Desktop by adding this to your `claude_desktop_config.json`:
   ```json
   {
     "mcpServers": {
       "ai-video-weaver": {
         "command": "python3",
         "args": ["/absolute/path/to/ai-video-weaver/mcp_server.py"],
         "env": {
           "GEMINI_API_KEY": "your_gemini_api_key_here"
         }
       }
     }
   }
   ```

3. Restart Claude Desktop

4. Ask Claude to generate videos:
   > "Generate a 2-minute video about the solar system in cinematic style"

### Parameters You Can Set

When asking Claude to generate videos, you can specify:
- **Duration**: "2 minutes", "30 seconds" (0.5-10 minutes)
- **Aspect Ratio**: "vertical" (9:16), "horizontal" (16:9), "square" (1:1)
- **Style**: "cinematic", "photorealistic", "cartoon", "anime", etc.
- **Topic**: Any subject for your video

**Examples:**
```
"Create a 1-minute vertical video about fitness in cartoon style"
"Generate a 2-minute square video about cooking in photorealistic style"
"Make a 30-second TikTok video about travel tips"
```

### Available MCP Tools

- `generate_video` - Generate complete video from a topic
- `list_videos` - List all generated videos
- `get_video_info` - Get detailed info about a video file

### Documentation

- **[MCP_SERVER.md](MCP_SERVER.md)** - Complete MCP server setup and configuration
- **[MCP_USAGE_EXAMPLES.md](MCP_USAGE_EXAMPLES.md)** - Detailed usage examples with all parameters
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Quick reference cheat sheet

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

This project is licensed under the MIT License.
