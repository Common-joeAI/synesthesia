# Synesthesia 🎶🌀

**Synesthesia** is an AI-powered music video generator that transforms audio tracks and lyrics into cinematic, biblically inspired visuals — entirely in the cloud.

## ✨ Features
- Text-to-video generation using Wan2.1_14B VACE (GGUF)
- Automatic lyric-based prompt generation
- Audio mood, tempo, and genre analysis using `musicnn`
- Dockerized workflow for fast GH200 deployment
- CLI-based frontend with SSH + Lambda Cloud API integration
- Intro/outro stitching, synced audio, and no leftover storage costs

## 🧠 Secure Access
- Encrypted temporary credential store (API + SSH)
- Protected by a master password

## 📦 Usage (CLI)
```bash
python main.py
```
