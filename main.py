import os
import argparse
import logging
from dotenv import load_dotenv
from lambda_control import create_instance, wait_for_instance, terminate_instance
from generate_video import analyze_audio, align_lyrics, build_scene_prompts, generate_frames

load_dotenv()
logging.basicConfig(level=logging.INFO)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio", required=True)
    parser.add_argument("--lyrics", required=True)
    parser.add_argument("--output", default="final_output.mp4")
    parser.add_argument("--model", default=os.getenv("MODEL_PATH"))
    parser.add_argument("--use-lambda", action="store_true")
    args = parser.parse_args()

    logging.info("Analyzing audio...")
    analysis = analyze_audio(args.audio)
    segments = align_lyrics(args.lyrics)
    prompts = build_scene_prompts(segments, analysis["mood"])

    if args.use_lambda:
        instance_id = create_instance()
        logging.info(f"Instance launched: {instance_id}")
        ip = wait_for_instance(instance_id)
        logging.info(f"Instance ready at: {ip}")

    generate_frames(prompts, args.model)

    if args.use_lambda:
        terminate_instance(instance_id)
        logging.info("Instance terminated.")

    logging.info(f"Video output: {args.output}")


if __name__ == "__main__":
    main()
