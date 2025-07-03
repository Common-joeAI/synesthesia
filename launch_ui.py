import subprocess
import threading
import time
import os
import signal
import sys

if os.name == 'nt':
    subprocess.CREATE_NEW_CONSOLE

def run_flask():
    flask_proc = subprocess.Popen(
        ["python", "backend/app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return flask_proc

def run_electron():
    return subprocess.Popen(
        ["npm", "start"],
        cwd="frontend",
        shell=True,
        creationflags=subprocess.CREATE_NEW_CONSOLE  # Windows-specific
    )

if __name__ == "__main__":
    print("🚀 Launching Synesthesia UI...")

    try:
        # Start Flask backend
        print("🔧 Starting Flask backend...")
        flask_proc = run_flask()

        # Wait a moment for Flask to be ready
        time.sleep(2)

        # Start Electron frontend
        print("🖥️ Launching Electron frontend...")
        electron_proc = run_electron()

        # Wait for Electron to exit
        electron_proc.wait()

    except KeyboardInterrupt:
        print("\n🛑 Keyboard interrupt detected. Shutting down...")

    finally:
        # Kill Flask server
        if flask_proc.poll() is None:
            flask_proc.terminate()
            try:
                flask_proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                flask_proc.kill()

        print("✅ Clean shutdown complete.")
        sys.exit(0)
