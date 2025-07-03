# Synesthesia - AI Music Video Generator

Synesthesia transforms audio tracks and lyrics into visually stunning music videos inspired by biblical imagery.

## Features

- Audio analysis for beat detection and mood interpretation
- Lyric-to-visual transformation using AI
- Biblical imagery generation
- Seamless video composition
- Lambda Cloud integration for high-performance processing

## Installation

### Prerequisites
- Python 3.8+
- CUDA-compatible GPU (recommended)

### Setup

1. Clone the repository:
git clone https://github.com/Common-joeAI/synesthesia.git
cd synesthesia


2. Install dependencies:
pip install -r requirements.txt

3. Download the required model:


4. Set up environment variables:
Create a `.env` file with the following:
LAMBDA_API_KEY=your_lambda_cloud_api_key
MODEL_PATH=/path/to/model


## Usage

### Basic Usage

python main.py --audio path/to/audio.mp3 --lyrics path/to/lyrics.txt


### Advanced Options
python main.py --audio path/to/audio.mp3 --lyrics path/to/lyrics.txt --output output_video.mp4 --resolution 1080p --style apocalyptic


### Configuration

Edit `config.json` to customize video generation parameters:

```json
{
  "fps": 24,
  "resolution": "1080p",
  "style": "biblical",
  "transition_duration": 1.0
}

Examples
[Include screenshots or video examples here]

Troubleshooting
Error: Model not found - Ensure the model path is correctly set in your .env file
CUDA out of memory - Try reducing batch size or resolution in config.json
License
[Specify your license here]


## 3. Configuration File Template (config.json)

```json
{
  "video": {
    "fps": 24,
    "resolution": "1080p",
    "duration_multiplier": 1.0,
    "transition_duration": 1.0
  },
  "audio": {
    "beat_sensitivity": 0.5,
    "tempo_analysis": true
  },
  "generation": {
    "style": "biblical",
    "intensity": 0.8,
    "creativity": 0.7,
    "seed": -1
  },
  "lambda_cloud": {
    "instance_type": "gpu-1x-a10",
    "region": "us-east-1"
  },
  "model": {
    "name": "Wan2.1_14B_VACE",
    "parameters": {
      "temperature": 0.7,
      "top_p": 0.9,
      "max_tokens": 1024
    }
  }
}

4. Lambda Cloud Integration Code Example
# lambda_integration.py
import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

LAMBDA_API_KEY = os.getenv("LAMBDA_API_KEY")
API_BASE = "https://cloud.lambdalabs.com/api/v1"

