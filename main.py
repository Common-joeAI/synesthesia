import os
from secrets_manager import load_credentials
from generate_video import run_generation

def main():
    creds = load_credentials()
    print(f"[✓] Credentials loaded.")
    print("Please make sure your MP3 file is located at ./input/track.mp3")
    run_generation(creds)

if __name__ == "__main__":
    main()
