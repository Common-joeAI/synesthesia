import os
import requests
import time

API_BASE = "https://cloud.lambdalabs.com/api/v1"
LAMBDA_API_KEY = os.getenv("LAMBDA_API_KEY")
HEADERS = {"Authorization": f"Bearer {LAMBDA_API_KEY}"}


def create_instance(instance_type="gpu-1x-a10", region="us-east-1", ssh_key="default"):
    response = requests.post(
        f"{API_BASE}/instance-operations/launch",
        headers=HEADERS,
        json={
            "instance_type": instance_type,
            "region": region,
            "ssh_key_names": [ssh_key],
            "file_system_names": [],
            "quantity": 1
        }
    )
    response.raise_for_status()
    return response.json()["data"]["instance_ids"][0]


def wait_for_instance(instance_id):
    while True:
        response = requests.get(f"{API_BASE}/instances/{instance_id}", headers=HEADERS)
        data = response.json()["data"]
        status = data["status"]
        if status == "active":
            return data["ip"]
        elif status == "failed":
            raise RuntimeError("Instance startup failed.")
        time.sleep(10)


def terminate_instance(instance_id):
    requests.post(
        f"{API_BASE}/instance-operations/terminate",
        headers=HEADERS,
        json={"instance_ids": [instance_id]}
    )
