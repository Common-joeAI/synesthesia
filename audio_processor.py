
import os
import torch
import torchaudio
import whisperx
import librosa
import musicnn.extractor as extractor
from typing import Tuple, Dict, List

class AudioProcessor:
    def __init__(self, device: str = "cuda" if torch.cuda.is_available() else "cpu"):
        self.device = device
        self.whisper_model = whisperx.load_model("large-v3", device=self.device)
    
    def transcribe_and_align(self, audio_path: str) -> Dict:
        audio = whisperx.load_audio(audio_path)
        result = self.whisper_model.transcribe(audio, batch_size=16)
        model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=self.device)
        result_aligned = whisperx.align(result["segments"], model_a, metadata, audio, self.device, return_char_alignments=False)
        return result_aligned

    def analyze_mood(self, audio_path: str) -> List[str]:
        tags = extractor.extract(audio_path, model='MTT_musicnn', input_length=3, verbose=0)
        top_tags = sorted(tags.items(), key=lambda x: x[1], reverse=True)[:5]
        return [tag for tag, _ in top_tags]

    def process(self, audio_path: str) -> Tuple[Dict, List[str]]:
        aligned_transcription = self.transcribe_and_align(audio_path)
        mood_tags = self.analyze_mood(audio_path)
        return aligned_transcription, mood_tags
