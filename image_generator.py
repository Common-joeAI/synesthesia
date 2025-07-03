
import os
import json
import hashlib
import requests
from PIL import Image
from io import BytesIO
from pathlib import Path

CACHE_DIR = os.getenv("CACHE_DIR", "cache/")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "images/")
PROMPT_LOG_PATH = "prompt_log.json"
CACHE_METADATA = "cache_metadata.json"
MODEL_API_ENDPOINT = os.getenv("MODEL_API_ENDPOINT", "http://localhost:8000/generate")

def sha256_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def load_prompt_log():
    with open(PROMPT_LOG_PATH, "r") as f:
        return json.load(f)

def load_cache_metadata():
    if os.path.exists(CACHE_METADATA):
        with open(CACHE_METADATA, "r") as f:
            return json.load(f)
    return {}

def save_cache_metadata(metadata):
    with open(CACHE_METADATA, "w") as f:
        json.dump(metadata, f, indent=2)

def check_cache(prompt_hash, cache_meta):
    return cache_meta.get(prompt_hash)

def save_image_to_cache(prompt_hash, image_data):
    cache_path = os.path.join(CACHE_DIR, f"{prompt_hash}.png")
    with open(cache_path, "wb") as f:
        f.write(image_data)
    return cache_path

def generate_image(prompt):
    response = requests.post(MODEL_API_ENDPOINT, json={"prompt": prompt})
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Image generation failed: {response.text}")

def save_final_image(prompt_hash, image_data, scene_index):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, f"scene_{scene_index:03d}_{prompt_hash}.png")
    with open(output_path, "wb") as f:
        f.write(image_data)
    return output_path

def main():
    prompts = load_prompt_log()
    cache_meta = load_cache_metadata()
    os.makedirs(CACHE_DIR, exist_ok=True)

    for i, entry in enumerate(prompts):
        prompt = entry["prompt"]
        prompt_hash = sha256_hash(prompt)

        print(f"[{i+1}/{len(prompts)}] Processing prompt: {prompt}")

        cached_path = check_cache(prompt_hash, cache_meta)
        if cached_path and os.path.exists(cached_path):
            print("  → Using cached image.")
            with open(cached_path, "rb") as f:
                image_data = f.read()
        else:
            image_data = generate_image(prompt)
            cached_path = save_image_to_cache(prompt_hash, image_data)
            cache_meta[prompt_hash] = cached_path
            save_cache_metadata(cache_meta)

        save_final_image(prompt_hash, image_data, i)

if __name__ == "__main__":
    main()
