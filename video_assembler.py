
import os
import subprocess
from typing import List

def assemble_video(image_dir: str, audio_path: str, output_path: str, fps: int = 24):
    image_pattern = os.path.join(image_dir, "frame_%05d.png")

    command = [
        "ffmpeg",
        "-y",
        "-framerate", str(fps),
        "-i", image_pattern,
        "-i", audio_path,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-shortest",
        output_path
    ]

    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg failed: {result.stderr}")
    return output_path

def prepend_intro_and_append_outro(intro_path: str, main_video_path: str, outro_path: str, output_path: str):
    concat_list_path = "concat_list.txt"
    with open(concat_list_path, "w") as f:
        f.write(f"file '{os.path.abspath(intro_path)}'\n")
        f.write(f"file '{os.path.abspath(main_video_path)}'\n")
        f.write(f"file '{os.path.abspath(outro_path)}'\n")

    command = [
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list_path,
        "-c", "copy",
        output_path
    ]

    result = subprocess.run(command, capture_output=True, text=True)
    os.remove(concat_list_path)

    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg concat failed: {result.stderr}")
    return output_path
