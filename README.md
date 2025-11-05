# GALTech AI Faceless Video Generator

<div align="center">
<img width="1200" height="475" alt="galtech school" src="https://www.galtechlearning.com/_next/image?url=%2Flogo.webp" />
</div>

This project is an AI-powered video generator that creates "faceless" videos based on a given topic. It automatically generates a storyboard, scripts, images, and voice-overs, and then combines them into a final video.

## About GALTech

This project is an initiative of [GALTech Learning](https://www.galtechlearning.com/), an educational venture by GALTech Technologies Pvt Ltd. GALTech is a leading IT training institute in Kerala, India, specializing in AI-powered education and next-generation technology courses. They are recognized by Startup India and the Kerala Startup Mission.

## Features

-   **Automated Video Creation**: Generate complete videos from a single topic.
-   **Storyboard Generation**: Automatically creates a scene-by-scene storyboard.
-   **AI-Generated Content**: Uses AI to generate scripts, images, and voice-overs.
-   **Customizable Output**: Supports different aspect ratios and image styles.
-   **Web-Based Interface**: Easy-to-use interface for generating and previewing videos.
-   **MCP Server Integration**: Model Context Protocol server for integration with Claude Desktop, n8n, and other MCP-compatible applications.

## Tech Stack

**Frontend:**

-   React
-   Vite
-   TypeScript
-   Google Gemini API

**Backend:**

-   Python
-   Flask
-   MCP (Model Context Protocol)

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

## MCP Server Integration

This project includes an MCP (Model Context Protocol) server that allows you to integrate video generation capabilities with Claude Desktop, n8n, and other MCP-compatible applications.

### Quick Start with MCP

1.  **Install MCP dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the MCP server:**

    ```bash
    ./run_mcp_server.sh
    ```

    Or manually:

    ```bash
    python3 mcp_server.py
    ```

3.  **Configure Claude Desktop:**

    Add this configuration to your Claude Desktop config file (replace paths with your actual paths):

    ```json
    {
      "mcpServers": {
        "galtech-video-generator": {
          "command": "python3",
          "args": [
            "/path/to/GALTech-AI-Faceless-Video-Generator/mcp_server.py"
          ],
          "env": {
            "PYTHONPATH": "/path/to/GALTech-AI-Faceless-Video-Generator"
          }
        }
      }
    }
    ```

4.  **Start using it in Claude Desktop:**

    Once configured, you can ask Claude to generate videos naturally:

    ```
    Generate a video with these scenes:
    - Scene 1: Image at /path/to/image1.jpg, audio at /path/to/audio1.wav, caption "Welcome"
    - Scene 2: Image at /path/to/image2.jpg, audio at /path/to/audio2.wav, caption "Thank you"

    Use 16:9 aspect ratio and save as "my_video.mp4"
    ```

### MCP Server Features

The MCP server exposes these tools:

-   **generate_video** - Generate videos from local file paths
-   **generate_video_from_base64** - Generate videos from base64-encoded media
-   **get_video_info** - Get information about generated videos
-   **list_generated_videos** - List all generated videos
-   **cleanup_old_files** - Clean up old temporary and video files

### Detailed MCP Documentation

For complete MCP server documentation, including:
-   Claude Desktop setup instructions
-   n8n integration guide
-   API reference
-   Troubleshooting tips
-   Usage examples

See **[MCP_SERVER.md](MCP_SERVER.md)**

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

This project is licensed under the MIT License.
