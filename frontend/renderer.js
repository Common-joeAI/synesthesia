function toggleCloud() {
  const cloudFields = document.getElementById('cloudFields');
  cloudFields.style.display = document.getElementById('useCloud').checked ? 'block' : 'none';
}

async function runPipeline() {
  const formData = new FormData();
  const mp3File = document.getElementById('mp3File').files[0];
  const lyricsFile = document.getElementById('lyricsFile').files[0];
  const configPath = document.getElementById('configPath').value || "config/config.json";
  const useCloud = document.getElementById('useCloud').checked;
  const apiToken = document.getElementById('apiToken').value;
  const sshKey = document.getElementById('sshKey').files[0];

  if (mp3File) formData.append("mp3", mp3File);
  if (lyricsFile) formData.append("lyrics", lyricsFile);
  formData.append("config_path", configPath);
  formData.append("use_cloud", useCloud);
  if (useCloud) {
    formData.append("api_token", apiToken);
    if (sshKey) formData.append("ssh_key", sshKey);
  }

  document.getElementById('status').innerText = "Uploading...";
  await fetch("http://localhost:5000/run", {
    method: "POST",
    body: formData
  });

  document.getElementById('status').innerText = "Running...";
  pollStatus();
  pollLogs();
}

async function pollStatus() {
  const res = await fetch("http://localhost:5000/status");
  const json = await res.json();
  document.getElementById("status").innerText = json.state;
  if (json.state !== "idle") setTimeout(pollStatus, 2000);
}

async function pollLogs() {
  const res = await fetch("http://localhost:5000/logs");
  const text = await res.text();
  document.getElementById("logBox").innerText = text;
  setTimeout(pollLogs, 3000);
}
