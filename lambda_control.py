import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

API_BASE = "https://cloud.lambdalabs.com/api/v1"
LAMBDA_API_KEY = os.getenv("LAMBDA_API_KEY")
HEADERS = {"Authorization": f"Bearer {LAMBDA_API_KEY}"}

def launch_instance(instance_type="gpu-1x-a10", region="us-east-1", ssh_key="default-key", storage=[]):
    payload = {
        "instance_type": instance_type,
        "region": region,
        "ssh_key_names": [ssh_key],
        "file_system_names": storage,
        "quantity": 1
    }
    response = requests.post(f"{API_BASE}/instance-operations/launch", headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()["data"]["instance_ids"][0]

def get_instance_ip(instance_id):
    while True:
        response = requests.get(f"{API_BASE}/instances/{instance_id}", headers=HEADERS)
        response.raise_for_status()
        status = response.json()["data"]["status"]
        if status == "active":
            return response.json()["data"]["ip"]
        elif status == "failed":
            raise RuntimeError("Instance failed to boot.")
        time.sleep(10)

def terminate_instance(instance_id):
    payload = {"instance_ids": [instance_id]}
    response = requests.post(f"{API_BASE}/instance-operations/terminate", headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()["data"]

def attach_storage(instance_id, file_system_name):
    payload = {
        "instance_id": instance_id,
        "file_system_name": file_system_name
    }
    response = requests.post(f"{API_BASE}/instance-operations/attach-storage", headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()["data"]
