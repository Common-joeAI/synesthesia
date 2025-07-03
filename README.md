# 🎶 Synesthesia – AI Music Video Generator

**Synesthesia** transforms audio tracks and lyrics into visually stunning music videos inspired by biblical imagery.

---

## ✨ Features

- 🎵 Audio analysis for beat detection and mood interpretation
- 📝 Lyric-to-visual transformation using AI
- 📖 Biblical imagery generation using WAN2.1 or ComfyUI
- 🎬 Seamless intro/outro merging and video composition
- ☁️ Lambda Cloud orchestration for high-performance processing

---

## 🧰 Installation

### Prerequisites
- Python 3.8+
- CUDA-compatible GPU (for local use, optional)
- [Lambda Cloud](https://lambdalabs.com) account

### Setup
```bash
git clone https://github.com/Common-joeAI/synesthesia.git
cd synesthesia
pip install -r requirements.txt
```

### Configure Environment
Create a `.env` file:
```dotenv
LAMBDA_API_KEY=your_lambda_cloud_api_key
MODEL_PATH=/path/to/model
```

---

## 🚀 Usage

### Basic Example
```bash
python main.py --audio path/to/audio.mp3 --lyrics path/to/lyrics.txt
```

### Advanced Options
```bash
python main.py \
  --audio path/to/audio.mp3 \
  --lyrics path/to/lyrics.txt \
  --output output_video.mp4 \
  --resolution 1080p \
  --style apocalyptic
```

---

## ⚙️ Configuration

Edit `config.json` for custom video generation parameters:
```json
{
  "video": {
    "fps": 24,
    "resolution": "1080p",
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
```

---

## 📦 Lambda Cloud Integration

```python
from lambda_integration import create_instance, wait_for_instance, terminate_instance

instance_id = create_instance()
ip = wait_for_instance(instance_id)
# SSH and run generation...
terminate_instance(instance_id)
```

---

## 🛠️ Error Handling

Structured exceptions with `error_handling.py` ensure consistent logging and graceful failures.

---

## 📹 Video Plan Template

```json
{
  "metadata": {
    "song_title": "Example Song",
    "duration": 180.5,
    "bpm": 120
  },
  "segments": [
    {
      "start_time": 0.0,
      "end_time": 15.5,
      "lyrics": "In the beginning was the Word",
      "mood": "contemplative",
      "prompt": "A cosmic void with light emerging, biblical creation imagery"
    }
  ]
}
```

---

## 📽 Future Plans

- [ ] GUI Frontend
- [ ] Real-time preview
- [ ] Auto-deployment with persistent volume storage
- [ ] Fine-tuning prompt templates by genre/mood

---

## 📜 License

MIT License © [Common-joeAI](https://github.com/Common-joeAI)