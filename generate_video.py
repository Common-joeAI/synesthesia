import os
import json
from pathlib import Path
import numpy as np
import musicnn.extractor as extractor

def extract_mood_genre(mp3_path):
    print(f"🔍 Analyzing audio at {mp3_path} using musicnn...")
    tags, scores = extractor.extractor(mp3_path, extract_features=False)
    tag_scores = sorted(zip(tags, scores), key=lambda x: -x[1])
    top_tags = tag_scores[:5]
    print("🎶 Top tags:")
    for tag, score in top_tags:
        print(f"  - {tag}: {score:.2f}")
    return [tag for tag, score in top_tags]

def generate_scene_prompts(tags):
    prompts = []
    for i in range(15):
        mood = tags[i % len(tags)]
        prompts.append({
            "timestamp": i * 10,
            "prompt": f"A cinematic scene inspired by '{mood}', biblical style, atmospheric lighting (scene {i})"
        })
    return prompts

def run_generation(creds):
    mp3_path = "./input/track.mp3"
    if not os.path.exists(mp3_path):
        print("❌ MP3 file not found at ./input/track.mp3")
        return

    tags = extract_mood_genre(mp3_path)
    scene_prompts = generate_scene_prompts(tags)

    with open("video_plan.json", "w") as f:
        json.dump(scene_prompts, f, indent=2)

    print("🎥 Generating video scenes (simulated)...")
    os.makedirs("output", exist_ok=True)
    for scene in scene_prompts:
        scene_path = f"output/scene_{scene['timestamp']:03d}.mp4"
        with open(scene_path, "wb") as f:
            f.write(b"FAKE_VIDEO_DATA")
        print(f"✅ {scene_path}")

    print("🎞️ Stitching intro + scenes + outro with ffmpeg (simulated)...")
    print("✅ Final video exported to 'output/WhereYouGoIWillGo_FINAL.mp4'")
