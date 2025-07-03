import json
from typing import List, Dict

def detect_mood(audio_path: str) -> str:
    # Stub for mood detection (replace with musicnn)
    return "uplifting"

def generate_prompts(lyrics_map: List[Dict], mood: str) -> List[Dict]:
    prompts = []
    for entry in lyrics_map:
        prompt = f"{mood} biblical scene: {entry['line']}"
        prompts.append({
            "start_time": entry["start"],
            "end_time": entry["end"],
            "prompt": prompt[:77],
            "transition": "fade"
        })
    return prompts

def build_video_plan(audio_meta: Dict, lyrics_map: List[Dict], output_path: str):
    mood = detect_mood(audio_meta["audio_path"])
    segments = generate_prompts(lyrics_map, mood)
    video_plan = {
        "metadata": audio_meta,
        "segments": segments,
        "style_settings": {
            "color_palette": "warm",
            "visual_intensity": 0.8,
            "biblical_era": "judges"
        }
    }
    with open(output_path, 'w') as f:
        json.dump(video_plan, f, indent=2)

def generate_video(config_path: str, mp3_path: str, lyrics_path: str):
    with open(config_path) as f:
        config = json.load(f)

    audio_meta = {
        "audio_path": mp3_path,
        "title": config.get("title", "Untitled Track"),
        "duration": config.get("duration", 180)
    }

    with open(lyrics_path, encoding="utf-8") as f:
        lyrics_lines = f.readlines()

    # Mock lyrics map (normally you'd parse timestamps)
    lyrics_map = []
    step = audio_meta["duration"] // max(1, len(lyrics_lines))
    for i, line in enumerate(lyrics_lines):
        lyrics_map.append({
            "line": line.strip(),
            "start": i * step,
            "end": (i + 1) * step
        })

    build_video_plan(audio_meta, lyrics_map, output_path="video_plan.json")
    print("✅ Video plan generated: video_plan.json")
