#!/usr/bin/env python3
"""
AI Video Weaver - FFmpeg Video Generator
Generates videos with image transitions, text overlays, and audio sync
"""

import subprocess
import os
import json
import tempfile
from pathlib import Path
from typing import List, Dict, Optional
import shutil


class VideoGenerator:
    def __init__(self, output_dir: str = "./output"):
        """
        Initialize the video generator

        Args:
            output_dir: Directory to save output videos
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.temp_dir = None

        # Check if ffmpeg is installed
        if not self._check_ffmpeg():
            raise RuntimeError("FFmpeg is not installed. Please install it first.")

    def _check_disk_space(self, required_gb: float = 2.0) -> bool:
        """
        Check if there's enough disk space available

        Args:
            required_gb: Minimum required space in GB

        Returns:
            True if enough space available
        """
        import shutil
        stat = shutil.disk_usage(str(self.output_dir))
        available_gb = stat.free / (1024**3)

        print(f"💾 Disk space: {available_gb:.2f} GB free")

        if available_gb < required_gb:
            print(f"⚠️  WARNING: Low disk space! Need at least {required_gb} GB, have {available_gb:.2f} GB")
            return False
        return True

    def _check_ffmpeg(self) -> bool:
        """Check if FFmpeg is installed"""
        try:
            subprocess.run(['ffmpeg', '-version'],
                         capture_output=True,
                         check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def _get_audio_duration(self, audio_path: str) -> float:
        """Get duration of audio file in seconds"""
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            audio_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)

        # Debug output
        if result.returncode != 0:
            print(f"❌ FFprobe error for {audio_path}:")
            print(f"   stderr: {result.stderr}")
            raise RuntimeError(f"Failed to get audio duration: {result.stderr}")

        duration_str = result.stdout.strip()
        if not duration_str:
            print(f"❌ FFprobe returned empty duration for {audio_path}")
            print(f"   stderr: {result.stderr}")
            # Try alternative method
            return self._get_audio_duration_alternative(audio_path)

        try:
            return float(duration_str)
        except ValueError as e:
            print(f"❌ Could not parse duration: {duration_str}")
            raise RuntimeError(f"Invalid audio duration: {duration_str}")

    def _get_audio_duration_alternative(self, audio_path: str) -> float:
        """Alternative method to get audio duration using ffmpeg"""
        try:
            import wave
            with wave.open(audio_path, 'rb') as audio_file:
                frames = audio_file.getnframes()
                rate = audio_file.getframerate()
                duration = frames / float(rate)
                print(f"✅ Got duration from WAV header: {duration}s")
                return duration
        except Exception as e:
            print(f"❌ Wave library failed: {e}")
            # Last resort: use ffmpeg to convert and get info
            cmd = [
                'ffmpeg',
                '-i', audio_path,
                '-f', 'null',
                '-'
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, stderr=subprocess.STDOUT)
            # Parse duration from ffmpeg output
            import re
            match = re.search(r'Duration: (\d{2}):(\d{2}):(\d{2}\.\d{2})', result.stdout)
            if match:
                hours, minutes, seconds = match.groups()
                duration = int(hours) * 3600 + int(minutes) * 60 + float(seconds)
                print(f"✅ Got duration from ffmpeg: {duration}s")
                return duration
            raise RuntimeError("Could not determine audio duration")

    def generate_video(self,
                      scenes: List[Dict],
                      output_filename: str = "output.mp4",
                      aspect_ratio: str = "16:9",
                      transition_duration: float = 0.5,
                      fps: int = 30,
                      resolution: str = "1920x1080",
                      enable_captions: bool = True) -> str:
        """
        Generate video from scenes with transitions and text overlays

        Args:
            scenes: List of scene dictionaries with keys:
                   - image_path: Path to scene image
                   - audio_path: Path to scene audio
                   - caption: Text to overlay
                   - voice_over: (optional) Additional text
            output_filename: Name of output video file
            aspect_ratio: Video aspect ratio (16:9, 9:16, 1:1, 4:3, 3:4)
            transition_duration: Duration of transition effect in seconds
            fps: Frames per second
            resolution: Video resolution (e.g., "1920x1080")
            enable_captions: Whether to display captions on video (default: True)

        Returns:
            Path to generated video file
        """
        self.temp_dir = tempfile.mkdtemp(prefix="video_gen_")

        try:
            print(f"🎬 Starting video generation with {len(scenes)} scenes...")

            # Check disk space before starting
            if not self._check_disk_space(required_gb=3.0):
                raise RuntimeError(
                    "Insufficient disk space! Please free up at least 3 GB of space.\n"
                    "Run: rm -rf temp_uploads/* generated_videos/*.mp4"
                )

            # Calculate dimensions based on aspect ratio
            width, height = self._get_dimensions(aspect_ratio, resolution)

            # Step 1: Prepare scene videos
            scene_videos = []
            for i, scene in enumerate(scenes):
                print(f"📹 Processing scene {i+1}/{len(scenes)}...")
                scene_video = self._create_scene_video(
                    scene, i, width, height, fps, transition_duration, effect_type='auto', enable_captions=enable_captions
                )
                scene_videos.append(scene_video)

            # Step 2: Concatenate all scenes with smooth crossfade transitions
            output_path = self.output_dir / output_filename
            print(f"🎞️  Creating smooth transitions between scenes...")
            self._concatenate_videos_with_transitions(scene_videos, output_path, fps, transition_duration)

            print(f"✅ Video generated successfully: {output_path}")
            return str(output_path)

        finally:
            # Cleanup temp directory
            if self.temp_dir and os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)

    def _get_dimensions(self, aspect_ratio: str, resolution: str) -> tuple:
        """Get video dimensions based on aspect ratio"""
        aspect_map = {
            "16:9": (1920, 1080),
            "9:16": (1080, 1920),
            "1:1": (1080, 1080),
            "4:3": (1440, 1080),
            "3:4": (1080, 1440),
        }

        if aspect_ratio in aspect_map:
            return aspect_map[aspect_ratio]

        # Parse custom resolution
        try:
            w, h = resolution.split('x')
            return int(w), int(h)
        except:
            return 1920, 1080

    def _detect_script(self, text: str) -> str:
        """
        Detect the script/language of the text
        Returns: 'malayalam', 'hindi', 'arabic', 'chinese', 'japanese', 'korean', or 'latin'
        """
        # Malayalam Unicode range: U+0D00 to U+0D7F
        if any('\u0D00' <= char <= '\u0D7F' for char in text):
            return 'malayalam'
        # Hindi/Devanagari Unicode range: U+0900 to U+097F
        elif any('\u0900' <= char <= '\u097F' for char in text):
            return 'hindi'
        # Arabic Unicode range: U+0600 to U+06FF
        elif any('\u0600' <= char <= '\u06FF' for char in text):
            return 'arabic'
        # Chinese Unicode ranges
        elif any('\u4E00' <= char <= '\u9FFF' or '\u3400' <= char <= '\u4DBF' for char in text):
            return 'chinese'
        # Japanese (Hiragana, Katakana)
        elif any('\u3040' <= char <= '\u309F' or '\u30A0' <= char <= '\u30FF' for char in text):
            return 'japanese'
        # Korean (Hangul)
        elif any('\uAC00' <= char <= '\uD7AF' for char in text):
            return 'korean'
        # Default to Latin
        return 'latin'

    def _get_font_path(self, script: str) -> str:
        """
        Get the appropriate font path for the detected script
        Returns the full path to a font file that supports the script
        """
        import platform
        system = platform.system()

        # Font paths based on script and OS
        font_map = {
            'malayalam': {
                'Darwin': '/System/Library/Fonts/Supplemental/Malayalam Sangam MN.ttc',  # macOS
                'Linux': '/usr/share/fonts/truetype/noto/NotoSansMalayalam-Regular.ttf',
                'Windows': 'C:\\Windows\\Fonts\\NirmalaB.ttf'  # Nirmala UI Bold
            },
            'hindi': {
                'Darwin': '/System/Library/Fonts/Supplemental/Devanagari Sangam MN.ttc',
                'Linux': '/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf',
                'Windows': 'C:\\Windows\\Fonts\\NirmalaB.ttf'
            },
            'arabic': {
                'Darwin': '/System/Library/Fonts/Supplemental/Baghdad.ttf',
                'Linux': '/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf',
                'Windows': 'C:\\Windows\\Fonts\\tahoma.ttf'
            },
            'chinese': {
                'Darwin': '/System/Library/Fonts/PingFang.ttc',
                'Linux': '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
                'Windows': 'C:\\Windows\\Fonts\\msyh.ttc'
            },
            'japanese': {
                'Darwin': '/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc',
                'Linux': '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
                'Windows': 'C:\\Windows\\Fonts\\msmincho.ttc'
            },
            'korean': {
                'Darwin': '/System/Library/Fonts/AppleSDGothicNeo.ttc',
                'Linux': '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
                'Windows': 'C:\\Windows\\Fonts\\malgun.ttf'
            },
            'latin': {
                'Darwin': '/System/Library/Fonts/Helvetica.ttc',
                'Linux': '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
                'Windows': 'C:\\Windows\\Fonts\\Arial.ttf'
            }
        }

        font_path = font_map.get(script, font_map['latin']).get(system, font_map['latin']['Darwin'])

        # Check if font exists, fallback to Noto Sans if not
        if not os.path.exists(font_path):
            print(f"⚠️  Font not found: {font_path}")
            # Try fallback fonts
            fallback_fonts = []
            if system == 'Darwin':
                fallback_fonts = [
                    '/System/Library/Fonts/Supplemental/Arial Unicode.ttf',
                    '/System/Library/Fonts/Helvetica.ttc',
                ]
            elif system == 'Linux':
                fallback_fonts = [
                    '/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf',
                    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
                ]

            for fallback in fallback_fonts:
                if os.path.exists(fallback):
                    print(f"✅ Using fallback font: {fallback}")
                    return fallback

            print(f"⚠️  Using default font path: {font_path} (may not exist)")

        return font_path

    def _get_zoom_effect(self, effect_type: str, total_frames: int,
                        width: int, height: int, fps: int) -> str:
        """
        Get zoom/pan effect filter based on effect type

        Args:
            effect_type: Type of effect (ken_burns, zoom_in, zoom_out, pan_right, pan_left, static)
            total_frames: Total number of frames
            width, height: Video dimensions
            fps: Frames per second

        Returns:
            FFmpeg zoompan filter string
        """
        effects = {
            'ken_burns': (
                # Classic Ken Burns: Slow zoom out with subtle pan
                f"zoompan="
                f"z='if(lte(zoom,1.0),1.0,max(1.0,1.2-0.0008*on))':"
                f"d={total_frames}:"
                f"x='if(gte(zoom,1.0),iw/2-(iw/zoom/2),iw/2-(iw/zoom/2)+sin(on/30)*20)':"
                f"y='if(gte(zoom,1.0),ih/2-(ih/zoom/2),ih/2-(ih/zoom/2)+cos(on/40)*15)':"
                f"s={width}x{height}:fps={fps}"
            ),
            'zoom_in': (
                # Dramatic zoom in
                f"zoompan="
                f"z='min(1.5,1.0+0.0015*on)':"
                f"d={total_frames}:"
                f"x='iw/2-(iw/zoom/2)':"
                f"y='ih/2-(ih/zoom/2)':"
                f"s={width}x{height}:fps={fps}"
            ),
            'zoom_out': (
                # Smooth zoom out
                f"zoompan="
                f"z='if(lte(zoom,1.0),1.0,max(1.0,1.3-0.0012*on))':"
                f"d={total_frames}:"
                f"x='iw/2-(iw/zoom/2)':"
                f"y='ih/2-(ih/zoom/2)':"
                f"s={width}x{height}:fps={fps}"
            ),
            'pan_right': (
                # Pan from left to right with slight zoom
                f"zoompan="
                f"z='1.1':"
                f"d={total_frames}:"
                f"x='(on/{total_frames})*(iw-iw/zoom)':"
                f"y='ih/2-(ih/zoom/2)':"
                f"s={width}x{height}:fps={fps}"
            ),
            'pan_left': (
                # Pan from right to left with slight zoom
                f"zoompan="
                f"z='1.1':"
                f"d={total_frames}:"
                f"x='(1-on/{total_frames})*(iw-iw/zoom)':"
                f"y='ih/2-(ih/zoom/2)':"
                f"s={width}x{height}:fps={fps}"
            ),
            'dynamic': (
                # Dynamic movement: zoom and pan
                f"zoompan="
                f"z='if(lte(on,{total_frames//2}),1.0+0.0015*on,max(1.0,1.0+0.0015*{total_frames//2}-0.0015*(on-{total_frames//2})))':"
                f"d={total_frames}:"
                f"x='iw/2-(iw/zoom/2)+sin(on/20)*30':"
                f"y='ih/2-(ih/zoom/2)+cos(on/25)*20':"
                f"s={width}x{height}:fps={fps}"
            ),
        }

        return effects.get(effect_type, effects['ken_burns'])

    def _create_scene_video(self, scene: Dict, index: int,
                           width: int, height: int, fps: int,
                           transition_duration: float, effect_type: str = 'ken_burns', enable_captions: bool = True) -> str:
        """Create video for a single scene with text overlay"""
        image_path = scene['image_path']
        audio_path = scene['audio_path']
        caption = scene['caption']

        # Get audio duration
        audio_duration = self._get_audio_duration(audio_path)

        # Output path for this scene
        scene_output = os.path.join(self.temp_dir, f"scene_{index:03d}.mp4")

        # Create complex filter for text animation and effects (only if captions enabled)
        text_filter = self._create_text_filter(
            caption, width, height, audio_duration, index
        ) if enable_captions else ""

        # Calculate zoom parameters for smooth, dynamic motion
        total_frames = int(audio_duration * fps)

        # Cycle through 4 cinematic effects for variety
        effect_types = ['pan_right', 'pan_left', 'dynamic', 'zoom_out']
        selected_effect = effect_types[index % len(effect_types)]

        # Display which effect is being used
        effect_names = {
            'pan_right': 'Pan right with zoom',
            'pan_left': 'Pan left with zoom',
            'dynamic': 'Dynamic zoom & pan',
            'zoom_out': 'Smooth zoom out'
        }
        print(f"   🎬 Effect: {effect_names.get(selected_effect, selected_effect)}")

        # Get the zoom/pan filter for this scene
        zoom_filter = self._get_zoom_effect(selected_effect, total_frames, width, height, fps)

        # Scale factor for smooth zooming (higher for zoom/dynamic effects)
        scale_factor = 2 if selected_effect in ['dynamic', 'zoom_out'] else 1.5

        cmd = [
            'ffmpeg',
            '-loop', '1',
            '-i', image_path,
            '-i', audio_path,
            '-filter_complex',
            f"[0:v]scale={int(width*scale_factor)}:{int(height*scale_factor)}:force_original_aspect_ratio=increase,"
            f"crop={int(width*scale_factor)}:{int(height*scale_factor)},"
            f"{zoom_filter},"
            # Add slight sharpening for crisp output
            f"unsharp=5:5:0.8:5:5:0.0,"
            # Fade in effect at start only (crossfade will handle transitions)
            f"fade=t=in:st=0:d=0.5"
            f"{text_filter}[v]",
            '-map', '[v]',
            '-map', '1:a',
            '-c:v', 'libx264',
            '-preset', 'fast',  # Faster encoding
            '-crf', '25',  # Good quality but smaller file size
            '-c:a', 'aac',
            '-b:a', '128k',  # Reduced audio bitrate
            '-shortest',
            '-movflags', '+faststart',
            '-y',
            scene_output
        ]

        # Run FFmpeg
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"❌ Error creating scene {index}:")
            print(result.stderr)
            raise RuntimeError(f"Failed to create scene {index}")

        return scene_output

    def _create_text_filter(self, caption: str, width: int, height: int,
                           duration: float, scene_index: int) -> str:
        """
        Create FFmpeg text overlay with live caption style (3-4 words at a time)
        Supports multiple scripts including Malayalam, Hindi, Arabic, Chinese, Japanese, Korean

        Args:
            caption: Text to display (full voice over)
            width, height: Video dimensions
            duration: Scene duration in seconds
            scene_index: Scene number for color variation
        """
        # Detect script and get appropriate font
        script = self._detect_script(caption)
        font_path = self._get_font_path(script)
        print(f"   📝 Detected script: {script}, using font: {font_path}")
        # Determine aspect ratio orientation
        aspect = width / height
        is_vertical = aspect < 0.8  # 9:16, 3:4
        is_square = 0.8 <= aspect <= 1.2  # 1:1
        is_horizontal = aspect > 1.2  # 16:9, 4:3

        # BIGGER font sizes for live caption style
        base_size = min(width, height)

        if is_vertical:
            # Vertical videos: very large text
            font_size = max(48, int(base_size * 0.065))
        elif is_square:
            # Square videos: large text
            font_size = max(44, int(base_size * 0.06))
        else:
            # Horizontal videos: large text
            font_size = max(40, int(height * 0.055))

        # Text position - BOTTOM CENTER for all aspect ratios
        if is_vertical:
            text_y = int(height * 0.82)  # Bottom area for vertical
        elif is_square:
            text_y = int(height * 0.80)  # Bottom area for square
        else:
            text_y = int(height * 0.78)  # Bottom area for horizontal

        # Split caption into 3-4 word chunks
        words = caption.split()
        chunks = []

        # Group words into chunks of 3-4 words
        words_per_chunk = 3
        for i in range(0, len(words), words_per_chunk):
            chunk_words = words[i:i + words_per_chunk]
            chunk_text = ' '.join(chunk_words)
            chunks.append(chunk_text)

        # Calculate timing for each chunk
        num_chunks = len(chunks)
        time_per_chunk = duration / num_chunks if num_chunks > 0 else duration

        print(f"   📝 Caption split into {num_chunks} chunks ({words_per_chunk} words each)")

        # Create drawtext filter for each chunk
        text_filters = []

        for i, chunk in enumerate(chunks):
            # Escape special characters for FFmpeg
            chunk_escaped = chunk.replace("'", "'\\\\\\''").replace(":", "\\:").replace("%", "\\\\%")

            start_time = i * time_per_chunk
            end_time = (i + 1) * time_per_chunk

            # Create filter for this chunk with proper font support
            text_filters.append(
                f"drawtext="
                f"fontfile={font_path}:"
                f"fontsize={font_size}:"
                f"fontcolor=white:"
                f"borderw=3:"
                f"bordercolor=black@0.95:"
                # Larger semi-transparent background box
                f"box=1:"
                f"boxcolor=black@0.7:"
                f"boxborderw=15:"
                # Center horizontally and vertically
                f"x=(w-text_w)/2:"
                f"y={text_y}:"
                f"text='{chunk_escaped}':"
                # Smooth fade in/out
                f"alpha='if(lt(t,{start_time}),0,"
                f"if(lt(t,{start_time + 0.2}),(t-{start_time})/0.2,"
                f"if(lt(t,{end_time - 0.2}),1,"
                f"if(lt(t,{end_time}),({end_time}-t)/0.2,0))))':"
                f"enable='between(t,{start_time},{end_time})'"
            )

        # Combine all chunk filters
        text_filter = "," + ",".join(text_filters)

        return text_filter

    def _create_concat_file(self, video_files: List[str]) -> str:
        """Create concat file for FFmpeg"""
        concat_file = os.path.join(self.temp_dir, "concat_list.txt")

        with open(concat_file, 'w') as f:
            for video in video_files:
                f.write(f"file '{video}'\n")

        return concat_file

    def _get_video_duration(self, video_path: str) -> float:
        """Get duration of video file in seconds"""
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            video_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return float(result.stdout.strip())

    def _concatenate_videos_with_transitions(self, video_files: List[str], output_path: Path,
                                            fps: int, transition_duration: float):
        """Concatenate videos with smooth crossfade transitions between scenes"""

        if len(video_files) == 1:
            # Only one video, just copy it
            import shutil
            shutil.copy(video_files[0], output_path)
            return

        print(f"🎬 Adding {transition_duration}s crossfade transitions between {len(video_files)} scenes...")

        # Get durations of all videos
        durations = [self._get_video_duration(vf) for vf in video_files]

        # Build complex filter for crossfade transitions
        filter_parts = []

        # Process videos and create crossfades
        current_video = "[0:v]"
        current_audio = "[0:a]"
        offset = durations[0] - transition_duration  # Start first transition before first video ends

        for i in range(1, len(video_files)):
            # Video crossfade
            prev_video = current_video
            next_video = f"[{i}:v]"

            # Last video outputs directly to final format filter
            if i == len(video_files) - 1:
                xfade_output = "[vtmp]"
            else:
                xfade_output = f"[v{i}]"

            # Use xfade with proper offset
            filter_parts.append(
                f"{prev_video}{next_video}xfade=transition=smoothleft:duration={transition_duration}:offset={offset}{xfade_output}"
            )
            current_video = xfade_output

            # Audio crossfade
            prev_audio = current_audio
            next_audio = f"[{i}:a]"

            # Last audio outputs directly to [aout]
            if i == len(video_files) - 1:
                acrossfade_output = "[aout]"
            else:
                acrossfade_output = f"[a{i}]"

            filter_parts.append(
                f"{prev_audio}{next_audio}acrossfade=d={transition_duration}{acrossfade_output}"
            )
            current_audio = acrossfade_output

            # Update offset for next transition
            if i < len(video_files) - 1:
                offset += durations[i] - transition_duration

        # Format final video output
        filter_parts.append(f"[vtmp]format=yuv420p[vout]")

        # Build FFmpeg command
        cmd = ['ffmpeg']

        # Add all input files
        for video_file in video_files:
            cmd.extend(['-i', video_file])

        # Add filter complex
        filter_complex = ';'.join(filter_parts)
        cmd.extend([
            '-filter_complex', filter_complex,
            '-map', '[vout]',
            '-map', '[aout]',
            '-c:v', 'libx264',
            '-preset', 'fast',  # Faster encoding
            '-crf', '25',  # Good quality but smaller file size
            '-c:a', 'aac',
            '-b:a', '128k',  # Reduced audio bitrate
            '-movflags', '+faststart',
            '-y',
            str(output_path)
        ])

        print(f"   ⏱️  Video durations: {[f'{d:.1f}s' for d in durations]}")
        print(f"   🔀 Transition type: smoothleft ({transition_duration}s)")

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"❌ Error creating transitions:")
            print(f"   Filter: {filter_complex}")
            print(f"   Error: {result.stderr}")

            # Check if it's a disk space issue
            if "No space left on device" in result.stderr or "No space left" in result.stderr:
                self._check_disk_space(required_gb=3.0)
                raise RuntimeError(
                    "Ran out of disk space during video generation!\n"
                    "Please free up at least 3-5 GB of space and try again.\n"
                    "The video encoding process needs temporary space."
                )

            raise RuntimeError(f"Failed to create video with transitions: {result.stderr[-500:]}")

    def _concatenate_videos(self, concat_file: str, output_path: Path, fps: int):
        """Concatenate all scene videos into final output (simple method without transitions)"""
        cmd = [
            'ffmpeg',
            '-f', 'concat',
            '-safe', '0',
            '-i', concat_file,
            '-c:v', 'libx264',
            '-preset', 'medium',
            '-crf', '23',
            '-c:a', 'aac',
            '-b:a', '192k',
            '-movflags', '+faststart',
            '-r', str(fps),
            '-y',
            str(output_path)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"❌ Error concatenating videos:")
            print(result.stderr)
            raise RuntimeError("Failed to concatenate videos")


def main():
    """
    Example usage of VideoGenerator
    """
    # Example scene data
    scenes = [
        {
            "image_path": "./scene1_image.jpg",
            "audio_path": "./scene1_audio.wav",
            "caption": "Welcome to the world of dinosaurs",
            "voice_over": "Millions of years ago..."
        },
        {
            "image_path": "./scene2_image.jpg",
            "audio_path": "./scene2_audio.wav",
            "caption": "The mighty T-Rex ruled the land",
            "voice_over": "The most fearsome predator..."
        },
        {
            "image_path": "./scene3_image.jpg",
            "audio_path": "./scene3_audio.wav",
            "caption": "Until one fateful day...",
            "voice_over": "An asteroid changed everything..."
        }
    ]

    # Initialize generator
    generator = VideoGenerator(output_dir="./generated_videos")

    # Generate video
    output_video = generator.generate_video(
        scenes=scenes,
        output_filename="my_video.mp4",
        aspect_ratio="16:9",
        transition_duration=0.5,
        fps=30
    )

    print(f"\n🎉 Video successfully created: {output_video}")


if __name__ == "__main__":
    main()