def create_instance(instance_type="gpu-1x-a10", region="us-east-1"):
    """Create a Lambda Cloud instance for processing."""
    headers = {"Authorization": f"Bearer {LAMBDA_API_KEY}"}
    payload = {
        "instance_type": instance_type,
        "region": region,
        "ssh_key_names": ["your-ssh-key-name"],  # Replace with your SSH key name
        "file_system_names": [],
        "quantity": 1
    }
    
    response = requests.post(f"{API_BASE}/instance-operations/launch", 
                            headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()["data"]["instance_ids"][0]
    else:
        raise Exception(f"Failed to create instance: {response.text}")

def wait_for_instance(instance_id):
    """Wait for the instance to be ready."""
    headers = {"Authorization": f"Bearer {LAMBDA_API_KEY}"}
    
    while True:
        response = requests.get(f"{API_BASE}/instances/{instance_id}", headers=headers)
        if response.status_code == 200:
            status = response.json()["data"]["status"]
            if status == "active":
                return response.json()["data"]["ip"]
            elif status == "failed":
                raise Exception("Instance failed to start")
        time.sleep(10)

def terminate_instance(instance_id):
    """Terminate the Lambda Cloud instance."""
    headers = {"Authorization": f"Bearer {LAMBDA_API_KEY}"}
    payload = {"instance_ids": [instance_id]}
    
    response = requests.post(f"{API_BASE}/instance-operations/terminate", 
                           headers=headers, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"Failed to terminate instance: {response.text}")

5. Error Handling Improvements
# error_handling.py
import sys
import logging
import traceback
from functools import wraps

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("synesthesia.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("synesthesia")

class SynesthesiaError(Exception):
    """Base exception class for Synesthesia errors."""
    pass

class ModelError(SynesthesiaError):
    """Raised when there's an issue with the AI model."""
    pass

class AudioProcessingError(SynesthesiaError):
    """Raised when there's an issue processing audio."""
    pass

class VideoGenerationError(SynesthesiaError):
    """Raised when there's an issue generating video."""
    pass

def error_handler(func):
    """Decorator for handling errors in functions."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SynesthesiaError as e:
            logger.error(f"Synesthesia error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            logger.error(traceback.format_exc())
            raise SynesthesiaError(f"An unexpected error occurred: {str(e)}")
    return wrapper

6. Sample Video Plan Template
{
  "metadata": {
    "song_title": "Example Song",
    "artist": "Example Artist",
    "duration": 180.5,
    "bpm": 120
  },
  "segments": [
    {
      "start_time": 0.0,
      "end_time": 15.5,
      "lyrics": "In the beginning was the Word",
      "mood": "contemplative",
      "prompt": "A cosmic void with light emerging, biblical creation imagery",
      "transition": "fade"
    },
    {
      "start_time": 15.5,
      "end_time": 30.2,
      "lyrics": "And the Word was with God",
      "mood": "reverent",
      "prompt": "Ethereal light forming divine presence, heavenly atmosphere",
      "transition": "dissolve"
    }
  ],
  "style_settings": {
    "color_palette": "celestial",
    "visual_intensity": 0.8,
    "biblical_era": "creation"
  }
}
7. Main Script Structure Improvements
#!/usr/bin/env python3
# main.py

import os
import argparse
import json
import logging
from dotenv import load_dotenv

# Import your modules
# from audio_processor import AudioProcessor
# from lyric_analyzer import LyricAnalyzer
# from video_generator import VideoGenerator
# from lambda_integration import create_instance, wait_for_instance, terminate_instance
# from error_handling import error_handler, SynesthesiaError

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Synesthesia - AI Music Video Generator")
    parser.add_argument("--audio", required=True, help="Path to audio file")
    parser.add_argument("--lyrics", required=True, help="Path to lyrics file")
    parser.add_argument("--output", default="output.mp4", help="Output video file path")
    parser.add_argument("--config", default="config.json", help="Path to configuration file")
    parser.add_argument("--use-lambda", action="store_true", help="Use Lambda Cloud for processing")
    parser.add_argument("--resolution", default="1080p", help="Video resolution")
    parser.add_argument("--style", default="biblical", help="Visual style for the video")
    return parser.parse_args()

def load_config(config_path):
    """Load configuration from JSON file."""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning(f"Config file {config_path} not found. Using default configuration.")
        return {
            "video": {"fps": 24, "resolution": "1080p"},
            "audio": {"beat_sensitivity": 0.5},
            "generation": {"style": "biblical"}
        }

@error_handler
def main():
    """Main execution function."""
    args = parse_arguments()
    config = load_config(args.config)
    
    # Override config with command line arguments
    if args.resolution:
        config["video"]["resolution"] = args.resolution
    if args.style:
        config["generation"]["style"] = args.style
    
    logger.info(f"Processing audio: {args.audio}")
    logger.info(f"Processing lyrics: {args.lyrics}")
    
    # Check if files exist
    if not os.path.exists(args.audio):
        raise FileNotFoundError(f"Audio file not found: {args.audio}")
    if not os.path.exists(args.lyrics):
        raise FileNotFoundError(f"Lyrics file not found: {args.lyrics}")
    
    # Main processing logic here
    # 1. Process audio
    # 2. Analyze lyrics
    # 3. Generate video plan
    # 4. Generate video frames
    # 5. Compose final video
    
    logger.info(f"Video generated successfully: {args.output}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        exit(1)
