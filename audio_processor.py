import os
import json
import subprocess
import tempfile
import librosa
import numpy as np
from whisper import load_model

class AudioProcessor:
    def __init__(self, audio_path):
        self.audio_path = audio_path
        self.transcription = []
        self.beats = []

    def transcribe(self, model_size='base'):
        model = load_model(model_size)
        result = model.transcribe(self.audio_path, word_timestamps=True)
        self.transcription = result.get('segments', [])
        return self.transcription

    def detect_beats(self):
        y, sr = librosa.load(self.audio_path)
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        self.beats = librosa.frames_to_time(beat_frames, sr=sr)
        return self.beats.tolist()

    def detect_gaps_and_moods(self, silence_threshold=1.0):
        lyrics_map = []
        last_end = 0.0
        for seg in self.transcription:
            start, end, text = seg['start'], seg['end'], seg['text'].strip()
            if start - last_end > silence_threshold:
                lyrics_map.append({
                    'start': last_end,
                    'end': start,
                    'type': 'instrumental',
                    'mood': 'ambient',
                    'prompt': 'Biblical scenery reacting to music tempo'
                })
            lyrics_map.append({
                'start': start,
                'end': end,
                'type': 'lyrical',
                'text': text,
                'prompt': f"Visualize: {text}",
                'mood': 'dynamic'
            })
            last_end = end
        return lyrics_map

    def export_lyrics_map(self, lyrics_map, out_path='lyrics_map.json'):
        with open(out_path, 'w') as f:
            json.dump(lyrics_map, f, indent=2)
        return out_path
