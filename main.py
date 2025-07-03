import os
from secrets_manager import load_credentials
from generate_video import run_generation

if __name__ == "__main__":
    creds = load_credentials()
    print(f"[✓] Using API token and SSH key from temp store.")
    run_generation(creds)
