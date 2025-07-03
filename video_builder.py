
import subprocess

def compose_video(image_dir, audio_path, output_path, fps=24):
    cmd = [
        "ffmpeg",
        "-y",
        "-framerate", str(fps),
        "-i", f"{image_dir}/%04d.png",
        "-i", audio_path,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        output_path
    ]
    subprocess.run(cmd, check=True)
