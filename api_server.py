#!/usr/bin/env python3
"""
Flask API Server for AI Video Weaver
Provides endpoints for video generation using FFmpeg
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import base64
import os
import tempfile
import uuid
from pathlib import Path
from video_generator import VideoGenerator
import traceback

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Configuration
UPLOAD_FOLDER = Path("./temp_uploads")
OUTPUT_FOLDER = Path("./generated_videos")
UPLOAD_FOLDER.mkdir(exist_ok=True)
OUTPUT_FOLDER.mkdir(exist_ok=True)

# Initialize video generator
video_generator = VideoGenerator(output_dir=str(OUTPUT_FOLDER))


def save_base64_file(base64_data: str, file_extension: str) -> str:
    """
    Save base64 encoded file to disk

    Args:
        base64_data: Base64 encoded file data (with or without data URI prefix)
        file_extension: File extension (.jpg, .wav, etc.)

    Returns:
        Path to saved file
    """
    # Remove data URI prefix if present
    if ',' in base64_data and base64_data.startswith('data:'):
        base64_data = base64_data.split(',')[1]

    # Decode base64
    file_data = base64.b64decode(base64_data)

    # Generate unique filename
    filename = f"{uuid.uuid4()}{file_extension}"
    file_path = UPLOAD_FOLDER / filename

    # Save file
    with open(file_path, 'wb') as f:
        f.write(file_data)

    # If it's an audio file, validate and re-encode it
    if file_extension in ['.wav', '.mp3', '.m4a']:
        file_path = validate_and_fix_audio(str(file_path))

    return str(file_path)


def validate_and_fix_audio(audio_path: str) -> str:
    """
    Validate audio file and re-encode if necessary to ensure FFmpeg compatibility

    Args:
        audio_path: Path to audio file

    Returns:
        Path to validated/fixed audio file
    """
    import subprocess

    # Debug: Check file size
    file_size = os.path.getsize(audio_path)
    print(f"📊 Audio file size: {file_size} bytes")

    # Debug: Check WAV header
    try:
        with open(audio_path, 'rb') as f:
            header = f.read(44)  # WAV header is 44 bytes
            print(f"🔍 WAV Header (hex): {header[:12].hex()}")

            # Check if it's actually a WAV file
            if header[:4] != b'RIFF':
                print(f"❌ Not a valid WAV file (missing RIFF header)")
            elif header[8:12] != b'WAVE':
                print(f"❌ Not a valid WAV file (missing WAVE marker)")
            else:
                print(f"✅ WAV header looks valid")
    except Exception as e:
        print(f"❌ Error reading WAV header: {e}")

    try:
        # Try to get audio info
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            audio_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)

        # If ffprobe can read it properly, we're good
        if result.returncode == 0 and result.stdout.strip():
            print(f"✅ Audio file is valid, duration: {result.stdout.strip()}s")
            return audio_path

        print(f"⚠️  Audio file needs re-encoding: {audio_path}")
        print(f"    ffprobe stderr: {result.stderr}")

    except Exception as e:
        print(f"⚠️  Audio validation error: {e}")

    # Re-encode the audio to ensure compatibility
    fixed_path = audio_path.replace('.wav', '_fixed.wav')

    print(f"🔧 Attempting to re-encode audio...")
    cmd = [
        'ffmpeg',
        '-f', 's16le',  # Force input format to raw 16-bit PCM
        '-ar', '24000',  # Input sample rate
        '-ac', '1',      # Mono input
        '-i', audio_path,
        '-ar', '24000',  # Output sample rate
        '-ac', '1',      # Mono output
        '-c:a', 'pcm_s16le',  # 16-bit PCM output
        '-y',
        fixed_path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0 and os.path.exists(fixed_path):
        print(f"✅ Audio re-encoded successfully: {fixed_path}")
        # Remove original file
        try:
            os.remove(audio_path)
        except:
            pass
        return fixed_path
    else:
        print(f"❌ Audio re-encoding failed")
        print(f"   Command: {' '.join(cmd)}")
        print(f"   stderr: {result.stderr}")
        return audio_path  # Return original even if re-encoding failed


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Video generation API is running"})


@app.route('/api/generate-video', methods=['POST'])
def generate_video():
    """
    Generate video from scenes with transitions and text overlays

    Expected JSON payload:
    {
        "scenes": [
            {
                "imageUrl": "data:image/jpeg;base64,...",
                "imageMimeType": "image/jpeg",
                "audioUrl": "data:audio/wav;base64,...",
                "caption": "Scene caption text",
                "voiceOver": "Voice over script"
            }
        ],
        "aspectRatio": "16:9",
        "transitionDuration": 0.5,
        "fps": 30,
        "filename": "my_video.mp4",
        "enableCaptions": true
    }

    Returns:
        JSON with video URL or error message
    """
    try:
        data = request.json
        scenes_data = data.get('scenes', [])
        aspect_ratio = data.get('aspectRatio', '16:9')
        transition_duration = data.get('transitionDuration', 0.5)
        fps = data.get('fps', 30)
        filename = data.get('filename', f'video_{uuid.uuid4()}.mp4')
        enable_captions = data.get('enableCaptions', True)  # Default to True for backward compatibility

        if not scenes_data:
            return jsonify({"error": "No scenes provided"}), 400

        print(f"📥 Received request to generate video with {len(scenes_data)} scenes")
        print(f"   Captions enabled: {enable_captions}")

        # Process each scene and save files
        processed_scenes = []
        temp_files = []  # Track temp files for cleanup

        for i, scene in enumerate(scenes_data):
            print(f"💾 Processing scene {i+1}/{len(scenes_data)}...")

            # Determine image extension from mime type
            mime_type = scene.get('imageMimeType', 'image/jpeg')
            img_ext = '.jpg' if 'jpeg' in mime_type else '.png'

            # Save image
            image_path = save_base64_file(scene['imageUrl'], img_ext)
            temp_files.append(image_path)

            # Save audio (assuming WAV format, adjust if needed)
            audio_path = save_base64_file(scene['audioUrl'], '.wav')
            temp_files.append(audio_path)

            processed_scenes.append({
                'image_path': image_path,
                'audio_path': audio_path,
                'caption': scene.get('caption', ''),
                'voice_over': scene.get('voiceOver', '')
            })

        # Generate video
        print("🎬 Starting video generation with FFmpeg...")
        output_path = video_generator.generate_video(
            scenes=processed_scenes,
            output_filename=filename,
            aspect_ratio=aspect_ratio,
            transition_duration=transition_duration,
            fps=fps,
            enable_captions=enable_captions
        )

        # Cleanup temp files
        print("🧹 Cleaning up temporary files...")
        for temp_file in temp_files:
            try:
                os.remove(temp_file)
            except:
                pass

        # Auto-cleanup old generated videos (older than 1 hour to prevent disk full)
        print("🧹 Auto-cleaning old generated videos...")
        import time
        current_time = time.time()
        cleaned_count = 0
        for old_file in OUTPUT_FOLDER.glob('*.mp4'):
            try:
                file_age = current_time - os.path.getmtime(old_file)
                # Keep only the current video and recent ones (1 hour)
                if file_age > 3600 and str(old_file) != str(output_path):  # 1 hour
                    os.remove(old_file)
                    cleaned_count += 1
            except Exception as e:
                print(f"⚠️  Could not remove {old_file}: {e}")
                pass

        if cleaned_count > 0:
            print(f"✅ Removed {cleaned_count} old video(s) to free up space")

        # Return video URL
        video_url = f"/api/download/{os.path.basename(output_path)}"
        return jsonify({
            "success": True,
            "videoUrl": video_url,
            "filename": os.path.basename(output_path),
            "message": "Video generated successfully"
        })

    except Exception as e:
        print(f"❌ Error generating video: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            "error": str(e),
            "details": traceback.format_exc()
        }), 500


@app.route('/api/download/<filename>', methods=['GET'])
def download_video(filename):
    """
    Download generated video file

    Args:
        filename: Name of the video file to download
    """
    try:
        file_path = OUTPUT_FOLDER / filename

        if not file_path.exists():
            return jsonify({"error": "File not found"}), 404

        return send_file(
            file_path,
            mimetype='video/mp4',
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        print(f"❌ Error downloading video: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/cleanup', methods=['POST'])
def cleanup_files():
    """
    Cleanup old temporary and output files
    """
    try:
        # Cleanup temp uploads
        for file in UPLOAD_FOLDER.glob('*'):
            try:
                os.remove(file)
            except:
                pass

        # Optionally cleanup old generated videos (older than 24 hours)
        import time
        current_time = time.time()
        for file in OUTPUT_FOLDER.glob('*.mp4'):
            try:
                file_age = current_time - os.path.getmtime(file)
                if file_age > 86400:  # 24 hours in seconds
                    os.remove(file)
            except:
                pass

        return jsonify({"success": True, "message": "Cleanup completed"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def startup_cleanup():
    """Clean up old files on server startup to prevent disk space issues"""
    import time
    print("\n🧹 Performing startup cleanup...")

    # Clean all temp uploads
    temp_count = 0
    for file in UPLOAD_FOLDER.glob('*'):
        try:
            os.remove(file)
            temp_count += 1
        except:
            pass

    # Clean old generated videos (older than 1 hour)
    current_time = time.time()
    video_count = 0
    for file in OUTPUT_FOLDER.glob('*.mp4'):
        try:
            file_age = current_time - os.path.getmtime(file)
            if file_age > 3600:  # 1 hour
                os.remove(file)
                video_count += 1
        except:
            pass

    print(f"✅ Startup cleanup: Removed {temp_count} temp files and {video_count} old videos")


if __name__ == '__main__':
    print("""
    🎬 AI Video Weaver API Server
    ============================
    Server starting on http://localhost:5001

    Available endpoints:
    - POST /api/generate-video  : Generate video from scenes
    - GET  /api/download/<file> : Download generated video
    - POST /api/cleanup         : Cleanup old files
    - GET  /api/health          : Health check

    Make sure FFmpeg is installed!
    """)

    # Run startup cleanup
    startup_cleanup()

    app.run(debug=True, host='0.0.0.0', port=5001)
