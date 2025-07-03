# Entry point for full Synesthesia pipeline
import argparse
import os
import sys
from generate_video import generate_video  # Replace with actual function if different

def main():
    parser = argparse.ArgumentParser(description="Synesthesia Pipeline Entry Point")
    parser.add_argument("--config", required=True, help="Path to config JSON file")
    parser.add_argument("--mp3", required=True, help="Path to input MP3 file")
    parser.add_argument("--lyrics", required=True, help="Path to lyrics TXT file")

    args = parser.parse_args()

    print("🟢 Synesthesia pipeline started")
    print(f"📄 Config: {args.config}")
    print(f"🎵 MP3: {args.mp3}")
    print(f"📝 Lyrics: {args.lyrics}")

    # Here you could call your actual orchestration logic
    generate_video(
        config_path=args.config,
        mp3_path=args.mp3,
        lyrics_path=args.lyrics
    )

if __name__ == "__main__":
    main()
