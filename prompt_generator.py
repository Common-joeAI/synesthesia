import hashlib
import json
import random

class PromptGenerator:
    def __init__(self, global_style='biblical', creativity=0.7):
        self.global_style = global_style
        self.creativity = creativity

    def _hash_prompt(self, prompt):
        return hashlib.sha256(prompt.encode('utf-8')).hexdigest()

    def generate_prompt(self, segment, extra_context=None):
        if segment['type'] == 'instrumental':
            mood = segment.get('mood', 'ambient')
            base_prompt = f"A sweeping biblical landscape, {mood} mood, {self.global_style} style"
        else:
            text = segment.get('text', '')
            mood = segment.get('mood', 'dynamic')
            base_prompt = f"{text}. Style: {self.global_style}, mood: {mood}"

        if extra_context:
            base_prompt += f", context: {extra_context}"

        return {
            "prompt": base_prompt,
            "hash": self._hash_prompt(base_prompt)
        }

    def generate_all_prompts(self, lyrics_map, extra_context=None):
        return [
            {
                **seg,
                **self.generate_prompt(seg, extra_context)
            }
            for seg in lyrics_map
        ]

    def export_prompt_log(self, prompts, output_path='prompt_log.json'):
        with open(output_path, 'w') as f:
            json.dump(prompts, f, indent=2)
        return output_path
