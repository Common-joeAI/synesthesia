import subprocess
import threading
import time
import os
import requests
import sys

COMFYUI_HEALTH_URL = "http://127.0.0.1:8188"
COMFYUI_TIMEOUT = 60  # seconds


def run_flask():
    return subprocess.Popen(
        ["python", "backend/app.py"],
        stdout=sys.stdout,
        stderr=sys.stderr
    )

def run_comfyui(path):
    print("💻 Launching ComfyUI...")
    return subprocess.Popen(
        [path],
        cwd=os.path.dirname(path),
        shell=True
    )

def wait_for_comfyui(url=COMFYUI_HEALTH_URL, timeout=COMFYUI_TIMEOUT):
    print("⏳ Waiting for ComfyUI to be ready...", end="")
    start = time.time()
    while time.time() - start < timeout:
        try:
            res = requests.get(url, timeout=2)
            if res.status_code == 200:
                print(" ✅")
                return True
        except Exception:
            pass
        print(".", end="", flush=True)
        time.sleep(1)
    print(" ❌ Timed out.")
    return False

def run_electron():
    return subprocess.Popen(
        ["npm", "start"],
        cwd="frontend",
        shell=True,
        creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
    )

if __name__ == "__main__":
    print("🚀 Launching Synesthesia UI...")

    # Start Flask backend
    print("🔧 Starting Flask backend...")
    flask_proc = run_flask()
    time.sleep(2)

    # Load ComfyUI path from config
    try:
        import json
        with open(".synconfig.json") as f:
            config = json.load(f)
            comfyui_path = config.get("comfyui_path")
            if not comfyui_path or not os.path.exists(comfyui_path):
                raise Exception("Missing or invalid comfyui_path in synconfig.json")
    except Exception as e:
        print("❌ Error:", e)
        sys.exit(1)

    # Start ComfyUI and wait until it's ready
    comfyui_proc = run_comfyui(comfyui_path)
    if not wait_for_comfyui():
        print("❌ ComfyUI did not start in time.")
        comfyui_proc.terminate()
        flask_proc.terminate()
        sys.exit(1)

    # Launch Electron frontend
    print("🖥️ Launching Electron frontend...")
    electron_proc = run_electron()

    # Wait for Electron to finish
    electron_proc.wait()

    print("\n🛑 Shutting down...")
    if flask_proc.poll() is None:
        flask_proc.terminate()
    if comfyui_proc.poll() is None:
        comfyui_proc.terminate()
    print("✅ Clean shutdown complete.")
