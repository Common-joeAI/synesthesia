from flask import request, jsonify, send_file
import subprocess
import threading
import os

LOG_PATH = os.path.join(os.path.dirname(__file__), "pipeline.log")
UPLOAD_DIR = "backend/uploads"
STATUS = {"state": "idle"}

os.makedirs(UPLOAD_DIR, exist_ok=True)

def run_pipeline_thread(config_path):
    global STATUS
    STATUS["state"] = "running"

    # Define paths for uploaded files
    mp3_path = os.path.join(UPLOAD_DIR, "input.mp3")
    lyrics_path = os.path.join(UPLOAD_DIR, "lyrics.txt")

    os.makedirs("backend", exist_ok=True)

    with open(LOG_PATH, "w") as log_file:
        process = subprocess.Popen(
            [
                "python", "main.py",
                "--config", config_path,
                "--mp3", mp3_path,
                "--lyrics", lyrics_path
            ],
            stdout=log_file,
            stderr=subprocess.STDOUT
        )
        process.wait()

    STATUS["state"] = "idle"

def register_routes(app):
    @app.route("/run", methods=["POST"])
    def run():
        # Save uploaded MP3
        if "mp3" in request.files:
            mp3_file = request.files["mp3"]
            mp3_path = os.path.join(UPLOAD_DIR, "input.mp3")
            mp3_file.save(mp3_path)

        # Save uploaded lyrics
        if "lyrics" in request.files:
            lyrics_file = request.files["lyrics"]
            lyrics_path = os.path.join(UPLOAD_DIR, "lyrics.txt")
            lyrics_file.save(lyrics_path)

        # Save SSH key (if present)
        if "ssh_key" in request.files:
            ssh_key_file = request.files["ssh_key"]
            ssh_path = os.path.join(UPLOAD_DIR, "ssh_key.pem")
            ssh_key_file.save(ssh_path)

        # Save API token to temp env var
        if "api_token" in request.form:
            os.environ["LAMBDA_API_TOKEN"] = request.form["api_token"]

        # Use custom config if provided
        config_path = request.form.get("config_path", "config/config.json")

        thread = threading.Thread(target=run_pipeline_thread, args=(config_path,))
        thread.start()
        return jsonify({"status": "started"})

    @app.route("/status", methods=["GET"])
    def status():
        return jsonify(STATUS)

    @app.route("/logs", methods=["GET"])
    def logs():
        if not os.path.exists(LOG_PATH):
            return "No logs yet.", 200
        return send_file(LOG_PATH, mimetype="text/plain")

