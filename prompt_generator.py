
import hashlib
import json
from typing import List, Dict, Tuple

class PromptGenerator:
    def __init__(self, global_style: str = "biblical", character_desc: str = "", quality_tags: str = ""):
        self.global_style = global_style
        self.character_desc = character_desc
        self.quality_tags = quality_tags

    def hash_prompt(self, text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def generate_prompts(self, aligned_transcription: Dict, mood_tags: List[str], bible_context: str = "") -> List[Dict]:
        prompts = []
        segments = aligned_transcription.get("segments", [])
        mood = ", ".join(mood_tags)

        for i, seg in enumerate(segments):
            words = seg.get("text", "").strip()
            if not words:
                continue

            scene_prompt = {
                "start": seg["start"],
                "end": seg["end"],
                "text": words,
                "mood": mood,
                "prompt": self.compose_prompt(words, mood, bible_context),
                "hash": self.hash_prompt(words + mood + bible_context)
            }
            prompts.append(scene_prompt)
        return prompts

    def compose_prompt(self, text: str, mood: str, bible_context: str) -> str:
        base = f"{self.quality_tags}, {self.character_desc}, {self.global_style} style"
        return f"{text} — mood: {mood}, theme: {bible_context}, visual: {base}".strip()
