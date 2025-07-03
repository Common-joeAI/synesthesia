
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
