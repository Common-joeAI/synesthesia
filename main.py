import os
from secrets_manager import load_credentials
from generate_video import run_generation

def main():
    creds = load_credentials()
    print(f"[✓] Credentials loaded.")
    print("Please ensure your MP3 file is placed in /input/")
    run_generation(creds)

if __name__ == "__main__":
    main()
