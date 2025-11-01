#!/usr/bin/env python3
"""
Example: Standalone Video Generation
This script demonstrates how to use the VideoGenerator directly
without the web interface.
"""

from video_generator import VideoGenerator
import os

def create_sample_video():
    """
    Create a sample video from existing images and audio files
    """
    print("🎬 AI Video Weaver - Standalone Example")
    print("=" * 50)

    # Example scenes - replace these paths with your actual files
    scenes = [
        {
            "image_path": "./examples/scene1.jpg",  # Replace with your image
            "audio_path": "./examples/scene1.wav",  # Replace with your audio
            "caption": "Welcome to AI Video Weaver",
            "voice_over": "An amazing tool to create videos"
        },
        {
            "image_path": "./examples/scene2.jpg",
            "audio_path": "./examples/scene2.wav",
            "caption": "Powered by FFmpeg and AI",
            "voice_over": "Professional video generation made easy"
        },
        {
            "image_path": "./examples/scene3.jpg",
            "audio_path": "./examples/scene3.wav",
            "caption": "Create stunning videos in minutes",
            "voice_over": "With smooth transitions and effects"
        }
    ]

    # Check if example files exist
    print("\n📋 Checking scene files...")
    all_files_exist = True
    for i, scene in enumerate(scenes):
        image_exists = os.path.exists(scene['image_path'])
        audio_exists = os.path.exists(scene['audio_path'])

        status_img = "✅" if image_exists else "❌"
        status_aud = "✅" if audio_exists else "❌"

        print(f"Scene {i+1}: Image {status_img}  Audio {status_aud}")

        if not image_exists or not audio_exists:
            all_files_exist = False

    if not all_files_exist:
        print("\n⚠️  Some files are missing!")
        print("Please create an 'examples' folder with your image and audio files.")
        print("\nRequired structure:")
        print("examples/")
        print("  ├── scene1.jpg")
        print("  ├── scene1.wav")
        print("  ├── scene2.jpg")
        print("  ├── scene2.wav")
        print("  ├── scene3.jpg")
        print("  └── scene3.wav")
        return

    # Initialize video generator
    print("\n🎥 Initializing video generator...")
    generator = VideoGenerator(output_dir="./output")

    # Generate video with different configurations
    print("\n" + "="*50)
    print("Generating videos...")
    print("="*50)

    configs = [
        {
            "name": "Standard 16:9",
            "aspect_ratio": "16:9",
            "filename": "video_16x9.mp4"
        },
        {
            "name": "Vertical 9:16 (Mobile)",
            "aspect_ratio": "9:16",
            "filename": "video_9x16_vertical.mp4"
        },
        {
            "name": "Square 1:1 (Instagram)",
            "aspect_ratio": "1:1",
            "filename": "video_1x1_square.mp4"
        }
    ]

    for config in configs:
        print(f"\n🎬 Generating: {config['name']}")
        print("-" * 50)

        try:
            output_path = generator.generate_video(
                scenes=scenes,
                output_filename=config['filename'],
                aspect_ratio=config['aspect_ratio'],
                transition_duration=0.5,
                fps=30
            )
            print(f"✅ Success! Video saved to: {output_path}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")

    print("\n" + "="*50)
    print("🎉 Video generation complete!")
    print("="*50)
    print(f"\nCheck the './output' directory for your videos.")


def create_test_scene():
    """
    Create a simple test video from a single image and audio
    (Useful for testing without multiple scenes)
    """
    print("🧪 Creating test video from single scene...")

    # Simple test with one scene repeated
    scene = {
        "image_path": "./test_image.jpg",  # Replace with any image
        "audio_path": "./test_audio.wav",  # Replace with any audio
        "caption": "Test Video Generation",
        "voice_over": "Testing FFmpeg video generator"
    }

    if not os.path.exists(scene['image_path']):
        print(f"❌ Image not found: {scene['image_path']}")
        print("Please provide a test_image.jpg file")
        return

    if not os.path.exists(scene['audio_path']):
        print(f"❌ Audio not found: {scene['audio_path']}")
        print("Please provide a test_audio.wav file")
        return

    generator = VideoGenerator(output_dir="./output")

    output_path = generator.generate_video(
        scenes=[scene],  # Single scene
        output_filename="test_video.mp4",
        aspect_ratio="16:9",
        transition_duration=0.5,
        fps=30
    )

    print(f"✅ Test video created: {output_path}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        # Run simple test mode
        create_test_scene()
    else:
        # Run full example
        create_sample_video()

    print("\n💡 Tips:")
    print("  - Use '--test' flag for single scene testing")
    print("  - Edit this file to customize your scenes")
    print("  - Check FFMPEG_SETUP.md for more options")
