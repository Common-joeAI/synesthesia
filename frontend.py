
import os
import argparse
import json
from getpass import getpass
from secrets_manager import save_secrets, load_secrets
from lambda_control import launch_instance, terminate_instance
from main import main as run_synesthesia


def upload_file(prompt):
    path = input(f"{prompt} (provide full path): ")
    if not os.path.exists(path):
        raise FileNotFoundError(f"File does not exist: {path}")
    return path


def main():
    print("🎵 Welcome to Synesthesia Cloud Frontend 🎵\n")

    use_lambda = input("Do you want to run on Lambda Cloud? (y/n): ").strip().lower() == "y"
    instance = None

    if use_lambda:
        print("\n🔐 Lambda Cloud Credentials Setup")
        api_key = getpass("Enter Lambda API Key: ")
        ssh_key_name = input("Enter your Lambda SSH key name: ")
        save_secrets("lambda", {"api_key": api_key, "ssh_key_name": ssh_key_name})

        print("\n🚀 Launching Lambda Cloud instance...")
        instance = launch_instance()

    audio_path = upload_file("Upload your MP3 file")
    lyrics_path = upload_file("Upload your lyrics TXT file")

    config = {
        "audio": audio_path,
        "lyrics": lyrics_path,
        "output": "final_video.mp4",
        "use_lambda": use_lambda
    }

    print("\n🎬 Starting Synesthesia Video Generation...")
    run_synesthesia(config)

    print("\n✅ Video generation complete!")

    if use_lambda and instance:
        terminate = input("Do you want to terminate the Lambda instance now? (y/n): ").strip().lower()
        if terminate == "y":
            print("🛑 Terminating instance...")
            terminate_instance(instance)

    print("\n🎉 Done! Your video is ready at: final_video.mp4")


if __name__ == "__main__":
    main()
