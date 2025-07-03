
import requests
import time
import json
from typing import Dict, List

class ComfyUIClient:
    def __init__(self, base_url: str = "http://localhost:8188"):
        self.base_url = base_url.rstrip("/")

    def submit_prompt(self, prompt_data: Dict) -> str:
        url = f"{self.base_url}/prompt"
        response = requests.post(url, json=prompt_data)
        if response.status_code != 200:
            raise RuntimeError(f"Prompt submission failed: {response.text}")
        return response.json().get("prompt_id")

    def wait_for_completion(self, prompt_id: str, timeout: int = 300) -> List[str]:
        url = f"{self.base_url}/history/{prompt_id}"
        start_time = time.time()
        while time.time() - start_time < timeout:
            resp = requests.get(url)
            if resp.status_code == 200:
                data = resp.json()
                outputs = data.get("outputs")
                if outputs:
                    images = self.extract_images(outputs)
                    return images
            time.sleep(2)
        raise TimeoutError("Timed out waiting for image generation.")

    def extract_images(self, outputs: Dict) -> List[str]:
        images = []
        for node_id, content in outputs.items():
            for image in content.get("images", []):
                images.append(image.get("filename"))
        return images

    def generate_image(self, prompt_json: Dict) -> List[str]:
        prompt_id = self.submit_prompt(prompt_json)
        return self.wait_for_completion(prompt_id)
