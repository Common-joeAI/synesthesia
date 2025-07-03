import json
import subprocess
import paramiko
import time
from secrets_manager import load_credentials

def launch_instance():
    print("🚀 Launching Lambda Cloud GH200 instance...")
    # Placeholder: integrate with Lambda API or use CLI
    time.sleep(2)
    return "gh200-instance-id"

def attach_storage(instance_id):
    print(f"💾 Attaching storage to instance {instance_id}...")
    time.sleep(1)

def ssh_and_run(instance_ip, ssh_key_path, cmd):
    print(f"🔐 Running remote command on {instance_ip}: {cmd}")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    creds = load_credentials()
    ssh.connect(instance_ip, username='ubuntu', key_filename=ssh_key_path)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print(stdout.read().decode())
    ssh.close()

def download_results(instance_ip, ssh_key_path):
    print("⬇️ Downloading results from remote...")
    os.makedirs("downloaded_output", exist_ok=True)
    subprocess.run([
        "scp", "-i", ssh_key_path,
        f"ubuntu@{instance_ip}:/home/ubuntu/output/*.mp4",
        "./downloaded_output/"
    ])

def terminate_instance(instance_id):
    print(f"💀 Terminating instance {instance_id}...")
    time.sleep(1)
