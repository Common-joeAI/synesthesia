import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

API_BASE = "https://cloud.lambdalabs.com/api/v1"
LAMBDA_API_KEY = os.getenv("LAMBDA_API_KEY")
SSH_KEY_NAME = os.getenv("SSH_KEY_NAME", "synesthesia-key")
FILE_SYSTEM_NAME = os.getenv("LAMBDA_STORAGE_NAME", "synesthesia-storage")

HEADERS = {
    "Authorization": f"Bearer {LAMBDA_API_KEY}"
}


def launch_instance(instance_type="gpu-1x-gh200", region="us-east-1"):
    """Launch a GH200 Lambda Cloud instance."""
    payload = {
        "instance_type": instance_type,
        "region": region,
        "ssh_key_names": [SSH_KEY_NAME],
        "file_system_names": [FILE_SYSTEM_NAME],
        "quantity": 1
    }

    resp = requests.post(f"{API_BASE}/instance-operations/launch", headers=HEADERS, json=payload)
    resp.raise_for_status()
    instance_id = resp.json()["data"]["instance_ids"][0]
    return instance_id


def wait_for_instance(instance_id):
    """Poll until the instance becomes active and return its IP."""
    while True:
        resp = requests.get(f"{API_BASE}/instances/{instance_id}", headers=HEADERS)
        resp.raise_for_status()
        data = resp.json()["data"]
        if data["status"] == "active":
            return data["ip"]
        elif data["status"] == "failed":
            raise RuntimeError("Instance failed to start.")
        time.sleep(10)


def terminate_instance(instance_id):
    """Terminate the GH200 instance to save cost."""
    payload = {"instance_ids": [instance_id]}
    resp = requests.post(f"{API_BASE}/instance-operations/terminate", headers=HEADERS, json=payload)
    resp.raise_for_status()
    return True


def upload_docker(ip, ssh_key_path, dockerfile_path="Dockerfile", remote_name="synesthesia"):
    """Upload Dockerfile and build remotely."""
    import paramiko
    from scp import SCPClient

    key = paramiko.RSAKey.from_private_key_file(ssh_key_path)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username="ubuntu", pkey=key)

    with SCPClient(ssh.get_transport()) as scp:
        scp.put(dockerfile_path, remote_path=f"/home/ubuntu/{remote_name}/Dockerfile")

    stdin, stdout, stderr = ssh.exec_command(f"cd {remote_name} && docker build -t {remote_name} .")
    print(stdout.read().decode(), stderr.read().decode())
    ssh.close()