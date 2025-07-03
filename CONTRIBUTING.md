# Contributing to Synesthesia

🎶 Thank you for your interest in contributing to Synesthesia — an open-source AI music video generation pipeline.

We welcome contributions from developers, artists, and creatives alike. Here’s how you can help:

---

## 🛠️ Getting Started

1. **Fork the Repository**
2. **Clone Your Fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/synesthesia.git
   cd synesthesia
   ```
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## 📁 Structure Overview

- `audio_processor.py` — Transcribes lyrics and detects instrumental gaps
- `prompt_generator.py` — Generates scene prompts from lyrics and mood
- `generate_video.py` — Controls text-to-video generation
- `video_assembler.py` — Compiles the final video with transitions and audio
- `lambda_control.py` — Launch/terminate GPU instances on Lambda Cloud
- `config/config.json` — Controls video/audio/model settings

---

## 🧪 How to Contribute

- 🔧 **Bug Fixes** — See [Issues](../../issues) and submit a PR with a clear description.
- 🧠 **Feature Suggestions** — Open an issue or submit a draft pull request.
- 🧪 **Testing** — Add tests for `prompt_generator` or `video_assembler`.
- 🧰 **Refactors** — Make the code more readable or modular.

---

## 🧼 Code Standards

- Follow [PEP8](https://pep8.org/)
- Include docstrings for functions and classes
- Use descriptive commit messages
- Pull requests should target the `main` branch

---

## 📄 Licensing

All contributions will be licensed under the [MIT License](LICENSE).

---

Thank you for helping us bring music to life visually, one verse at a time.

— The Synesthesia Team 🎨🎶
