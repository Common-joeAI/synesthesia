# 🎵 Synesthesia — AI Music Video Generator

**Synesthesia** transforms audio tracks and lyrics into cinematic, biblically inspired music videos using advanced AI and cloud infrastructure.

---

## ✨ Features

- 🎶 **Mood-Based Audio Analysis** (tempo, genre, emotion)
- 📝 **Lyric-to-Scene Prompt Generation**
- 🖼️ **HD Scene Rendering via T2V Models (e.g., Wan2.1_14B_VACE)**
- 🎞️ **Scene-to-Video Assembly (Intro, Scenes, Outro)**
- ☁️ **One-Click Lambda Cloud Deployment & Teardown**
- 🔐 **Master-Password Encrypted SSH & API Credential Storage**
- 📦 **Containerized with Docker for Fast Reuse**
- 🌐 Optional: Local Python or Web UI Interface

---

## 🚀 Quick Start

### 🔧 Prerequisites

- Python 3.8+
- Docker (for local builds or Lambda container snapshots)
- CUDA-compatible GPU (for local generation) *(Optional)*
- [Lambda Cloud](https://lambdalabs.com/cloud) account

### 📦 Installation

```bash
git clone https://github.com/Common-joeAI/synesthesia.git
cd synesthesia
pip install -r requirements.txt
```

---

## ⚙️ Usage

### 🎬 Generate Music Video (Local)

```bash
python main.py --audio ./inputs/song.mp3 --lyrics ./inputs/lyrics.txt
```

### ☁️ Cloud-Optimized Workflow (Lambda Cloud)

```bash
python main.py --audio ./inputs/song.mp3 --lyrics ./inputs/lyrics.txt --use-lambda
```

> **Tip:** Upload assets and retrieve the finished video via the CLI or optional UI frontend.

---

## 🔐 Credential Setup

1. Add `.env` file:

```env
LAMBDA_API_KEY=your_lambda_api_key
MASTER_PASSWORD=your_master_password
```

2. On first launch, you'll be prompted to provide:
   - SSH private key file (for instance connection)
   - Lambda Cloud API token
   - Storage setup preference

Credentials are encrypted and saved locally for session reuse.

---

## 🧠 Configuration

Edit `config.json`:

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
    "instance_type": "gpu-1x-gh200",
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

## 🧩 Modules

| Module | Purpose |
|--------|---------|
| `main.py` | Pipeline coordinator |
| `audio_processor.py` | Mood, beat, genre, lyric mapping |
| `prompt_generator.py` | Converts lyrics to detailed scene prompts |
| `image_generator.py` | Calls T2V model to generate HD scenes |
| `generate_video.py` | Assembles intro, scenes, outro into full video |
| `lambda_control.py` | Manages Lambda Cloud instance lifecycle |
| `frontend.py` | Command-line UI for orchestration |
| `utils.py` | Helper functions (file I/O, hashing, config) |

---

## 🎞️ Example Workflow

1. Upload `song.mp3` and `lyrics.txt`
2. Detect mood/tempo/emotion
3. Generate prompts for every scene
4. Spawn Lambda GH200 instance
5. Generate images → scenes → full video
6. Prepend intro, append outro
7. Deliver final video download link
8. Auto-kill instance to save cost

---

## 🔮 Future Features

- 🔁 Caching prompts → images for reuse
- 📈 Mood-intensity scene transitions
- 📤 Public web upload (if Lambda allows)
- 🔗 YouTube upload + title/description generation
- 🧪 Integrated unit tests
- 🧠 Music tagging via MTG-Jamendo models

---

## 🛠️ Development

To rebuild Docker container:

```bash
docker build -t synesthesia .
docker run --rm -v ${PWD}:/app synesthesia
```

To snapshot the container for Lambda:

```bash
# Save state to storage blob on Lambda
```

---

## 📜 License

MIT © 2025 Electric Christian & Common-Joe AI
