
import os
import json
import subprocess
from pathlib import Path
from typing import List, Dict
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, ImageClip, CompositeAudioClip

def load_lyrics_map(path: str) -> List[Dict]:
    with open(path, 'r') as f:
        return json.load(f)["segments"]

def generate_video_from_images(segments, image_dir, temp_dir, fps=24, resolution=(1920, 1080)):
    os.makedirs(temp_dir, exist_ok=True)
    frame_paths = []
    for idx, segment in enumerate(segments):
        image_file = Path(image_dir) / f"{idx:04d}.png"
        if not image_file.exists():
            continue
        duration = segment["end"] - segment["start"]
        out_frame = Path(temp_dir) / f"{idx:04d}.mp4"
        clip = ImageClip(str(image_file)).set_duration(duration).resize(resolution)
        clip.write_videofile(str(out_frame), fps=fps, codec="libx264", audio=False, verbose=False, logger=None)
        frame_paths.append(str(out_frame))
    return frame_paths

def concat_videos(video_paths: List[str], output_path: str):
    with open("concat.txt", "w") as f:
        for path in video_paths:
            f.write(f"file '{path}'\n")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", "concat.txt", "-c", "copy", output_path
    ])

def compose_full_video(lyrics_map_path, image_dir, audio_path, intro_path, thunder_path, outro_path, output_path):
    segments = load_lyrics_map(lyrics_map_path)
    temp_video_parts = generate_video_from_images(segments, image_dir, "temp_frames")

    main_video = "main_body.mp4"
    concat_videos(temp_video_parts, main_video)

    # Add audio to main video
    final_with_audio = "main_with_audio.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-i", main_video, "-i", audio_path,
        "-c:v", "copy", "-c:a", "aac", "-shortest", final_with_audio
    ])

    # Add thunder to intro
    intro_temp = "intro_with_audio.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-i", intro_path, "-i", thunder_path,
        "-c:v", "copy", "-c:a", "aac", "-shortest", intro_temp
    ])

    # Final concat: intro + main_with_audio + outro
    with open("final_concat.txt", "w") as f:
        for vid in [intro_temp, final_with_audio, outro_path]:
            f.write(f"file '{Path(vid).as_posix()}'\n")

    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", "final_concat.txt", "-c", "copy", output_path
    ])

    print(f"[✓] Final video saved as {output_path}")
