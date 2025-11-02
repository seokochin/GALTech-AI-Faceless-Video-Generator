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

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

This project is licensed under the MIT License.
