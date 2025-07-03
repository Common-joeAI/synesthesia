
import argparse
import json
import os
from generate_video import build_video_plan

def load_lyrics_map(path):
    with open(path, 'r') as f:
        return json.load(f)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio", required=True)
    parser.add_argument("--lyrics_map", required=True)
    parser.add_argument("--output", default="video_plan.json")
    parser.add_argument("--backend", choices=["comfy", "openai"], default="comfy")
    args = parser.parse_args()

    lyrics_map = load_lyrics_map(args.lyrics_map)
    audio_meta = {
        "song_title": os.path.basename(args.audio),
        "audio_path": args.audio,
        "duration": 180,
        "bpm": 128
    }

    build_video_plan(audio_meta, lyrics_map, args.output)
    print(f"Video plan written to {args.output}")

if __name__ == "__main__":
    main()
